"""
priorisation.py — Projet smartEngine Groupe G8
Sprint 4 : Segmentation risque / valeur et génération de outputs/priorisation.csv

Utilisation :
    python src/priorisation.py

Prérequis :
    - outputs/scores.csv          (généré par generate_scores.py, Sprint 3)
    - data/processed/analytics.csv (généré par build_analytics.py, Sprint 2)

Résultat :
    - outputs/priorisation.csv
      Colonnes : account_id, churn_score, risk_level, mrr, quadrant, action
      Trié par priorité décroissante (quadrant 1 en premier, puis churn_score)
"""

import pandas as pd
import numpy as np
import os


# ── Seuils de segmentation ─────────────────────────────────────────────────────
# Risque élevé : churn_score >= 0.5  (risque de churn supérieur à 50 %)
# Valeur élevée : mrr >= médiane du MRR de l'ensemble du portefeuille
RISK_THRESHOLD = 0.5

# ── Mapping quadrant → action ──────────────────────────────────────────────────
QUADRANT_CONFIG = {
    1: {
        "label": "Risque élevé / Valeur élevée",
        "profil": "Gros compte en danger",
        "action": "Appel CSM sous 48h + offre de rétention personnalisée",
    },
    2: {
        "label": "Risque élevé / Valeur faible",
        "profil": "Petit compte en danger",
        "action": "Email automatisé de réengagement + relance à J+7",
    },
    3: {
        "label": "Risque faible / Valeur élevée",
        "profil": "Gros compte fidèle",
        "action": "Surveiller, programme de fidélisation, ne pas déranger",
    },
    4: {
        "label": "Risque faible / Valeur faible",
        "profil": "Petit compte stable",
        "action": "Aucune action prioritaire",
    },
}


def assign_quadrant(churn_score: float, mrr: float, mrr_median: float) -> int:
    """Retourne le quadrant (1-4) selon le croisement risque / valeur."""
    risque_eleve = churn_score >= RISK_THRESHOLD
    valeur_elevee = mrr >= mrr_median

    if risque_eleve and valeur_elevee:
        return 1
    elif risque_eleve and not valeur_elevee:
        return 2
    elif not risque_eleve and valeur_elevee:
        return 3
    else:
        return 4


def main():
    os.makedirs("outputs", exist_ok=True)

    # ── Chargement de scores.csv ───────────────────────────────────────────────
    scores_path = "outputs/scores.csv"
    if not os.path.exists(scores_path):
        print(f"ERREUR : {scores_path} introuvable.")
        print("Exécutez d'abord : python src/generate_scores.py")
        return

    print("Chargement de scores.csv...")
    scores_df = pd.read_csv(scores_path)
    print(f"  {len(scores_df)} comptes scorés")

    # ── Chargement de analytics.csv pour récupérer le MRR ─────────────────────
    analytics_path = "data/processed/analytics.csv"
    if not os.path.exists(analytics_path):
        print(f"ERREUR : {analytics_path} introuvable.")
        print("Exécutez d'abord : python src/build_analytics.py")
        return

    print("Chargement de analytics.csv...")
    analytics_df = pd.read_csv(analytics_path)

    # Colonnes contextuelles à récupérer pour enrichir la priorisation
    context_cols = [
        "account_id", "avg_mrr", "plan_tier", "industry", "seats",
        "avg_usage_count", "unique_features_used", "nb_tickets",
        "avg_satisfaction", "nb_escalations", "avg_sub_duration",
        "auto_renew_rate", "total_usage_count", "avg_error_rate",
        "nb_urgent_tickets"
    ]
    available_context = [c for c in context_cols if c in analytics_df.columns]
    analytics_subset = analytics_df[available_context].copy()

    # ── Fusion ─────────────────────────────────────────────────────────────────
    df = scores_df.merge(analytics_subset, on="account_id", how="left")
    print(f"  {df['avg_mrr'].isna().sum()} comptes sans MRR (imputés à la médiane)")

    # Imputation des MRR manquants par la médiane
    mrr_median = df["avg_mrr"].median()
    df["avg_mrr"] = df["avg_mrr"].fillna(mrr_median)

    print(f"\nSeuil MRR (médiane)  : {mrr_median:,.0f} €/mois")
    print(f"Seuil risque         : churn_score >= {RISK_THRESHOLD}")

    # ── Segmentation ──────────────────────────────────────────────────────────
    df["quadrant"] = df.apply(
        lambda row: assign_quadrant(row["churn_score"], row["avg_mrr"], mrr_median),
        axis=1
    )
    df["quadrant_label"] = df["quadrant"].map(
        lambda q: QUADRANT_CONFIG[q]["label"]
    )
    df["action"] = df["quadrant"].map(
        lambda q: QUADRANT_CONFIG[q]["action"]
    )

    # ── Tri : priorité 1 en premier, puis churn_score décroissant ─────────────
    df = df.sort_values(
        ["quadrant", "churn_score"],
        ascending=[True, False]
    ).reset_index(drop=True)

    # ── Construction du CSV de priorisation ───────────────────────────────────
    output_cols = [
        "account_id", "churn_score", "risk_level", "avg_mrr",
        "quadrant", "quadrant_label", "action"
    ]
    # Colonnes contextuelles additionnelles présentes
    for col in ["plan_tier", "industry", "seats", "avg_usage_count",
                "unique_features_used", "nb_tickets", "avg_satisfaction",
                "nb_escalations", "avg_sub_duration", "auto_renew_rate",
                "total_usage_count", "avg_error_rate", "nb_urgent_tickets"]:
        if col in df.columns:
            output_cols.append(col)

    output_df = df[output_cols].rename(columns={"avg_mrr": "mrr"})

    output_path = "outputs/priorisation.csv"
    output_df.to_csv(output_path, index=False)

    # ── Résumé ────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("RÉSUMÉ DE LA SEGMENTATION RISQUE / VALEUR")
    print(f"{'='*60}")

    quadrant_stats = (
        df.groupby("quadrant")
        .agg(
            nb_comptes=("account_id", "count"),
            mrr_total=("avg_mrr", "sum"),
            score_moyen=("churn_score", "mean"),
        )
        .reset_index()
    )

    total_mrr = df["avg_mrr"].sum()
    for _, row in quadrant_stats.iterrows():
        q = int(row["quadrant"])
        cfg = QUADRANT_CONFIG[q]
        pct = row["nb_comptes"] / len(df) * 100
        mrr_pct = row["mrr_total"] / total_mrr * 100
        print(f"\n  Q{q} — {cfg['label']}")
        print(f"      Comptes : {int(row['nb_comptes'])} ({pct:.1f}%)")
        print(f"      MRR     : {row['mrr_total']:,.0f} € ({mrr_pct:.1f}% du portefeuille)")
        print(f"      Score moyen : {row['score_moyen']:.3f}")
        print(f"      Action  : {cfg['action']}")

    mrr_a_risque = df[df["quadrant"].isin([1, 2])]["avg_mrr"].sum()
    print(f"\n  MRR total à risque (Q1 + Q2) : {mrr_a_risque:,.0f} €/mois")
    print(f"  ({mrr_a_risque / total_mrr * 100:.1f}% du MRR total)")

    print(f"\nFichier de priorisation sauvegarde : {output_path}")
    print("Prochaine etape : streamlit run src/dashboard.py")


if __name__ == "__main__":
    main()
