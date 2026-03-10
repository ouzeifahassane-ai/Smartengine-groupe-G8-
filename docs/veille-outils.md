# Veille Technologique : Outils du Projet SmartEngine

Ce document présente les outils retenus pour le développement de la plateforme **SmartEngine**, une solution d'analyse et de prédiction du churn.

---

## 1. Gemini CLI
**Présentation :** Interface en ligne de commande (CLI) propulsée par l'intelligence artificielle générative de Google. Elle permet d'interagir avec le code, d'automatiser des tâches et d'analyser des datasets via un agent conversationnel expert en ingénierie logicielle.

*   **Rôle dans le projet :** Assistant de développement principal, aide à l'exploration des données, à la génération de scripts d'analyse et à la gestion du cycle de vie du projet (Git, documentation).
*   **Avantages :** Gain de temps sur les tâches répétitives, compréhension contextuelle du codebase, intégration directe dans le terminal.
*   **Limites :** Dépendance à une connexion internet, risque de hallucinations sur des bibliothèques très récentes ou spécifiques.
*   **Alternatives :** GitHub Copilot CLI, Aider, OpenDevin.
*   *Source : Documentation officielle Google Cloud AI.*

---

## 2. Python / pandas
**Présentation :** Langage de programmation polyvalent et sa bibliothèque phare pour la manipulation et l'analyse de données structurées.

*   **Rôle dans le projet :** Nettoyage des données (ETL), ingénierie des caractéristiques (feature engineering) et analyse exploratoire des fichiers CSV de `data/raw`.
*   **Avantages :** Écosystème mature, manipulation performante de gros volumes de données avec les DataFrames, syntaxe lisible.
*   **Limites :** Consommation mémoire élevée pour les très grands datasets (plusieurs Go), exécution monothread par défaut.
*   **Alternatives :** Polars, Dask, Apache Spark (PySpark).
*   *Source : pandas.pydata.org.*

---

## 3. scikit-learn
**Présentation :** Bibliothèque Python de référence pour l'apprentissage automatique (Machine Learning).

*   **Rôle dans le projet :** Modélisation du churn via des algorithmes de classification (Random Forest, Logistic Regression), évaluation des modèles (Précision, Rappel, Score F1).
*   **Avantages :** Interface unifiée, vaste documentation, outils intégrés pour le prétraitement et la validation croisée.
*   **Limites :** Pas optimisé pour le Deep Learning ou les réseaux de neurones complexes.
*   **Alternatives :** XGBoost, LightGBM, CatBoost.
*   *Source : scikit-learn.org.*

---

## 4. Streamlit
**Présentation :** Framework open-source permettant de créer des applications web interactives pour la science des données en pur Python.

*   **Rôle dans le projet :** Création du tableau de bord (Dashboard) utilisateur pour visualiser les prédictions de churn et les indicateurs clés (KPIs) en temps réel.
*   **Avantages :** Aucun besoin de compétences en Front-end (HTML/CSS/JS), déploiement ultra-rapide, widgets interactifs natifs.
*   **Limites :** Personnalisation du design plus limitée qu'une application React/Vue sur mesure.
*   **Alternatives :** Dash (Plotly), Gradio, Shiny (Python).
*   *Source : streamlit.io.*

---

## 5. n8n
**Présentation :** Outil d'automatisation de workflow (iPaaS) "low-code" et auto-hébergeable.

*   **Rôle dans le projet :** Orchestration des flux de données entre les différentes sources (CRM, support) et déclenchement d'alertes automatiques lorsqu'un client est détecté à haut risque de churn.
*   **Avantages :** No-code/Low-code, plus de 200 intégrations natives, contrôle total sur l'hébergement des données.
*   **Limites :** Courbe d'apprentissage pour les workflows complexes, nécessite un serveur pour l'auto-hébergement.
*   **Alternatives :** Zapier, Make (Integromat), Apache Airflow.
*   *Source : n8n.io.*

---

## 6. GitHub
**Présentation :** Plateforme d'hébergement de code source utilisant le système de versionnage Git.

*   **Rôle dans le projet :** Gestion du versionnage du code, collaboration d'équipe (Pull Requests), suivi des tâches (Issues) et déploiement continu via GitHub Actions.
*   **Avantages :** Standard de l'industrie, robustesse, intégration avec de nombreux outils tiers (CI/CD, sécurité).
*   **Limites :** Les dépôts privés peuvent devenir coûteux pour les grandes organisations (hors plan gratuit).
*   **Alternatives :** GitLab, Bitbucket, Azure DevOps.
*   *Source : github.com.*

---
*Document généré par Gemini CLI - 10 Mars 2026*
