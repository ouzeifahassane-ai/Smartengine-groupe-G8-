# Agent : Model Trainer
**Rôle** : Entraînement et évaluation du modèle prédictif.
**Entrées** : outputs/dataset_final.csv
**Actions** :
- Préparer les données (encodage, scaling si nécessaire).
- Entraîner un modèle Random Forest.
- Évaluer les performances (AUC-ROC, Matrice de confusion).
- Identifier l'importance des variables.
**Sorties** : 
- Modèle sauvegardé dans outputs/model/
- Rapport de performance dans outputs/reports/
