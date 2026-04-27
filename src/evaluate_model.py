import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os

# Configuration
INPUT_PATH = "data/processed/analytics.csv"
MODEL_PATH = "outputs/models/churn_model.joblib"
OUTPUT_DIR = "outputs/plots"

def evaluate():
    # 1. Chargement
    df = pd.read_csv(INPUT_PATH)
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparation des variables (identique à train_model)
    drop_cols = ['account_id', 'account_name', 'signup_date', 'churn_flag']
    X = df.drop(columns=drop_cols)
    y = df['churn_flag'].astype(int)
    
    # On reprend le même split
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    # 3. Prédictions
    y_pred = model.predict(X_test)
    
    # 4. Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Fidèle', 'Churn'], yticklabels=['Fidèle', 'Churn'])
    plt.ylabel('Réel')
    plt.xlabel('Prédit')
    plt.title('Matrice de Confusion - Meilleur Modèle')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f"{OUTPUT_DIR}/confusion_matrix.png")
    
    # 5. Importance des Features (Coefficients pour Logistic Regression)
    # Récupérer les noms des features après transformation
    preprocessor = model.named_steps['preprocessor']
    classifier = model.named_steps['classifier']
    
    num_features = preprocessor.transformers_[0][2]
    cat_features = preprocessor.transformers_[1][1].get_feature_names_out(preprocessor.transformers_[1][2])
    feature_names = list(num_features) + list(cat_features)
    
    if hasattr(classifier, 'coef_'):
        importance = classifier.coef_[0]
        feat_importances = pd.Series(importance, index=feature_names)
        
        plt.figure(figsize=(10, 8))
        feat_importances.nlargest(15).plot(kind='barh')
        plt.title('Top 15 des Features (Coefficients positifs - Facteurs de Churn)')
        plt.savefig(f"{OUTPUT_DIR}/feature_importance_churn.png")
        
        plt.figure(figsize=(10, 8))
        feat_importances.nsmallest(15).plot(kind='barh')
        plt.title('Top 15 des Features (Coefficients négatifs - Facteurs de Fidélité)')
        plt.savefig(f"{OUTPUT_DIR}/feature_importance_loyalty.png")

    print(f"Évaluation terminée. Rapports visuels sauvegardés dans {OUTPUT_DIR}")
    print("\nClassification Report :")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    evaluate()
