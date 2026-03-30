"""
clean_data.py — Projet smartEngine Groupe G8
Sprint 2 : Nettoyage des 5 fichiers CSV bruts

Utilisation :
    python src/clean_data.py

Résultat :
    - 5 fichiers nettoyés dans data/processed/
    - Rapport de nettoyage dans outputs/rapport-nettoyage.md
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


def clean_data():

    raw_dir       = "data/raw"
    processed_dir = "data/processed"
    output_dir    = "outputs"

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(output_dir,    exist_ok=True)

    files = {
        "accounts":        "ravenstack_accounts.csv",
        "subscriptions":   "ravenstack_subscriptions.csv",
        "feature_usage":   "ravenstack_feature_usage.csv",
        "support_tickets": "ravenstack_support_tickets.csv",
        "churn_events":    "ravenstack_churn_events.csv",
    }

    report_lines = [
        "# Rapport de nettoyage des données — smartEngine",
        f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]

    for key, filename in files.items():
        file_path = os.path.join(raw_dir, filename)
        if not os.path.exists(file_path):
            report_lines.append(f"## {filename} : FICHIER NON TROUVÉ\n")
            continue

        print(f"Nettoyage de {filename}...")
        df = pd.read_csv(file_path)
        nb_avant = len(df)

        report_lines.append(f"## {filename}")
        report_lines.append(f"- Lignes initiales : {nb_avant}")

        # ── 1. Conversion des dates ────────────────────────────────────────
        date_cols = [c for c in df.columns if "date" in c.lower() or "_at" in c.lower()]
        for col in date_cols:
            # end_date peut être NaT (abonnement actif) : errors='coerce' préserve les NaT
            df[col] = pd.to_datetime(df[col], errors="coerce")
        if date_cols:
            report_lines.append(f"- Colonnes dates converties : {', '.join(date_cols)}")

        # ── 2. Doublons ────────────────────────────────────────────────────
        id_col_map = {
            "accounts":        "account_id",
            "subscriptions":   "subscription_id",
            "feature_usage":   "usage_id",
            "support_tickets": "ticket_id",
            "churn_events":    "churn_event_id",
        }
        id_col = id_col_map.get(key)
        if id_col and id_col in df.columns:
            nb_dups = df[id_col].duplicated().sum()
            report_lines.append(f"- Doublons sur {id_col} : {nb_dups}")
            if nb_dups > 0:
                df = df.drop_duplicates(subset=[id_col])
                report_lines.append(f"  → Stratégie : suppression des {nb_dups} doublons")

        # ── 3. Valeurs manquantes ──────────────────────────────────────────
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            report_lines.append("- Valeurs manquantes :")
            for col, count in missing.items():
                pct = round(count / nb_avant * 100, 2)
                report_lines.append(f"  - {col} : {count} ({pct}%)")

                # Stratégie spécifique end_date : valeur métier, ne pas imputer
                if col == "end_date":
                    report_lines.append("    → Stratégie : conservation (NULL = abonnement actif)")
                    continue

                # Imputation numérique → médiane (robuste aux outliers)
                if df[col].dtype in ["float64", "int64"]:
                    df[col] = df[col].fillna(df[col].median())
                    report_lines.append("    → Stratégie : imputation par la médiane")
                else:
                    df[col] = df[col].fillna("Unknown")
                    report_lines.append("    → Stratégie : remplacement par 'Unknown'")
        else:
            report_lines.append("- Valeurs manquantes : aucune")

        # ── 4. Standardisation du texte ────────────────────────────────────
        text_cols = df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            df[col] = df[col].astype(str).str.strip()
        report_lines.append(f"- Standardisation texte (strip) sur {len(text_cols)} colonnes")

        # ── 5. Outliers (z-score > 3) ──────────────────────────────────────
        # On détecte mais on NE supprime PAS : les valeurs extrêmes sont souvent
        # réelles (ex : gros comptes Enterprise avec MRR élevé).
        num_cols = df.select_dtypes(include=["float64", "int64"]).columns
        outliers_found = []
        for col in num_cols:
            if df[col].std() == 0:
                continue
            z_scores = (df[col] - df[col].mean()) / df[col].std()
            n_out = (np.abs(z_scores) > 3).sum()
            if n_out > 0:
                outliers_found.append(f"{col} ({n_out})")
        if outliers_found:
            report_lines.append(f"- Outliers détectés (z-score > 3) : {', '.join(outliers_found)}")
            report_lines.append("  → Stratégie : conservation (valeurs réelles, ex : comptes Enterprise)")
        else:
            report_lines.append("- Outliers : aucun détecté")

        # ── 6. Sauvegarde dans data/processed/ ────────────────────────────
        nb_apres = len(df)
        taux = round(nb_apres / nb_avant * 100, 1)
        report_lines.append(f"- Lignes après nettoyage : {nb_apres} ({taux}% conservées)")

        clean_path = os.path.join(processed_dir, f"{key}.csv")
        df.to_csv(clean_path, index=False)
        report_lines.append(f"- Fichier sauvegardé : {clean_path}\n")
        print(f"  ✓ {nb_apres} lignes → {clean_path}")

    # ── Rapport final ──────────────────────────────────────────────────────
    report_lines.append("## Bilan global")
    report_lines.append("- Tous les fichiers nettoyés sont dans data/processed/")
    report_lines.append("- Prochaine étape : python src/build_features.py")

    report_path = os.path.join(output_dir, "rapport-nettoyage.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n✓ Rapport de nettoyage généré : {report_path}")


if __name__ == "__main__":
    clean_data()