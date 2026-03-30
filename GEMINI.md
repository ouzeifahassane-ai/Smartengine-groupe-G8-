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
│       └── data-explorer.md        # agent enrichi Sprint 2
├── data/
│   ├── raw/                         # les 5 CSV (jamais modifiés)
│   └── processed/
│       └── analytics.csv            # table analytique finale
├── outputs/
│   └── rapport-nettoyage.md
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

## Équipe — Sprint 2

- Product Owner : emmanuel
- Scrum Master : etya-ale
- Développeurs IA : autres membres du groupe

## Bilan Sprint 1 (terminé)

- Dépôt GitHub créé et structuré
- Les 5 CSV explorés et documentés dans data/raw/
- Veille outils réalisée
- Brief client rédigé
- Agent d'exploration data-explorer.md créé dans .gemini/agents/
- Backlog initialisé
- Section 1 du dossier de conception rédigée
- Compte-rendu sprint review déposé dans docs/standups/

## Sprint en cours — Sprint 2 (30 mars 2026)

Objectif : transformer les données brutes en table analytique prête pour la modélisation.

Étapes :
1. Nettoyage des 5 CSV (valeurs manquantes, types, doublons, outliers, cohérences)
2. Construction de la table analytique data/processed/analytics.csv (1 ligne par account_id)
3. Feature engineering : variables dérivées capturant les signaux de churn
4. Enrichissement de l'agent data-explorer.md avec les instructions de traitement
5. Rapport de nettoyage dans outputs/rapport-nettoyage.md
6. Section 2 du dossier de conception

## Agent IA — data-explorer.md (enrichi Sprint 2)

L'agent data-explorer.md a été enrichi pour couvrir le nettoyage et la transformation.
Choix justifié dans le dossier de conception : un seul agent couvre tout le périmètre données
pour éviter la duplication de contexte entre exploration et traitement.
