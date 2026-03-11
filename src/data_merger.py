import pandas as pd
import os

def merge_data():
    cleaned_dir = 'outputs/cleaned'
    features_dir = 'outputs/features'
    output_dir = 'outputs'
    
    # Base accounts info
    accounts = pd.read_csv(os.path.join(cleaned_dir, 'cleaned_accounts.csv'))
    
    # Aggregated features
    features = pd.read_csv(os.path.join(features_dir, 'features_per_account.csv'))
    
    # Merge on account_id
    # We use inner join or left join depending on if we want all accounts or only those with features.
    # Since features_per_account.csv was built from accounts, left join is safe.
    dataset = accounts.merge(features, on='account_id', how='left')
    
    # Handle duplicates (if any)
    dataset = dataset.drop_duplicates()
    
    # Final cleanup
    # Remove redundant columns if necessary (like duplicate is_trial if it was in both)
    if 'is_trial_x' in dataset.columns and 'is_trial_y' in dataset.columns:
        dataset['is_trial'] = dataset['is_trial_x']
        dataset = dataset.drop(columns=['is_trial_x', 'is_trial_y'])
    
    # Fill remaining NaNs if any
    dataset = dataset.fillna(0)
    
    # Save final dataset
    output_path = os.path.join(output_dir, 'dataset_final.csv')
    dataset.to_csv(output_path, index=False)
    print(f'Final dataset merged and saved to {output_path}')
    print(f'Shape: {dataset.shape}')

if __name__ == '__main__':
    merge_data()
