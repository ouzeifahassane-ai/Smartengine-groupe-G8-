import pandas as pd
import joblib
import os

def generate_scores():
    model_path = 'outputs/models/churn_model.joblib'
    data_path = 'outputs/dataset_final_v2.csv'
    output_path = 'outputs/scores.csv'

    if not os.path.exists(model_path):
        print(f"Erreur : Le modèle {model_path} est introuvable.")
        return

    if not os.path.exists(data_path):
        print(f"Erreur : Le dataset {data_path} est introuvable.")
        return

    print("Chargement du modèle et des données...")
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)

    # Détection des features attendues
    if hasattr(model, 'feature_names_in_'):
        features = list(model.feature_names_in_)
        print(f"Features attendues : {features}")
    else:
        # Fallback sur les colonnes communes si non spécifié
        features = ['industry', 'country', 'referral_source', 'plan_tier', 'seats', 'is_trial']
        print(f"Avertissement : feature_names_in_ non trouvé, utilisation par défaut : {features}")

    # Vérification de la présence des colonnes
    missing_cols = [c for c in features if c not in df.columns]
    if missing_cols:
        print(f"Erreur : Colonnes manquantes dans le CSV : {missing_cols}")
        return

    X = df[features].copy()

    # Prétraitement minimal : conversion is_trial en bool si nécessaire
    if 'is_trial' in X.columns and X['is_trial'].dtype == 'object':
        X['is_trial'] = X['is_trial'].astype(str).map({'True': True, 'False': False, 'true': True, 'false': False})

    print("Calcul des scores de churn...")
    try:
        # On récupère la probabilité de la classe 1 (churn)
        # predict_proba renvoie [P(class 0), P(class 1)]
        churn_scores = model.predict_proba(X)[:, 1]
    except Exception as e:
        print(f"Échec de la prédiction directe : {e}")
        print("Tentative avec encodage catégoriel (factorize)...")
        # Si la prédiction échoue, c'est probablement car le modèle attend des nombres
        for col in X.select_dtypes(include=['object']).columns:
            X[col] = pd.factorize(X[col])[0]
        
        try:
            churn_scores = model.predict_proba(X)[:, 1]
        except Exception as e2:
            print(f"Erreur critique lors de la prédiction : {e2}")
            return

    # Création du DataFrame de résultats
    results = pd.DataFrame({
        'account_id': df['account_id'],
        'churn_score': churn_scores
    })

    # Ajout du niveau de risque
    def get_risk_level(score):
        if score < 0.3:
            return 'low'
        elif score <= 0.7:
            return 'medium'
        else:
            return 'high'

    results['risk_level'] = results['churn_score'].apply(get_risk_level)

    # Sauvegarde
    results.to_csv(output_path, index=False)
    print(f"Fichier de scores généré avec succès : {output_path}")
    print(results.head())

if __name__ == "__main__":
    generate_scores()
