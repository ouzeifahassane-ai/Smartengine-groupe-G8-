# Recommandations stratégiques — Projet smartEngine
**Direction RavenStack | Sprint 4 — Mai 2026**

---

## 1. Ce que dit le modèle

### 1.1 Résultats globaux (en langage non technique)

Notre système analyse les comportements de vos 500 clients pour estimer la probabilité que chacun résilie son abonnement dans les semaines à venir. Il ne s'agit pas d'une certitude, mais d'une alerte précoce basée sur des signaux mesurables : fréquence d'utilisation de la plateforme, nombre de tickets de support, ancienneté de l'abonnement, etc.

**Ce que nous avons observé :**
- **208 comptes** (41,6 % du portefeuille) présentent un score de churn supérieur à 50 % — ils constituent la zone prioritaire d'intervention.
- **93 comptes** sont classés Q1 : risque élevé *et* valeur élevée. Ce sont les comptes Enterprise et Pro en danger maximal. Ils représentent 308 011 €/mois de MRR, soit 27,2 % du MRR total.
- Le MRR total à risque (Q1 + Q2) s'élève à **454 499 €/mois**, soit 40,1 % du portefeuille.

### 1.2 Profils les plus à risque

Les signaux qui prédisent le mieux le churn dans notre modèle sont :
- **Faible utilisation** : les comptes qui se connectent rarement ou n'utilisent que peu de fonctionnalités.
- **Tickets de support non résolus** ou escaladés : signe d'insatisfaction persistante.
- **Renouvellement non automatique** : les clients qui ont désactivé le renouvellement auto ont 3× plus de risque de partir.
- **Faible satisfaction déclarée** (score inférieur à 3/5).
- **Durée d'abonnement courte** : les clients de moins de 12 mois sont plus volatils.

---

## 2. Actions recommandées par quadrant

### Q1 — Risque élevé / Valeur élevée (93 comptes — 308 011 €/mois)
**Profil :** Gros comptes Enterprise et Pro en danger immédiat.
**Action : Appel téléphonique du CSM sous 48 heures**
- Contacter le décisionnaire principal du compte.
- Proposer un audit personnalisé de l'usage (session de formation, nouvelles fonctionnalités).
- Offrir une option de fidélisation : remise sur renouvellement annuel, extension de période d'essai d'une fonctionnalité premium.
- Documenter le motif d'insatisfaction et remonter au Product.

### Q2 — Risque élevé / Valeur faible (115 comptes — 146 488 €/mois)
**Profil :** Petits comptes (Basic) en danger, principalement des PME.
**Action : Email automatisé de réengagement**
- Séquence automatisée J0 → J7 → J14 via CRM.
- Message personnalisé avec les fonctionnalités non encore utilisées.
- Proposer une session d'onboarding courte (30 min).
- Si pas de réponse à J+14 : escalader vers l'équipe support.

### Q3 — Risque faible / Valeur élevée (157 comptes — 516 316 €/mois)
**Profil :** Gros comptes fidèles et actifs — votre socle de revenus stable.
**Action : Surveiller et fidéliser sans déranger**
- Alerter le CSM si le score de churn augmente de >0,20 en un mois.
- Programme de Customer Success proactif : QBR (Quarterly Business Review) trimestriel.
- Proposer un accès anticipé aux nouvelles fonctionnalités.
- **Ne pas envoyer de communications de réengagement** : elles peuvent signaler une inquiétude là où il n'y en a pas.

### Q4 — Risque faible / Valeur faible (135 comptes — 161 273 €/mois)
**Profil :** Petits comptes stables, peu actifs mais non menacés.
**Action : Aucune action prioritaire**
- Intégrer dans les campagnes marketing globales (newsletter, nouveautés).
- Surveiller passivement le score au prochain cycle d'actualisation.

---

## 3. ROI estimé

### 3.1 Coût actuel du churn

En supposant un taux de churn réel de 20 % sur 12 mois (hypothèse conservatrice basée sur les données historiques) :

| Indicateur | Valeur estimée |
|---|---|
| MRR total du portefeuille | 1 132 088 €/mois |
| MRR perdu par churn sur 12 mois (20 %) | ~226 418 €/mois de MRR × 12 = **2 717 016 €/an** |
| MRR Q1 + Q2 à risque immédiat | 454 499 €/mois |

### 3.2 Gain potentiel si on retient 30 % des comptes Q1 + Q2

| Scénario | Taux de rétention additionnel | MRR sauvé/mois | MRR sauvé/an |
|---|---|---|---|
| Pessimiste | 15 % des Q1+Q2 | 68 175 € | **818 099 €** |
| Réaliste | 30 % des Q1+Q2 | 136 350 € | **1 636 198 €** |
| Optimiste | 45 % des Q1+Q2 | 204 525 € | **2 454 297 €** |

