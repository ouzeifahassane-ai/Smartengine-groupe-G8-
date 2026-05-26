---
name: data-merger
description: Agent de construction de la table analytique unifiée à partir des données nettoyées. Utilise cet agent pour fusionner les 5 tables sur account_id et produire analytics.csv.
version: "1.0"
author: Boulama (Développeur IA — G8)
scope: data-integration
inputs:
  - data/processed/accounts.csv
  - data/processed/subscriptions.csv
  - data/processed/feature_usage.csv
  - data/processed/support_tickets.csv
  - data/processed/churn_events.csv
outputs:
  - data/processed/analytics.csv
script: src/build_analytics.py
---

# Agent : Data Merger

**Rôle** : Fusionner les 5 tables nettoyées (produites par `clean_data.py`) en une table analytique unique par `account_id`. Cette table est le point d'entrée de toute la chaîne ML. Elle contient exactement une ligne par compte et la variable cible `churned`.

---

## Étape 1 — Chargement

- Lire les 5 fichiers depuis `data/processed/` (sortie de `clean_data.py`).
- Vérifier la présence de chaque fichier avant de continuer.
- Construire l'index de jointure `subscription_id → account_id` (pour brancher feature_usage).

---

## Étape 2 — Agrégation par account_id

| Source | Métriques calculées | Clé de jointure |
|--------|--------------------|-|
| subscriptions | `mrr_current`, `nb_upgrades`, `nb_downgrades`, `nb_plan_changes`, `subscription_age_days`, `auto_renew_flag` | `account_id` direct |
| feature_usage | `total_usage_count`, `avg_usage_count`, `nb_features_used`, `error_rate`, `days_since_last_usage` | via `subscription_id → account_id` |
| support_tickets | `nb_tickets_total`, `nb_tickets_urgent`, `escalation_rate`, `avg_resolution_hours`, `avg_satisfaction` | `account_id` direct |
| churn_events | `churned` (1 si présent, sinon 0) | `account_id` direct |

---

## Étape 3 — Construction de la table finale

- Partir de `accounts.csv` comme table de référence (500 comptes).
- Calculer `account_age_days` = (date_ref - signup_date).
- Fusionner les agrégations en left join (tous les comptes conservés même sans tickets/usage).
- Variable cible : `churned = 1` si account_id dans churn_events, sinon `0`.
- Imputer les valeurs manquantes résiduelles par la médiane.
- Garantir **une seule ligne par compte**.

---

## Étape 4 — Export

- Sauvegarder dans `data/processed/analytics.csv`.
- Afficher : nombre de lignes, colonnes, taux de churn.

---

## Règles absolues

- **`churned` doit être 1 ou 0** (entier) — jamais True/False ou une chaîne.
- **`is_active`** n'existe pas dans le CSV — la dériver : `subs["is_active"] = subs["end_date"].isnull()`.
- **Une seule ligne par `account_id`** — 500 lignes attendues.
- Comptes sans tickets : `nb_tickets_total = 0`, `escalation_rate = 0`.
- Ne jamais modifier les fichiers sources dans `data/processed/`.
