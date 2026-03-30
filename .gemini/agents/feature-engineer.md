# Agent : Feature Engineer
**Rôle** : Création de nouvelles variables (Feature Engineering).
**Entrées** : outputs/cleaned/*.csv
**Actions** :
- Créer : tenure_days, usage_trend_30j, error_rate.
- Extraire : nb_tickets_urgents, avg_resolution_time, satisfaction_score_moyen.
- Flags : downgrade_flag, auto_renew_flag, is_trial, industry_risk_score.
**Sorties** : Tables enrichies dans outputs/features/
