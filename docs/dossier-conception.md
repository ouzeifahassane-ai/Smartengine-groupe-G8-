# Dossier de Conception - Projet SmartEngine

## Sprint 1 : Cadrage du Projet

### 1. Contexte métier de RavenStack
RavenStack est un fournisseur de services SaaS (Software as a Service) en pleine croissance. Dans un marché B2B hautement concurrentiel, la rétention des clients est devenue la priorité stratégique numéro un. RavenStack fait face à un phénomène de "churn" (résiliation) qui impacte son revenu récurrent mensuel (MRR). Pour pérenniser son activité, l'entreprise doit passer d'une posture réactive (constater le départ d'un client) à une posture proactive (prédire le risque de départ pour intervenir en amont).

### 2. Objectifs du projet smartEngine
Le projet **smartEngine** a pour but de concevoir et déployer une plateforme d'intelligence artificielle capable de :
*   Identifier les signaux faibles de désengagement client.
*   Prédire avec précision la probabilité de churn pour chaque compte.
*   Fournir une interface visuelle (Dashboard) aux équipes de Customer Success pour prioriser leurs actions de rétention.
*   Automatiser des alertes via des workflows intelligents (n8n).

## Sprint 2 : Modélisation et Résultats

### 3. Modélisation prédictive
#### 3.1 Algorithmes et Performance
Plusieurs algorithmes ont été évalués pour identifier le plus performant :
*   **Logistic Regression (Retenu) :** Offre le meilleur équilibre avec un **AUC-ROC de 0.696**. Son interprétabilité est un atout majeur pour expliquer le score aux équipes métiers.
*   **Random Forest :** Testé mais présentant des performances moindres sur le rappel.
*   **XGBoost :** Écarté en raison de l'absence de la bibliothèque `libomp` sur l'environnement d'exécution, empêchant son déploiement stable.

#### 3.2 Stratégie d'entraînement
*   **Split :** Répartition 80% entraînement / 20% test avec **stratification** pour préserver la distribution des classes.
*   **Gestion du déséquilibre :** Le jeu de données contient 78% de clients actifs et 22% de churn. L'utilisation de `class_weight='balanced'` a permis de compenser ce déséquilibre.
*   **Métriques :** Évaluation basée sur l'AUC-ROC, la précision, le rappel (recall) et le F1-score.

#### 3.3 Caractéristiques (Features) importantes
Le modèle identifie le risque de churn principalement via :
*   **Engagement :** `days_since_last_login` et `usage_trend_3m`.
*   **Support :** `ratio_critical_tickets` et `avg_resolution_delay`.
*   **Fidélité :** `seniority_months`.

#### 3.4 Seuils de risque et Actions
Le score de probabilité (0 à 1) est traduit en niveaux d'alerte :
*   **Élevé (> 0.7) :** Risque critique, intervention immédiate requise.
*   **Modéré (0.4 - 0.7) :** Surveillance accrue et contact préventif.
*   **Faible (< 0.4) :** Risque normal, maintien de la relation standard.

#### 3.5 Limites et Biais potentiels
*   **Biais géographiques et sectoriels :** Des disparités de comportement peuvent exister par pays ou par industrie, pouvant biaiser les prédictions pour les segments sous-représentés.
*   **Limites :** Le modèle est basé sur des données historiques et nécessite un réapprentissage régulier pour s'adapter aux nouvelles tendances d'utilisation du SaaS.

### 4. Contraintes RGPD
Le traitement des données clients est soumis au Règlement Général sur la Protection des Données (RGPD) :
*   **Principes généraux :** Limitation des finalités (les données ne servent qu'à la rétention), minimisation des données (seules les données utiles au churn sont traitées) et sécurité renforcée.
*   **Article 22 (Décisions automatisées) :** Le RGPD interdit les décisions produisant des effets juridiques basées uniquement sur un traitement automatisé sans intervention humaine.
*   **Application au score de churn :** Le score de churn ne doit pas entraîner une résiliation automatique du contrat par RavenStack, mais doit servir d'outil d'aide à la décision pour un gestionnaire humain. Le client doit pouvoir contester ou obtenir une explication sur son score.
*   **Loi Informatique et Libertés :** En complément du RGPD, elle encadre la protection des données personnelles en France, notamment sur les droits d'accès et de rectification.

### 5. Choix d'outils justifiés
*   **Python/pandas :** Standard industriel pour le traitement de données tabulaires (CSV).
*   **scikit-learn :** Pour sa robustesse et sa simplicité dans la mise en œuvre de modèles de classification performants.
*   **Streamlit :** Choisi pour sa capacité à transformer des scripts Python en applications web interactives en quelques minutes, facilitant l'adoption par les métiers.
*   **n8n :** Pour son approche "low-code" permettant de connecter les prédictions du modèle aux outils de communication (Email, Slack, CRM) sans développement lourd.
*   **Gemini CLI :** Utilisé comme agent d'ingénierie pour accélérer le développement, la documentation et le respect des standards de code.

---
*Document de conception - Mise à jour Sprint 2 - 27 Avril 2026*
## Section 4 : Déploiement

### 4.1 Segmentation risque / valeur

**Pourquoi la matrice risque/valeur plutôt qu'un clustering ?**
Le clustering (K-means) produit des groupes automatiques difficiles à interpréter pour les équipes métier. La matrice risque/valeur est volontairement simple : chaque quadrant correspond à une décision claire et immédiate. Elle parle directement aux équipes Customer Success sans nécessiter de formation technique.

**Définition des seuils de valeur :**
Le seuil MRR est défini sur la médiane du MRR de la table analytique. Les comptes au-dessus de la médiane sont classés "valeur élevée", en dessous "valeur faible". Ce choix garantit une répartition équilibrée des comptes entre les quadrants.

**Les 4 quadrants et actions associées :**

| Quadrant | Profil | Action |
|---|---|---|
| Risque élevé / Valeur élevée | Gros comptes en danger | Appel CSM dans les 24h |
| Risque élevé / Valeur faible | Petits comptes en danger | Email automatisé de rétention |
| Risque faible / Valeur élevée | Gros comptes fidèles | Fidélisation proactive |
| Risque faible / Valeur faible | Petits comptes stables | Aucune action prioritaire |

---

### 4.2 Dashboard Streamlit

**Choix des visualisations :**
Trois vues complémentaires ont été conçues pour répondre aux besoins des équipes métier :
- Vue portefeuille : KPIs globaux, distribution des scores, répartition par quadrant
- Vue priorisation : matrice risque/valeur interactive, liste filtrable par score/MRR/plan
- Vue fiche compte : profil détaillé, score, quadrant, action recommandée, explication SHAP

**Accessibilité (WCAG) :**
Les couleurs choisies respectent les critères WCAG 2.1 pour le daltonisme : rouge/vert remplacés par des palettes orange/bleu accessibles. Chaque élément visuel est accompagné d'un libellé textuel.

**Retour d'expérience Streamlit :**
Streamlit permet de créer une interface interactive sans HTML/CSS. La courbe d'apprentissage est faible, idéale pour un prototype rapide. Limite principale : les performances sur de grands datasets nécessitent une mise en cache avec `@st.cache_data`.

---

### 4.3 Recommandations et mesure d'impact

**Méthode de calcul du ROI :**
- Coût actuel du churn = nombre de churners × MRR moyen
- Gain estimé = MRR à risque × taux de rétention cible × taux de succès des actions
- Coût des actions = coût par contact × nombre de comptes ciblés
- ROI = (Gain estimé - Coût des actions) / Coût des actions

**Protocole de mesure d'impact :**
Pour prouver que les actions de rétention créent de la valeur :
1. Groupe traité : reçoit l'action de rétention (appel CSM ou email)
2. Groupe témoin : aucune action (sélection aléatoire parmi les comptes à risque)
3. Mesure après 30 jours : taux de rétention des deux groupes
4. Uplift = taux de rétention groupe traité - taux de rétention groupe témoin
5. KPIs suivis : taux de rétention, MRR sauvé, coût par compte retenu

**Conduite du changement :**
Le déploiement suit une approche progressive : phase pilote sur le quadrant "risque élevé / valeur élevée" (impact maximal), puis élargissement selon les résultats. Les équipes CSM sont formées à la lecture du dashboard et à l'interprétation des scores SHAP.

---

### 4.4 Bilan des agents IA sur les 4 sprints

| Sprint | Agent | Rôle | Bilan |
|---|---|---|---|
| Sprint 1 | data-explorer.md | Exploration des CSV | Efficace pour la découverte initiale |
| Sprint 2 | data-engineer.md | Nettoyage et feature engineering | Bon résultat, interventions manuelles sur les types |
| Sprint 3 | model-trainer.md | Entraînement et évaluation des modèles | Performant, SHAP nécessite ajustement manuel |
| Sprint 4 | agent-deploiement.md | Segmentation et dashboard | Génération rapide du code Streamlit |

**Ce qui a bien fonctionné :** La décomposition en agents spécialisés par sprint. Chaque agent a un périmètre clair et des instructions précises.

**Ce qui a nécessité des interventions manuelles :** La gestion des conflits de merge Git, l'ajustement des hyperparamètres du modèle, et la personnalisation des visualisations SHAP.

---

### 4.5 Limites et perspectives

**Limites du modèle :**
- Le modèle est entraîné sur des données historiques : il ne capture pas les changements récents du marché
- Biais potentiel par industrie et par plan tarifaire (Enterprise mieux représentés)
- Le score de churn est une probabilité, pas une certitude : l'humain reste dans la boucle (Art. 22 RGPD)
- Performance dégradée sur les nouveaux comptes (moins de 3 mois d'historique)

**Perspectives d'amélioration :**
- Réentraînement mensuel automatique avec les nouvelles données
- Intégration de signaux temps réel (connexions, tickets ouverts)
- Modèle séparé par segment (Starter / Growth / Enterprise)
- Alertes automatisées via n8n pour les comptes qui passent en risque élevé