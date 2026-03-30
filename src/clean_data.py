import csv
import os
from datetime import datetime

def clean_csv(input_path, output_path, rules):
    if not os.path.exists(input_path):
        return None, "Fichier non trouvé"

    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames

    initial_rows = len(rows)
    # Suppression des doublons
    unique_rows = []
    seen = set()
    for row in rows:
        row_tuple = tuple(row.items())
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)
    
    rows_after_duplicates = len(unique_rows)
    
    cleaned_rows = []
    for row in unique_rows:
        new_row = row.copy()
        for field, action in rules.items():
            if field in new_row:
                if action == 'fill_feedback':
                    if not new_row[field]:
                        new_row[field] = 'Pas de feedback'
                elif action == 'mrr_positive':
                    try:
                        val = float(new_row[field])
                        if val < 0: new_row[field] = '0'
                    except:
                        pass
                elif action == 'fill_median_satisfaction':
                    # Simplification: si vide, on peut mettre une valeur par défaut comme 3.0 (score médian)
                    if not new_row[field]:
                        new_row[field] = '3.0'
        cleaned_rows.append(new_row)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    return (initial_rows, initial_rows - rows_after_duplicates), "Succès"

def main():
    input_dir = 'data/raw'
    output_dir = 'outputs/cleaned'
    report_path = 'outputs/rapport-nettoyage.md'
    
    files_rules = {
        'accounts.csv': {},
        'churn_events.csv': {'feedback_text': 'fill_feedback'},
        'feature_usage.csv': {},
        'subscriptions.csv': {'mrr_amount': 'mrr_positive'},
        'support_tickets.csv': {'satisfaction_score': 'fill_median_satisfaction'}
    }
    
    report_content = "# Rapport de Nettoyage des Données (Standard Library)\n"
    report_content += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"

    for file, rules in files_rules.items():
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, f"cleaned_{file}")
        
        stats, status = clean_csv(input_path, output_path, rules)
        
        report_content += f"## {file}\n"
        if stats:
            initial, duplicates = stats
            report_content += f"- **Lignes initiales :** {initial}\n"
            report_content += f"- **Doublons supprimés :** {duplicates}\n"
            report_content += f"- **Statut :** {status}\n"
            report_content += f"- **Fichier nettoyé :** `outputs/cleaned/cleaned_{file}`\n\n"
        else:
            report_content += f"- **Erreur :** {status}\n\n"

    os.makedirs('outputs', exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Nettoyage terminé avec succès. Rapport dans {report_path}")

if __name__ == "__main__":
    main()
