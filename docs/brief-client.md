# Brief client — Projet smartEngine

> Sprint 1 · MSc2 Manager Data Marketing · INSEEC Lyon  
> Rédigé par : Etya'alé [Product Owner]  
> Date : Mars 2026

---

## 1. Le client : RavenStack

RavenStack est une entreprise française éditrice de logiciels vendus sous forme d'abonnement (modèle SaaS — Software as a Service). Sa plateforme s'adresse exclusivement à des entreprises clientes (modèle B2B), plus précisément aux équipes techniques (développeurs, chefs de projets tech) qui ont besoin d'un outil de gestion de projets centralisé.

RavenStack propose trois niveaux d'offre adaptés à la taille et aux besoins de ses clients :
- **Starter** : pour les petites équipes
- **Growth** : pour les équipes en croissance
- **Enterprise** : pour les grandes organisations

Son modèle économique repose entièrement sur les **abonnements récurrents** : chaque client paie un montant mensuel ou annuel. La santé financière de RavenStack dépend donc directement de sa capacité à conserver ses clients d'un mois à l'autre.

---

## 2. Le problème : le churn menace les revenus récurrents

Chaque mois, une partie des clients de RavenStack **résilie son abonnement**. Ce phénomène s'appelle le **churn** (ou attrition client). C'est l'une des menaces principales pour les entreprises SaaS : perdre un client ne génère pas seulement une perte ponctuelle, mais une perte de revenus qui se répète chaque mois indéfiniment.

Le churn impacte directement le **MRR (Monthly Recurring Revenue)** — l'indicateur central de santé financière d'un SaaS — de deux façons : il réduit les revenus existants et il force l'entreprise à dépenser davantage en acquisition pour compenser les clients perdus. Dans le secteur SaaS B2B, acquérir un nouveau client coûte en moyenne 5 à 7 fois plus cher que de conserver un client existant.

Le problème central est l'**absence d'anticipation** : aujourd'hui, RavenStack découvre qu'un client churne au moment où il résilie, sans avoir pu intervenir en amont. Les équipes Customer Success (les collaborateurs chargés de la satisfaction et de la rétention client) n'ont aucune visibilité sur les comptes à risque avant qu'il soit trop tard.

---

## 3. La solution attendue : smartEngine

RavenStack nous mandate pour concevoir **smartEngine**, un système intelligent de prédiction du churn. L'objectif est de détecter, avant la résiliation, les signaux faibles qui indiquent qu'un client risque de partir — et de permettre aux équipes Customer Success d'intervenir proactivement.

smartEngine couvrira l'ensemble de la chaîne de valeur data :

1. **Analyse et nettoyage des données** : exploitation des 5 fichiers de données fournis (comptes, abonnements, usage des fonctionnalités, tickets support, événements de résiliation)
2. **Identification des signaux précurseurs** : quelles variables comportementales sont corrélées avec le churn ? (baisse d'utilisation, hausse des tickets, modification du plan, etc.)
3. **Modèle de scoring prédictif** : attribution d'un score de risque de churn (0 à 100) à chaque compte client
4. **Dashboard interactif** : interface Streamlit à destination des équipes Customer Success pour visualiser les scores et identifier les comptes prioritaires
5. **Alertes automatisées** : via n8n, notification automatique des équipes lorsqu'un compte passe au-dessus d'un seuil critique

---

## 4. Périmètre et contraintes

### Périmètre inclus
- Analyse des données des ~5 000 comptes RavenStack
- Prédiction binaire : churn / non-churn dans les 30 prochains jours
- Dashboard à usage interne (équipes Customer Success uniquement)

### Contraintes réglementaires
- Les données clients sont soumises au **RGPD** (Règlement Général sur la Protection des Données)
- L'article 22 du RGPD encadre les décisions automatisées et le profilage : le score de churn, s'il conditionne des actions commerciales, doit être documenté et explicable
- Principe de **minimisation des données** : seules les variables nécessaires à la prédiction sont utilisées
- La **loi Informatique et Libertés** (France) complète le RGPD avec des obligations spécifiques sur le territoire national

### Stack technique imposée
Gemini CLI · Python / pandas · scikit-learn · Streamlit · n8n · GitHub

---

## 5. Critères de succès

| # | Critère | Mesure |
|---|---|---|
| 1 | **Performance du modèle** | AUC-ROC ≥ 0,80 sur le jeu de test |
| 2 | **Couverture des comptes à risque** | Recall (sensibilité) ≥ 70 % : le modèle identifie au moins 7 clients churners sur 10 |
| 3 | **Délai d'anticipation** | Le score prédit le churn avec au moins 30 jours d'avance |
| 4 | **Adoption par les équipes** | Le dashboard est opérationnel et utilisable sans formation technique |
| 5 | **Conformité RGPD** | Chaque variable utilisée dans le modèle est justifiée et documentée dans le dossier de conception |
| 6 | **Automatisation des alertes** | Les comptes dépassant le seuil critique déclenchent une notification dans les 24h via n8n |

---

*Brief rédigé dans le cadre du Sprint 1 du projet smartEngine — INSEEC MSc2 Manager Data Marketing*
