import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

def train_model():
    dataset_path = 'outputs/dataset_final.csv'
    model_dir = 'outputs/model'
    report_dir = 'outputs/reports'
    
    if not os.path.exists(dataset_path):
        print(f'Dataset {dataset_path} not found.')
        return
        
    df = pd.read_csv(dataset_path)
    
    # Target variable
    y = df['churn_flag'].astype(int)
    
    # Features (drop non-predictive columns)
    X = df.drop(columns=['account_id', 'account_name', 'signup_date', 'churn_flag'])
    
    # Basic encoding for categorical columns
    X = pd.get_dummies(X, drop_first=True)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Predictions
    y_pred_proba = rf.predict_proba(X_test)[:, 1]
    y_pred = rf.predict(X_test)
    
    # Evaluation
    auc_roc = roc_auc_score(y_test, y_pred_proba)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Variable importance
    importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    # Save model
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(rf, os.path.join(model_dir, 'churn_model_rf.joblib'))
    
    # Save report
    os.makedirs(report_dir, exist_ok=True)
    with open(os.path.join(report_dir, 'performance_report.txt'), 'w') as f:
        f.write(f'AUC-ROC: {auc_roc:.4f}\\n\\n')
        f.write('Classification Report:\\n')
        f.write(report)
        f.write('\\nConfusion Matrix:\\n')
        f.write(str(conf_matrix))
        f.write('\\n\\nFeature Importances:\\n')
        f.write(importances.to_string())
        
    print(f'Model trained and saved. AUC-ROC: {auc_roc:.4f}')
    print(f'Report saved to {os.path.join(report_dir, "performance_report.txt")}')

if __name__ == '__main__':
    train_model()
