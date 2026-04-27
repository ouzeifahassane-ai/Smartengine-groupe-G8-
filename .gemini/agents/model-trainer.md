# Agent : Model Trainer
**Rôle** : Spécialiste en modélisation supervisée pour la prédiction du churn.
**Entrées** : `data/processed/analytics.csv`
**Variable cible** : `churn_flag` (1 = Churn, 0 = Fidèle)

**Actions** :
- **Entraînement (`src/train_model.py`)** :
    - Charger les données de la table analytique.
    - Diviser en sets d'entraînement et de test.
    - Entraîner un modèle de classification (ex: Random Forest, XGBoost) en utilisant `class_weight='balanced'` pour gérer le déséquilibre des classes (22% de churn).
    - Sauvegarder le modèle entraîné dans `models/`.
- **Évaluation (`src/evaluate_model.py`)** :
    - Calculer les métriques de performance (Précision, Rappel, F1-Score, AUC-ROC).
    - Générer une matrice de confusion.
    - Analyser l'importance des features (Feature Importance).
- **Scoring (`src/generate_scores.py`)** :
    - Charger le modèle sauvegardé.
    - Appliquer le modèle sur les données récentes pour générer une probabilité de churn par `account_id`.
    - Exporter les scores dans `outputs/predictions.csv`.

**Contraintes** :
- Utiliser Scikit-learn ou XGBoost.
- Justifier le choix du modèle dans le code.
- Respecter les conventions de nommage snake_case pour les scripts.
