# Découverte du Dataset

## accounts.csv

- **Nombre de colonnes :** 10
- **Nombre de lignes :** 500

### Colonnes et Types (estimés)
- `account_id` : 0 valeurs manquantes
- `account_name` : 0 valeurs manquantes
- `industry` : 0 valeurs manquantes
- `country` : 0 valeurs manquantes
- `signup_date` : 0 valeurs manquantes
- `referral_source` : 0 valeurs manquantes
- `plan_tier` : 0 valeurs manquantes
- `seats` : 0 valeurs manquantes
- `is_trial` : 0 valeurs manquantes
- `churn_flag` : 0 valeurs manquantes

### 3 premières lignes
| account_id | account_name | industry | country | signup_date | referral_source | plan_tier | seats | is_trial | churn_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-2e4581 | Company_0 | EdTech | US | 2024-10-16 | partner | Basic | 9 | False | False |
| A-43a9e3 | Company_1 | FinTech | IN | 2023-08-17 | other | Basic | 18 | False | True |
| A-0a282f | Company_2 | DevTools | US | 2024-08-27 | organic | Basic | 1 | False | False |

### Analyse pour la prédiction du churn
Les informations de segment et la date de création sont utiles pour le profil utilisateur.

---

## churn_events.csv

- **Nombre de colonnes :** 9
- **Nombre de lignes :** 600

### Colonnes et Types (estimés)
- `churn_event_id` : 0 valeurs manquantes
- `account_id` : 0 valeurs manquantes
- `churn_date` : 0 valeurs manquantes
- `reason_code` : 0 valeurs manquantes
- `refund_amount_usd` : 0 valeurs manquantes
- `preceding_upgrade_flag` : 0 valeurs manquantes
- `preceding_downgrade_flag` : 0 valeurs manquantes
- `is_reactivation` : 0 valeurs manquantes
- `feedback_text` : 148 valeurs manquantes

### 3 premières lignes
| churn_event_id | account_id | churn_date | reason_code | refund_amount_usd | preceding_upgrade_flag | preceding_downgrade_flag | is_reactivation | feedback_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-816288 | A-c37cab | 2024-10-27 | pricing | 4.03 | False | False | False | switched to competitor |
| C-5a81e7 | A-37f969 | 2024-06-25 | support | 96.45 | True | False | False |  |
| C-a174be | A-b07346 | 2024-11-12 | budget | 0.0 | False | False | False | missing features |

### Analyse pour la prédiction du churn
C'est la variable cible (churn_date).

---

## feature_usage.csv

- **Nombre de colonnes :** 8
- **Nombre de lignes :** 25000

### Colonnes et Types (estimés)
- `usage_id` : 0 valeurs manquantes
- `subscription_id` : 0 valeurs manquantes
- `usage_date` : 0 valeurs manquantes
- `feature_name` : 0 valeurs manquantes
- `usage_count` : 0 valeurs manquantes
- `usage_duration_secs` : 0 valeurs manquantes
- `error_count` : 0 valeurs manquantes
- `is_beta_feature` : 0 valeurs manquantes

### 3 premières lignes
| usage_id | subscription_id | usage_date | feature_name | usage_count | usage_duration_secs | error_count | is_beta_feature |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U-1c6c24 | S-0fcf7d | 2023-07-27 | feature_20 | 9 | 5004 | 0 | False |
| U-f07cb8 | S-c25263 | 2023-08-07 | feature_5 | 9 | 369 | 0 | False |
| U-096807 | S-f29e7f | 2023-12-07 | feature_3 | 9 | 1458 | 0 | False |

### Analyse pour la prédiction du churn
Très important : la fréquence d'utilisation des fonctionnalités est un indicateur clé de l'engagement.

---

## subscriptions.csv

- **Nombre de colonnes :** 14
- **Nombre de lignes :** 5000

### Colonnes et Types (estimés)
- `subscription_id` : 0 valeurs manquantes
- `account_id` : 0 valeurs manquantes
- `start_date` : 0 valeurs manquantes
- `end_date` : 4514 valeurs manquantes
- `plan_tier` : 0 valeurs manquantes
- `seats` : 0 valeurs manquantes
- `mrr_amount` : 0 valeurs manquantes
- `arr_amount` : 0 valeurs manquantes
- `is_trial` : 0 valeurs manquantes
- `upgrade_flag` : 0 valeurs manquantes
- `downgrade_flag` : 0 valeurs manquantes
- `churn_flag` : 0 valeurs manquantes
- `billing_frequency` : 0 valeurs manquantes
- `auto_renew_flag` : 0 valeurs manquantes

### 3 premières lignes
| subscription_id | account_id | start_date | end_date | plan_tier | seats | mrr_amount | arr_amount | is_trial | upgrade_flag | downgrade_flag | churn_flag | billing_frequency | auto_renew_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-8cec59 | A-3c1a3f | 2023-12-23 | 2024-04-12 | Enterprise | 14 | 2786 | 33432 | False | False | False | True | monthly | True |
| S-0f6f44 | A-9b9fe9 | 2024-06-11 |  | Pro | 17 | 833 | 9996 | False | False | False | False | monthly | True |
| S-51c0d1 | A-659280 | 2024-11-25 |  | Enterprise | 62 | 0 | 0 | True | True | False | False | annual | False |

### Analyse pour la prédiction du churn
Les types de plans et les montants peuvent indiquer le niveau d'investissement financier.

---

## support_tickets.csv

- **Nombre de colonnes :** 9
- **Nombre de lignes :** 2000

### Colonnes et Types (estimés)
- `ticket_id` : 0 valeurs manquantes
- `account_id` : 0 valeurs manquantes
- `submitted_at` : 0 valeurs manquantes
- `closed_at` : 0 valeurs manquantes
- `resolution_time_hours` : 0 valeurs manquantes
- `priority` : 0 valeurs manquantes
- `first_response_time_minutes` : 0 valeurs manquantes
- `satisfaction_score` : 825 valeurs manquantes
- `escalation_flag` : 0 valeurs manquantes

### 3 premières lignes
| ticket_id | account_id | submitted_at | closed_at | resolution_time_hours | priority | first_response_time_minutes | satisfaction_score | escalation_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-0024de | A-712f1c | 2023-07-27 | 2023-07-28 03:00:00 | 27.0 | high | 74 |  | False |
| T-4d04b9 | A-e43bf7 | 2024-07-08 | 2024-07-09 03:00:00 | 27.0 | urgent | 144 |  | False |
| T-d5e12f | A-0f3e88 | 2024-10-17 | 2024-10-17 19:00:00 | 19.0 | urgent | 93 | 4.0 | False |

### Analyse pour la prédiction du churn
Le volume et la priorité des tickets peuvent signaler une insatisfaction.

---

