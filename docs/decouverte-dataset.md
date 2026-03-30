# Fiche collective — Découverte du dataset RavenStack

> Sprint 1 · Projet smartEngine · INSEEC MSc2 Manager Data Marketing  
> Rédigée par : [Scrum Master], consolidée avec toute l'équipe  
> Date : Mars 2026  
> Source : Kaggle — SaaS Subscription and Churn Analytics Dataset

---

## Tableau récapitulatif des fichiers CSV

| Fichier | Lignes | Colonnes | Colonnes clés | Observations principales |
|---|---|---|---|---|
| `ravenstack_accounts.csv` | 500 | 10 | account_id, plan_tier, industry, churn_flag | Taux de churn global : 22 % · 3 plans · 5 secteurs · 7 pays |
| `ravenstack_subscriptions.csv` | 5 000 | 14 | subscription_id, account_id, mrr_amount, churn_flag | 4 514 end_date manquantes (= abonnements actifs) · MRR moyen 2 268 $ |
| `ravenstack_feature_usage.csv` | 25 000 | 8 | subscription_id, feature_name, usage_count, error_count | 40 features · 7 731 lignes avec erreurs (31 %) |
| `ravenstack_support_tickets.csv` | 2 000 | 9 | account_id, priority, resolution_time_hours, satisfaction_score | 825 scores de satisfaction manquants (41 %) · délai moyen 36 h |
| `ravenstack_churn_events.csv` | 600 | 9 | account_id, churn_date, reason_code, feedback_text | 6 raisons de churn équilibrées · 148 feedbacks manquants (25 %) |

---

## Relations entre les fichiers

```
ravenstack_accounts.csv  (500 comptes — clé : account_id)
         │
         ├──► ravenstack_subscriptions.csv  (5 000 abonnements — clé : subscription_id)
         │              │
         │              └──► ravenstack_feature_usage.csv  (25 000 usages — clé : subscription_id)
         │
         ├──► ravenstack_support_tickets.csv  (2 000 tickets — clé : account_id)
         │
         └──► ravenstack_churn_events.csv  (600 événements — clé : account_id)
                  └── Présent UNIQUEMENT si le compte a churné → variable cible du modèle
```

> **Note** : `feature_usage` est lié aux abonnements (`subscription_id`), pas directement aux comptes.
> Une jointure en deux étapes sera nécessaire : `feature_usage` → `subscriptions` → `accounts`.

---

## Exploration détaillée par fichier

### 1. ravenstack_accounts.csv — 500 lignes · 10 colonnes

| Colonne | Type | Valeurs manquantes | Pertinence churn |
|---|---|---|---|
| account_id | str | 0 | Clé primaire — jointure |
| account_name | str | 0 | ⚠️ Donnée potentiellement personnelle (RGPD) |
| industry | str | 0 | MOYEN — DevTools churne 2x plus que Cybersecurity |
| country | str | 0 | MOYEN — à analyser par marché |
| signup_date | str | 0 | FORT — ancienneté = proxy de fidélité |
| referral_source | str | 0 | MOYEN — qualité client selon canal d'acquisition |
| plan_tier | str | 0 | MOYEN — churn quasi-identique entre plans (≈22%) |
| seats | int | 0 | MOYEN — taille de l'équipe utilisatrice |
| is_trial | bool | 0 | FORT — 97 comptes en trial, souvent moins engagés |
| churn_flag | bool | 0 | VARIABLE CIBLE principale (22 % positifs) |

**Observations clés :**
- Taux de churn global : **22 %** (110 comptes sur 500)
- Churn par plan : Basic 22% · Pro 21.9% · Enterprise 22.1% → **pas de différence significative entre plans**
- Churn par secteur : **DevTools 31%** (le plus à risque) vs Cybersecurity 16% et EdTech 16.5% (les plus stables)
- Marché dominant : **US 58%** (291/500), puis UK 11.6%
- Aucune valeur manquante · aucun doublon

---

### 2. ravenstack_subscriptions.csv — 5 000 lignes · 14 colonnes

