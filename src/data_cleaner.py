import pandas as pd
import numpy as np
import os

def clean_data():
    raw_dir = 'data/raw'
    cleaned_dir = 'outputs/cleaned'
    os.makedirs(cleaned_dir, exist_ok=True)
    
    files = {
        'accounts': 'ravenstack_accounts.csv',
        'churn_events': 'ravenstack_churn_events.csv',
        'feature_usage': 'ravenstack_feature_usage.csv',
        'subscriptions': 'ravenstack_subscriptions.csv',
        'support_tickets': 'ravenstack_support_tickets.csv'
    }
    
    for key, filename in files.items():
        path = os.path.join(raw_dir, filename)
        if not os.path.exists(path):
            print(f'File {path} not found.')
            continue
            
        df = pd.read_csv(path)
        
        # 1. Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        if len(df) < initial_rows:
            print(f'{key}: Removed {initial_rows - len(df)} duplicates.')
            
        # 2. Normalize column names (already snake_case mostly, but let\\'s be sure)
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # 3. Handle specific missing values and types
        if key == 'accounts':
            df['signup_date'] = pd.to_datetime(df['signup_date'])
            
        elif key == 'churn_events':
            df['churn_date'] = pd.to_datetime(df['churn_date'])
            df['feedback_text'] = df['feedback_text'].fillna('no feedback')
            
        elif key == 'feature_usage':
            df['usage_date'] = pd.to_datetime(df['usage_date'])
            
        elif key == 'subscriptions':
            df['start_date'] = pd.to_datetime(df['start_date'])
            df['end_date'] = pd.to_datetime(df['end_date'])
            # end_date is NaN for active subscriptions, which is fine as NaT
            
        elif key == 'support_tickets':
            df['submitted_at'] = pd.to_datetime(df['submitted_at'])
            df['closed_at'] = pd.to_datetime(df['closed_at'])
            # Median imputation for satisfaction_score
            median_score = df['satisfaction_score'].median()
            df['satisfaction_score'] = df['satisfaction_score'].fillna(median_score)
            
        # 4. Save cleaned file
        output_path = os.path.join(cleaned_dir, f'cleaned_{key}.csv')
        df.to_csv(output_path, index=False)
        print(f'{key}: Cleaned and saved to {output_path}')

if __name__ == '__main__':
    clean_data()
