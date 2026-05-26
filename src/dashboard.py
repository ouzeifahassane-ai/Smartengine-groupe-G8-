"""
dashboard.py — Projet smartEngine Groupe G8
Sprint 4 : Dashboard Streamlit de prédiction du churn

Exécution :
    streamlit run src/dashboard.py

Prérequis :
    - outputs/priorisation.csv  (généré par src/priorisation.py)
    - outputs/scores.csv        (généré par src/generate_scores.py)
    - outputs/models/churn_model.joblib  (optionnel pour les SHAP)
    - data/processed/analytics.csv      (optionnel pour les SHAP)

Trois vues :
    1. Portefeuille  — indicateurs globaux et distribution des scores
    2. Priorisation  — matrice risque/valeur et liste filtrable des comptes
    3. Fiche compte  — profil détaillé + explication SHAP des facteurs de risque
"""

import os
import warnings
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="smartEngine — Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette daltonisme-friendly (WCAG AA) ─────────────────────────────────────
COLORS = {
    "danger":  "#D62728",   # rouge vif
    "warning": "#FF7F0E",   # orange
    "safe":    "#2CA02C",   # vert
    "neutral": "#1F77B4",   # bleu
    "q1": "#D62728",
    "q2": "#FF7F0E",
    "q3": "#1F77B4",
    "q4": "#2CA02C",
}

QUADRANT_COLORS = {1: COLORS["q1"], 2: COLORS["q2"], 3: COLORS["q3"], 4: COLORS["q4"]}

# ── Chargement des données ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    priorisation_path = os.path.join(base, "outputs", "priorisation.csv")
    scores_path       = os.path.join(base, "outputs", "scores.csv")

    if not os.path.exists(priorisation_path):
        st.error(
            "Fichier outputs/priorisation.csv introuvable.\n\n"
            "Exécutez d'abord : `python src/priorisation.py`"
        )
        st.stop()

    df = pd.read_csv(priorisation_path)
    return df


@st.cache_resource
def load_model_and_analytics():
    base     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path    = os.path.join(base, "outputs", "models", "churn_model.joblib")
    analytics_path = os.path.join(base, "data", "processed", "analytics.csv")

    model_bundle = None
    analytics_df = None

    if os.path.exists(model_path):
        try:
            import joblib
            model_bundle = joblib.load(model_path)
        except Exception:
            pass

    if os.path.exists(analytics_path):
        try:
            analytics_df = pd.read_csv(analytics_path)
        except Exception:
            pass

    return model_bundle, analytics_df


# ── Helpers ───────────────────────────────────────────────────────────────────
def format_mrr(value: float) -> str:
    """Formate un MRR en euros lisible."""
    if value >= 1_000:
        return f"{value/1_000:.1f}k €"
    return f"{value:.0f} €"


def risk_badge(level: str) -> str:
    """Retourne un badge HTML coloré pour le niveau de risque."""
    palette = {"high": "#D62728", "medium": "#FF7F0E", "low": "#2CA02C"}
    labels  = {"high": "Risque élevé", "medium": "Risque moyen", "low": "Risque faible"}
    color   = palette.get(level, "#888888")
    label   = labels.get(level, level)
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">{label}</span>'


def quadrant_badge(q: int, label: str) -> str:
    color = QUADRANT_COLORS.get(q, "#888888")
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">Q{q} — {label}</span>'


# ── Sidebar : navigation + filtres globaux ────────────────────────────────────
def sidebar(df: pd.DataFrame):
    st.sidebar.image(
        "https://img.icons8.com/fluency/48/bar-chart.png",
        width=48
    )
    st.sidebar.title("smartEngine")
    st.sidebar.caption("Prédiction de churn — RavenStack")
    st.sidebar.divider()

    vue = st.sidebar.radio(
        "Navigation",
        ["📊 Portefeuille", "🎯 Priorisation", "🔍 Fiche compte"],
        index=0
    )

    st.sidebar.divider()
    st.sidebar.subheader("Filtres globaux")

    # Filtre plan
    plans = sorted(df["plan_tier"].dropna().unique().tolist()) if "plan_tier" in df.columns else []
    selected_plans = st.sidebar.multiselect("Plan tarifaire", plans, default=plans)

    # Filtre industry
    industries = sorted(df["industry"].dropna().unique().tolist()) if "industry" in df.columns else []
    selected_industries = st.sidebar.multiselect("Secteur", industries, default=industries)

    st.sidebar.divider()
    st.sidebar.caption(
        "ℹ️ Les scores de churn sont des *probabilités estimées*, pas des certitudes. "
        "Toute décision commerciale doit impliquer un responsable humain (Art. 22 RGPD)."
    )

    return vue, selected_plans, selected_industries


