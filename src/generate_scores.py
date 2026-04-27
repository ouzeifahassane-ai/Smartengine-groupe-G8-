import pandas as pd
import joblib
import os
import numpy as np

# Configuration
INPUT_PATH = "data/processed/analytics.csv"
MODEL_PATH = "outputs/models/churn_model.joblib"
OUTPUT_PATH = "outputs/scores.csv"

def generate_risk_scores():
    # 1. Chargement
    if not os.path.exists(MODEL_PATH):
        print(f"Erreur : Modèle introuvable à {MODEL_PATH}")
        return

    df = pd.read_csv(INPUT_PATH)
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparation des variables (exclusion des métadonnées)
    drop_cols = ['account_id', 'account_name', 'signup_date', 'churn_flag']
    X = df.drop(columns=drop_cols)
    
    # 3. Calcul des scores (probabilités de la classe 1)
    # predict_proba renvoie [prob_0, prob_1]
    churn_scores = model.predict_proba(X)[:, 1]
    
    # 4. Définition des niveaux de risque
    def get_risk_level(score):
        if score > 0.7:
            return 'high'
        elif score > 0.4:
            return 'medium'
        else:
            return 'low'
    
    # 5. Création du DataFrame final
    output_df = pd.DataFrame({
        'account_id': df['account_id'],
        'churn_score': churn_scores
    })
    
    output_df['risk_level'] = output_df['churn_score'].apply(get_risk_level)
    
    # Trier par score décroissant pour mettre en avant les risques
    output_df = output_df.sort_values(by='churn_score', ascending=False)
    
    # 6. Sauvegarde
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    output_df.to_csv(OUTPUT_PATH, index=False)
    
    print(f"Fichier de scores généré : {OUTPUT_PATH}")
    print(f"\nRépartition des niveaux de risque :\n{output_df['risk_level'].value_counts()}")
    print(f"\nAperçu du top 5 :\n{output_df.head()}")

if __name__ == "__main__":
    generate_risk_scores()
