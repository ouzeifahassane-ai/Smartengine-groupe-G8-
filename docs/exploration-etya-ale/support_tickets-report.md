# Rapport d\'exploration : support_tickets

## 1. Nombre de lignes et colonnes
- **Lignes** : 2000
- **Colonnes** : 9

## 2. Types de colonnes
`
ticket_id                          str
account_id                         str
submitted_at                       str
closed_at                          str
resolution_time_hours          float64
priority                           str
first_response_time_minutes      int64
satisfaction_score             float64
escalation_flag                   bool
`

## 3. Les 5 premières lignes
|    | ticket_id   | account_id   | submitted_at   | closed_at           |   resolution_time_hours | priority   |   first_response_time_minutes |   satisfaction_score | escalation_flag   |
|---:|:------------|:-------------|:---------------|:--------------------|------------------------:|:-----------|------------------------------:|---------------------:|:------------------|
|  0 | T-0024de    | A-712f1c     | 2023-07-27     | 2023-07-28 03:00:00 |                      27 | high       |                            74 |                  nan | False             |
|  1 | T-4d04b9    | A-e43bf7     | 2024-07-08     | 2024-07-09 03:00:00 |                      27 | urgent     |                           144 |                  nan | False             |
|  2 | T-d5e12f    | A-0f3e88     | 2024-10-17     | 2024-10-17 19:00:00 |                      19 | urgent     |                            93 |                    4 | False             |
|  3 | T-dfce9a    | A-4c56c9     | 2024-09-08     | 2024-09-09 23:00:00 |                      47 | medium     |                           126 |                    5 | False             |
|  4 | T-c59f77    | A-6f8ad2     | 2024-11-30     | 2024-12-01 02:00:00 |                      26 | medium     |                             8 |                  nan | False             |

## 4. Valeurs manquantes
`
ticket_id                        0
account_id                       0
submitted_at                     0
closed_at                        0
resolution_time_hours            0
priority                         0
first_response_time_minutes      0
satisfaction_score             825
escalation_flag                  0
`

## 5. Colonnes les plus utiles pour prédire le churn
account_id, ticket_priority, ticket_status, resolution_time_hours
