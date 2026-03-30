# Rapport de Nettoyage des Données - smartEngine
Date : 2026-03-11 12:03:48

## ravenstack_accounts.csv
- Lignes initiales : 500
- Colonnes de dates converties : signup_date, seats
- Fichier nettoyé sauvegardé : outputs\accounts_clean.csv

## ravenstack_subscriptions.csv
- Lignes initiales : 5000
- Colonnes de dates converties : start_date, end_date, seats
- Valeurs manquantes identifiées :
  - end_date : 4514 (90.28%)
- Outliers détectés dans mrr_amount : 134
- Outliers détectés dans arr_amount : 134
- Fichier nettoyé sauvegardé : outputs\subscriptions_clean.csv

## ravenstack_feature_usage.csv
- Lignes initiales : 25000
- Colonnes de dates converties : usage_date, feature_name, usage_duration_secs, is_beta_feature
- Valeurs manquantes identifiées :
  - feature_name : 25000 (100.0%)
  - is_beta_feature : 25000 (100.0%)
- Outliers détectés dans usage_count : 97
- Outliers détectés dans error_count : 564
- Fichier nettoyé sauvegardé : outputs\feature_usage_clean.csv

## ravenstack_support_tickets.csv
- Lignes initiales : 2000
- Colonnes de dates converties : submitted_at, closed_at, satisfaction_score, escalation_flag
- Valeurs manquantes identifiées :
  - satisfaction_score : 825 (41.25%)
  - escalation_flag : 2000 (100.0%)
- Fichier nettoyé sauvegardé : outputs\support_tickets_clean.csv

## ravenstack_churn_events.csv
- Lignes initiales : 600
- Colonnes de dates converties : churn_date, is_reactivation
- Valeurs manquantes identifiées :
  - is_reactivation : 600 (100.0%)
  - feedback_text : 148 (24.67%)
- Outliers détectés dans refund_amount_usd : 15
- Fichier nettoyé sauvegardé : outputs\churn_events_clean.csv
