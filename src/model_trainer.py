import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix

def train_and_compare():
    dataset_path = 'outputs/dataset_final.csv'
    model_dir = 'outputs/model'
    report_dir = 'outputs/reports'
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    if not os.path.exists(dataset_path):
        print(f'Dataset {dataset_path} not found.')
        return
        
    df = pd.read_csv(dataset_path)
    y = df['churn_flag'].astype(int)
    X = df.drop(columns=['account_id', 'account_name', 'signup_date', 'churn_flag'])
    X = pd.get_dummies(X, drop_first=True)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 1. Random Forest with GridSearchCV
    print('Tuning Random Forest...')
    rf_param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, cv=3, scoring='roc_auc', n_jobs=-1)
    rf_grid.fit(X_train, y_train)
    
    best_rf = rf_grid.best_estimator_
    rf_auc = roc_auc_score(y_test, best_rf.predict_proba(X_test)[:, 1])
    print(f'Best Random Forest AUC: {rf_auc:.4f}')
    
    # 2. XGBoost
    print('Training XGBoost...')
    xgb = XGBClassifier(random_state=42, eval_metric='logloss')
    xgb.fit(X_train, y_train)
    xgb_auc = roc_auc_score(y_test, xgb.predict_proba(X_test)[:, 1])
    print(f'XGBoost AUC: {xgb_auc:.4f}')
    
    # Compare and Save Best
    best_model_name = 'RandomForest' if rf_auc >= xgb_auc else 'XGBoost'
    best_model = best_rf if rf_auc >= xgb_auc else xgb
    best_auc = max(rf_auc, xgb_auc)
    
    joblib.dump(best_model, os.path.join(model_dir, f'best_churn_model.joblib'))
    
    # Feature Importance (for best model)
    importances = pd.Series(best_model.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    # Save Report
    with open(os.path.join(report_dir, 'model_comparison_report.txt'), 'w') as f:
        f.write('--- Model Comparison Report ---\\n')
        f.write(f'Random Forest (Tuned) AUC: {rf_auc:.4f}\\n')
        f.write(f'XGBoost AUC: {xgb_auc:.4f}\\n')
        f.write(f'Best Model: {best_model_name}\\n\\n')
        f.write(f'--- Best Model Performance ({best_model_name}) ---\\n')
        f.write(f'Classification Report:\\n')
        f.write(classification_report(y_test, best_model.predict(X_test)))
        f.write('\\nConfusion Matrix:\\n')
        f.write(str(confusion_matrix(y_test, best_model.predict(X_test))))
        f.write('\\n\\nFeature Importances:\\n')
        f.write(importances.to_string())
        
    print(f'Comparison complete. Best Model: {best_model_name} (AUC: {best_auc:.4f})')

if __name__ == '__main__':
    train_and_compare()
