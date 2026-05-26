import pandas as pd
import numpy as np
import os

def build_features():
    """
    Script de feature engineering pour la prédiction de churn.
    Agrège les données brutes par account_id pour créer une table analytique.
    """
    # Configuration des chemins — données nettoyées par clean_data.py
    processed_dir = os.path.join('data', 'processed')

    os.makedirs(processed_dir, exist_ok=True)

    print("Chargement des données nettoyées...")

    try:
        df_accounts = pd.read_csv(os.path.join(processed_dir, 'accounts.csv'))
        df_subs = pd.read_csv(os.path.join(processed_dir, 'subscriptions.csv'))
        df_usage = pd.read_csv(os.path.join(processed_dir, 'feature_usage.csv'))
        df_tickets = pd.read_csv(os.path.join(processed_dir, 'support_tickets.csv'))
        df_churn = pd.read_csv(os.path.join(processed_dir, 'churn_events.csv'))
    except FileNotFoundError as e:
        print(f"Erreur : Un ou plusieurs fichiers introuvables. Exécutez d'abord clean_data.py. {e}")
        return

    # --- 1. PRÉPARATION DES DONNÉES ---

    # Conversion des dates
    df_subs['start_date'] = pd.to_datetime(df_subs['start_date'], errors='coerce')
    df_subs['end_date'] = pd.to_datetime(df_subs['end_date'], errors='coerce')
    
    # Calcul de la durée d'abonnement (en jours)
    df_subs['sub_duration_days'] = (df_subs['end_date'] - df_subs['start_date']).dt.days

    # Joindre account_id à l'usage (via subscriptions)
    # Note: On suppose que subscription_id fait le lien
    df_usage = df_usage.merge(df_subs[['subscription_id', 'account_id']], on='subscription_id', how='left')

    # --- 2. AGRÉGATIONS PAR ACCOUNT_ID ---

    print("Calcul des features agrégées...")

    # A. Features Abonnements
    subs_agg = df_subs.groupby('account_id').agg(
        avg_mrr=('mrr_amount', 'mean'),
        total_subs=('subscription_id', 'count'),
        avg_sub_duration=('sub_duration_days', 'mean'),
        auto_renew_rate=('auto_renew_flag', 'mean'),
        total_seats=('seats', 'sum')
    ).reset_index()

    # B. Features Usage
    usage_agg = df_usage.groupby('account_id').agg(
        total_usage_count=('usage_count', 'sum'),
        avg_usage_count=('usage_count', 'mean'),
        unique_features_used=('feature_name', 'nunique'),
        total_errors=('error_count', 'sum'),
        avg_error_rate=('error_count', 'mean')
    ).reset_index()

    # C. Features Support
    # On gère le cas où satisfaction_score peut être nul
    tickets_agg = df_tickets.groupby('account_id').agg(
        nb_tickets=('ticket_id', 'count'),
        avg_satisfaction=('satisfaction_score', 'mean'),
        nb_escalations=('escalation_flag', 'sum'),
        # Count high/urgent priority tickets
        nb_urgent_tickets=('priority', lambda x: x.isin(['high', 'urgent']).sum())
    ).reset_index()

    # --- 3. FUSION FINALE ---

    print("Fusion des features dans la table analytique...")
    
    # On part de la table accounts comme base
    master_df = df_accounts[['account_id', 'industry', 'plan_tier', 'seats']].copy()

    # Fusion successive
    master_df = master_df.merge(subs_agg, on='account_id', how='left')
    master_df = master_df.merge(usage_agg, on='account_id', how='left')
    master_df = master_df.merge(tickets_agg, on='account_id', how='left')

    # --- 4. GESTION DES VALEURS MANQUANTES ---

    # Remplissage par 0 pour les compteurs (si pas de tickets/usage -> 0)
    cols_to_zero = [
        'total_subs', 'total_usage_count', 'unique_features_used', 
        'total_errors', 'nb_tickets', 'nb_escalations', 'nb_urgent_tickets'
    ]
    master_df[cols_to_zero] = master_df[cols_to_zero].fillna(0)

    # Pour les moyennes (satisfaction, mrr), on peut laisser NaN ou imputer par la médiane
    # Ici, on laisse tel quel pour permettre une analyse de la corrélation
    
    # Variable cible : churn_flag dérivée de churn_events (1 = churné, 0 = fidèle)
    churned_ids = set(df_churn['account_id'])
    master_df['churn_flag'] = master_df['account_id'].apply(lambda x: 1 if x in churned_ids else 0)

    # --- 5. SAUVEGARDE ---

    output_path = os.path.join(processed_dir, 'analytics.csv')
    master_df.to_csv(output_path, index=False)
    
    print(f"Succès ! Table analytique générée : {output_path}")
    print(f"Dimensions : {master_df.shape[0]} lignes, {master_df.shape[1]} colonnes.")
    print("\nAperçu des colonnes créées :")
    print(master_df.columns.tolist())

if __name__ == "__main__":
    build_features()
