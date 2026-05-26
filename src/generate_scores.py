"""
generate_scores.py — Projet smartEngine Groupe G8
Sprint 3 : Génération des scores de churn pour tous les comptes

Utilisation :
    python src/generate_scores.py

Prérequis :
    - outputs/models/churn_model.joblib (généré par train_model.py)
    - data/processed/analytics.csv (généré par build_analytics.py)

Résultat :
    - outputs/scores.csv
      Colonnes : account_id, churn_score, risk_level, industry, plan_tier, country
      Trié par churn_score décroissant (comptes les plus urgents en premier)
"""

import pandas as pd
import numpy as np
import os
import joblib


def assign_risk_level(score: float) -> str:
    """
    Seuils métier validés avec l'équipe Customer Success :
    - high   (≥ 0.70) : action immédiate — appel CSM sous 48h
    - medium (≥ 0.40) : surveillance — email de réengagement recommandé
    - low    (< 0.40) : aucune action requise — compte sain
    """
    if score >= 0.70:
        return "high"
    elif score >= 0.40:
        return "medium"
    else:
        return "low"


def main():
    os.makedirs("outputs", exist_ok=True)

    # ── Chargement du modèle ───────────────────────────────────────────────────
    model_path = "outputs/models/churn_model.joblib"
    if not os.path.exists(model_path):
        print(f"ERREUR : {model_path} introuvable.")
        print("Exécutez d'abord : python src/train_model.py")
        return

    print("Chargement du modèle...")
    bundle      = joblib.load(model_path)
    model       = bundle["model"]
    feature_cols = bundle["feature_cols"]
    model_name  = bundle["model_name"]
    print(f"  Modèle : {model_name}")
    print(f"  Features : {len(feature_cols)}")

    # ── Chargement de la table analytique complète ────────────────────────────
    analytics_path = "data/processed/analytics.csv"
    if not os.path.exists(analytics_path):
        print(f"ERREUR : {analytics_path} introuvable.")
        print("Exécutez d'abord : python src/build_analytics.py")
        return

    print("Chargement de analytics.csv...")
    df = pd.read_csv(analytics_path)
    print(f"  {len(df)} comptes à scorer")

    # ── Préparation des features ───────────────────────────────────────────────
    # Vérifier que toutes les features attendues sont disponibles
    missing_feats = [c for c in feature_cols if c not in df.columns]
    if missing_feats:
        print(f"AVERTISSEMENT : features manquantes dans analytics.csv : {missing_feats}")
        feature_cols = [c for c in feature_cols if c in df.columns]

    X_all = df[feature_cols].copy()

    # Imputation des valeurs manquantes résiduelles par la médiane
    for col in X_all.columns:
        if X_all[col].isnull().sum() > 0:
            X_all[col] = X_all[col].fillna(X_all[col].median())

    # ── Génération des scores ──────────────────────────────────────────────────
    print("Calcul des scores de churn...")
    churn_scores = model.predict_proba(X_all)[:, 1]

    # ── Construction du fichier de scores ─────────────────────────────────────
    scores_df = pd.DataFrame({
        "account_id":  df["account_id"],
        "churn_score": np.round(churn_scores, 4),
        "risk_level":  [assign_risk_level(s) for s in churn_scores],
    })

    # Enrichissement avec colonnes contextuelles (utiles pour le dashboard Sprint 4)
    for col in ["industry", "plan_tier", "country", "seats"]:
        if col in df.columns:
            scores_df[col] = df[col].values

    # Tri par churn_score décroissant : comptes les plus urgents en premier
    scores_df = scores_df.sort_values("churn_score", ascending=False).reset_index(drop=True)

    # ── Sauvegarde ────────────────────────────────────────────────────────────
    output_path = "outputs/scores.csv"
    scores_df.to_csv(output_path, index=False)

    # ── Résumé ────────────────────────────────────────────────────────────────
    counts = scores_df["risk_level"].value_counts()
    print(f"\n✓ Scores sauvegardés : {output_path}")
    print(f"  Total comptes : {len(scores_df)}")
    print(f"\n  Distribution des niveaux de risque :")
    for level in ["high", "medium", "low"]:
        n   = counts.get(level, 0)
        pct = n / len(scores_df) * 100
        bar = "█" * int(pct / 3)
        print(f"    {level:6} : {n:3} comptes ({pct:5.1f}%)  {bar}")

    print(f"\n  Score moyen  : {scores_df['churn_score'].mean():.3f}")
    print(f"  Score médian : {scores_df['churn_score'].median():.3f}")

    print(f"\n  Top 10 comptes à risque élevé :")
    top_cols = ["account_id", "churn_score", "risk_level"]
    for c in ["industry", "plan_tier"]:
        if c in scores_df.columns:
            top_cols.append(c)
    print(scores_df[top_cols].head(10).to_string(index=False))

    print("\nSprint 3 terminé !")
    print("Prochaine étape : Sprint 4 — Dashboard Streamlit")
    print(f"Le fichier outputs/scores.csv sera la source principale du dashboard.")


if __name__ == "__main__":
    main()
