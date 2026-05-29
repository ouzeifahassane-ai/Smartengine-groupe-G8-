"""
API FastAPI — SmartEngine
Expose les données de churn pour les outils externes (n8n, dashboards, etc.)
"""

import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Initialisation de l'app ---
app = FastAPI(
    title="SmartEngine API",
    description="API de scoring churn — Groupe G8",
    version="1.0.0",
)

# --- CORS : autorise les appels externes (n8n, navigateur, etc.) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Chemins vers les fichiers de données ---
SCORES_PATH = Path("outputs/scores.csv")
PRIORISATION_PATH = Path("outputs/priorisation.csv")


# --- Utilitaire : charger un CSV avec gestion d'erreur propre ---
def charger_csv(chemin: Path) -> pd.DataFrame:
    if not chemin.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Fichier introuvable : {chemin}. Lance /run-pipeline pour générer les données."
        )
    return pd.read_csv(chemin)


# --- Utilitaire : convertir les types numpy en types Python natifs ---
def to_python(obj):
    if hasattr(obj, "item"):
        return obj.item()
    return obj


# ─────────────────────────────────────────────
# 1. GET /health — vérification que l'API tourne
# ─────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


# ─────────────────────────────────────────────
# 2. GET /scores — tous les comptes
# ─────────────────────────────────────────────
@app.get("/scores")
def get_scores():
    df = charger_csv(SCORES_PATH)
    return df.where(pd.notnull(df), None).applymap(to_python).to_dict(orient="records")


# ─────────────────────────────────────────────
# 3. GET /scores/{account_id} — un compte précis
# ─────────────────────────────────────────────
@app.get("/scores/{account_id}")
def get_score(account_id: str):
    df = charger_csv(SCORES_PATH)

    df["account_id"] = df["account_id"].astype(str)
    ligne = df[df["account_id"] == account_id]

    if ligne.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Compte '{account_id}' introuvable dans scores.csv."
        )

    record = ligne.iloc[0].where(pd.notnull(ligne.iloc[0]), None).to_dict()
    return {k: to_python(v) for k, v in record.items()}


# ─────────────────────────────────────────────
# 4. GET /portfolio — synthèse globale du portefeuille
# ─────────────────────────────────────────────
@app.get("/portfolio")
def get_portfolio():
    df_scores = charger_csv(SCORES_PATH)

    risk = df_scores["risk_level"].str.lower()
    high_count   = int((risk == "high").sum())
    medium_count = int((risk == "medium").sum())
    low_count    = int((risk == "low").sum())

    # MRR à risque : on utilise priorisation.csv si disponible, sinon 0
    mrr_a_risque = 0
    if PRIORISATION_PATH.exists():
        df_prio = pd.read_csv(PRIORISATION_PATH)
        comptes_high = df_prio[df_prio["risk_level"].str.lower() == "high"]
        if "mrr" in comptes_high.columns:
            mrr_a_risque = int(comptes_high["mrr"].sum())

    avg_score = round(float(df_scores["churn_probability"].mean()), 3)

    return {
        "total_accounts": int(len(df_scores)),
        "high_count":     high_count,
        "medium_count":   medium_count,
        "low_count":      low_count,
        "mrr_a_risque":   mrr_a_risque,
        "avg_score":      avg_score,
    }


# ─────────────────────────────────────────────
# 5. GET /priorisation — contenu de priorisation.csv
# ─────────────────────────────────────────────
@app.get("/priorisation")
def get_priorisation():
    if not PRIORISATION_PATH.exists():
        return {
            "message": "Le fichier priorisation.csv n'est pas encore généré. Lance /run-pipeline d'abord."
        }

    df = pd.read_csv(PRIORISATION_PATH)
    return df.where(pd.notnull(df), None).applymap(to_python).to_dict(orient="records")


# ─────────────────────────────────────────────
# 6. POST /run-pipeline — régénère scores.csv et priorisation.csv
#    ⚠️  Ne réentraîne PAS le modèle (train_model.py reste manuel)
# ─────────────────────────────────────────────
@app.post("/run-pipeline")
def run_pipeline():
    # Noms exacts des scripts présents dans src/
    scripts = [
        "src/generate_scores.py",
        "src/generate_prioritization.py",
    ]

    etapes = []

    for script in scripts:
        try:
            resultat = subprocess.run(
                ["python", script],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if resultat.returncode == 0:
                etapes.append({"script": Path(script).name, "statut": "ok"})
            else:
                etapes.append({
                    "script": Path(script).name,
                    "statut": "erreur",
                    "detail": resultat.stderr.strip() or resultat.stdout.strip(),
                })

        except subprocess.TimeoutExpired:
            etapes.append({
                "script": Path(script).name,
                "statut": "erreur",
                "detail": "Timeout dépassé (120 secondes).",
            })
        except Exception as e:
            etapes.append({
                "script": Path(script).name,
                "statut": "erreur",
                "detail": str(e),
            })

    statut_global = "ok" if all(e["statut"] == "ok" for e in etapes) else "erreur"

    return {
        "status": statut_global,
        "etapes": etapes,
        "regenere_le": datetime.now().isoformat(timespec="seconds"),
    }
