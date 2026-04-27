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
