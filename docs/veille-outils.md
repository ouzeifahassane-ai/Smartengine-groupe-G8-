# Rapport de veille outils — Projet smartEngine

> Sprint 1 · MSc2 Manager Data Marketing · INSEEC Lyon  
> Préparé par : [Toute l'équipe]  
> Date : Mars 2026

---

## 1. Gemini CLI

### Présentation
Gemini CLI est un outil en ligne de commande développé par Google permettant d'interagir avec un agent IA (Gemini) directement depuis le terminal. Il est capable de lire, créer et modifier des fichiers de manière autonome en suivant des instructions rédigées en langage naturel.

### Rôle dans le projet
Gemini CLI est l'outil central d'orchestration du projet. Il lit le fichier `GEMINI.md` à chaque démarrage (contexte permanent) et exécute les agents spécialisés rédigés par l'équipe. Il génère le code Python, l'exécute et produit les rapports. L'équipe dirige les agents sans coder directement.

### Avantages
- Pas besoin de compétences avancées en Python pour piloter les analyses
- Mémoire de contexte persistante via `GEMINI.md`
- Agents réutilisables et partageables entre membres de l'équipe
- Intégration native avec le système de fichiers (lecture/écriture automatique)
- Modèle Gemini puissant, adapté aux tâches de data analysis

### Limites
- Pas de mémoire entre deux sessions (compense par `GEMINI.md`)
- Dépend d'une connexion internet et d'un compte Google
- Les résultats des agents doivent être systématiquement vérifiés par l'équipe
- Moins adapté aux projets nécessitant un contrôle très fin du code généré

### Alternatives
- **Claude Code** (Anthropic) : outil similaire, fort en raisonnement et en génération de code
- **GitHub Copilot CLI** : intégration GitHub native, orienté code
- **LangChain + Python** : orchestration d'agents plus flexible mais requiert du code

### Sources
- Documentation officielle : https://geminicli.com/docs/
- Sous-agents Gemini CLI : https://geminicli.com/docs/core/subagents/

---

## 2. Python / pandas

### Présentation
Python est un langage de programmation open source, généraliste et particulièrement dominant dans l'écosystème data science. pandas est une bibliothèque Python spécialisée dans la manipulation et l'analyse de données tabulaires (DataFrames).

### Rôle dans le projet
Python est le langage de base de tous les scripts générés par les agents. pandas est utilisé pour charger les CSV, nettoyer les données, réaliser des jointures entre fichiers et préparer les features du modèle de prédiction de churn.

### Avantages
- Langage le plus utilisé en data science (vaste communauté, nombreux tutoriels)
- pandas : manipulation intuitive de DataFrames, lecture native des CSV
- Écosystème très riche : compatible scikit-learn, matplotlib, Streamlit
- Gratuit et open source
- Facile à intégrer dans des workflows automatisés

### Limites
- pandas n'est pas adapté aux très grands volumes de données (>10 Go en mémoire)
- Courbe d'apprentissage initiale pour les opérations avancées (groupby, merge, pivot)
- Gestion manuelle du typage des colonnes parfois nécessaire

### Alternatives
- **Polars** : alternative à pandas, beaucoup plus rapide sur les grands volumes
- **R / dplyr** : langage statistique, fort en analyse exploratoire
- **SQL + DuckDB** : requêtes SQL directement sur des fichiers CSV

### Sources
- Documentation pandas : https://pandas.pydata.org/docs/
- Python officiel : https://www.python.org/

---

## 3. scikit-learn

### Présentation
scikit-learn est la bibliothèque Python de référence pour le machine learning supervisé et non supervisé. Elle propose des algorithmes de classification, régression, clustering, ainsi que des outils de prétraitement, de validation croisée et d'évaluation des modèles.

### Rôle dans le projet
scikit-learn est utilisé pour construire le modèle de scoring prédictif du churn. Il permettra d'entraîner des algorithmes de classification (ex : Random Forest, Logistic Regression, XGBoost) sur les données RavenStack et d'évaluer leurs performances (AUC-ROC, précision, rappel).

### Avantages
- API unifiée et cohérente (fit / predict / score) pour tous les algorithmes
- Outils complets de prétraitement (StandardScaler, OneHotEncoder, Pipeline)
- Validation croisée et tuning des hyperparamètres intégrés
- Excellente documentation avec exemples concrets
- Intégration naturelle avec pandas et matplotlib

### Limites
- Moins adapté au deep learning (préférer TensorFlow ou PyTorch pour réseaux de neurones)
- Performances limitées sur très grands datasets (pas de traitement distribué natif)
- Pas d'interface graphique intégrée pour l'exploration des modèles

### Alternatives
- **XGBoost / LightGBM** : algorithmes de gradient boosting très performants, compatibles scikit-learn
- **TensorFlow / PyTorch** : deep learning
- **H2O AutoML** : automatisation complète du processus de modélisation

### Sources
- Documentation officielle : https://scikit-learn.org/stable/
- Guide débutant : https://scikit-learn.org/stable/getting_started.html

---

## 4. Streamlit

### Présentation
Streamlit est un framework Python open source permettant de créer des applications web interactives et des dashboards à partir de scripts Python, sans écrire de HTML, CSS ou JavaScript.

### Rôle dans le projet
Streamlit est utilisé pour déployer le dashboard interactif à destination des équipes Customer Success de RavenStack. Ce dashboard affichera les scores de churn par compte, les alertes, les visualisations de l'utilisation des fonctionnalités et les recommandations d'actions.

### Avantages
- Développement très rapide : un script Python devient une appli web en quelques lignes
- Composants interactifs natifs (sliders, filtres, graphiques dynamiques)
- Intégration directe avec pandas, matplotlib, plotly
- Déploiement facile via Streamlit Cloud (gratuit pour projets publics)
- Pas de connaissance en développement web requise

### Limites
- Moins adapté aux applications web complexes ou très personnalisées
- Performances limitées avec des très grands datasets chargés en mémoire
- Moins de contrôle sur le design et l'UX qu'une application React/Vue
- Le rechargement complet de la page à chaque interaction peut être gênant

### Alternatives
- **Dash (Plotly)** : plus flexible mais plus complexe
- **Power BI / Tableau** : outils BI no-code, mais moins intégrables dans un workflow Python
- **Gradio** : orienté démos de modèles ML

### Sources
- Documentation officielle : https://docs.streamlit.io/
- Galerie d'exemples : https://streamlit.io/gallery

---

## 5. n8n

### Présentation
n8n est un outil d'automatisation de workflows open source et auto-hébergeable. Il permet de connecter des applications, des APIs et des services via une interface visuelle no-code/low-code, en créant des flux déclenchés par des événements.

### Rôle dans le projet
n8n est utilisé pour automatiser les alertes envoyées aux équipes Customer Success lorsqu'un compte dépasse un seuil de score de churn critique. Il orchestrera les flux entre le modèle de scoring, les outils de communication (email, Slack) et éventuellement le CRM de RavenStack.

### Avantages
- Open source et auto-hébergeable (maîtrise des données, conformité RGPD)
- Interface visuelle intuitive (no-code pour les workflows simples)
- Plus de 400 intégrations natives (Slack, email, HTTP, bases de données)
- Nœuds de code Python/JavaScript pour les logiques personnalisées
- Déclencheurs variés : webhook, cron, événement API

### Limites
- Requiert un serveur pour l'auto-hébergement (configuration technique initiale)
- Moins mature que Zapier ou Make pour certaines intégrations complexes
- Documentation parfois incomplète pour les cas d'usage avancés
- Scalabilité limitée en version community sur des volumes très élevés

### Alternatives
- **Zapier** : très populaire, mais payant et hébergé (moins adapté RGPD)
- **Make (ex-Integromat)** : bonne alternative visuelle, aussi hébergé
- **Apache Airflow** : orchestration de pipelines data, plus technique

### Sources
- Site officiel : https://n8n.io/
- Documentation : https://docs.n8n.io/

---

## 6. GitHub

### Présentation
GitHub est une plateforme de gestion de code source et de collaboration basée sur Git, le système de contrôle de version distribué. GitHub permet le versionning du code, la gestion de branches, les pull requests et la collaboration asynchrone entre développeurs.

### Rôle dans le projet
GitHub est le dépôt central du projet smartEngine. Il héberge l'ensemble du code, des agents, des rapports et du dossier de conception. Il garantit la traçabilité des contributions de chaque membre et permet de travailler en parallèle via un système de branches.

### Avantages
- Versionning complet : chaque modification est tracée avec auteur, date et message
- Branches isolées : chaque membre travaille sans bloquer les autres
- GitHub Projects intégré pour le suivi du backlog Scrum
- Actions GitHub : intégration continue (CI/CD) possible
- Gratuit pour les dépôts privés (jusqu'à une certaine limite de collaborateurs)

### Limites
- Courbe d'apprentissage initiale pour les commandes Git (clone, merge, rebase)
- Conflits de merge à gérer lors de modifications simultanées du même fichier
- Pas adapté au versionnage de fichiers volumineux (>100 Mo) sans Git LFS
- Interface parfois complexe pour les débutants

### Alternatives
- **GitLab** : alternative open source et auto-hébergeable, fonctionnalités CI/CD avancées
- **Bitbucket** : intégration native avec Jira, orienté entreprise
- **Notion** : pour la documentation uniquement, sans versionning de code

### Sources
- Introduction à Git et GitHub : https://docs.github.com/fr/get-started
- Git branches (documentation officielle) : https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Les-branches-en-bref

---

*Rapport rédigé dans le cadre du Sprint 1 du projet smartEngine — INSEEC MSc2 Manager Data Marketing*
