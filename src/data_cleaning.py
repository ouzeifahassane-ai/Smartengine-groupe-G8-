import pandas as pd
import numpy as np
import os
from datetime import datetime

def clean_data():
    raw_dir = 'data/raw'
    output_dir = 'outputs'
    
    # S'assurer que le répertoire de sortie existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    files = {
        'accounts': 'ravenstack_accounts.csv',
        'subscriptions': 'ravenstack_subscriptions.csv',
        'feature_usage': 'ravenstack_feature_usage.csv',
        'support_tickets': 'ravenstack_support_tickets.csv',
        'churn_events': 'ravenstack_churn_events.csv'
    }
    
    report_lines = ["# Rapport de Nettoyage des Données - smartEngine", f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
    
    for key, filename in files.items():
        file_path = os.path.join(raw_dir, filename)
        if not os.path.exists(file_path):
            report_lines.append(f"## {filename} : FICHIER NON TROUVÉ")
            continue
            
        print(f"Nettoyage de {filename}...")
        df = pd.read_csv(file_path)
        
        report_lines.append(f"## {filename}")
        report_lines.append(f"- Lignes initiales : {len(df)}")
        
        # 1. Conversion des dates
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'at' in col.lower()]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        report_lines.append(f"- Colonnes de dates converties : {', '.join(date_cols)}")
        
        # 2. Valeurs manquantes
        missing = df.isnull().sum()
        if missing.any():
            report_lines.append("- Valeurs manquantes identifiées :")
            for col, count in missing[missing > 0].items():
                report_lines.append(f"  - {col} : {count} ({round(count/len(df)*100, 2)}%)")
                # Stratégies simples de remplissage
                if df[col].dtype in ['float64', 'int64']:
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna('Unknown')
        
        # 3. Standardisation du texte
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            df[col] = df[col].astype(str).str.strip()
            
        # 4. Outliers (z-score simple > 3)
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in num_cols:
            z_scores = (df[col] - df[col].mean()) / df[col].std()
            outliers_count = (np.abs(z_scores) > 3).sum()
            if outliers_count > 0:
                report_lines.append(f"- Outliers détectés dans {col} : {outliers_count}")
        
        # 5. Sauvegarde
        clean_filename = f"{key}_clean.csv"
        clean_path = os.path.join(output_dir, clean_filename)
        df.to_csv(clean_path, index=False)
        report_lines.append(f"- Fichier nettoyé sauvegardé : {clean_path}\n")

    # Rapport final
    report_path = os.path.join(output_dir, 'rapport-nettoyage.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    print(f"Rapport de nettoyage généré : {report_path}")

if __name__ == "__main__":
    clean_data()
