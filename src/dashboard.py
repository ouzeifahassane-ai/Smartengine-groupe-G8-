import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration de la page
st.set_page_config(page_title="smartEngine - Dashboard CSM", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    priorisation_path = 'outputs/priorisation.csv'
    analytics_path = 'data/processed/analytics.csv'
    
    df_prior = pd.read_csv(priorisation_path)
    
    # On tente de charger analytics pour les features détaillées
    if os.path.exists(analytics_path):
        df_analytics = pd.read_csv(analytics_path)
    else:
        df_analytics = None
        
    return df_prior, df_analytics

df_prior, df_analytics = load_data()

# --- BARRE LATÉRALE ---
st.sidebar.title("smartEngine 🚀")
st.sidebar.markdown("Système de prédiction de churn")
view = st.sidebar.radio("Navigation", ["Portefeuille", "Priorisation", "Fiche compte"])

st.sidebar.divider()
st.sidebar.info(f"Dernière mise à jour : {pd.Timestamp.now().strftime('%d/%m/%Y')}")

# --- VUE 1 : PORTEFEUILLE ---
if view == "Portefeuille":
    st.title("📊 Vue Portefeuille")
    
    # Métriques clés
    col1, col2, col3 = st.columns(3)
    
    total_accounts = len(df_prior)
    high_risk_pct = (df_prior['risk_level'] == 'high').mean() * 100
    mrr_at_risk = df_prior[df_prior['risk_level'] == 'high']['mrr'].sum()
    
    col1.metric("Nombre total de comptes", total_accounts)
    col2.metric("Taux de risque élevé", f"{high_risk_pct:.1f}%", delta_color="inverse")
    col3.metric("MRR à risque (High Risk)", f"{mrr_at_risk:,.0f} €")
    
    st.divider()
    
    # Graphiques
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Distribution des scores de churn")
        fig_hist = px.histogram(df_prior, x="churn_score", 
                                color="risk_level",
                                color_discrete_map={'low': 'green', 'medium': 'orange', 'high': 'red'},
                                nbins=20,
                                labels={'churn_score': 'Score de churn', 'count': 'Nombre de comptes'})
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_right:
        st.subheader("Répartition par quadrant")
        fig_pie = px.pie(df_prior, names="quadrant",
                         color="quadrant",
                         color_discrete_map={
                             'Priorité maximale': '#D32F2F', 
                             'Action automatisée': '#FF5722',
                             'Fidéliser': '#1976D2',
                             'Aucune action': '#9E9E9E'
                         })
        st.plotly_chart(fig_pie, use_container_width=True)

# --- VUE 2 : PRIORISATION ---
elif view == "Priorisation":
    st.title("🎯 Priorisation des actions")
    
    st.subheader("Matrice Risque / Valeur")
    fig_scatter = px.scatter(df_prior, x="churn_score", y="mrr",
                             color="quadrant",
                             hover_name="account_id",
                             size="mrr",
                             color_discrete_map={
                                 'Priorité maximale': '#D32F2F', 
                                 'Action automatisée': '#FF5722',
                                 'Fidéliser': '#1976D2',
                                 'Aucune action': '#9E9E9E'
                             },
                             labels={'churn_score': 'Score de Churn', 'mrr': 'MRR (€)'})
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.divider()
    
    st.subheader("Tableau de bord opérationnel")
    
    # Filtres
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_quadrant = st.multiselect("Filtrer par Quadrant", options=df_prior['quadrant'].unique())
    with f_col2:
        selected_risk = st.multiselect("Filtrer par Niveau de risque", options=df_prior['risk_level'].unique())
    
    # Application des filtres
    df_filtered = df_prior.copy()
    if selected_quadrant:
        df_filtered = df_filtered[df_filtered['quadrant'].isin(selected_quadrant)]
    if selected_risk:
        df_filtered = df_filtered[df_filtered['risk_level'].isin(selected_risk)]
        
    # Tri par score décroissant
    df_filtered = df_filtered.sort_values(by="churn_score", ascending=False)
    
    st.dataframe(df_filtered, use_container_width=True)

# --- VUE 3 : FICHE COMPTE ---
elif view == "Fiche compte":
    st.title("👤 Fiche compte détaillée")
    
    account_id = st.selectbox("Sélectionner un compte (ID)", options=df_prior['account_id'].unique())
    
    if account_id:
        # Données de base
        acc_info = df_prior[df_prior['account_id'] == account_id].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score de Churn", f"{acc_info['churn_score']:.2f}")
            st.write(f"**Niveau de risque :** {acc_info['risk_level'].upper()}")
        with col2:
            st.metric("Valeur (MRR)", f"{acc_info['mrr']:,.0f} €")
            st.write(f"**Quadrant :** {acc_info['quadrant']}")
        with col3:
            st.success(f"**Action recommandée :**\n\n{acc_info['action_recommandee']}")
            
        st.divider()
        
        st.subheader("Signaux précurseurs (Features clés)")
        
        if df_analytics is not None:
            # On récupère les features pour ce compte
            acc_features = df_analytics[df_analytics['account_id'] == account_id]
            
            if not acc_features.empty:
                # Top features identifiées lors de l'entraînement
                # error_rate, avg_resolution_hours, account_age_days
                top_features = {
                    'error_rate': "Taux d'erreur rencontré",
                    'avg_resolution_hours': "Délai moyen de résolution (heures)",
                    'account_age_days': "Ancienneté du compte (jours)"
                }
                
                feat_cols = st.columns(3)
                for i, (col_name, label) in enumerate(top_features.items()):
                    if col_name in acc_features.columns:
                        val = acc_features.iloc[0][col_name]
                        # Formatage selon le type
                        if isinstance(val, float):
                            val_str = f"{val:.2f}"
                        else:
                            val_str = str(val)
                        feat_cols[i].metric(label, val_str)
            else:
                st.warning("Détails analytiques non disponibles pour ce compte.")
        else:
            st.warning("Le fichier analytics.csv est introuvable pour afficher les features détaillées.")
