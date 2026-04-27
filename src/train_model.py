import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_score, recall_score, f1_score

# Configuration
INPUT_PATH = "data/processed/analytics.csv"
MODEL_OUTPUT_PATH = "outputs/models/churn_model.joblib"
REPORT_PATH = "outputs/rapport-modele.md"

def train_and_evaluate():
    # 1. Chargement des données
    df = pd.read_csv(INPUT_PATH)
    
    # 2. Préparation des variables
    # On exclut les identifiants et les colonnes temporelles pour le modèle
    drop_cols = ['account_id', 'account_name', 'signup_date', 'churn_flag']
    X = df.drop(columns=drop_cols)
    y = df['churn_flag'].astype(int)
    
    # Identification des types de colonnes
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # 3. Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    # 4. Prétraitement
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # 5. Définition des modèles
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42)
    }
    
    results = {}
    best_auc = 0
    best_model_name = ""
    best_pipe = None
    
    # 6. Entraînement et évaluation
    for name, model in models.items():
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        pipe.fit(X_train, y_train)
        
        y_pred = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1]
        
        results[name] = {
            "AUC-ROC": roc_auc_score(y_test, y_proba),
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1-Score": f1_score(y_test, y_pred)
        }
        
        if results[name]["AUC-ROC"] > best_auc:
            best_auc = results[name]["AUC-ROC"]
            best_model_name = name
            best_pipe = pipe
            
    # 7. Sauvegarde du meilleur modèle
    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    joblib.dump(best_pipe, MODEL_OUTPUT_PATH)
    
    # 8. Génération du rapport
    generate_report(results, best_model_name, y_test)
    print(f"Meilleur modèle : {best_model_name} avec AUC-ROC = {best_auc:.4f}")

def generate_report(results, best_model_name, y_test):
    with open(REPORT_PATH, "w") as f:
        f.write("# Rapport de Performance du Modèle de Churn\n\n")
        f.write("## Distribution de la variable cible (Test Set)\n")
        f.write(f"- Non-churn : {sum(y_test == 0)}\n")
        f.write(f"- Churn : {sum(y_test == 1)}\n\n")
        
        f.write("## Comparaison des Modèles\n")
        f.write("| Modèle | AUC-ROC | Precision | Recall | F1-Score |\n")
        f.write("|--------|---------|-----------|--------|----------|\n")
        for name, metrics in results.items():
            f.write(f"| {name} | {metrics['AUC-ROC']:.4f} | {metrics['Precision']:.4f} | {metrics['Recall']:.4f} | {metrics['F1-Score']:.4f} |\n")
        
        f.write(f"\n**Modèle retenu : {best_model_name}**\n")
        f.write("\n## Stratégie\n")
        f.write("- Split : 80% Entraînement / 20% Test\n")
        f.write("- Gestion du déséquilibre : `class_weight='balanced'`\n")
        f.write("- Prétraitement : StandardScaler pour le numérique, OneHotEncoder pour le catégoriel.\n")

if __name__ == "__main__":
    train_and_evaluate()