| Colonne | Type | Valeurs manquantes | Pertinence churn |
|---|---|---|---|
| subscription_id | str | 0 | Clé primaire |
| account_id | str | 0 | Clé de jointure avec accounts |
| start_date | str | 0 | FORT — permet de calculer la durée (tenure) |
| end_date | str | 4 514 (90.3%) | FORT — NaN = abonnement actif ; renseigné = terminé |
| plan_tier | str | 0 | MOYEN — Basic / Pro / Enterprise |
| seats | int | 0 | MOYEN — nb de sièges souscrits |
| mrr_amount | int | 0 | FORT — Basic ≈474$ · Pro ≈1257$ · Enterprise ≈4918$ |
| arr_amount | int | 0 | MOYEN — revenu annuel (= MRR × 12) |
| is_trial | bool | 0 | FORT — abonnements gratuits |
| upgrade_flag | bool | 0 | FORT — signal d'engagement positif |
| downgrade_flag | bool | 0 | FORT — signal précurseur de churn classique |
| churn_flag | bool | 0 | Variable cible niveau abonnement (486/5000 = 9.7%) |
| billing_frequency | str | 0 | MOYEN — monthly (50.8%) / annual (49.2%) |
| auto_renew_flag | bool | 0 | FORT — désactivation = intention probable de départ |

**Observations clés :**
- **4 514 end_date manquantes** : normal, ce sont les abonnements encore actifs — ne pas traiter comme des erreurs
- MRR moyen global : **2 268 $** (écart fort entre Basic 475$ et Enterprise 4 918$)
- 486 abonnements churned sur 5 000 = 9.7% au niveau abonnement (un compte peut avoir plusieurs abonnements successifs)
- Billing quasi-équilibré : monthly/annual 50/50

---

### 3. ravenstack_feature_usage.csv — 25 000 lignes · 8 colonnes

| Colonne | Type | Valeurs manquantes | Pertinence churn |
|---|---|---|---|
| usage_id | str | 0 | Clé primaire |
| subscription_id | str | 0 | Clé de jointure avec subscriptions |
| usage_date | str | 0 | FORT — évolution temporelle de l'usage |
| feature_name | str | 0 | FORT — 40 features (feature_1 à feature_40) |
| usage_count | int | 0 | FORT — fréquence d'utilisation (moy. 10, min 0, max 26) |
| usage_duration_secs | int | 0 | FORT — temps passé dans la feature |
| error_count | int | 0 | FORT — 7 731 lignes avec erreurs (31%) → frustration |
| is_beta_feature | bool | 0 | FAIBLE — usage de features beta (10.2%) |

**Observations clés :**
- **40 features distinctes** (feature_1 à feature_40)
- **31% des enregistrements présentent au moins 1 erreur** → signal fort de mauvaise expérience
- usage_count moyen : 10, distribution resserrée (écart-type 3.1)
- Ce fichier est le plus riche pour la prédiction : la **baisse progressive de l'usage** est le signal précurseur de churn le plus documenté
- ⚠️ Lié à `subscription_id` et non à `account_id` → jointure double nécessaire pour remonter au compte

---

### 4. ravenstack_support_tickets.csv — 2 000 lignes · 9 colonnes

| Colonne | Type | Valeurs manquantes | Pertinence churn |
|---|---|---|---|
| ticket_id | str | 0 | Clé primaire |
| account_id | str | 0 | Clé de jointure avec accounts |
| submitted_at | str | 0 | FORT — timing des tickets avant churn |
| closed_at | str | 0 | MOYEN — calcul du temps de résolution |
| resolution_time_hours | float | 0 | FORT — moy. 35.9h · indicateur qualité support |
| priority | str | 0 | FORT — urgent(26%) · high(25%) · medium(25%) · low(24%) |
| first_response_time_minutes | int | 0 | FORT — temps de première réponse |
| satisfaction_score | float | **825 (41.3%)** | FORT — score 1-5 · moy. 3.98 · mais 41% manquants |
| escalation_flag | bool | 0 | FORT — 95 tickets escaladés (4.75%) → incidents graves |

