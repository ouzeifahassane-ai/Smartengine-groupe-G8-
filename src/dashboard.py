import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px

st.set_page_config(page_title="SmartEngine - Churn Dashboard", layout="wide")

st.title("📊 SmartEngine : Dashboard de Prédiction du Churn")
st.markdown("---")

# Load data and model
@st.cache_resource
def load_assets():
    model = joblib.load('outputs/model/best_churn_model.joblib')
    df = pd.read_csv('outputs/dataset_final.csv')
    return model, df

try:
    model, df = load_assets()
    
    # Sidebar filters
    st.sidebar.header("Filtres")
    industries = ['Tous'] + sorted(df['industry'].unique().tolist())
    selected_industry = st.sidebar.selectbox("Secteur d'activité", industries)
    
    # Filter data
    filtered_df = df.copy()
    if selected_industry != 'Tous':
        filtered_df = filtered_df[filtered_df['industry'] == selected_industry]
        
    # Predictions
    # Prepare features for prediction (same as in model_trainer.py)
    X = filtered_df.drop(columns=['account_id', 'account_name', 'signup_date', 'churn_flag'])
    # Handle categorical columns manually for consistency with training
    # We need all columns from training set to be present
    # Re-run dummy encoding on FULL dataset first to get all columns
    full_X = df.drop(columns=['account_id', 'account_name', 'signup_date', 'churn_flag'])
    full_X = pd.get_dummies(full_X, drop_first=True)
    
    # Now get same columns for filtered set
    X_predict = pd.get_dummies(X, drop_first=True)
    # Align columns
    X_predict = X_predict.reindex(columns=full_X.columns, fill_value=0)
    
    # Get scores
    filtered_df['churn_probability'] = model.predict_proba(X_predict)[:, 1]
    filtered_df['churn_prediction'] = model.predict(X_predict)
    
    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de comptes", len(filtered_df))
    col2.metric("Probabilité Moyenne de Churn", f"{filtered_df['churn_probability'].mean():.2%}")
    col3.metric("Comptes à Risque (>50%)", len(filtered_df[filtered_df['churn_probability'] > 0.5]))
    
    st.markdown("---")
    
    # Top 10 High Risk Accounts
    st.subheader("🚨 Top 10 des comptes à haut risque")
    high_risk = filtered_df[['account_id', 'account_name', 'industry', 'churn_probability']].sort_values(by='churn_probability', ascending=False).head(10)
    st.dataframe(high_risk, use_container_width=True)
    
    # Feature Importance Visualization
    st.subheader("📈 Importance des Variables")
    importances = pd.Series(model.feature_importances_, index=full_X.columns).sort_values(ascending=False).head(10)
    fig = px.bar(importances, x=importances.values, y=importances.index, orientation='h', 
                 labels={'x': 'Importance Score', 'y': 'Feature'},
                 title="Top 10 des variables prédictives")
    st.plotly_chart(fig, use_container_width=True)
    
    # Churn Probability Distribution
    st.subheader("📊 Distribution de la Probabilité de Churn")
    fig_dist = px.histogram(filtered_df, x="churn_probability", nbins=20, 
                           title="Distribution des scores de churn",
                           labels={'churn_probability': 'Probabilité de Churn'})
    st.plotly_chart(fig_dist, use_container_width=True)

except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.info("Assurez-vous d'avoir exécuté model_trainer.py pour générer le modèle et le dataset final.")

