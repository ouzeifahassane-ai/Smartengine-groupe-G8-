# Rapport d\'exploration : churn_events

## 1. Nombre de lignes et colonnes
- **Lignes** : 600
- **Colonnes** : 9

## 2. Types de colonnes
`
churn_event_id                  str
account_id                      str
churn_date                      str
reason_code                     str
refund_amount_usd           float64
preceding_upgrade_flag         bool
preceding_downgrade_flag       bool
is_reactivation                bool
feedback_text                   str
`

## 3. Les 5 premières lignes
|    | churn_event_id   | account_id   | churn_date   | reason_code   |   refund_amount_usd | preceding_upgrade_flag   | preceding_downgrade_flag   | is_reactivation   | feedback_text          |
|---:|:-----------------|:-------------|:-------------|:--------------|--------------------:|:-------------------------|:---------------------------|:------------------|:-----------------------|
|  0 | C-816288         | A-c37cab     | 2024-10-27   | pricing       |                4.03 | False                    | False                      | False             | switched to competitor |
|  1 | C-5a81e7         | A-37f969     | 2024-06-25   | support       |               96.45 | True                     | False                      | False             | nan                    |
|  2 | C-a174be         | A-b07346     | 2024-11-12   | budget        |                0    | False                    | False                      | False             | missing features       |
|  3 | C-accb39         | A-1e50e0     | 2023-11-01   | budget        |               54.94 | False                    | False                      | False             | switched to competitor |
|  4 | C-92f889         | A-956988     | 2024-12-30   | unknown       |                0    | False                    | True                       | True              | too expensive          |

## 4. Valeurs manquantes
`
churn_event_id                0
account_id                    0
churn_date                    0
reason_code                   0
refund_amount_usd             0
preceding_upgrade_flag        0
preceding_downgrade_flag      0
is_reactivation               0
feedback_text               148
`

## 5. Colonnes les plus utiles pour prédire le churn
account_id, churn_date, churn_reason
