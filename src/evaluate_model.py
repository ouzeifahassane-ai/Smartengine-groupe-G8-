"""
evaluate_model.py — Projet smartEngine Groupe G8
Sprint 3 : Évaluation, interprétation et analyse des biais du modèle

Utilisation :
    python src/evaluate_model.py

Prérequis :
    - outputs/models/all_models.joblib (généré par train_model.py)
    - data/processed/analytics.csv

Résultat :
    - outputs/rapport-modele.md
    - outputs/plots/confusion_matrix.png
    - outputs/plots/feature_importance_churn.png
"""

import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime

from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, f1_score, recall_score,
    precision_score, accuracy_score
)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("matplotlib non disponible — les graphiques ne seront pas générés.")
    print("Installez-le avec : pip install matplotlib")


# ── Visualisations ─────────────────────────────────────────────────────────────

def save_confusion_matrix(cm, model_name):
    if not MATPLOTLIB_OK:
        return
    os.makedirs("outputs/plots", exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.colorbar(im)

    labels = ["Non-churn (0)", "Churn (1)"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, rotation=15)
    ax.set_yticklabels(labels)

    thresh = cm.max() / 2
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=14, fontweight="bold")

    ax.set_ylabel("Réalité", fontsize=12)
    ax.set_xlabel("Prédiction", fontsize=12)
    ax.set_title(f"Matrice de confusion — {model_name}", fontsize=13)
    plt.tight_layout()
    plt.savefig("outputs/plots/confusion_matrix.png", dpi=120)
    plt.close()
    print("✓ outputs/plots/confusion_matrix.png")


def save_feature_importance(model, feature_cols, model_name):
    if not MATPLOTLIB_OK:
        return
    if not hasattr(model, "feature_importances_"):
        print("  (Feature importances non disponibles pour ce modèle)")
        return
    os.makedirs("outputs/plots", exist_ok=True)

    importances = pd.Series(model.feature_importances_, index=feature_cols)
    top = importances.sort_values(ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=(9, 6))
    top.plot(kind="barh", ax=ax, color="steelblue", edgecolor="white")
    ax.set_title(f"Importance des features — {model_name}", fontsize=13)
    ax.set_xlabel("Importance relative")
    plt.tight_layout()
    plt.savefig("outputs/plots/feature_importance_churn.png", dpi=120)
    plt.close()
    print("✓ outputs/plots/feature_importance_churn.png")


# ── Analyse des biais ──────────────────────────────────────────────────────────

def bias_analysis(model, X_test, y_test, df_original):
    """
    Évalue le recall du modèle par sous-groupe (industrie, plan).
    Objectif RGPD art. 22 : détecter les biais algorithmiques.
    """
    lines = []
    y_pred = model.predict(X_test)

    # Aligner avec le DataFrame original sur les index du test
    try:
        df_sub = df_original.loc[X_test.index].copy()
        df_sub["y_true"] = y_test.values
        df_sub["y_pred"] = y_pred
    except Exception:
        lines.append("Analyse de biais non disponible (index non alignés).")
        return lines

    # Biais par industrie
    if "industry" in df_sub.columns:
        lines.append("### Recall par industrie")
        lines.append("")
        lines.append("| Industrie | Recall | Comptes (test) |")
        lines.append("|---|---|---|")
        for industry, grp in df_sub.groupby("industry"):
            if len(grp) >= 5 and grp["y_true"].sum() > 0:
                r = recall_score(grp["y_true"], grp["y_pred"], zero_division=0)
                lines.append(f"| {industry} | {r:.2f} | {len(grp)} |")

    lines.append("")

    # Biais par plan tarifaire
    plan_col = next((c for c in ["plan_tier", "current_plan_tier"] if c in df_sub.columns), None)
    if plan_col:
        lines.append("### Recall par plan tarifaire")
        lines.append("")
        lines.append("| Plan | Recall | Comptes (test) |")
        lines.append("|---|---|---|")
        for plan, grp in df_sub.groupby(plan_col):
            if len(grp) >= 5 and grp["y_true"].sum() > 0:
                r = recall_score(grp["y_true"], grp["y_pred"], zero_division=0)
                lines.append(f"| {plan} | {r:.2f} | {len(grp)} |")

    return lines


