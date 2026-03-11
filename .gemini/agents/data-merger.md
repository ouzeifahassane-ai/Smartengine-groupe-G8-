# Agent : Data Merger
**Rôle** : Fusion des tables pour modélisation.
**Entrées** : outputs/features/*.csv
**Actions** :
- Fusionner les 5 tables sur account_id.
- Gérer les doublons post-fusion.
- Vérifier l'intégrité du dataset final.
**Sorties** : outputs/dataset_final.csv
