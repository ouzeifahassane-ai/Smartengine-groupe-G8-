# Agent : Model Trainer
**Rôle** : Entraînement, évaluation et optimisation des modèles de prédiction de churn.
**Entrées** : data/processed/analytics.csv
**Actions** :
- Entraîner des modèles de classification (Random Forest, XGBoost, etc.).
- Optimiser les hyperparamètres via GridSearchCV ou RandomSearch.
- Évaluer les performances (AUC-ROC, Précision, Rappel).
- Générer des rapports d'importance des variables.
**Sorties** : Modèles sauvegardés dans outputs/model/ et rapports de performance.
