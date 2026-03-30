# Projet smartEngine - Groupe G8

## Contexte métier
Nous construisons smartEngine, un système de prédiction de churn pour RavenStack, un éditeur SaaS B2B qui vend une plateforme de gestion de projets. RavenStack perd des clients chaque mois et veut anticiper ces résiliations pour que son équipe Customer Success puisse intervenir avant le départ.

## Données
- Les 5 fichiers CSV bruts sont dans data/raw/ - ne jamais les modifier
- accounts.csv : 500 clients avec leur plan, secteur et churn_flag
- subscriptions.csv : 5000 abonnements avec MRR et dates
- feature_usage.csv : 25000 lignes d'utilisation des fonctionnalités
- support_tickets.csv : 2000 tickets de support
- churn_events.csv : 600 événements de résiliation

## Conventions
- Langue : tous les rapports et outputs sont en français
- Ne jamais modifier les fichiers dans data/raw/
- Les scripts Python vont dans src/
- Les rapports et fichiers produits vont dans outputs/
- Les agents vont dans .gemini/agents/

## Équipe
- Product Owner : Emmanuel
- Scrum Master : ouzeifahassane
- Développeurs IA : autres membres du groupe

## Sprint en cours
Sprint 2 - Traitement des données
- Nettoyage des 5 fichiers CSV
- Feature engineering : créer un tableau master avec une ligne par client
- Objectif final : prédire le churn (variable cible : churn_flag)
