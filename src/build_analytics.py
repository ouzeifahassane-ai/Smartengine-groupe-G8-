import csv
import os
from collections import defaultdict

def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def build_analytics():
    cleaned_dir = 'outputs/cleaned'
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)

    # 1. Chargement des données
    accounts = load_csv(os.path.join(cleaned_dir, 'cleaned_accounts.csv'))
    subs = load_csv(os.path.join(cleaned_dir, 'cleaned_subscriptions.csv'))
    usage = load_csv(os.path.join(cleaned_dir, 'cleaned_feature_usage.csv'))
    tickets = load_csv(os.path.join(cleaned_dir, 'cleaned_support_tickets.csv'))
    churns = load_csv(os.path.join(cleaned_dir, 'cleaned_churn_events.csv'))

    if not accounts:
        print("Erreur : Aucun compte trouvé dans cleaned_accounts.csv")
        return

    # 2. Préparation des agrégations
    
    # Map subscription_id -> account_id et agrégation MRR
    sub_to_account = {}
    account_subs_metrics = defaultdict(lambda: {'total_mrr': 0.0, 'sub_count': 0})
    for s in subs:
        acc_id = s['account_id']
        sub_id = s['subscription_id']
        sub_to_account[sub_id] = acc_id
        try:
            account_subs_metrics[acc_id]['total_mrr'] += float(s['mrr_amount'])
            account_subs_metrics[acc_id]['sub_count'] += 1
        except: pass

    # Agrégation Usage
    account_usage_metrics = defaultdict(lambda: {'total_usage': 0, 'total_duration': 0.0})
    for u in usage:
        sub_id = u['subscription_id']
        acc_id = sub_to_account.get(sub_id)
        if acc_id:
            try:
                account_usage_metrics[acc_id]['total_usage'] += int(u['usage_count'])
                account_usage_metrics[acc_id]['total_duration'] += float(u['usage_duration_secs'])
            except: pass

    # Agrégation Tickets
    account_ticket_metrics = defaultdict(lambda: {'ticket_count': 0, 'avg_res_time': 0.0})
    for t in tickets:
        acc_id = t['account_id']
        account_ticket_metrics[acc_id]['ticket_count'] += 1
        try:
            account_ticket_metrics[acc_id]['avg_res_time'] += float(t['resolution_time_hours'])
        except: pass
    
    for acc_id in account_ticket_metrics:
        if account_ticket_metrics[acc_id]['ticket_count'] > 0:
            account_ticket_metrics[acc_id]['avg_res_time'] /= account_ticket_metrics[acc_id]['ticket_count']

    # Churn Flags
    churned_accounts = {c['account_id'] for c in churns}

    # 3. Construction de la table finale
    analytics_table = []
    for acc in accounts:
        acc_id = acc['account_id']
        
        row = acc.copy()
        # Fusion avec Subscriptions
        row['total_mrr'] = account_subs_metrics[acc_id]['total_mrr']
        row['sub_count'] = account_subs_metrics[acc_id]['sub_count']
        
        # Fusion avec Usage
        row['total_usage_count'] = account_usage_metrics[acc_id]['total_usage']
        row['total_usage_duration'] = account_usage_metrics[acc_id]['total_duration']
        
        # Fusion avec Tickets
        row['support_ticket_count'] = account_ticket_metrics[acc_id]['ticket_count']
        row['avg_ticket_resolution_time'] = round(account_ticket_metrics[acc_id]['avg_res_time'], 2)
        
        # Flag de churn (target variable)
        row['has_churn_event'] = acc_id in churned_accounts
        
        analytics_table.append(row)

    # 4. Export
    if analytics_table:
        keys = analytics_table[0].keys()
        output_path = os.path.join(output_dir, 'analytics.csv')
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(analytics_table)
        print(f"Table analytique générée avec succès : {output_path} ({len(analytics_table)} lignes)")

if __name__ == "__main__":
    build_analytics()