def apply_filters(df, selected_plans, selected_industries):
    mask = pd.Series([True] * len(df), index=df.index)
    if selected_plans and "plan_tier" in df.columns:
        mask &= df["plan_tier"].isin(selected_plans)
    if selected_industries and "industry" in df.columns:
        mask &= df["industry"].isin(selected_industries)
    return df[mask].copy()


# ══════════════════════════════════════════════════════════════════════════════
# VUE 1 : PORTEFEUILLE
# ══════════════════════════════════════════════════════════════════════════════
def vue_portefeuille(df: pd.DataFrame):
    st.title("📊 Vue Portefeuille")
    st.caption("Indicateurs globaux du portefeuille client RavenStack")

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_comptes = len(df)
    comptes_risque_eleve = (df["risk_level"] == "high").sum()
    taux_risque = comptes_risque_eleve / total_comptes * 100
    mrr_total = df["mrr"].sum() if "mrr" in df.columns else 0
    mrr_risque = df.loc[df["quadrant"].isin([1, 2]), "mrr"].sum() if "mrr" in df.columns else 0
    score_moyen = df["churn_score"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Comptes total", f"{total_comptes:,}")
    col2.metric("Risque élevé", f"{comptes_risque_eleve}", f"{taux_risque:.1f}%")
    col3.metric("MRR total", format_mrr(mrr_total))
    col4.metric("MRR à risque", format_mrr(mrr_risque), f"{mrr_risque/mrr_total*100:.1f}%" if mrr_total else "")
    col5.metric("Score moyen", f"{score_moyen:.2f}", help="Probabilité de churn moyenne (0 = aucun risque, 1 = certitude)")

    st.divider()

    col_left, col_right = st.columns(2)

    # ── Distribution des scores ───────────────────────────────────────────────
    with col_left:
        st.subheader("Distribution des scores de churn")
        st.caption("Un score proche de 1 indique un risque élevé de résiliation")

        fig_hist = px.histogram(
            df,
            x="churn_score",
            nbins=30,
            color="risk_level",
            color_discrete_map={
                "high": COLORS["danger"],
                "medium": COLORS["warning"],
                "low": COLORS["safe"]
            },
            category_orders={"risk_level": ["high", "medium", "low"]},
            labels={"churn_score": "Score de churn", "risk_level": "Niveau de risque", "count": "Nombre de comptes"},
            title=""
        )
        fig_hist.update_layout(
            bargap=0.05,
            legend_title_text="Niveau de risque",
            xaxis_title="Score de churn (probabilité estimée)",
            yaxis_title="Nombre de comptes",
            plot_bgcolor="white",
        )
        fig_hist.add_vrect(
            x0=0.5, x1=1.0,
            fillcolor="rgba(214, 39, 40, 0.08)",
            layer="below", line_width=0,
            annotation_text="Zone à risque",
            annotation_position="top left"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Répartition par quadrant ──────────────────────────────────────────────
    with col_right:
        st.subheader("Répartition par quadrant")
        st.caption("Croisement risque (score de churn) × valeur (MRR)")

        q_counts = df.groupby(["quadrant", "quadrant_label"]).size().reset_index(name="nb")
        q_counts["color"] = q_counts["quadrant"].map(QUADRANT_COLORS)
        q_counts["label_court"] = q_counts["quadrant"].map({
            1: "Q1 — Urgents",
            2: "Q2 — Automatiser",
            3: "Q3 — Fidéliser",
            4: "Q4 — Stables",
        })

        fig_pie = px.pie(
            q_counts,
            names="label_court",
            values="nb",
            color="label_court",
            color_discrete_map={
                "Q1 — Urgents":    COLORS["q1"],
                "Q2 — Automatiser": COLORS["q2"],
                "Q3 — Fidéliser":  COLORS["q3"],
                "Q4 — Stables":    COLORS["q4"],
            },
            hole=0.4,
        )
        fig_pie.update_traces(textposition="outside", textinfo="percent+label")
        fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # ── MRR par quadrant ──────────────────────────────────────────────────────
    st.subheader("MRR à risque par quadrant")
    if "mrr" in df.columns:
        mrr_q = df.groupby(["quadrant", "quadrant_label"])["mrr"].agg(["sum", "mean", "count"]).reset_index()
        mrr_q.columns = ["quadrant", "label", "MRR total (€)", "MRR moyen (€)", "Comptes"]
        mrr_q["label_court"] = mrr_q["quadrant"].map({
            1: "Q1 — Urgents", 2: "Q2 — Automatiser",
            3: "Q3 — Fidéliser", 4: "Q4 — Stables"
        })
        mrr_q["MRR total (€)"] = mrr_q["MRR total (€)"].round(0)
        mrr_q["MRR moyen (€)"] = mrr_q["MRR moyen (€)"].round(0)

        fig_bar = px.bar(
            mrr_q, x="label_court", y="MRR total (€)",
            color="label_court",
            color_discrete_map={
                "Q1 — Urgents":    COLORS["q1"],
                "Q2 — Automatiser": COLORS["q2"],
                "Q3 — Fidéliser":  COLORS["q3"],
                "Q4 — Stables":    COLORS["q4"],
            },
            text_auto=".3s",
            labels={"label_court": "Quadrant", "MRR total (€)": "MRR total (€/mois)"},
        )
        fig_bar.update_layout(showlegend=False, plot_bgcolor="white", xaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Légende quadrants ────────────────────────────────────────────────────
    with st.expander("Définition des quadrants"):
        st.markdown("""
| Quadrant | Profil | Action |
|----------|--------|--------|
| **Q1 — Risque élevé / Valeur élevée** | Gros comptes en danger | Appel CSM sous 48h + offre personnalisée |
| **Q2 — Risque élevé / Valeur faible** | Petits comptes en danger | Email automatisé de réengagement |
| **Q3 — Risque faible / Valeur élevée** | Gros comptes fidèles | Surveiller, programme de fidélisation |
| **Q4 — Risque faible / Valeur faible** | Petits comptes stables | Aucune action prioritaire |

*Seuil risque : score de churn ≥ 0.50 — Seuil valeur : MRR ≥ médiane du portefeuille (~1 923 €/mois)*
        """)


# ══════════════════════════════════════════════════════════════════════════════
# VUE 2 : PRIORISATION
# ══════════════════════════════════════════════════════════════════════════════
def vue_priorisation(df: pd.DataFrame):
    st.title("🎯 Vue Priorisation")
    st.caption("Matrice risque / valeur et liste des comptes à traiter en priorité")

    # ── Matrice scatter ───────────────────────────────────────────────────────
    st.subheader("Matrice risque × valeur")

    if "mrr" not in df.columns:
        st.warning("Colonne MRR absente — impossible d'afficher la matrice.")
    else:
        mrr_median = df["mrr"].median()
        risk_threshold = 0.5

        hover_cols = ["account_id", "churn_score", "risk_level", "mrr", "quadrant_label", "action"]
        for c in ["plan_tier", "industry"]:
            if c in df.columns:
                hover_cols.append(c)

        fig_scatter = px.scatter(
            df,
            x="churn_score",
            y="mrr",
            color="quadrant_label",
            color_discrete_map={
                "Risque élevé / Valeur élevée": COLORS["q1"],
                "Risque élevé / Valeur faible":  COLORS["q2"],
                "Risque faible / Valeur élevée": COLORS["q3"],
                "Risque faible / Valeur faible":  COLORS["q4"],
            },
            hover_data={c: True for c in hover_cols if c in df.columns},
            size_max=10,
            opacity=0.75,
            labels={
                "churn_score": "Score de churn (probabilité)",
                "mrr": "MRR mensuel (€)",
                "quadrant_label": "Segment",
            },
        )
        # Lignes de seuil
        fig_scatter.add_vline(
            x=risk_threshold, line_dash="dash", line_color="gray",
            annotation_text=f"Seuil risque ({risk_threshold})",
            annotation_position="top right"
        )
        fig_scatter.add_hline(
            y=mrr_median, line_dash="dash", line_color="gray",
            annotation_text=f"Médiane MRR ({mrr_median:,.0f} €)",
            annotation_position="right"
        )
        fig_scatter.update_layout(
            height=500,
            plot_bgcolor="white",
            legend_title_text="Segment",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # ── Filtres de la liste ───────────────────────────────────────────────────
    st.subheader("Liste des comptes")

    col1, col2, col3 = st.columns(3)
    with col1:
        quadrants_options = {
            "Q1 — Urgents (risque élevé / valeur élevée)": 1,
            "Q2 — Automatiser (risque élevé / valeur faible)": 2,
            "Q3 — Fidéliser (risque faible / valeur élevée)": 3,
            "Q4 — Stables (risque faible / valeur faible)": 4,
        }
        selected_q_labels = st.multiselect(
            "Quadrant",
            list(quadrants_options.keys()),
            default=["Q1 — Urgents (risque élevé / valeur élevée)", "Q2 — Automatiser (risque élevé / valeur faible)"]
        )
        selected_qs = [quadrants_options[l] for l in selected_q_labels]

    with col2:
        sort_by = st.selectbox("Trier par", ["churn_score ↓", "mrr ↓", "quadrant ↑"])

    with col3:
        search = st.text_input("Rechercher un compte (ID)")

    # Application des filtres
    filtered = df.copy()
    if selected_qs:
        filtered = filtered[filtered["quadrant"].isin(selected_qs)]
    if search:
        filtered = filtered[filtered["account_id"].str.contains(search, case=False, na=False)]

    # Tri
    sort_map = {
        "churn_score ↓": ("churn_score", False),
        "mrr ↓": ("mrr", False),
        "quadrant ↑": ("quadrant", True),
    }
    sort_col, sort_asc = sort_map[sort_by]
    filtered = filtered.sort_values(sort_col, ascending=sort_asc)

    st.caption(f"{len(filtered)} compte(s) affichés sur {len(df)} total")

    # Colonnes à afficher
    display_cols = ["account_id", "churn_score", "risk_level", "quadrant", "action"]
    if "mrr" in filtered.columns:
        display_cols.insert(3, "mrr")
    for c in ["plan_tier", "industry"]:
        if c in filtered.columns:
            display_cols.append(c)

    display_df = filtered[display_cols].copy()
    if "mrr" in display_df.columns:
        display_df["mrr"] = display_df["mrr"].round(0).astype(int)
    display_df["churn_score"] = display_df["churn_score"].round(3)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "account_id": st.column_config.TextColumn("Compte", width="small"),
            "churn_score": st.column_config.ProgressColumn(
                "Score churn", min_value=0, max_value=1, format="%.3f"
            ),
            "risk_level": st.column_config.TextColumn("Risque", width="small"),
            "mrr": st.column_config.NumberColumn("MRR (€)", format="%.0f"),
            "quadrant": st.column_config.NumberColumn("Q", width="small"),
            "action": st.column_config.TextColumn("Action recommandée", width="large"),
        }
    )


# ══════════════════════════════════════════════════════════════════════════════
# VUE 3 : FICHE COMPTE
# ══════════════════════════════════════════════════════════════════════════════
def vue_fiche_compte(df: pd.DataFrame):
    st.title("🔍 Fiche Compte")
    st.caption("Profil détaillé d'un compte, son score de churn et l'explication des facteurs de risque")

    # ── Sélection du compte ───────────────────────────────────────────────────
    compte_ids = df["account_id"].tolist()
    default_idx = 0  # Q1 par défaut (déjà trié par priorité)

    selected_id = st.selectbox(
        "Sélectionner un compte",
        compte_ids,
        index=default_idx,
        help="Les comptes sont triés par priorité décroissante (Q1 d'abord)"
    )

    compte = df[df["account_id"] == selected_id].iloc[0]

    # ── En-tête du compte ─────────────────────────────────────────────────────
    col_id, col_risk, col_q = st.columns([2, 2, 3])
    with col_id:
        st.metric("Compte", compte["account_id"])
    with col_risk:
        st.metric("Score de churn", f"{compte['churn_score']:.1%}")
        st.caption("Probabilité estimée de résiliation")
    with col_q:
        st.markdown(
            f"**Segment :** {quadrant_badge(int(compte['quadrant']), compte['quadrant_label'])}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"**Risque :** {risk_badge(compte['risk_level'])}",
            unsafe_allow_html=True
        )

    st.divider()

    # ── Profil du compte ──────────────────────────────────────────────────────
    col_profil, col_gauge = st.columns([1, 1])

    with col_profil:
        st.subheader("Profil du compte")
        profil_data = {}

        if "plan_tier" in compte.index:
            profil_data["Plan tarifaire"] = compte["plan_tier"]
        if "industry" in compte.index:
            profil_data["Secteur"] = compte["industry"]
        if "seats" in compte.index and not pd.isna(compte["seats"]):
            profil_data["Utilisateurs"] = f"{int(compte['seats'])}"
        if "mrr" in compte.index:
            profil_data["MRR mensuel"] = f"{compte['mrr']:,.0f} €"
        if "avg_sub_duration" in compte.index and not pd.isna(compte["avg_sub_duration"]):
            profil_data["Ancienneté (mois)"] = f"{compte['avg_sub_duration']:.0f}"
        if "auto_renew_rate" in compte.index and not pd.isna(compte["auto_renew_rate"]):
            profil_data["Taux renouvellement auto"] = f"{compte['auto_renew_rate']:.0%}"

        for key, val in profil_data.items():
            col_k, col_v = st.columns([2, 2])
            col_k.write(f"**{key}**")
            col_v.write(val)

    with col_gauge:
        st.subheader("Score de churn")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(compte["churn_score"]),
            number={"suffix": "", "valueformat": ".1%"},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 1], "tickformat": ".0%"},
                "bar": {"color": QUADRANT_COLORS.get(int(compte["quadrant"]), "#888")},
                "steps": [
                    {"range": [0, 0.4],  "color": "#d4edda"},
                    {"range": [0.4, 0.7], "color": "#fff3cd"},
                    {"range": [0.7, 1.0], "color": "#f8d7da"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "thickness": 0.8,
                    "value": float(compte["churn_score"])
                },
            },
            title={"text": "Probabilité de churn estimée"}
        ))
        fig_gauge.update_layout(height=280, margin=dict(t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(
            "⚠️ Ce score est une *estimation statistique*, non une certitude. "
            "Il doit guider, pas remplacer, le jugement humain."
        )

    st.divider()

    # ── Métriques d'usage et support ──────────────────────────────────────────
    st.subheader("Signaux d'usage et support")

    metrics_cols = st.columns(4)
    metric_defs = [
        ("avg_usage_count",      "Sessions/mois",      ".1f"),
        ("unique_features_used", "Fonctionnalités",    ".0f"),
        ("nb_tickets",           "Tickets support",    ".0f"),
        ("avg_satisfaction",     "Satisfaction",       ".1f"),
        ("nb_escalations",       "Escalations",        ".0f"),
        ("avg_error_rate",       "Taux d'erreurs",     ".1%"),
        ("nb_urgent_tickets",    "Tickets urgents",    ".0f"),
        ("total_usage_count",    "Usages total",       ".0f"),
    ]
    col_idx = 0
    for field, label, fmt in metric_defs:
        if field in compte.index and not pd.isna(compte[field]):
            val = compte[field]
            metrics_cols[col_idx % 4].metric(label, f"{val:{fmt}}")
            col_idx += 1

    st.divider()

    # ── Action recommandée ────────────────────────────────────────────────────
    st.subheader("Action recommandée")
    action_colors = {1: "#f8d7da", 2: "#fff3cd", 3: "#d1ecf1", 4: "#d4edda"}
    bg = action_colors.get(int(compte["quadrant"]), "#f8f9fa")
    st.markdown(
        f"""
        <div style="background:{bg};padding:16px;border-radius:8px;font-size:1.1em">
        <b>Q{int(compte['quadrant'])} — {compte['quadrant_label']}</b><br><br>
        {compte['action']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ── Explication SHAP ──────────────────────────────────────────────────────
    st.subheader("Explication du score (facteurs de risque)")
    st.caption(
        "Les facteurs ci-dessous expliquent pourquoi ce compte obtient ce score. "
        "Un facteur positif (rouge) augmente le risque de churn ; un facteur négatif (vert) le réduit."
    )

    model_bundle, analytics_df = load_model_and_analytics()

    if model_bundle is not None and analytics_df is not None:
        try:
            import shap
            model       = model_bundle["model"]
            feature_cols = model_bundle["feature_cols"]

            account_row = analytics_df[analytics_df["account_id"] == selected_id]
            if account_row.empty:
                st.info("Données analytiques introuvables pour ce compte — explication SHAP non disponible.")
            else:
                X_account = account_row[feature_cols].copy()
                for col in X_account.columns:
                    if X_account[col].isnull().any():
                        X_account[col] = X_account[col].fillna(analytics_df[col].median())

                explainer  = shap.TreeExplainer(model)
                shap_vals  = explainer.shap_values(X_account)

                # Pour les classifieurs multi-output (random forest), prendre classe 1
                if isinstance(shap_vals, list):
                    sv = shap_vals[1][0]
                else:
                    sv = shap_vals[0]

                shap_df = pd.DataFrame({
                    "feature": feature_cols,
                    "shap_value": sv,
                    "feature_value": X_account.iloc[0].values
                }).sort_values("shap_value", key=abs, ascending=False).head(10)

                shap_df["direction"] = shap_df["shap_value"].apply(
                    lambda v: "Augmente le risque" if v > 0 else "Réduit le risque"
                )
                shap_df["abs_val"] = shap_df["shap_value"].abs()

                fig_shap = px.bar(
                    shap_df.sort_values("shap_value"),
                    x="shap_value",
                    y="feature",
                    orientation="h",
                    color="direction",
                    color_discrete_map={
                        "Augmente le risque": COLORS["danger"],
                        "Réduit le risque":   COLORS["safe"]
                    },
                    labels={
                        "shap_value": "Impact sur le score (valeur SHAP)",
                        "feature": "Facteur",
                        "direction": ""
                    },
                    text=shap_df.sort_values("shap_value")["feature_value"].apply(lambda v: f"{v:.2f}"),
                    hover_data={"feature_value": True}
                )
                fig_shap.update_layout(
                    height=400,
                    plot_bgcolor="white",
                    xaxis_title="Impact sur le score de churn",
                    yaxis_title="",
                    legend_title_text=""
                )
                fig_shap.add_vline(x=0, line_color="black", line_width=1)
                st.plotly_chart(fig_shap, use_container_width=True)

                with st.expander("Lire l'explication"):
                    top_pos = shap_df[shap_df["shap_value"] > 0].head(3)
                    top_neg = shap_df[shap_df["shap_value"] < 0].head(3)
                    explanation = f"Pour le compte **{selected_id}**, les principaux facteurs qui *augmentent* le risque de churn sont : "
                    if not top_pos.empty:
                        explanation += ", ".join([f"**{r['feature']}** (valeur : {r['feature_value']:.2f})" for _, r in top_pos.iterrows()])
                    explanation += ". Les facteurs qui *réduisent* ce risque sont : "
                    if not top_neg.empty:
                        explanation += ", ".join([f"**{r['feature']}** (valeur : {r['feature_value']:.2f})" for _, r in top_neg.iterrows()])
                    explanation += "."
                    st.markdown(explanation)

        except ImportError:
            _shap_fallback(model_bundle, analytics_df, selected_id)
        except Exception as e:
            st.warning(f"Calcul SHAP indisponible : {e}")
            _shap_fallback(model_bundle, analytics_df, selected_id)
    else:
        _shap_fallback(None, None, selected_id)


def _shap_fallback(model_bundle, analytics_df, selected_id):
    """Affiche les feature importances si SHAP n'est pas disponible."""
    if model_bundle is not None:
        model       = model_bundle["model"]
        feature_cols = model_bundle["feature_cols"]

        try:
            importances = model.feature_importances_
            imp_df = pd.DataFrame({
                "feature": feature_cols,
                "importance": importances
            }).sort_values("importance", ascending=False).head(10)

            st.info("SHAP non disponible — affichage des importances globales du modèle à la place.")
            fig = px.bar(
                imp_df.sort_values("importance"),
                x="importance", y="feature", orientation="h",
                color_discrete_sequence=[COLORS["neutral"]],
                labels={"importance": "Importance globale", "feature": "Facteur"}
            )
            fig.update_layout(plot_bgcolor="white", height=400)
            st.plotly_chart(fig, use_container_width=True)
        except AttributeError:
            st.info("Le modèle chargé ne fournit pas d'importances de features. Installez `shap` pour les explications individuelles.")
    else:
        st.info(
            "Le modèle ou les données analytiques ne sont pas disponibles dans cette instance. "
            "Pour activer les explications SHAP, assurez-vous que `outputs/models/churn_model.joblib` "
            "et `data/processed/analytics.csv` sont présents, puis installez `shap`."
        )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    df_raw = load_data()

    vue, selected_plans, selected_industries = sidebar(df_raw)
    df = apply_filters(df_raw, selected_plans, selected_industries)

    if len(df) == 0:
        st.warning("Aucun compte ne correspond aux filtres sélectionnés.")
        return

    if vue == "📊 Portefeuille":
        vue_portefeuille(df)
    elif vue == "🎯 Priorisation":
        vue_priorisation(df)
    elif vue == "🔍 Fiche compte":
        vue_fiche_compte(df)


if __name__ == "__main__":
    main()