### 3.3 Coût des actions

| Action | Coût estimé/mois |
|---|---|
| CSM calls Q1 (93 comptes × 1h × 80 €/h) | 7 440 €/mois |
| Séquence email automatisée Q2 (plateforme + temps) | 1 200 €/mois |
| Total actions | **8 640 €/mois** |

### 3.4 ROI

**Scénario réaliste :**
- Gain : 136 350 €/mois
- Coût : 8 640 €/mois
- **ROI mensuel : 1 478 %**
- **Retour sur investissement dès le 1er mois**

*Ces chiffres sont des estimations basées sur les données disponibles. Ils seront affinés après la phase pilote.*

---

## 4. Feuille de route de déploiement

### Phase 1 — Pilote (Semaines 1-4)
- Sélectionner **20 comptes Q1** pour le pilote CSM.
- Former l'équipe Customer Success au dashboard Streamlit (1h de formation).
- Lancer la séquence email automatisée sur **30 comptes Q2**.
- Mettre en place le groupe témoin (voir section 5).

### Phase 2 — Mesure (Semaines 5-8)
- Comparer le taux de rétention entre groupe traité et groupe témoin.
- Calculer l'uplift réel.
- Ajuster les messages et les seuils si nécessaire.

### Phase 3 — Généralisation (Semaine 9+)
- Déployer les actions sur l'ensemble des Q1 et Q2.
- Automatiser l'actualisation hebdomadaire des scores (script `generate_scores.py`).
- Intégrer le dashboard dans les outils quotidiens du CSM.

---

## 5. Protocole de mesure d'impact

### 5.1 Pourquoi un groupe témoin est indispensable

Si on applique des actions sur tous les comptes à risque et qu'on observe 70 % de rétention, on ne sait pas si c'est *grâce aux actions* ou si ces comptes auraient de toute façon renouvelé. Le groupe témoin répond à cette question : il reçoit un traitement identique à l'exception de l'action testée.

### 5.2 Dispositif expérimental (Test A/B)

**Constitution des groupes :**
- Prendre les 208 comptes des quadrants Q1 et Q2.
- Les diviser aléatoirement en deux groupes de taille égale (stratifié par quadrant) :
  - **Groupe traité (n=104)** : reçoit les actions de rétention (appel CSM ou email).
  - **Groupe témoin (n=104)** : ne reçoit aucune action de rétention spécifique.

**Durée :** 8 semaines minimum.

**Méthode d'allocation :**
```python
import numpy as np
q1_q2_accounts = priorisation_df[priorisation_df['quadrant'].isin([1, 2])]['account_id']
np.random.seed(42)
traite = np.random.choice(q1_q2_accounts, size=len(q1_q2_accounts)//2, replace=False)
temoin = [a for a in q1_q2_accounts if a not in traite]
```

### 5.3 Indicateurs de mesure (KPIs)

| KPI | Définition | Cible |
|---|---|---|
| Taux de rétention | % de comptes Q1+Q2 qui renouvellent à 8 semaines | Groupe traité > Groupe témoin |
| Uplift | Taux rétention traité − taux rétention témoin | > +10 pp |
| MRR sauvé | MRR des comptes Q1+Q2 ayant renouvelé | > 40 000 €/mois |
| Coût par compte retenu | Coût total actions / nb comptes retenus supplémentaires | < 200 €/compte |
| NPS post-action | Score Net Promoter Score après interaction CSM | > 40 |

### 5.4 Interprétation de l'uplift

```
Uplift = Taux rétention (traité) - Taux rétention (témoin)

Exemple :
  Rétention groupe traité  : 72 %
  Rétention groupe témoin  : 55 %
  Uplift                   : +17 points de pourcentage
  
→ L'action de rétention a permis de sauver 17 % de comptes supplémentaires
  par rapport à ce qui se serait passé naturellement.
```

**Si uplift < 5 pp** : revoir le message, le timing ou l'identification des comptes.
**Si uplift ≥ 15 pp** : le modèle et les actions sont validés → généraliser.

---

## 6. Note sur le RGPD (Article 22)

Le score de churn est un score de probabilité produit par un algorithme. Conformément à l'article 22 du RGPD relatif aux décisions automatisées :

- **Le score ne déclenche jamais une action automatique sans intervention humaine.** C'est le CSM ou le responsable marketing qui décide d'agir, sur la base du score, pas l'algorithme seul.
- Chaque compte peut demander une explication de son score (droit à l'explication — fourni par les valeurs SHAP dans le dashboard).
- Les données utilisées pour la prédiction sont limitées aux données comportementales et d'usage nécessaires (principe de minimisation des données).
- Un registre des décisions de traitement est maintenu dans le dossier de conception.

---

*Document rédigé par Boulama — Sprint 4, mai 2026*
*Projet smartEngine — Groupe G8 — INSEEC MSc*