# ── Rapport markdown ───────────────────────────────────────────────────────────

def generate_report(models, X_test, y_test, feature_cols, best_name, df_original):

    best_model  = models[best_name]
    y_pred_best = best_model.predict(X_test)
    y_prob_best = best_model.predict_proba(X_test)[:, 1]
    cm          = confusion_matrix(y_test, y_pred_best)
    tn, fp, fn, tp = cm.ravel()

    lines = [
        "# Rapport de modélisation — smartEngine",
        f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "Projet : Prédiction de churn B2B — RavenStack | Groupe G8",
        "",
        "---",
        "",
        "## 1. Contexte",
        "",
        "Objectif : prédire le churn (résiliation) des comptes RavenStack avec ≥ 30 jours d'avance.",
        "Objectifs de performance : AUC-ROC ≥ 0.80, Recall ≥ 70% sur la classe churn.",
        "",
        "**Métrique prioritaire : Recall**",
        "Justification métier : dans un contexte B2B SaaS, rater un churn (faux négatif) coûte",
        "5 à 7 fois plus cher en coût d'acquisition que de déclencher une alerte inutile (faux positif).",
        "L'équipe Customer Success préfère contacter un client sain plutôt que de laisser partir un churner.",
        "",
        "## 2. Données d'entrée",
        "",
        f"- Source : `data/processed/analytics.csv`",
        f"- Comptes total : {len(X_test) * 5} (approximation — 500 comptes RavenStack)",
        f"- Comptes en test : {len(X_test)}",
        f"- Features utilisées : {len(feature_cols)}",
        f"- Taux de churn (test) : {y_test.mean()*100:.1f}%",
        f"- Split : 80% train / 20% test, stratifié (random_state=42)",
        "",
        "## 3. Gestion du déséquilibre des classes",
        "",
        "Stratégie retenue : **`class_weight='balanced'`** pour Logistic Regression et Random Forest.",
        "Pour XGBoost : **`scale_pos_weight = nb_négatifs / nb_positifs`**.",
        "",
        "Justification : approche simple et sans sur-échantillonnage artificiel (SMOTE génère des données",
        "synthétiques qui peuvent fausser la distribution réelle sur un petit dataset de 500 comptes).",
        "",
        "## 4. Résultats comparatifs",
        "",
        "| Modèle | Accuracy | Recall churn | Précision | F1 | AUC-ROC |",
        "|---|---|---|---|---|---|",
    ]

    for name, model in models.items():
        y_pred  = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        marker  = " ← **retenu**" if name == best_name else ""
        lines.append(
            f"| {name} "
            f"| {accuracy_score(y_test, y_pred):.3f} "
            f"| {recall_score(y_test, y_pred):.3f} "
            f"| {precision_score(y_test, y_pred, zero_division=0):.3f} "
            f"| {f1_score(y_test, y_pred):.3f} "
            f"| {roc_auc_score(y_test, y_proba):.3f} |{marker}"
        )

    lines += [
        "",
        f"**Modèle retenu : {best_name}**",
        "Critère : recall maximal sur la classe churn (minimiser les churns non détectés).",
        "",
        "## 5. Matrice de confusion — modèle retenu",
        "",
        "```",
        f"                    Prédit non-churn   Prédit churn",
        f"Réel non-churn      {tn:>15}   {fp:>12}",
        f"Réel churn          {fn:>15}   {tp:>12}",
        "```",
        "",
        f"- **Vrais positifs  (VP)** : {tp} churns correctement détectés",
        f"- **Faux négatifs   (FN)** : {fn} churns ratés → à minimiser",
        f"- **Faux positifs   (FP)** : {fp} alertes à tort (coût acceptable)",
        f"- **Vrais négatifs  (VN)** : {tn} non-churns correctement identifiés",
        "",
        "## 6. Importance des features",
        "",
    ]

    if hasattr(best_model, "feature_importances_"):
        importances = pd.Series(best_model.feature_importances_, index=feature_cols)
        top10 = importances.sort_values(ascending=False).head(10)

        interpretations = {
            "days_since_last_usage":  "Inactivité récente = désengagement fort",
            "avg_satisfaction":        "Insatisfaction support précède souvent le churn",
            "mrr_current":             "MRR faible = moins d'ancrage financier",
            "nb_tickets_urgent":       "Tickets urgents = problèmes non résolus",
            "escalation_rate":         "Escalades fréquentes = insatisfaction chronique",
            "account_age_days":        "Comptes récents plus à risque de churn précoce",
            "nb_plan_changes":         "Changements de plan = instabilité",
            "error_rate":              "Taux d'erreur élevé = friction produit",
            "avg_usage_count":         "Faible usage = faible adoption",
            "subscription_age_days":   "Abonnement récent = relation non consolidée",
            "nb_tickets_total":        "Volume de tickets élevé = friction récurrente",
            "total_usage_count":       "Usage total faible = faible engagement",
        }

        lines.append("| Rang | Feature | Importance | Interprétation métier |")
        lines.append("|---|---|---|---|")
        for i, (feat, imp) in enumerate(top10.items(), 1):
            interp = interpretations.get(feat, "À valider avec l'équipe métier")
            lines.append(f"| {i} | {feat} | {imp:.4f} | {interp} |")
    else:
        lines.append("Feature importances non disponibles pour ce type de modèle.")

    lines += [
        "",
        "## 7. Analyse des biais",
        "",
        "Un modèle techniquement bon peut être métier biaisé.",
        "Évaluation du recall par sous-groupe pour détecter les inégalités de traitement (RGPD art. 22).",
        "",
    ]

    lines += bias_analysis(best_model, X_test, y_test, df_original)

    lines += [
        "",
        "## 8. Limites connues du modèle",
        "",
        "- **Volume** : 500 comptes est un dataset petit pour le ML.",
        "  Risque d'overfitting modéré, à surveiller lors de l'ajout de nouvelles données.",
        "- **feature_usage.csv** : colonnes `feature_name` et `is_beta_feature` à 100% manquantes.",
        "  Le signal d'adoption des fonctionnalités n'est pas exploitable en l'état.",
        "- **Temporalité** : pas de validation walk-forward stricte.",
        "  Le split stratifié est une approximation acceptable pour ce volume.",
        "- **Déséquilibre résiduel** : malgré class_weight='balanced', les faux négatifs",
        "  restent une limitation à monitorer en production.",
        "",
        "## 9. Seuils de décision retenus",
        "",
        "| Niveau | Seuil churn_score | Action Customer Success |",
        "|---|---|---|",
        "| 🔴 **High**   | ≥ 0.70 | Appel CSM sous 48h — risque immédiat |",
        "| 🟡 **Medium** | 0.40 – 0.70 | Email de réengagement — surveillance renforcée |",
        "| 🟢 **Low**    | < 0.40 | Aucune action requise — compte sain |",
        "",
        "Justification : seuil 0.70 limite les faux positifs en zone haute.",
        "Seuil 0.40 permet d'anticiper à 30 jours et d'activer les campagnes de rétention.",
        "",
        "---",
        "*Rapport généré automatiquement par evaluate_model.py — smartEngine Groupe G8*",
    ]

    path = "outputs/rapport-modele.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ {path}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    os.makedirs("outputs/plots", exist_ok=True)

    models_path = "outputs/models/all_models.joblib"
    if not os.path.exists(models_path):
        print(f"ERREUR : {models_path} introuvable.")
        print("Exécutez d'abord : python src/train_model.py")
        return

    print("Chargement des modèles...")
    bundle     = joblib.load(models_path)
    models     = bundle["models"]
    X_test     = bundle["X_test"]
    y_test     = bundle["y_test"]
    feat_cols  = bundle["feature_cols"]
    best_name  = bundle["best_model_name"]

    print(f"  Modèles disponibles : {list(models.keys())}")
    print(f"  Meilleur modèle     : {best_name}")

    df_original = pd.read_csv("data/processed/analytics.csv")

    best_model = models[best_name]
    y_pred     = best_model.predict(X_test)
    cm         = confusion_matrix(y_test, y_pred)

    print("\nGénération des visualisations...")
    save_confusion_matrix(cm, best_name)
    save_feature_importance(best_model, feat_cols, best_name)

    print("Génération du rapport...")
    generate_report(models, X_test, y_test, feat_cols, best_name, df_original)

    print("\nÉtape suivante : python src/generate_scores.py")


if __name__ == "__main__":
    main()
