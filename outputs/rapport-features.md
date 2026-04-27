# Rapport de Feature Engineering - smartEngine
Date : 2026-03-11 12:07:30

## Statistiques descriptives du tableau final
|       |   mrr_amount |   nb_subscriptions |   duree_abonnement_jours |   auto_renew_rate |   nb_tickets |   satisfaction_score_moyen |   nb_tickets_urgents |   nb_escalations |   usage_count_moyen |   nb_features_distinctes |   error_count_moyen |   a_churne |
|:------|-------------:|-------------------:|-------------------------:|------------------:|-------------:|---------------------------:|---------------------:|-----------------:|--------------------:|-------------------------:|--------------------:|-----------:|
| count |       500    |           500      |                 312      |        500        |    500       |                          0 |                  500 |              500 |          500        |                      500 |          500        | 500        |
| mean  |      2264.18 |            10      |                  82.789  |          0.800621 |      4       |                        nan |                    0 |                0 |           10.0197   |                        1 |            0.564014 |   0.704    |
| std   |      1600.41 |             3.2713 |                  94.8945 |          0.138414 |      1.89293 |                        nan |                    0 |                0 |            0.464163 |                        0 |            0.153814 |   0.456948 |
| min   |        95    |             2      |                   0      |          0.25     |      0       |                        nan |                    0 |                0 |            8.09091  |                        1 |            0        |   0        |
| 25%   |      1259.45 |             7      |                  16.75   |          0.727273 |      3       |                        nan |                    0 |                0 |            9.7234   |                        1 |            0.460317 |   0        |
| 50%   |      1923.15 |            10      |                  48      |          0.80625  |      4       |                        nan |                    0 |                0 |           10.022    |                        1 |            0.543706 |   1        |
| 75%   |      2744.29 |            12      |                 117      |          0.9      |      5       |                        nan |                    0 |                0 |           10.308    |                        1 |            0.666667 |   1        |
| max   |     13806    |            19      |                 466      |          1        |     11       |                        nan |                    0 |                0 |           11.5556   |                        1 |            1.0625   |   1        |

## Observations clés
- Nombre total de clients : 500
- Taux de churn global : 70.40%
- Nombre de features créées : 16 (hors account_id)
- Secteur le plus représenté : DevTools

## Détail des colonnes
- `plan_tier` : Plan tarifaire du client
- `industry` : Secteur d'activité
- `seats` : Nombre de sièges
- `mrr_amount` : Revenu mensuel récurrent moyen
- `nb_subscriptions` : Nombre total d'abonnements
- `duree_abonnement_jours` : Durée moyenne des abonnements
- `auto_renew_rate` : Taux de renouvellement automatique
- `nb_tickets` : Volume de tickets de support
- `satisfaction_score_moyen` : Score CSAT moyen
- `nb_tickets_urgents` : Nombre de tickets de priorité urgente
- `nb_escalations` : Nombre d'escalades de support
- `usage_count_moyen` : Intensité moyenne d'utilisation
- `nb_features_distinctes` : Diversité des fonctionnalités utilisées
- `error_count_moyen` : Taux d'erreur moyen rencontré
- `a_churne` : Indicateur de présence dans les événements de churn
- `churn_flag` : Variable cible (churn réel)