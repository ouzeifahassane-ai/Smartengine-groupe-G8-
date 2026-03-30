import pandas as pd
import numpy as np
import os

def run_feature_engineering():
    # Chemins des fichiers
    outputs_dir = 'outputs'
    accounts_path = os.path.join(outputs_dir, 'accounts_clean.csv')
    subscriptions_path = os.path.join(outputs_dir, 'subscriptions_clean.csv')
    feature_usage_path = os.path.join(outputs_dir, 'feature_usage_clean.csv')
    support_tickets_path = os.path.join(outputs_dir, 'support_tickets_clean.csv')
    churn_events_path = os.path.join(outputs_dir, 'churn_events_clean.csv')
    
    # Charger les fichiers
    print("Chargement des fichiers...")
    try:
        df_accounts = pd.read_csv(accounts_path)
        df_subs = pd.read_csv(subscriptions_path)
        df_usage = pd.read_csv(feature_usage_path)
        df_tickets = pd.read_csv(support_tickets_path)
        df_churn_events = pd.read_csv(churn_events_path)
    except FileNotFoundError as e:
        print(f"Erreur : {e}")
        return

    # Convertir les colonnes numériques pour gérer les 'Unknown'
    df_subs['mrr_amount'] = pd.to_numeric(df_subs['mrr_amount'], errors='coerce')
    df_subs['auto_renew_flag'] = pd.to_numeric(df_subs['auto_renew_flag'], errors='coerce')
    df_tickets['satisfaction_score'] = pd.to_numeric(df_tickets['satisfaction_score'], errors='coerce')
    df_tickets['escalation_flag'] = pd.to_numeric(df_tickets['escalation_flag'], errors='coerce')
    df_usage['usage_count'] = pd.to_numeric(df_usage['usage_count'], errors='coerce')
    df_usage['error_count'] = pd.to_numeric(df_usage['error_count'], errors='coerce')

    # Joindre account_id à usage via subscriptions
    # car account_id n'est pas directement dans usage
    df_usage = df_usage.merge(df_subs[['subscription_id', 'account_id']], on='subscription_id', how='left')


    # Prétraitement des dates pour subscriptions
    df_subs['start_date'] = pd.to_datetime(df_subs['start_date'], errors='coerce')
    df_subs['end_date'] = pd.to_datetime(df_subs['end_date'], errors='coerce')
    df_subs['duree_jours'] = (df_subs['end_date'] - df_subs['start_date']).dt.days

    # 1. Agrégations par client (account_id)
    
    # Subscriptions
    subs_agg = df_subs.groupby('account_id').agg(
        mrr_amount=('mrr_amount', 'mean'),
        nb_subscriptions=('subscription_id', 'count'),
        duree_abonnement_jours=('duree_jours', 'mean'),
        auto_renew_rate=('auto_renew_flag', 'mean')
    ).reset_index()

    # Support Tickets
    tickets_agg = df_tickets.groupby('account_id').agg(
        nb_tickets=('ticket_id', 'count'),
        satisfaction_score_moyen=('satisfaction_score', 'mean'),
        nb_tickets_urgents=('priority', lambda x: (x == 'Urgent').sum()),
        nb_escalations=('escalation_flag', 'sum')
    ).reset_index()

    # Feature Usage
    usage_agg = df_usage.groupby('account_id').agg(
        usage_count_moyen=('usage_count', 'mean'),
        nb_features_distinctes=('feature_name', 'nunique'),
        error_count_moyen=('error_count', 'mean')
    ).reset_index()

    # Churn Events
    df_churn_events['a_churne'] = 1
    churn_agg = df_churn_events[['account_id', 'a_churne']].drop_duplicates()

    # 2. Fusionner le tout dans le tableau final (à partir de accounts)
    features_master = df_accounts[['account_id', 'plan_tier', 'industry', 'seats', 'churn_flag']].copy()
    
    # Joindre les agrégations
    features_master = features_master.merge(subs_agg, on='account_id', how='left')
    features_master = features_master.merge(tickets_agg, on='account_id', how='left')
    features_master = features_master.merge(usage_agg, on='account_id', how='left')
    features_master = features_master.merge(churn_agg, on='account_id', how='left')

    # Remplir les valeurs manquantes
    features_master['a_churne'] = features_master['a_churne'].fillna(0).astype(int)
    # Pour les comptes sans tickets ou sans usage, on met 0 pour les comptes de tickets
    cols_to_fill_zero = ['nb_subscriptions', 'nb_tickets', 'nb_tickets_urgents', 'nb_escalations', 'nb_features_distinctes']
    features_master[cols_to_fill_zero] = features_master[cols_to_fill_zero].fillna(0)
    
    # Sauvegarder le fichier final
    output_path = os.path.join(outputs_dir, 'features_master.csv')
    features_master.to_csv(output_path, index=False)
    print(f"Tableau final sauvegardé dans {output_path}")

    # Générer le rapport de feature engineering
    report_path = os.path.join(outputs_dir, 'rapport-features.md')
    report_content = [
        "# Rapport de Feature Engineering - smartEngine",
        f"Date : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## Statistiques descriptives du tableau final",
        features_master.describe().to_markdown(),
        "\n## Observations clés",
        f"- Nombre total de clients : {len(features_master)}",
        f"- Taux de churn global : {features_master['a_churne'].mean():.2%}",
        f"- Nombre de features créées : {len(features_master.columns) - 1} (hors account_id)",
        f"- Secteur le plus représenté : {features_master['industry'].mode()[0]}",
        "\n## Détail des colonnes",
        "- `plan_tier` : Plan tarifaire du client",
        "- `industry` : Secteur d'activité",
        "- `seats` : Nombre de sièges",
        "- `mrr_amount` : Revenu mensuel récurrent moyen",
        "- `nb_subscriptions` : Nombre total d'abonnements",
        "- `duree_abonnement_jours` : Durée moyenne des abonnements",
        "- `auto_renew_rate` : Taux de renouvellement automatique",
        "- `nb_tickets` : Volume de tickets de support",
        "- `satisfaction_score_moyen` : Score CSAT moyen",
        "- `nb_tickets_urgents` : Nombre de tickets de priorité urgente",
        "- `nb_escalations` : Nombre d'escalades de support",
        "- `usage_count_moyen` : Intensité moyenne d'utilisation",
        "- `nb_features_distinctes` : Diversité des fonctionnalités utilisées",
        "- `error_count_moyen` : Taux d'erreur moyen rencontré",
        "- `a_churne` : Indicateur de présence dans les événements de churn",
        "- `churn_flag` : Variable cible (churn réel)"
    ]
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_content))
    print(f"Rapport de feature engineering généré : {report_path}")

    # Afficher les premières lignes
    print("\n--- 5 premières lignes du tableau final ---")
    print(features_master.head())


if __name__ == "__main__":
    run_feature_engineering()
