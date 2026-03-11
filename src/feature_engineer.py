import pandas as pd
import numpy as np
import os

def feature_engineering():
    cleaned_dir = 'outputs/cleaned'
    features_dir = 'outputs/features'
    os.makedirs(features_dir, exist_ok=True)
    
    # Load data
    accounts = pd.read_csv(os.path.join(cleaned_dir, 'cleaned_accounts.csv'), parse_dates=['signup_date'])
    subs = pd.read_csv(os.path.join(cleaned_dir, 'cleaned_subscriptions.csv'), parse_dates=['start_date', 'end_date'])
    usage = pd.read_csv(os.path.join(cleaned_dir, 'cleaned_feature_usage.csv'), parse_dates=['usage_date'])
    tickets = pd.read_csv(os.path.join(cleaned_dir, 'cleaned_support_tickets.csv'), parse_dates=['submitted_at', 'closed_at'])
    
    # 1. tenure_days
    # Use 2026-03-11 as reference date (today)
    ref_date = pd.Timestamp('2026-03-11')
    accounts['tenure_days'] = (ref_date - accounts['signup_date']).dt.days
    
    # 2. usage_trend_30j & 3. error_rate
    # Need to link usage to account_id via subscriptions
    sub_map = subs[['subscription_id', 'account_id']].drop_duplicates()
    usage_with_acc = usage.merge(sub_map, on='subscription_id', how='left')
    
    # Error rate per account
    usage_stats = usage_with_acc.groupby('account_id').agg({
        'error_count': 'sum',
        'usage_count': 'sum'
    }).reset_index()
    usage_stats['error_rate'] = usage_stats['error_count'] / usage_stats['usage_count'].replace(0, 1)
    
    # Usage trend (very simplified: usage in last 30 days vs previous 30 days)
    last_30_days = usage_with_acc[usage_with_acc['usage_date'] >= (ref_date - pd.Timedelta(days=30))]
    prev_30_days = usage_with_acc[(usage_with_acc['usage_date'] < (ref_date - pd.Timedelta(days=30))) & 
                                  (usage_with_acc['usage_date'] >= (ref_date - pd.Timedelta(days=60)))]
    
    last_30_sum = last_30_days.groupby('account_id')['usage_count'].sum().rename('usage_last_30')
    prev_30_sum = prev_30_days.groupby('account_id')['usage_count'].sum().rename('usage_prev_30')
    
    trend = pd.concat([last_30_sum, prev_30_sum], axis=1).fillna(0)
    trend['usage_trend_30j'] = (trend['usage_last_30'] - trend['usage_prev_30']) / trend['usage_prev_30'].replace(0, 1)
    
    # 4. nb_tickets_urgents, 5. avg_resolution_time, 6. satisfaction_score_moyen
    ticket_stats = tickets.groupby('account_id').agg({
        'priority': lambda x: (x == 'urgent').sum(),
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean'
    }).rename(columns={
        'priority': 'nb_tickets_urgents',
        'resolution_time_hours': 'avg_resolution_time',
        'satisfaction_score': 'satisfaction_score_moyen'
    }).reset_index()
    
    # 7. downgrade_flag, 8. auto_renew_flag
    sub_stats = subs.groupby('account_id').agg({
        'downgrade_flag': 'max',
        'auto_renew_flag': 'any'
    }).reset_index()
    sub_stats['downgrade_flag'] = sub_stats['downgrade_flag'].astype(int)
    sub_stats['auto_renew_flag'] = sub_stats['auto_renew_flag'].astype(int)
    
    # 9. is_trial
    # Already in accounts, but let\\'s ensure it\\'s consistent
    
    # 10. industry_risk_score (heuristic mapping)
    industry_risk = {
        'FinTech': 0.2,
        'EdTech': 0.5,
        'HealthTech': 0.3,
        'DevTools': 0.1,
        'E-commerce': 0.6,
        'Other': 0.4
    }
    accounts['industry_risk_score'] = accounts['industry'].map(industry_risk).fillna(0.4)
    
    # Merge all into one feature table
    final_features = accounts[['account_id', 'tenure_days', 'is_trial', 'industry_risk_score']]
    final_features = final_features.merge(usage_stats[['account_id', 'error_rate']], on='account_id', how='left')
    final_features = final_features.merge(trend[['usage_trend_30j']], on='account_id', how='left')
    final_features = final_features.merge(ticket_stats, on='account_id', how='left')
    final_features = final_features.merge(sub_stats, on='account_id', how='left')
    
    # Fill NaNs for accounts without usage or tickets
    final_features = final_features.fillna(0)
    
    # Save results
    output_path = os.path.join(features_dir, 'features_per_account.csv')
    final_features.to_csv(output_path, index=False)
    print(f'Features created and saved to {output_path}')

if __name__ == '__main__':
    feature_engineering()
