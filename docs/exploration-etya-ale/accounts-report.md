# Rapport d\'exploration : accounts

## 1. Nombre de lignes et colonnes
- **Lignes** : 500
- **Colonnes** : 10

## 2. Types de colonnes
`
account_id           str
account_name         str
industry             str
country              str
signup_date          str
referral_source      str
plan_tier            str
seats              int64
is_trial            bool
churn_flag          bool
`

## 3. Les 5 premières lignes
|    | account_id   | account_name   | industry   | country   | signup_date   | referral_source   | plan_tier   |   seats | is_trial   | churn_flag   |
|---:|:-------------|:---------------|:-----------|:----------|:--------------|:------------------|:------------|--------:|:-----------|:-------------|
|  0 | A-2e4581     | Company_0      | EdTech     | US        | 2024-10-16    | partner           | Basic       |       9 | False      | False        |
|  1 | A-43a9e3     | Company_1      | FinTech    | IN        | 2023-08-17    | other             | Basic       |      18 | False      | True         |
|  2 | A-0a282f     | Company_2      | DevTools   | US        | 2024-08-27    | organic           | Basic       |       1 | False      | False        |
|  3 | A-1f0ac7     | Company_3      | HealthTech | UK        | 2023-08-27    | other             | Basic       |      24 | True       | False        |
|  4 | A-ce550d     | Company_4      | HealthTech | US        | 2024-10-27    | event             | Enterprise  |      35 | False      | True         |

## 4. Valeurs manquantes
`
account_id         0
account_name       0
industry           0
country            0
signup_date        0
referral_source    0
plan_tier          0
seats              0
is_trial           0
churn_flag         0
`

## 5. Colonnes les plus utiles pour prédire le churn
account_id, industry, company_size, country, created_at
