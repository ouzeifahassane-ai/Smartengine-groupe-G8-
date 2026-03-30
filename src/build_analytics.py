"""
build_analytics.py — Projet smartEngine Groupe G8
Sprint 2 : Construction de la table analytique

Utilisation :
    python src/build_analytics.py

Prérequis :
    - Avoir exécuté src/clean_data.py avant (fichiers dans data/processed/)

Résultat :
    - data/processed/analytics.csv (1 ligne par account_id)
"""

import pandas as pd
import numpy as np
import os


def build_analytics():

    processed_dir = "data/processed"
    output_dir    = "outputs"

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(output_dir,    exist_ok=True)

    # ── Chargement des fichiers nettoyés ───────────────────────────────────
    print("Chargement des fichiers nettoyés...")
    accounts = pd.read_csv(f"{processed_dir}/accounts.csv",        parse_dates=["signup_date"])
    subs     = pd.read_csv(f"{processed_dir}/subscriptions.csv",   parse_dates=["start_date", "end_date"])
    usage    = pd.read_csv(f"{processed_dir}/feature_usage.csv",   parse_dates=["usage_date"])
    tickets  = pd.read_csv(f"{processed_dir}/support_tickets.csv", parse_dates=["submitted_at", "closed_at"])
    churn    = pd.read_csv(f"{processed_dir}/churn_events.csv",    parse_dates=["churn_date"])

    # ── Table de référence : accounts ─────────────────────────────────────
    print("Construction de la table de référence...")
    analytics = accounts[["account_id", "industry", "country", "signup_date",
                           "referral_source", "plan_tier", "seats", "is_trial"]].copy()

    # Ancienneté du compte en jours
    date_ref = pd.Timestamp("today").normalize()
    analytics["account_age_days"] = (date_ref - analytics["signup_date"]).dt.days

    # ── Enrichissement depuis subscriptions ───────────────────────────────
    print("Agrégation subscriptions...")

    # Abonnement actif par compte (is_active = True)
    subs_active = subs[subs["is_active"] == True].sort_values("start_date")
    subs_active_agg = subs_active.groupby("account_id").agg(
        mrr_current       = ("mrr_amount",      "last"),
        current_plan_tier = ("plan_tier",        "last"),
        billing_frequency = ("billing_frequency","last"),
        auto_renew_flag   = ("auto_renew_flag",  "last"),
        subscription_start= ("start_date",       "min"),
    ).reset_index()
    subs_active_agg["subscription_age_days"] = (
        date_ref - subs_active_agg["subscription_start"]
    ).dt.days

    # Nombre total d'upgrades et downgrades par compte
    subs_changes = subs.groupby("account_id").agg(
        nb_upgrades   = ("upgrade_flag",   "sum"),
        nb_downgrades = ("downgrade_flag", "sum"),
        nb_subscriptions = ("subscription_id", "count"),
    ).reset_index()
    subs_changes["nb_plan_changes"] = (
        subs_changes["nb_upgrades"] + subs_changes["nb_downgrades"]
    )

    analytics = analytics.merge(subs_active_agg[[ 
        "account_id", "mrr_current", "current_plan_tier",
        "billing_frequency", "auto_renew_flag", "subscription_age_days"
    ]], on="account_id", how="left")

    analytics = analytics.merge(subs_changes[[
        "account_id", "nb_upgrades", "nb_downgrades", "nb_plan_changes", "nb_subscriptions"
    ]], on="account_id", how="left")

    # ── Enrichissement depuis feature_usage ───────────────────────────────
    print("Agrégation feature_usage...")

    # Joindre usage avec subscriptions pour récupérer account_id
    usage_with_account = usage.merge(
        subs[["subscription_id", "account_id"]], on="subscription_id", how="left"
    )

    # Agrégations globales par compte
    usage_agg = usage_with_account.groupby("account_id").agg(
        avg_usage_count       = ("usage_count",          "mean"),
        total_usage_count     = ("usage_count",          "sum"),
        nb_features_used      = ("feature_name",         "nunique"),
        avg_session_duration  = ("usage_duration_secs",  "mean"),
        total_errors          = ("error_count",          "sum"),
        total_usage_events    = ("usage_id",             "count"),
        last_usage_date       = ("usage_date",           "max"),
        beta_feature_used     = ("is_beta_feature",      "max"),
    ).reset_index()

    usage_agg["error_rate"] = (
        usage_agg["total_errors"] / usage_agg["total_usage_events"].replace(0, np.nan)
    ).fillna(0).round(4)

    usage_agg["days_since_last_usage"] = (
        date_ref - usage_agg["last_usage_date"]
    ).dt.days

    analytics = analytics.merge(usage_agg[[
        "account_id", "avg_usage_count", "total_usage_count", "nb_features_used",
        "avg_session_duration", "error_rate", "days_since_last_usage", "beta_feature_used"
    ]], on="account_id", how="left")

    # ── Enrichissement depuis support_tickets ─────────────────────────────
    print("Agrégation support_tickets...")

    tickets_agg = tickets.groupby("account_id").agg(
        nb_tickets_total      = ("ticket_id",                    "count"),
        nb_tickets_urgent     = ("priority",                     lambda x: (x == "urgent").sum()),
        nb_escalations        = ("escalation_flag",              "sum"),
        avg_resolution_hours  = ("resolution_time_hours",        "mean"),
        avg_satisfaction      = ("satisfaction_score",           "mean"),
        last_ticket_date      = ("submitted_at",                 "max"),
    ).reset_index()

    tickets_agg["escalation_rate"] = (
        tickets_agg["nb_escalations"] / tickets_agg["nb_tickets_total"].replace(0, np.nan)
    ).fillna(0).round(4)

    tickets_agg["days_since_last_ticket"] = (
        date_ref - tickets_agg["last_ticket_date"]
    ).dt.days

    analytics = analytics.merge(tickets_agg[[
        "account_id", "nb_tickets_total", "nb_tickets_urgent", "escalation_rate",
        "avg_resolution_hours", "avg_satisfaction", "days_since_last_ticket"
    ]], on="account_id", how="left")

    # Comptes sans ticket → imputation à 0 (absence de ticket = signal positif)
    ticket_cols_zero = ["nb_tickets_total", "nb_tickets_urgent", "nb_escalations", "escalation_rate"]
    for col in ticket_cols_zero:
        if col in analytics.columns:
            analytics[col] = analytics[col].fillna(0)

    # ── Variable cible depuis churn_events ────────────────────────────────
    print("Construction de la variable cible...")

    # Conserver uniquement le churn le plus récent par compte
    churn_latest = churn.sort_values("churn_date").groupby("account_id").last().reset_index()
    churn_latest = churn_latest[["account_id", "churn_date", "reason_code",
                                  "preceding_downgrade_flag", "is_reactivation"]]
    churn_latest["churned"] = 1

    analytics = analytics.merge(churn_latest[["account_id", "churned", "churn_date",
                                               "reason_code", "preceding_downgrade_flag"]],
                                 on="account_id", how="left")
    analytics["churned"] = analytics["churned"].fillna(0).astype(int)

    # ── Nettoyage final ────────────────────────────────────────────────────
    # Imputation des valeurs manquantes résiduelles (comptes sans abonnement actif)
    num_cols = analytics.select_dtypes(include=["float64", "int64"]).columns
    for col in num_cols:
        if analytics[col].isnull().sum() > 0:
            analytics[col] = analytics[col].fillna(analytics[col].median())

    # Supprimer les colonnes de dates intermédiaires non utiles au modèle
    analytics = analytics.drop(columns=["signup_date", "churn_date"], errors="ignore")

    # ── Sauvegarde ────────────────────────────────────────────────────────
    output_path = f"{processed_dir}/analytics.csv"
    analytics.to_csv(output_path, index=False)

    print(f"\n✓ Table analytique sauvegardée : {output_path}")
    print(f"  Lignes  : {len(analytics)}")
    print(f"  Colonnes: {len(analytics.columns)}")
    print(f"  Taux de churn : {round(analytics['churned'].mean() * 100, 1)}%")
    print(f"\nColonnes : {list(analytics.columns)}")


if __name__ == "__main__":
    build_analytics()