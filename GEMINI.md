# Projet smartEngine - Groupe G8

## Contexte
Nous construisons smartEngine, un système de prédiction de churn pour RavenStack, un SaaS B2B qui commercialise une plateforme de gestion de projets à destination des équipes tech. Les données sont dans /data/raw/ et ne doivent jamais être modifiées.

## Objectif
Concevoir un système complet de prédiction de churn : nettoyage des données, identification des signaux précurseurs, modèle de scoring prédictif, dashboard Streamlit pour les équipes Customer Success, alertes automatisées via n8n.

## Dataset
5 fichiers CSV dans /data/raw/ :
- accounts.csv (~500 lignes)
- subscriptions.csv (~5000 lignes)
- feature_usage.csv (~25000 lignes)
- support_tickets.csv (~2000 lignes)
- churn_events.csv (~600 lignes)

## Conventions
- Scripts Python -> /src/
- Rapports générés -> /outputs/
- Ne jamais modifier /data/raw/
- Tous les rapports sont en français
- Nommage fichiers : kebab-case

## Contraintes RGPD
- Article 22 applicable : le score de churn influence des décisions commerciales
- Minimisation des données : justifier chaque variable utilisée
- Transparence algorithmique obligatoire

## Sprint en cours
Sprint 1 - Découverte et mise en place (9-11 mars 2026)
# smartEngine – GEMINI.md

## Contexte projet
Projet de prédiction de churn pour RavenStack, un SaaS B2B fictif.
Groupe G8 – MSc2 Data Marketing – INSEEC Lyon.

## Sprint en cours
**Sprint 2** – Nettoyage, construction de la table analytique, feature engineering

## Rôles Sprint 2
- **Scrum Master** : [Etya'ale]
- **Product Owner** : [Emmanuel]
- **Développeurs IA** : Ouzeifa, [Boulama]

## Résumé Sprint 1 (Done)
- Dépôt GitHub initialisé avec structure de base
- GEMINI.md créé, agent data-explorer.md configuré
- Exploration des 5 CSV réalisée
- Brief client rédigé (docs/)
- Veille outils complétée
- Backlog initialisé
- Section 1 du dossier de conception rédigée

## Dataset
Les 5 fichiers CSV sont dans data/raw/ et ne doivent jamais être modifiés :
- accounts.csv
- subscriptions.csv
- feature_usage.csv
- support_tickets.csv
- churn_events.csv

## Objectif Sprint 2
Produire data/processed/analytics.csv :
- Une ligne par account_id
- Données nettoyées (valeurs manquantes, doublons, types, outliers)
- Features dérivées (tendances, ratios, agrégations)
- Variable cible churn binaire (0/1) alignée temporellement

## Structure du dépôt
smartengine-groupe-G8-/
├── .gemini/agents/
│   ├── data-explorer.md       # Sprint 1
│   └── data-engineer.md       # Sprint 2 (NOUVEAU)
├── data/
│   ├── raw/                   # CSV bruts (ne jamais modifier)
│   └── processed/             # analytics.csv (à produire)
├── src/
│   ├── clean_data.py
│   ├── build_features.py
│   └── build_analytics.py
├── outputs/
│   └── rapport-nettoyage.md
└── docs/
    ├── standups/
    └── dossier-conception.docx

## Conventions
- Langue : français pour les rapports, anglais pour le code
- Noms de fichiers : snake_case
- Commits : "[prénom] action courte" (ex: "ouzeifa clean accounts csv")
- La variable cible s'appelle : churn (0 = actif, 1 = churné)
- Ne jamais modifier les fichiers dans data/raw/

## Prochaine étape
Créer l'agent data-engineer.md dans .gemini/agents/