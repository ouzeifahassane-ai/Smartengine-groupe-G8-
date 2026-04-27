# Rapport de Performance du Modèle de Churn

## Distribution de la variable cible (Test Set)
- Non-churn : 78
- Churn : 22

## Comparaison des Modèles
| Modèle | AUC-ROC | Precision | Recall | F1-Score |
|--------|---------|-----------|--------|----------|
| Logistic Regression | 0.6964 | 0.2955 | 0.5909 | 0.3939 |
| Random Forest | 0.6638 | 0.0000 | 0.0000 | 0.0000 |

**Modèle retenu : Logistic Regression**

## Stratégie
- Split : 80% Entraînement / 20% Test
- Gestion du déséquilibre : `class_weight='balanced'`
- Prétraitement : StandardScaler pour le numérique, OneHotEncoder pour le catégoriel.
