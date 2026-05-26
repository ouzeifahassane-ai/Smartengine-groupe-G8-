import pandas as pd
import os

def generate_prioritization():
    scores_path = 'outputs/scores.csv'
    features_path = 'outputs/features_master.csv'
    output_path = 'outputs/priorisation.csv'

    if not os.path.exists(scores_path) or not os.path.exists(features_path):
        print("Erreur : Fichiers sources introuvables.")
        return

    print("Chargement des données...")
    df_scores = pd.read_csv(scores_path)
    # On ne charge que account_id et mrr_amount de features_master
    df_features = pd.read_csv(features_path)[['account_id', 'mrr_amount']]

    # Fusion des données
    df = df_scores.merge(df_features, on='account_id', how='left')
    
    # Renommer mrr_amount en mrr pour correspondre à la demande
    df = df.rename(columns={'mrr_amount': 'mrr'})

    # Calcul de la médiane du MRR
    mrr_median = df['mrr'].median()
    print(f"Médiane du MRR : {mrr_median}")

    # Fonction pour définir le quadrant et l'action
    def classify(row):
        risk = row['risk_level']
        mrr = row['mrr']
        
        if risk == 'high':
            if mrr >= mrr_median:
                return "Priorité maximale", "Appel CSM immédiat"
            else:
                return "Action automatisée", "Email automatisé"
        else: # risk is low or medium
            if mrr >= mrr_median:
                return "Fidéliser", "Programme fidélité"
            else:
                return "Aucune action", "Monitoring passif"

    # Application de la classification
    print("Classification des clients...")
    classification = df.apply(classify, axis=1)
    df['quadrant'] = [x[0] for x in classification]
    df['action_recommandee'] = [x[1] for x in classification]

    # Sélection des colonnes finales
    final_cols = ['account_id', 'churn_score', 'risk_level', 'mrr', 'quadrant', 'action_recommandee']
    df_final = df[final_cols]

    # Sauvegarde
    df_final.to_csv(output_path, index=False)
    print(f"Fichier de priorisation généré : {output_path}")
    print(df_final.head())
    
    # Statistiques rapides
    print("\nRépartition par quadrant :")
    print(df_final['quadrant'].value_counts())

if __name__ == "__main__":
    generate_prioritization()
