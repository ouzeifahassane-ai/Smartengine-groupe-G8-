# Projet smartEngine — Groupe G8

## Contexte métier

Nous construisons smartEngine, un système de prédiction de churn pour RavenStack, un éditeur SaaS B2B qui commercialise une plateforme de gestion de projets à destination des équipes tech. RavenStack perd des clients chaque mois et veut anticiper ces résiliations pour que son équipe Customer Success puisse intervenir avant le départ.

## Objectif du projet

Concevoir un système complet de prédiction de churn :
- Nettoyage des données et construction d'une table analytique
- Identification des signaux précurseurs de résiliation
- Modèle de scoring prédictif (Sprint 3)
- Dashboard Streamlit pour les équipes Customer Success
- Alertes automatisées via n8n

## Dataset

5 fichiers CSV dans data/raw/ — ne jamais modifier ces fichiers :

- accounts.csv (~500 lignes) : clients avec leur plan, secteur et churn_flag
- subscriptions.csv (~5000 lignes) : abonnements avec MRR, dates, upgrades/downgrades
- feature_usage.csv (~25000 lignes) : utilisation des fonctionnalités par mois
- support_tickets.csv (~2000 lignes) : tickets de support avec priorité et satisfaction
- churn_events.csv (~600 lignes) : événements de résiliation avec raison et date

## Conventions

- Langue : tous les rapports et outputs sont en français
- Ne jamais modifier les fichiers dans data/raw/
- Scripts Python → src/
- Rapports et fichiers produits → outputs/
- Données transformées → data/processed/
- Table analytique finale → data/processed/analytics.csv
- Agents IA → .gemini/agents/
- Nommage des fichiers : kebab-case
- Comptes-rendus de standup → docs/standups/AAAA-MM-JJ.md

## Structure du dépôt

smartengine-groupe-G8/
├── .gitignore
├── GEMINI.md
├── README.md
├── .gemini/
│   └── agents/
│       ├── data-explorer.md        # agent enrichi Sprint 2
│       └── model-trainer.md        # agent initialisé Sprint 3
├── data/
│   ├── raw/                         # les 5 CSV (jamais modifiés)
│   └── processed/
│       └── analytics.csv            # table analytique finale
├── outputs/
│   ├── rapport-nettoyage.md
│   ├── rapport-modele.md
│   └── models/
├── src/
│   ├── clean_data.py
│   ├── build_features.py
│   └── build_analytics.py
└── docs/
    ├── standups/
    └── dossier-conception.docx

## Contraintes RGPD

- Article 22 applicable : le score de churn influence des décisions commerciales
- Minimisation des données : justifier chaque variable utilisée dans le modèle
- Transparence algorithmique obligatoire
- Documenter toutes les décisions de traitement (rapport de nettoyage)

## Équipe — Sprint 3 (En cours)

- Product Owner : Ouzeifa
- Scrum Master : Joël-Samuel
- Model Trainer : Boulama (@model-trainer)
- Développeurs IA : autres membres du groupe

## Bilan des Sprints

### Sprint 1 (Terminé)
- Dépôt GitHub créé et structuré.
- Exploration du dataset réalisée.
- Veille outils et brief client rédigés.

### Sprint 2 (Terminé)
- Nettoyage des 5 CSV et construction de la table analytique (data/processed/analytics.csv).
- Feature engineering initial réalisé.
- Rapport de nettoyage produit.

## Sprint en cours — Sprint 3 (27 avril 2026)
**Objectif** : Modélisation et scoring prédictif.
**Statut** : En cours. Baseline Random Forest établie (AUC-ROC: 0.64 après tuning).
