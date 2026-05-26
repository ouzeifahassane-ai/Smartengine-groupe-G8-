# smartEngine – GEMINI.md
## Contexte projet
Projet de prédiction de churn pour RavenStack, un SaaS B2B fictif.
Groupe G8 – MSc2 Data Marketing – INSEEC Lyon.

## Sprint en cours
**Sprint 4** – Déploiement : segmentation, dashboard Streamlit, recommandations

## Rôles Sprint 4
- **Scrum Master** : Ouzeifa
- **Product Owner** : Emmanuel
- **Développeurs IA** : Joel, Boulama

## Résumé Sprint 1 (Done)q
- Dépôt GitHub initialisé avec structure de base
- Agent data-explorer.md configuré
- Exploration des 5 CSV réalisée
- Brief client et veille outils complétés
- Section 1 du dossier de conception rédigée

## Résumé Sprint 2 (Done)
- Table analytique construite : data/processed/analytics.csv
- Scripts : clean_data.py, build_features.py, build_analytics.py
- Rapport de nettoyage : outputs/rapport-nettoyage.md
- Section 2 du dossier de conception rédigée

## Résumé Sprint 3 (Done)
- 3 algorithmes entraînés : Logistic Regression, Random Forest, XGBoost
- Modèle retenu sauvegardé : outputs/models/churn_model.joblib
- Scores générés : outputs/scores.csv (account_id, churn_score, risk_level)
- Rapport de performance : outputs/rapport-modele.md
- Section 3 du dossier de conception rédigée

## Objectif Sprint 4
- Segmentation risque/valeur → outputs/priorisation.csv
- Dashboard Streamlit → src/dashboard.py
- Recommandations et ROI → outputs/recommandations.md
- Section 4 dossier de conception
- Support de soutenance → docs/soutenance.pptx

## Fichiers importants
- Modèle : outputs/models/churn_model.joblib
- Scores : outputs/scores.csv
- Priorisation : outputs/priorisation.csv (à produire)
- Dashboard : src/dashboard.py (à produire)

## Structure du dépôt
smartengine-groupe-G8-/
├── .gemini/agents/
│   ├── data-explorer.md        # Sprint 1
│   ├── data-engineer.md        # Sprint 2
│   ├── model-trainer.md        # Sprint 3
│   └── agent-deploiement.md    # Sprint 4 (NOUVEAU)
├── data/
│   ├── raw/                    # CSV bruts (ne jamais modifier)
│   └── processed/
│       └── analytics.csv
├── src/
│   ├── clean_data.py
│   ├── build_features.py
│   ├── build_analytics.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── generate_scores.py
│   └── dashboard.py            # NOUVEAU Sprint 4
├── outputs/
│   ├── rapport-nettoyage.md
│   ├── rapport-modele.md
│   ├── scores.csv
│   ├── priorisation.csv        # NOUVEAU Sprint 4
│   ├── recommandations.md      # NOUVEAU Sprint 4
│   └── models/
│       └── churn_model.joblib
├── docs/
│   ├── standups/
│   ├── dossier-conception.docx
│   └── soutenance.pptx         # NOUVEAU Sprint 4
├── requirements.txt            # NOUVEAU Sprint 4
└── README.md

## Conventions
- Langue : français pour les rapports, anglais pour le code
- Noms de fichiers : snake_case
- Commits : "[prénom] action courte"
- La variable cible s'appelle : churn (0 = actif, 1 = churné)
- Ne jamais modifier les fichiers dans data/raw/

## Contraintes RGPD
- Article 22 : le score de churn influence des décisions commerciales
- Droit à l'explication : SHAP obligatoire dans le dashboard
- L'humain reste dans la boucle : le score ne déclenche jamais une action seul
- Minimisation des données : chaque variable est justifiée