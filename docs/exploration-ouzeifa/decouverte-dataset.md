# Exploration du Dataset - Prédiction du Churn

Ce document récapitule les données disponibles pour l'analyse du churn (résiliation) et définit les axes de recherche prioritaires.

## Tableau Récapitulatif des Données

| Nom du Fichier | Lignes | Colonnes Clés | Observations |
| :--- | :--- | :--- | :--- |
| **accounts.csv** | 500 | `account_id`, `industry`, `plan_tier`, `churn_flag` | Profil client de base. Contient l'étiquette de churn cible. |
| **churn_events.csv** | 600 | `account_id`, `reason_code`, `feedback_text` | Détails sur les résiliations passées. Utile pour comprendre le "Pourquoi". |
| **feature_usage.csv** | 25 000 | `subscription_id`, `usage_count`, `usage_duration_secs` | Volume massif. Indispensable pour mesurer l'engagement produit. |
| **subscriptions.csv** | 5 000 | `account_id`, `mrr_amount`, `upgrade_flag`, `downgrade_flag` | Données financières. Les baisses de plan (downgrades) sont des signaux faibles de churn. |
| **support_tickets.csv** | 2 000 | `account_id`, `priority`, `satisfaction_score`, `resolution_time_hours` | Indicateur de frustration. Un score de satisfaction bas est corrélé au risque de départ. |

## 5 Questions Métier à Explorer

Pour construire un modèle de prédiction performant, nous devons répondre aux questions suivantes :

1. **L'adoption des fonctionnalités (Feature Adoption) :** Existe-t-il un seuil critique d'utilisation de certaines fonctionnalités (ex: `feature_20`) en dessous duquel la probabilité de churn augmente drastiquement ?
2. **Le signal "Downgrade" :** Un client qui réduit son niveau de forfait (`downgrade_flag`) dans `subscriptions.csv` est-il statistiquement plus susceptible de résilier dans les 3 mois suivants ?
3. **L'impact du Support :** Est-ce qu'un temps de résolution élevé (`resolution_time_hours` > 24h) sur un ticket "Urgent" est un déclencheur direct de départ pour les comptes Enterprise ?
4. **La saisonnalité et l'ancienneté :** Le churn est-il plus fréquent lors de la première période de renouvellement (fin de période d'essai ou premier mois) ou est-il réparti uniformément ?
5. **Le profil de risque par Secteur :** Certaines industries (`EdTech`, `FinTech`, etc.) présentent-elles des taux de churn structurellement plus élevés, nécessitant des stratégies de rétention spécifiques ?

---
*Document généré par Gemini CLI - 10 Mars 2026*
