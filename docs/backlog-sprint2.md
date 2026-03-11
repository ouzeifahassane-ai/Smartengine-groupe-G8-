# Backlog Sprint 2 — smartEngine Groupe G8
**Sprint 2 — Traitement des données**
**Date : 30 mars 2026**
**Durée : 6h**
**Rôles suggérés :**
- Product Owner : ETYA-ALE (Joël-Samuel)
- Scrum Master : à désigner
- Développeurs IA : 2 autres membres

---

## Objectif du Sprint 2

Produire un dataset propre et enrichi, prêt à être utilisé pour l'entraînement du modèle de prédiction de churn au Sprint 3.

---

## User Stories

### 🎯 EPIC 1 — Nettoyage des données

---

**US-201**
> En tant que **Développeur IA**, je veux nettoyer le fichier `accounts.csv` afin d'éliminer les doublons, corriger les types de colonnes et gérer les valeurs manquantes.

**Critères d'acceptation :**
- Aucun doublon sur `account_id`
- Colonnes dates converties en datetime
- Valeurs manquantes documentées et traitées
- Fichier nettoyé sauvegardé dans `outputs/`

**Responsable :** Dev IA 1
**Estimation :** 30 min

---

**US-202**
> En tant que **Développeur IA**, je veux nettoyer le fichier `subscriptions.csv` afin de corriger les incohérences de dates et valider les montants MRR.

**Critères d'acceptation :**
- `start_date` < `end_date` pour tous les enregistrements
- `mrr_amount` > 0 pour tous les abonnements actifs
- `churn_flag` est binaire (0/1)

**Responsable :** Dev IA 1
**Estimation :** 30 min

---

**US-203**
> En tant que **Développeur IA**, je veux nettoyer les fichiers `feature_usage.csv`, `support_tickets.csv` et `churn_events.csv` afin de garantir la cohérence des données avec les autres tables.

**Critères d'acceptation :**
- Toutes les `account_id` référencées existent dans `accounts.csv`
- `usage_count` et `error_count` ≥ 0
- Dates cohérentes avec les périodes d'abonnement

**Responsable :** Dev IA 2
**Estimation :** 45 min

---

### 🔧 EPIC 2 — Feature Engineering

---

**US-204**
> En tant que **Product Owner**, je veux définir les 10 variables prioritaires pour le modèle afin de guider le travail de feature engineering des Dev IA.

**Critères d'acceptation :**
- Liste documentée dans `docs/dossier-conception.docx` section 2
- Chaque variable est justifiée par une logique métier
- Validation par l'équipe avant implémentation

**Responsable :** ETYA-ALE (PO)
**Estimation :** 30 min

**Variables prioritaires suggérées :**
1. `tenure_days` — ancienneté du compte
2. `usage_trend_30j` — évolution usage sur 30 jours
3. `error_rate` — taux d'erreurs / total usage
4. `nb_tickets_urgents` — nombre de tickets high/urgent
5. `avg_resolution_time` — délai moyen résolution tickets
6. `satisfaction_score_moyen` — score satisfaction moyen
7. `downgrade_flag` — a-t-il rétrogradé son plan ?
8. `auto_renew_flag` — renouvellement automatique activé ?
9. `is_trial` — compte en période d'essai ?
10. `industry_risk_score` — secteur à risque (DevTools = élevé)

---

**US-205**
> En tant que **Développeur IA**, je veux créer la variable `tenure_days` afin de mesurer l'ancienneté de chaque compte client.

**Critères d'acceptation :**
- `tenure_days` = date_fin - date_début d'abonnement
- Valeur positive pour tous les comptes
- Ajoutée dans le dataset final

**Responsable :** Dev IA 1
**Estimation :** 20 min

---

**US-206**
> En tant que **Développeur IA**, je veux créer les variables d'usage (`usage_trend`, `error_rate`) afin de capturer les signaux comportementaux précurseurs du churn.

**Critères d'acceptation :**
- `usage_trend_30j` calculé par agrégation sur les 30 derniers jours
- `error_rate` = error_count / usage_count (gérer division par zéro)
- Variables ajoutées dans le dataset final

**Responsable :** Dev IA 1
**Estimation :** 30 min

---

**US-207**
> En tant que **Développeur IA**, je veux créer les variables support (`nb_tickets_urgents`, `avg_resolution_time`) afin de mesurer la frustration client.

**Critères d'acceptation :**
- Agrégation par `account_id`
- Distinction entre priorités low/medium/high/urgent
- Variables ajoutées dans le dataset final

**Responsable :** Dev IA 2
**Estimation :** 30 min

---

### 📊 EPIC 3 — Dataset final et documentation

---

**US-208**
> En tant que **Développeur IA**, je veux fusionner les 5 tables nettoyées en un seul dataset enrichi afin de produire le fichier d'entraînement du modèle.

**Critères d'acceptation :**
- Jointures sur `account_id` et `subscription_id`
- Aucune perte de données non justifiée
- Dataset final sauvegardé dans `outputs/dataset_final.csv`
- Rapport de qualité généré dans `outputs/`

**Responsable :** Dev IA 2
**Estimation :** 45 min

---

**US-209**
> En tant que **Product Owner**, je veux rédiger la section 2 du dossier de conception afin de documenter toutes les décisions de traitement des données.

**Critères d'acceptation :**
- Justification de chaque variable créée
- Description des traitements appliqués (nettoyage, imputation)
- Mention des biais potentiels identifiés
- Ajouté dans `docs/dossier-conception.docx`

**Responsable :** ETYA-ALE (PO)
**Estimation :** 45 min

---

**US-210**
> En tant que **Scrum Master**, je veux animer le daily standup et créer le compte-rendu afin de documenter l'avancement du Sprint 2.

**Critères d'acceptation :**
- Standup de 10 min max en début de séance
- Compte-rendu déposé dans `docs/standups/2026-03-30.md`

**Responsable :** Scrum Master
**Estimation :** 15 min

---

## Agents à créer pour ce Sprint

Déposer dans `.gemini/agents/` :

| Agent | Fichier | Mission |
|---|---|---|
| Nettoyeur de données | `data-cleaner.md` | Nettoyer les 5 CSV |
| Feature engineer | `feature-engineer.md` | Créer les 10 variables |
| Fusionneur | `data-merger.md` | Fusionner en dataset final |

---

## Livrables attendus en fin de Sprint 2

| Livrable | Fichier | Responsable |
|---|---|---|
| CSV nettoyés | `outputs/cleaned_*.csv` | Dev IA 1 & 2 |
| Dataset final enrichi | `outputs/dataset_final.csv` | Dev IA 2 |
| Rapport qualité données | `outputs/rapport-qualite.md` | Dev IA 1 |
| Agents Sprint 2 | `.gemini/agents/*.md` | Dev IA 1 & 2 |
| Section 2 dossier conception | `docs/dossier-conception.docx` | PO (ETYA-ALE) |
| Standup 30/03 | `docs/standups/2026-03-30.md` | Scrum Master |

---

## Définition of Done (Sprint 2)

- [ ] Dataset final produit et sauvegardé dans `outputs/`
- [ ] 10 variables créées et documentées
- [ ] Section 2 du dossier de conception rédigée
- [ ] Agents commités dans `.gemini/agents/`
- [ ] Toutes les branches mergées dans `main` par le Scrum Master
- [ ] Sprint Review présentée à l'enseignante
