# Rapport d\'exploration : subscriptions

## 1. Nombre de lignes et colonnes
- **Lignes** : 5000
- **Colonnes** : 14

## 2. Types de colonnes
`
subscription_id        str
account_id             str
start_date             str
end_date               str
plan_tier              str
seats                int64
mrr_amount           int64
arr_amount           int64
is_trial              bool
upgrade_flag          bool
downgrade_flag        bool
churn_flag            bool
billing_frequency      str
auto_renew_flag       bool
`

## 3. Les 5 premières lignes
|    | subscription_id   | account_id   | start_date   | end_date   | plan_tier   |   seats |   mrr_amount |   arr_amount | is_trial   | upgrade_flag   | downgrade_flag   | churn_flag   | billing_frequency   | auto_renew_flag   |
|---:|:------------------|:-------------|:-------------|:-----------|:------------|--------:|-------------:|-------------:|:-----------|:---------------|:-----------------|:-------------|:--------------------|:------------------|
|  0 | S-8cec59          | A-3c1a3f     | 2023-12-23   | 2024-04-12 | Enterprise  |      14 |         2786 |        33432 | False      | False          | False            | True         | monthly             | True              |
|  1 | S-0f6f44          | A-9b9fe9     | 2024-06-11   | nan        | Pro         |      17 |          833 |         9996 | False      | False          | False            | False        | monthly             | True              |
|  2 | S-51c0d1          | A-659280     | 2024-11-25   | nan        | Enterprise  |      62 |            0 |            0 | True       | True           | False            | False        | annual              | False             |
|  3 | S-f81687          | A-e7a1e2     | 2024-11-23   | 2024-12-13 | Enterprise  |       5 |          995 |        11940 | False      | False          | False            | True         | monthly             | True              |
|  4 | S-cff5a2          | A-ba6516     | 2024-01-10   | nan        | Enterprise  |      27 |         5373 |        64476 | False      | False          | False            | False        | monthly             | True              |

## 4. Valeurs manquantes
`
subscription_id         0
account_id              0
start_date              0
end_date             4514
plan_tier               0
seats                   0
mrr_amount              0
arr_amount              0
is_trial                0
upgrade_flag            0
downgrade_flag          0
churn_flag              0
billing_frequency       0
auto_renew_flag         0
`

## 5. Colonnes les plus utiles pour prédire le churn
account_id, plan_type, monthly_price, status, start_date
