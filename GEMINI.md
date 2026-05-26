# Projet smartEngine — Groupe G8

## Contexte métier

Nous construisons smartEngine, un système de prédiction de churn pour RavenStack, un éditeur SaaS B2B qui commercialise une plateforme de gestion de projets à destination des équipes tech. RavenStack perd des clients chaque mois et veut anticiper ces résiliations pour que son équipe Customer Success puisse intervenir avant le départ.

## Objectif du projet

Concevoir un système complet de prédiction de churn :
- Sprint 1 : Exploration des données et structuration du projet
- Sprint 2 : Nettoyage des données et construction de la table analytique
- Sprint 3 : Modèle de scoring prédictif (classification churn)
- Sprint 4 : Segmentation risque/valeur, dashboard Streamlit, recommandations stratégiques

## Dataset

5 fichiers CSV dans data/raw/ — **ne jamais modifier ces fichiers** :

- `accounts.csv` (~500 lignes) : clients avec leur plan, secteur et churn_flag
- `subscriptions.csv` (~5000 lignes) : abonnements avec MRR, dates, upgrades/downgrades
- `feature_usage.csv` (~25000 lignes) : utilisation des fonctionnalités par mois
- `support_tickets.csv` (~2000 lignes) : tickets de support avec priorité et satisfaction
- `churn_events.csv` (~600 lignes) : événements de résiliation avec raison et date

## Conventions

- Langue : tous les rapports et outputs sont en français
- Ne jamais modifier les fichiers dans `data/raw/`
- Scripts Python → `src/`
- Rapports et fichiers produits → `outputs/`
- Données transformées → `data/processed/`
- Table analytique finale → `data/processed/analytics.csv`
- Agents IA → `.gemini/agents/`
- Nommage des fichiers : kebab-case
- Comptes-rendus de standup → `docs/standups/AAAA-MM-JJ.md`

## Structure du dépôt (état final — Sprint 4)

```
smartengine-groupe-G8/
├── .gitignore
├── GEMINI.md                          # ce fichier
├── README.md
├── requirements.txt                   # dépendances Python (Sprint 4)
├── .gemini/
│   └── agents/
│       ├── data-cleaner.md            # Sprint 1/2
│       ├── data-engineer.md           # Sprint 2
│       ├── data-merger.md             # Sprint 2
│       ├── feature-engineer.md        # Sprint 2
│       ├── model-trainer.md           # Sprint 3
│       └── deployment-agent.md        # Sprint 4 (NOUVEAU)
├── data/
│   ├── raw/                           # les 5 CSV (jamais modifiés)
│   └── processed/
│       └── analytics.csv              # table analytique (Sprint 2)
├── outputs/
│   ├── rapport-nettoyage.md           # Sprint 2
│   ├── rapport-modele.md              # Sprint 3
│   ├── scores.csv                     # Sprint 3 (score par compte)
│   ├── priorisation.csv               # Sprint 4 (NOUVEAU)
│   ├── recommandations.md             # Sprint 4 (NOUVEAU)
│   └── models/
│       └── churn_model.joblib         # modèle sauvegardé (Sprint 3)
├── src/
│   ├── clean_data.py                  # Sprint 2
│   ├── build_features.py              # Sprint 2
│   ├── build_analytics.py             # Sprint 2
│   ├── feature_engineering.py         # Sprint 2
│   ├── train_model.py                 # Sprint 3
│   ├── evaluate_model.py              # Sprint 3
│   ├── generate_scores.py             # Sprint 3
│   ├── priorisation.py                # Sprint 4 (NOUVEAU)
│   └── dashboard.py                   # Sprint 4 (NOUVEAU)
└── docs/
    ├── standups/
    └── dossier-conception.docx        # sections 1 à 4
```

## Fichiers clés

| Fichier | Rôle |
|---|---|
| `data/processed/analytics.csv` | Table analytique — 500 comptes, 19 features |
| `outputs/scores.csv` | Score de churn et niveau de risque par compte |
| `outputs/priorisation.csv` | Segmentation risque/valeur avec action recommandée |
| `outputs/models/churn_model.joblib` | Modèle retenu du Sprint 3 |
| `src/dashboard.py` | Dashboard Streamlit — lancer avec `streamlit run src/dashboard.py` |

