1. Ce que dit le modèle
En langage simple
Sur les 500 comptes actifs de RavenStack, notre modèle de prédiction identifie que 37,4 % d'entre eux présentent un risque élevé de résiliation dans les prochaines semaines.
Cela représente 187 comptes dont le comportement ressemble à celui de clients qui ont churné par le passé : baisse d'usage des fonctionnalités, ouverture de tickets support, ancienneté courte, ou plan inadapté à leurs besoins.
Fiabilité du modèle
Le modèle a été évalué avec une AUC-ROC de 0,6428. Concrètement, cela signifie qu'il est capable de distinguer un compte à risque d'un compte stable dans environ 64 cas sur 100 — ce qui est significativement mieux qu'un tirage au hasard (50/50), mais pas parfait.

⚠️ Important : le score de churn est une aide à la décision, pas une certitude. Il ne doit jamais déclencher une action de manière automatique sans validation humaine (Article 22 du RGPD). Un Customer Success Manager doit toujours valider avant d'agir.

Ce qui caractérise les comptes à risque
Les facteurs qui contribuent le plus au risque de churn sont visibles pour chaque compte dans le dashboard (via les explications SHAP). De manière générale, les profils à risque présentent :

Une utilisation des fonctionnalités en baisse sur les 30 derniers jours
Un nombre élevé de tickets support non résolus
Une ancienneté inférieure à 6 mois (période critique d'onboarding)
Un plan Starter avec un usage proche des limites


2. Actions recommandées par quadrant
La segmentation croise deux dimensions : le risque de churn (score du modèle) et la valeur du compte (MRR). Le seuil de valeur est fixé à la médiane du MRR : 1 923 €/mois.
Vue d'ensemble du portefeuille
QuadrantNombre de comptesAction🔴 Risque élevé + Valeur élevée86 comptesAppel CSM sous 24h🟠 Risque élevé + Valeur faible101 comptesEmail automatisé de rétention🟡 Risque faible + Valeur élevée164 comptesSurveillance + fidélisation🟢 Risque faible + Valeur faible149 comptesAucune action prioritaire

🔴 Quadrant 1 — Risque élevé / Valeur élevée (86 comptes)
Priorité maximale
Ce sont les comptes les plus dangereux à perdre. Leur MRR est supérieur à 1 923 €/mois et leur probabilité de churn est élevée.
Action recommandée : appel téléphonique du CSM dans les 24 heures

Identifier les 3 principaux facteurs de risque via le dashboard (explication SHAP)
Préparer une offre de valeur personnalisée avant l'appel
Proposer si nécessaire : formation complémentaire, upgrade de plan, remise exceptionnelle
Documenter l'issue de l'appel dans le CRM


🟠 Quadrant 2 — Risque élevé / Valeur faible (101 comptes)
Action automatisée
Ces comptes sont en danger mais leur MRR individuel ne justifie pas un appel humain systématique.
Action recommandée : séquence email automatisée

Email J+0 : rappel des fonctionnalités clés non utilisées
Email J+3 : proposition d'une session d'onboarding en ligne
Email J+7 : offre limitée dans le temps (ex. 1 mois offert sur upgrade)
Si pas de réaction après J+7 : escalade vers le CSM pour les comptes au seuil de la médiane


🟡 Quadrant 3 — Risque faible / Valeur élevée (164 comptes)
Fidélisation et surveillance
Ces comptes sont stables aujourd'hui mais stratégiquement importants. Ils ne doivent pas être négligés.
Action recommandée : programme de fidélisation proactif

Check-in trimestriel du CSM (appel de santé, pas de vente)
Invitation aux bêtas de nouvelles fonctionnalités
Mise en avant des success stories et du ROI obtenu
Alerte automatique si leur score de churn dépasse le seuil à risque


🟢 Quadrant 4 — Risque faible / Valeur faible (149 comptes)
Aucune action prioritaire
Ces comptes sont stables et leur impact financier est limité. Toute action serait un coût disproportionné.
Action recommandée : communication standard (newsletter, release notes)

Aucune intervention humaine dédiée
Réactivation si le score de churn évolue défavorablement


3. ROI estimé
MRR actuellement à risque
Le MRR total des comptes à risque élevé (Quadrants 1 et 2) représente :

370 913 € de MRR mensuel exposé au churn

Si ces comptes résiliaient tous, la perte annuelle serait de l'ordre de 4,45 M€ de ARR.
Estimation des gains selon le taux de rétention
ScénarioTaux de rétention obtenuMRR sauvé / moisARR sauvéPessimiste15%~55 637 €~667 K€Réaliste25%~92 728 €~1,11 M€Optimiste40%~148 365 €~1,78 M€
Coût estimé des actions
ActionVolumeCoût unitaire estiméCoût totalAppels CSM (Q1)86 comptes~45 min CSM = ~30 €~2 580 €Emails automatisés (Q2)101 comptes~2 € (outil + contenu)~202 €Programme fidélisation (Q3)164 comptes~15 € / trimestre~2 460 € / trim.Total actions~5 242 €
Ratio ROI (scénario réaliste)

Pour ~5 200 € investis → ~92 700 € de MRR sauvé par mois
Soit un ROI estimé de x17 dès le premier mois d'actions.

Ces estimations sont basées sur des benchmarks sectoriels SaaS B2B. Elles seront affinées lors de la phase pilote.

4. Feuille de route de déploiement
Phase 1 — Pilote (Semaines 1 à 4)
Périmètre : Quadrant 1 uniquement (86 comptes prioritaires)

Semaine 1 : briefing des CSMs, accès au dashboard, formation de 30 min
Semaines 2-3 : appels de rétention sur les 86 comptes
Semaine 4 : premier bilan — taux de contact, retours qualitatifs, premiers résultats

Objectif du pilote : valider que le modèle identifie bien les comptes réellement à risque, et que l'action CSM crée un effet mesurable.
Phase 2 — Élargissement (Semaines 5 à 8)
Périmètre : Quadrants 1 + 2

Déploiement de la séquence email automatisée pour le Quadrant 2
Ajustement des actions Q1 selon les retours du pilote
Activation des alertes automatiques pour le Quadrant 3

Phase 3 — Opérationnalisation (À partir de la semaine 9)
Périmètre : l'ensemble du portefeuille

Le dashboard devient l'outil de référence pour les CSMs
Le modèle est re-scoré chaque semaine sur les nouvelles données
Bilan mensuel présenté à la direction avec les KPIs de rétention


5. Protocole de mesure d'impact
Pourquoi mesurer ?
Prédire le churn ne prouve pas qu'on sait le réduire. Sans mesure rigoureuse, impossible de savoir si les actions de rétention fonctionnent — ou si les comptes seraient restés d'eux-mêmes.
Dispositif : test A/B avec groupe témoin
Pour le Quadrant 2 (emails automatisés) :
Les 101 comptes du Quadrant 2 sont répartis aléatoirement en deux groupes :
GroupeTailleCe qu'ils reçoiventGroupe traité~50 comptesSéquence email de rétentionGroupe témoin~51 comptesAucune action (communication standard)
Après 4 semaines, on compare le taux de rétention des deux groupes.
Mesure de l'uplift

Uplift = Taux de rétention groupe traité − Taux de rétention groupe témoin

Si le groupe traité retient 70% des comptes et le groupe témoin 55%, l'uplift est de +15 points. C'est la preuve que l'action crée de la valeur — indépendamment de la performance du modèle.
Indicateurs de réussite (KPIs)
IndicateurCible à 8 semainesTaux de rétention Q1 (appels CSM)≥ 70%Taux de rétention Q2 groupe traité≥ 60%Uplift Q2 vs groupe témoin≥ +10 pointsMRR sauvé cumulé≥ 50 000 €Coût par compte retenu≤ 150 €
Bilan et ajustement
Un bilan est présenté à la direction à la fin de la Phase 1 (semaine 4) et à la fin de la Phase 2 (semaine 8). Si l'uplift est insuffisant, les actions sont ajustées avant l'opérationnalisation.

6. Limites et précautions

Le modèle n'est pas parfait (AUC 0,6428) : certains comptes identifiés comme à risque resteront, d'autres non identifiés partiront. Le jugement humain reste indispensable.
Le score ne remplace pas la relation client : un appel CSM de qualité vaut plus qu'un score élevé.
RGPD : conformément à l'article 22, aucune décision automatisée ne peut être prise sur la seule base du score. Chaque action significative (résiliation, offre commerciale) doit être validée par un humain.
Évolution des données : le modèle doit être ré-entraîné régulièrement (recommandé : tous les trimestres) pour rester pertinent.
