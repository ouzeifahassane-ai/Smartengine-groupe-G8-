import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict

def parse_date(date_str):
    if not date_str: return None
    for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def load_csv(path):
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def build_features():
    cleaned_dir = 'outputs/cleaned'
    processed_path = 'data/processed/analytics.csv'
    
    # 1. Chargement des données sources pour les calculs temporels
    accounts = load_csv(os.path.join(cleaned_dir, 'cleaned_accounts.csv'))
    usage = load_csv(os.path.join(cleaned_dir, 'cleaned_feature_usage.csv'))
    tickets = load_csv(os.path.join(cleaned_dir, 'cleaned_support_tickets.csv'))
    subs = load_csv(os.path.join(cleaned_dir, 'cleaned_subscriptions.csv'))
    
    # Définition d'une date de référence (max usage_date dans le dataset)
    usage_dates = [parse_date(u['usage_date']) for u in usage if u['usage_date']]
    ref_date = max(usage_dates) if usage_dates else datetime.now()
    
    # 2. Calcul des features
    
    # Map sub_id -> account_id
    sub_to_acc = {s['subscription_id']: s['account_id'] for s in subs}
    
    # Features Usage : trend et récence
    usage_stats = defaultdict(lambda: {'last_usage': None, 'vol_recent': 0, 'vol_old': 0})
    date_90d = ref_date - timedelta(days=90)
    date_180d = ref_date - timedelta(days=180)
    
    for u in usage:
        acc_id = sub_to_acc.get(u['subscription_id'])
        if not acc_id: continue
        
        dt = parse_date(u['usage_date'])
        if not dt: continue
        
        # Récence
        if not usage_stats[acc_id]['last_usage'] or dt > usage_stats[acc_id]['last_usage']:
            usage_stats[acc_id]['last_usage'] = dt
        
        # Trend (comparaison 90j vs 90-180j)
        count = int(u['usage_count'])
        if dt >= date_90d:
            usage_stats[acc_id]['vol_recent'] += count
        elif dt >= date_180d:
            usage_stats[acc_id]['vol_old'] += count

    # Features Tickets : ratio critiques
    ticket_stats = defaultdict(lambda: {'critical': 0, 'total': 0, 'delays': []})
    for t in tickets:
        acc_id = t['account_id']
        ticket_stats[acc_id]['total'] += 1
        if t['priority'].lower() in ['high', 'urgent', 'critical']:
            ticket_stats[acc_id]['critical'] += 1
        if t['resolution_time_hours']:
            ticket_stats[acc_id]['delays'].append(float(t['resolution_time_hours']))

    # Features Subs : mrr_evolution et plan_changes
    sub_stats = defaultdict(lambda: {'changes': 0, 'mrr_history': []})
    for s in subs:
        acc_id = s['account_id']
        if s['upgrade_flag'].lower() == 'true' or s['downgrade_flag'].lower() == 'true':
            sub_stats[acc_id]['changes'] += 1
        if s['mrr_amount']:
            sub_stats[acc_id]['mrr_history'].append(float(s['mrr_amount']))

    # 3. Enrichissement de la table analytics existante
    analytics_data = load_csv(processed_path)
    enriched_table = []
    
    for row in analytics_data:
        acc_id = row['account_id']
        
        # Seniority (en mois)
        signup_dt = parse_date(row['signup_date'])
        if signup_dt:
            seniority = (ref_date - signup_dt).days / 30.44
            row['seniority_months'] = round(seniority, 1)
        else:
            row['seniority_months'] = 0
            
        # Usage Features
        stats_u = usage_stats.get(acc_id, {'last_usage': None, 'vol_recent': 0, 'vol_old': 0})
        if stats_u['last_usage']:
            row['days_since_last_login'] = (ref_date - stats_u['last_usage']).days
        else:
            row['days_since_last_login'] = 999 # Valeur par défaut si aucun usage
            
        recent = stats_u['vol_recent']
        old = stats_u['vol_old']
        row['usage_trend_3m'] = round(recent / (old if old > 0 else 1), 2)
        
        # Tickets Features
        stats_t = ticket_stats.get(acc_id, {'critical': 0, 'total': 0, 'delays': []})
        row['ratio_critical_tickets'] = round(stats_t['critical'] / (stats_t['total'] if stats_t['total'] > 0 else 1), 2)
        row['avg_resolution_delay'] = round(sum(stats_t['delays']) / len(stats_t['delays']) if stats_t['delays'] else 0, 2)
        
        # Subscriptions Features
        stats_s = sub_stats.get(acc_id, {'changes': 0, 'mrr_history': []})
        row['plan_changes_count'] = stats_s['changes']
        if len(stats_s['mrr_history']) >= 2:
            row['mrr_evolution'] = round(stats_s['mrr_history'][-1] - stats_s['mrr_history'][0], 2)
        else:
            row['mrr_evolution'] = 0.0
            
        enriched_table.append(row)

    # 4. Export final
    if enriched_table:
        keys = enriched_table[0].keys()
        with open(processed_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(enriched_table)
        print(f"Features ajoutées avec succès dans {processed_path}")

if __name__ == "__main__":
    build_features()
