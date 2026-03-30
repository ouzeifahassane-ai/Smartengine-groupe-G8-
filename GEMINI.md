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

## Rôles

### Sprint 1 (9-11 mars 2026)
- Scrum Master : Nejma
- Product Owner : Emmanuel

### Sprint 2 (30 mars 2026 - en cours)
- Scrum Master : Joël-Samuel (Etya'alé)
- Product Owner : Ouzeifa

## Sprint en cours
Sprint 2 - Nettoyage et construction de la table analytique

## Bilan Sprint 1
- Dépôt GitHub initialisé, GEMINI.md créé
- Exploration du dataset réalisée (5 CSV analysés)
- Veille outils complétée
- Brief client rédigé
- Dossier de conception section 1 produit
- Agent data-explorer.md créé dans .gemini/agents/

## Table analytique à produire
data/processed/analytics.csv (une ligne par account_id)