# Rapport d\'exploration : feature_usage

## 1. Nombre de lignes et colonnes
- **Lignes** : 25000
- **Colonnes** : 8

## 2. Types de colonnes
`
usage_id                 str
subscription_id          str
usage_date               str
feature_name             str
usage_count            int64
usage_duration_secs    int64
error_count            int64
is_beta_feature         bool
`

## 3. Les 5 premières lignes
|    | usage_id   | subscription_id   | usage_date   | feature_name   |   usage_count |   usage_duration_secs |   error_count | is_beta_feature   |
|---:|:-----------|:------------------|:-------------|:---------------|--------------:|----------------------:|--------------:|:------------------|
|  0 | U-1c6c24   | S-0fcf7d          | 2023-07-27   | feature_20     |             9 |                  5004 |             0 | False             |
|  1 | U-f07cb8   | S-c25263          | 2023-08-07   | feature_5      |             9 |                   369 |             0 | False             |
|  2 | U-096807   | S-f29e7f          | 2023-12-07   | feature_3      |             9 |                  1458 |             0 | False             |
|  3 | U-6b1580   | S-be655e          | 2024-07-28   | feature_40     |             5 |                  2085 |             0 | False             |
|  4 | U-720a29   | S-f9b1d0          | 2024-12-02   | feature_12     |            12 |                   900 |             0 | False             |

## 4. Valeurs manquantes
`
usage_id               0
subscription_id        0
usage_date             0
feature_name           0
usage_count            0
usage_duration_secs    0
error_count            0
is_beta_feature        0
`

## 5. Colonnes les plus utiles pour prédire le churn
account_id, feature_name, usage_count, usage_date
