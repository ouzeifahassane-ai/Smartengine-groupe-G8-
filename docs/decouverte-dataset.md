# Découverte Collective du Dataset - SmartEngine

Ce document présente une vue d'ensemble des données collectées pour la plateforme de prédiction du churn.

## Tableau Récapitulatif des Données

| Nom du Fichier | Lignes | Colonnes Clés | Observations Importantes |
| :--- | :--- | :--- | :--- |
| **accounts.csv** | 500 | `account_id`, `industry`, `plan_tier`, `churn_flag` | Définit le profil de base des clients et l'état actuel (churn ou non). |
| **churn_events.csv** | 600 | `account_id`, `churn_date`, `reason_code` | Historique précis des résiliations. Crucial pour identifier les motifs de départ. |
| **feature_usage.csv** | 25 000 | `usage_id`, `usage_count`, `usage_duration_secs` | Données d'activité très granulaires. Principal indicateur de l'engagement produit. |
| **subscriptions.csv** | 5 000 | `account_id`, `mrr_amount`, `upgrade_flag` | Suivi financier et évolution des contrats. Permet de détecter les baisses de revenus. |
| **support_tickets.csv** | 2 000 | `priority`, `resolution_time_hours`, `satisfaction_score` | Reflet de la satisfaction client. Les tickets non résolus ou urgents sont des signaux de risque. |

## 5 Questions Métier à Explorer

1.  **Adoption du Produit :** Existe-t-il une corrélation entre une baisse soudaine de l'utilisation de certaines fonctionnalités clés dans `feature_usage.csv` et une résiliation dans les 30 jours ?
2.  **Santé Financière :** Est-ce qu'un client ayant effectué un "downgrade" (réduction de plan) dans `subscriptions.csv` a une probabilité de churn significativement plus élevée que les autres ?
3.  **Qualité du Support :** Un score de satisfaction client (`satisfaction_score`) inférieur à 3/5 sur les tickets de support est-il le principal déclencheur de départ pour les clients "Enterprise" ?
4.  **Profil à Risque :** Quels secteurs d'activité (`industry`) présentent le taux de churn le plus élevé, et faut-il ajuster notre modèle de prédiction pour ces segments spécifiques ?
5.  **Réactivité :** Le délai de première réponse du support influe-t-il davantage sur le churn que le temps total de résolution du ticket ?

---
*Document collectif généré par Gemini CLI - 10 Mars 2026*
