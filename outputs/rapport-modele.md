# Rapport de modélisation — smartEngine
Projet : Prédiction de churn B2B — RavenStack | Groupe G8
Statut : À générer en exécutant `python src/evaluate_model.py`

---

> **Note** : Ce rapport est généré automatiquement par `src/evaluate_model.py`.
> Pour obtenir les résultats réels avec les métriques et les graphiques, exécutez :
>
> ```bash
> python src/train_model.py      # Entraîne les modèles
> python src/evaluate_model.py   # Génère ce rapport
> python src/generate_scores.py  # Génère outputs/scores.csv
> ```

---

## 1. Contexte

Objectif : prédire le churn (résiliation) des comptes clients de RavenStack avec au moins 30 jours d'avance.

**Objectifs de performance :**
- AUC-ROC ≥ 0.80
- Recall ≥ 70% sur la classe churn

**Métrique prioritaire : Recall**
Justification métier : dans un contexte B2B SaaS, rater un churn coûte 5 à 7 fois plus cher en coût d'acquisition qu'une alerte inutile. L'équipe Customer Success préfère contacter un client sain plutôt que de laisser partir un churner sans intervention.

## 2. Données d'entrée

- Source : `data/processed/analytics.csv`
- 500 comptes clients RavenStack
- Split : 80% train (400 comptes) / 20% test (100 comptes), stratifié (random_state=42)
- Taux de churn global : ~22% (churn_flag dans accounts.csv)

## 3. Gestion du déséquilibre des classes

Stratégie retenue : `class_weight='balanced'` pour Logistic Regression et Random Forest.
Pour XGBoost : `scale_pos_weight = nb_négatifs / nb_positifs`.

Justification : approche simple sans sur-échantillonnage artificiel. SMOTE génère des données synthétiques qui peuvent fausser la distribution réelle sur un petit dataset de 500 comptes.

## 4. Algorithmes testés

| Algorithme | Avantages | Limites |
|---|---|---|
| Logistic Regression | Interprétable, rapide, bonne baseline | Performance limitée sur données non-linéaires |
| Random Forest | Robuste, gère les données hétérogènes, feature importances | Moins interprétable qu'une LR |
| XGBoost | Souvent le plus performant sur données tabulaires | Hyperparamétrage plus complexe |

## 5. Résultats

*À compléter après exécution de train_model.py et evaluate_model.py*

## 6. Seuils de décision retenus

| Niveau | Seuil churn_score | Action Customer Success |
|---|---|---|
| 🔴 **High**   | ≥ 0.70 | Appel CSM sous 48h — risque immédiat |
| 🟡 **Medium** | 0.40 – 0.70 | Email de réengagement — surveillance renforcée |
| 🟢 **Low**    | < 0.40 | Aucune action requise — compte sain |

Justification : seuil 0.70 minimise les faux positifs en zone haute.
Seuil 0.40 permet d'anticiper à 30 jours et d'activer les campagnes de rétention.

## 7. Limites connues

- **Volume** : 500 comptes est un petit dataset pour le ML.
- **feature_usage.csv** : colonnes `feature_name` et `is_beta_feature` à 100% manquantes — signal d'adoption des fonctionnalités non exploitable.
- **Temporalité** : split stratifié sans validation walk-forward.

---
*smartEngine Groupe G8 — Sprint 3*
