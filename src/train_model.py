"""
train_model.py — Projet smartEngine Groupe G8
Sprint 3 : Entraînement du modèle de prédiction de churn

Utilisation :
    python src/train_model.py

Prérequis :
    - data/processed/analytics.csv (généré par build_analytics.py)

Résultat :
    - outputs/models/churn_model.joblib  (meilleur modèle)
    - outputs/models/all_models.joblib   (tous les modèles + données test)
    - outputs/models/model_comparison.csv
"""

import pandas as pd
import numpy as np
import os
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, f1_score, roc_auc_score, accuracy_score

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost non disponible. Installez-le avec : pip install xgboost")


def prepare_data(df):
    """Prépare X (features) et y (cible) pour la modélisation."""

    # Identification de la variable cible
    if "churned" in df.columns:
        target_col = "churned"
    elif "churn_flag" in df.columns:
        target_col = "churn_flag"
    else:
        raise ValueError("Colonne cible introuvable (churned ou churn_flag)")

    y = df[target_col].astype(int)

    # Colonnes à exclure : identifiants, dates, textes, cibles redondantes
    exclude = {
        target_col, "account_id", "churn_date", "reason_code",
        "preceding_downgrade_flag", "signup_date", "industry",
        "country", "referral_source", "current_plan_tier",
        "billing_frequency", "plan_tier", "is_trial"
    }

    # On garde uniquement les colonnes numériques exploitables
    feature_cols = [
        c for c in df.columns
        if c not in exclude and df[c].dtype in ["float64", "int64", "int32", "float32"]
    ]

    X = df[feature_cols].copy()

    # Imputation des valeurs manquantes résiduelles par la médiane
    for col in X.columns:
        if X[col].isnull().sum() > 0:
            X[col] = X[col].fillna(X[col].median())

    print(f"\nFeatures sélectionnées ({len(feature_cols)}) :")
    for f in feature_cols:
        print(f"  - {f}")

    churn_rate = y.mean() * 100
    print(f"\nVariable cible : '{target_col}'")
    print(f"Distribution  : {y.value_counts().to_dict()}")
    print(f"Taux de churn : {churn_rate:.1f}%")
    print(f"Déséquilibre  : {(y == 0).sum()} non-churns vs {(y == 1).sum()} churns")

    return X, y, feature_cols


def train_all_models(X_train, y_train):
    """
    Entraîne 3 algorithmes avec gestion du déséquilibre des classes.
    Stratégie : class_weight='balanced' (simple, sans sur-échantillonnage artificiel).
    """
    models = {}

    # 1. Logistic Regression — baseline interprétable
    print("\n[1/3] Logistic Regression...")
    lr = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    )
    lr.fit(X_train, y_train)
    models["LogisticRegression"] = lr
    print("      OK")

    # 2. Random Forest — robuste, fournit feature_importances_
    print("[2/3] Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    models["RandomForest"] = rf
    print("      OK")

    # 3. XGBoost — souvent le plus performant sur données tabulaires
    if XGBOOST_AVAILABLE:
        print("[3/3] XGBoost...")
        # scale_pos_weight corrige le déséquilibre sans modifier les données
        scale = (y_train == 0).sum() / max((y_train == 1).sum(), 1)
        xgb = XGBClassifier(
            n_estimators=100,
            scale_pos_weight=scale,
            random_state=42,
            eval_metric="logloss",
            verbosity=0
        )
        xgb.fit(X_train, y_train)
        models["XGBoost"] = xgb
        print("      OK")
    else:
        print("[3/3] XGBoost ignoré (non installé).")

    return models


def compare_models(models, X_test, y_test):
    """Affiche et retourne un tableau comparatif des performances."""

    print("\n" + "=" * 60)
    print("COMPARAISON DES MODÈLES (set de test)")
    print("=" * 60)

    rows = []
    for name, model in models.items():
        y_pred  = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        row = {
            "model":         name,
            "accuracy":      round(accuracy_score(y_test, y_pred), 3),
            "recall_churn":  round(recall_score(y_test, y_pred), 3),
            "f1_churn":      round(f1_score(y_test, y_pred), 3),
            "auc_roc":       round(roc_auc_score(y_test, y_proba), 3),
        }
        rows.append(row)

        print(f"\n  {name}")
        print(f"    Accuracy      : {row['accuracy']}")
        print(f"    Recall churn  : {row['recall_churn']}  ← métrique prioritaire")
        print(f"    F1-score churn: {row['f1_churn']}")
        print(f"    AUC-ROC       : {row['auc_roc']}")

    return pd.DataFrame(rows)


def main():
    os.makedirs("outputs/models", exist_ok=True)

    # Chargement de la table analytique
    analytics_path = "data/processed/analytics.csv"
    if not os.path.exists(analytics_path):
        print(f"ERREUR : {analytics_path} introuvable.")
        print("Exécutez d'abord : python src/build_analytics.py")
        return

    print("Chargement de analytics.csv...")
    df = pd.read_csv(analytics_path)
    print(f"  {len(df)} comptes | {len(df.columns)} colonnes")

    # Préparation des données
    X, y, feature_cols = prepare_data(df)

    # Split stratifié 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    print(f"\nSplit : {len(X_train)} train / {len(X_test)} test")
    print(f"Churn train : {y_train.mean()*100:.1f}%  |  Churn test : {y_test.mean()*100:.1f}%")

    # Entraînement
    print("\n--- ENTRAÎNEMENT ---")
    models = train_all_models(X_train, y_train)

    # Comparaison
    results_df = compare_models(models, X_test, y_test)
    results_df.to_csv("outputs/models/model_comparison.csv", index=False)
    print(f"\n✓ Comparaison sauvegardée : outputs/models/model_comparison.csv")

    # Sélection du meilleur modèle (recall churn maximal)
    # Justification : minimiser les faux négatifs (churns ratés) est prioritaire
    best_name = results_df.loc[results_df["recall_churn"].idxmax(), "model"]
    best_model = models[best_name]
    print(f"\n✓ Meilleur modèle retenu : {best_name}")
    print(f"  (recall churn = {results_df.loc[results_df['model']==best_name, 'recall_churn'].values[0]})")

    # Sauvegarde du meilleur modèle
    joblib.dump(
        {"model": best_model, "feature_cols": feature_cols, "model_name": best_name},
        "outputs/models/churn_model.joblib"
    )
    print(f"✓ Modèle sauvegardé : outputs/models/churn_model.joblib")

    # Sauvegarde de tous les modèles + données test pour evaluate_model.py
    joblib.dump(
        {
            "models":          models,
            "X_test":          X_test,
            "y_test":          y_test,
            "feature_cols":    feature_cols,
            "best_model_name": best_name,
        },
        "outputs/models/all_models.joblib"
    )
    print(f"✓ Tous les modèles sauvegardés : outputs/models/all_models.joblib")
    print("\nÉtape suivante : python src/evaluate_model.py")


if __name__ == "__main__":
    main()