## Contraintes RGPD

- Article 22 applicable : le score de churn influence des décisions commerciales
- Le score ne déclenche **jamais** une action automatique sans intervention humaine
- Minimisation des données : chaque feature utilisée est justifiée dans `rapport-modele.md`
- Transparence algorithmique : explications SHAP disponibles dans la fiche compte du dashboard
- Droit à l'explication respecté par la vue "Fiche compte" du dashboard

## Agents IA — Bilan des 4 sprints

| Agent | Sprint | Rôle |
|---|---|---|
| `data-cleaner.md` | 1/2 | Nettoyage des 5 CSV bruts |
| `data-engineer.md` | 2 | Construction de la table analytique |
| `data-merger.md` | 2 | Fusion des sources de données |
| `feature-engineer.md` | 2 | Feature engineering et variables dérivées |
| `model-trainer.md` | 3 | Entraînement, évaluation et scoring du modèle |
| `deployment-agent.md` | 4 | Segmentation, dashboard Streamlit, recommandations |

Choix Sprint 4 : création d'un nouvel agent `deployment-agent.md` plutôt qu'enrichissement
de `model-trainer.md`, car le périmètre déploiement (Streamlit, segmentation) est distinct
du périmètre modélisation.

## Bilan Sprint 1 (terminé)

- Dépôt GitHub créé et structuré
- Les 5 CSV explorés et documentés
- Veille outils réalisée, brief client rédigé
- Agent `data-explorer.md` créé dans `.gemini/agents/`
- Backlog initialisé, section 1 du dossier de conception rédigée

## Bilan Sprint 2 (terminé)

- Nettoyage complet des 5 CSV (`src/clean_data.py`)
- Feature engineering (`src/build_features.py`, `src/feature_engineering.py`)
- Table analytique `data/processed/analytics.csv` construite (`src/build_analytics.py`)
- `outputs/rapport-nettoyage.md` produit
- Section 2 du dossier de conception rédigée

## Bilan Sprint 3 (terminé)

- 3 modèles entraînés : Logistic Regression, Random Forest, XGBoost
- Modèle retenu : celui maximisant le recall sur la classe churn
- `outputs/models/churn_model.joblib` sauvegardé
- `outputs/scores.csv` généré (500 comptes scorés)
- `outputs/rapport-modele.md` produit avec analyse SHAP
- Section 3 du dossier de conception rédigée

## Sprint 4 (en cours — mai 2026)

### Responsable : Boulama

Objectif : rendre le score de churn actionnable pour les équipes RavenStack.

Livrables :
- [x] `src/priorisation.py` — segmentation risque/valeur
- [x] `outputs/priorisation.csv` — 500 comptes segmentés en 4 quadrants
- [x] `src/dashboard.py` — dashboard Streamlit 3 vues
- [x] `requirements.txt` — dépendances Python
- [x] `outputs/recommandations.md` — recommandations et ROI estimé
- [x] `.gemini/agents/deployment-agent.md` — agent de déploiement
- [ ] Section 4 du dossier de conception (toute l'équipe)
- [ ] GEMINI.md final mis à jour (Scrum Master)
- [ ] Backlog Sprint 4 à jour

### Résultats de la segmentation

| Quadrant | Comptes | MRR | Action |
|---|---|---|---|
| Q1 — Risque élevé / Valeur élevée | 93 (18,6 %) | 308 011 €/mois | Appel CSM sous 48h |
| Q2 — Risque élevé / Valeur faible | 115 (23 %) | 146 488 €/mois | Email automatisé |
| Q3 — Risque faible / Valeur élevée | 157 (31,4 %) | 516 316 €/mois | Surveiller/fidéliser |
| Q4 — Risque faible / Valeur faible | 135 (27 %) | 161 273 €/mois | Aucune action |

**MRR total à risque (Q1+Q2) : 454 499 €/mois (40,1 % du portefeuille)**

## Comment exécuter le projet

```bash
# Installation des dépendances
pip install -r requirements.txt

# Sprint 2 : table analytique
python src/build_analytics.py

# Sprint 3 : modèle et scores
python src/train_model.py
python src/evaluate_model.py
python src/generate_scores.py

# Sprint 4 : priorisation et dashboard
python src/priorisation.py
streamlit run src/dashboard.py
```
