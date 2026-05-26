# Rapport de Nettoyage des Données — SmartEngine G8
**Auteur :** Boulama (Développeur IA) | **Script :** `src/clean_data.py`

---

## Synthèse globale

| Fichier | Lignes initiales | Lignes conservées | Doublons supprimés | Statut |
|---------|-----------------|-------------------|-------------------|--------|
| accounts.csv | 500 | 500 | 0 | ✅ Succès |
| subscriptions.csv | 5 000 | 5 000 | 0 | ✅ Succès |
| feature_usage.csv | 25 000 | 25 000 | 0 | ✅ Succès |
| support_tickets.csv | 2 000 | 2 000 | 0 | ✅ Succès |
| churn_events.csv | 600 | 600 | 0 | ✅ Succès |

**Total lignes traitées : 33 100** | **Fichiers nettoyés :** `data/processed/`

---

## 1. accounts.csv (500 lignes)

| Problème | Volume | Stratégie | Justification | Résultat |
|----------|--------|-----------|---------------|---------|
| Doublons | 0 | — | Données complètes et uniques | Aucun doublon |
| Valeurs manquantes | 0 | — | Données complètes | Colonne 100% renseignée |
| Outliers | 0 | — | Distribution normale | Aucun outlier |

**Fichier nettoyé :** `data/processed/accounts.csv`

---

## 2. subscriptions.csv (5 000 lignes)

| Problème | Volume | Stratégie | Justification | Résultat |
|----------|--------|-----------|---------------|---------|
| Doublons | 0 | — | Données uniques | Aucun doublon |
| `end_date` manquante | 4 514 (90,28%) | Conservation (NULL = actif) | `end_date` NULL signifie abonnement en cours — valeur métier, pas une erreur | Colonne non modifiée |
| `mrr_amount` outliers | 134 | Signalement sans suppression | Valeurs extrêmes réelles (comptes Enterprise avec MRR élevé) | Documenté, conservé |
| `arr_amount` outliers | 134 | Signalement sans suppression | Cohérent avec mrr_amount (ARR = MRR × 12) | Documenté, conservé |

**Fichier nettoyé :** `data/processed/subscriptions.csv`

---

## 3. feature_usage.csv (25 000 lignes)

| Problème | Volume | Stratégie | Justification | Résultat |
|----------|--------|-----------|---------------|---------|
| Doublons | 0 | — | Données uniques | Aucun doublon |
| `feature_name` manquant | 25 000 (100%) | Conservation | Colonne non utilisée en modélisation — on agrège sur `usage_count` et `usage_duration_secs` | Colonne conservée |
| `is_beta_feature` manquant | 25 000 (100%) | Conservation | Colonne non critique pour le modèle V1 | Colonne conservée |
| `usage_count` outliers | 97 | Signalement sans suppression | Pics d'usage légitimes (clients enterprise intensifs) | Documenté, conservé |
| `error_count` outliers | 564 | Signalement sans suppression | Erreurs élevées = signal de churn potentiel à préserver | Documenté, conservé |

**Fichier nettoyé :** `data/processed/feature_usage.csv`

---

## 4. support_tickets.csv (2 000 lignes)

| Problème | Volume | Stratégie | Justification | Résultat |
|----------|--------|-----------|---------------|---------|
| Doublons | 0 | — | Données uniques | Aucun doublon |
| `satisfaction_score` manquant | 825 (41,25%) | Imputation par la médiane | La médiane (3.0/5) est neutre et robuste aux outliers. Remplacer par 0 biaiserait le signal de satisfaction vers le bas. | 825 valeurs → 3.0 |
| `escalation_flag` manquant | 2 000 (100%) | Imputation par 'Unknown' (texte) ou 0 | Champ inexistant dans certains exports — traité comme absence d'escalation | Valeur 0 / Unknown |

**Fichier nettoyé :** `data/processed/support_tickets.csv`

---

## 5. churn_events.csv (600 lignes)

| Problème | Volume | Stratégie | Justification | Résultat |
|----------|--------|-----------|---------------|---------|
| Doublons | 0 | — | Données uniques | Aucun doublon |
| `is_reactivation` manquant | 600 (100%) | Imputation par 'Unknown' | Champ non disponible dans la source — non utilisé dans le modèle V1 | Valeur 'Unknown' |
| `feedback_text` manquant | 148 (24,67%) | Imputation par 'Unknown' | Texte libre non utilisé en ML, NULL non acceptable en CSV | Valeur 'Unknown' |
| `refund_amount_usd` outliers | 15 | Signalement sans suppression | Remboursements élevés = cas légitimes (résiliations Enterprise) | Documenté, conservé |

**Fichier nettoyé :** `data/processed/churn_events.csv`

---

## Décisions transversales

1. **Zéro suppression de lignes** : aucun cas ne justifie la suppression (volume limité = 500 comptes, chaque observation est précieuse pour le modèle).
2. **Imputation conservatrice** : seule `satisfaction_score` est imputée par la médiane (3.0). Les autres champs manquants reçoivent 'Unknown' ou sont conservés tels quels.
3. **Outliers conservés** : les valeurs extrêmes sont des signaux métier réels (comptes Enterprise, pics d'usage, MRR élevé). Leur suppression biaiserait le modèle.
4. **`end_date` NULL en subscriptions** = abonnement actif en cours — convention métier documentée, ne pas imputer.
5. **Variable cible `churn_flag`** : dérivée de `churn_events.csv` dans `build_features.py` (1 si account_id présent, 0 sinon). Taux de churn observé : **~22%** (110 comptes sur 500).

## Étape suivante

```
python src/build_analytics.py   # Fusion des 5 tables
python src/build_features.py    # Feature engineering
python src/train_model.py       # Entraînement du modèle
```