**Observations clés :**
- **41% de satisfaction_score manquants** : tickets fermés sans évaluation → ne pas imputer avec la moyenne, traiter comme catégorie distincte
- Distribution des priorités quasi-équilibrée entre les 4 niveaux
- Délai moyen de résolution : **35.9 heures** — à croiser avec la satisfaction et le churn
- 95 tickets escaladés (4.75%) = cas critiques à prioriser

---

### 5. ravenstack_churn_events.csv — 600 lignes · 9 colonnes

| Colonne | Type | Valeurs manquantes | Pertinence churn |
|---|---|---|---|
| churn_event_id | str | 0 | Clé primaire |
| account_id | str | 0 | Clé de jointure avec accounts |
| churn_date | str | 0 | FORT — date de résiliation (fenêtre de prédiction) |
| reason_code | str | 0 | FORT — 6 raisons équilibrées (voir tableau ci-dessous) |
| refund_amount_usd | float | 0 | MOYEN — moy. 14.42$ |
| preceding_upgrade_flag | bool | 0 | FORT — upgrade avant churn = comportement paradoxal |
| preceding_downgrade_flag | bool | 0 | FORT — signal précurseur classique |
| is_reactivation | bool | 0 | MOYEN — 61 réactivations (10%) → clients potentiellement récupérables |
| feedback_text | str | **148 (24.7%)** | MOYEN — texte libre · analyse NLP possible en Sprint 3 |

**Répartition des raisons de churn :**

| Raison | Nb | % |
|---|---|---|
| features | 114 | 19.0% |
| support | 104 | 17.3% |
| budget | 104 | 17.3% |
| unknown | 95 | 15.8% |
| competitor | 92 | 15.3% |
| pricing | 91 | 15.2% |

**Observations clés :**
- Les 6 raisons sont **quasi-équilibrées** → pas de cause unique dominante
- **"features"** est la première raison (19%) → confirme l'importance de l'analyse feature_usage
- **"support"** en 2ème position → corrélation probable avec les tickets support escaladés
- 10% des churners réactivés → segment rentable pour des campagnes de reconquête
- ⚠️ Ce fichier contient uniquement les comptes ayant churné → la variable cible binaire se construit par jointure avec accounts (`churn_flag`)

---

## Déséquilibre des classes

| Classe | Comptes | % |
|---|---|---|
| Non-churners (0) | 390 | 78% |
| Churners (1) | 110 | 22% |

Déséquilibre modéré (ratio 78/22). À gérer en Sprint 3 avec : `class_weight='balanced'`, SMOTE ou sous-échantillonnage.

---

## Points de vigilance RGPD

| Colonne | Fichier | Risque | Action recommandée |
|---|---|---|---|
| `account_name` | accounts | Nom d'entreprise, potentiellement personne physique | Vérifier l'absence de noms de personnes physiques |
| `feedback_text` | churn_events | Texte libre pouvant contenir des données personnelles | Anonymiser avant tout traitement NLP |

---

## 5 questions métier à explorer avec l'agent

1. **L'usage des features décline-t-il systématiquement dans les 90 jours précédant le churn ?**
   Construire une courbe d'usage moyen des comptes churners vs non-churners sur les 3 derniers mois avant résiliation.

2. **Existe-t-il un profil combiné "secteur + plan + is_trial" associé à un taux de churn significativement plus élevé ?**
   DevTools est déjà à 31% — ce taux est-il amplifié chez les comptes en trial ?

3. **Le taux d'erreur dans feature_usage est-il corrélé avec la probabilité de churn ?**
   Un error_count élevé sur certaines features spécifiques est-il prédictif de la résiliation ?

4. **Les comptes ayant ouvert des tickets de priorité "urgent" ou "high" dans les 60 jours avant le churn ont-ils un taux de churn plus élevé que la moyenne ?**
   Quantifier l'impact de la qualité du support sur la rétention.

5. **Quel est le délai médian entre le premier signal de désengagement (baisse d'usage) et la date de churn effective ?**
   Ce délai déterminera la fenêtre de prédiction optimale pour les alertes Customer Success.

---

*Fiche collective rédigée dans le cadre du Sprint 1 du projet smartEngine — INSEEC MSc2 Manager Data Marketing*
