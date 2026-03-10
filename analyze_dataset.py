import csv
import os

files = ['accounts.csv', 'churn_events.csv', 'feature_usage.csv', 'subscriptions.csv', 'support_tickets.csv']
data_dir = 'data/raw'
output_file = 'outputs/decouverte-dataset.md'

os.makedirs('outputs', exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Découverte du Dataset\n\n")

    for filename in files:
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            f.write(f"## {filename}\n\nFichier non trouvé.\n\n")
            continue

        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = list(csv.reader(csvfile))
            if not reader:
                f.write(f"## {filename}\n\nFichier vide.\n\n")
                continue

            header = reader[0]
            rows = reader[1:]
            num_cols = len(header)
            num_rows = len(rows)

            f.write(f"## {filename}\n\n")
            f.write(f"- **Nombre de colonnes :** {num_cols}\n")
            f.write(f"- **Nombre de lignes :** {num_rows}\n\n")

            f.write("### Colonnes et Types (estimés)\n")
            missing_counts = [0] * num_cols
            types = ["String"] * num_cols

            for row in rows:
                for i, val in enumerate(row):
                    if not val:
                        missing_counts[i] += 1

            for i, col in enumerate(header):
                f.write(f"- `{col}` : {missing_counts[i]} valeurs manquantes\n")

            f.write("\n### 3 premières lignes\n")
            f.write("| " + " | ".join(header) + " |\n")
            f.write("| " + " | ".join(["---"] * num_cols) + " |\n")
            for row in rows[:3]:
                f.write("| " + " | ".join(row) + " |\n")
            f.write("\n")

            # Simple churn prediction heuristic
            f.write("### Analyse pour la prédiction du churn\n")
            if filename == 'accounts.csv':
                f.write("Les informations de segment et la date de création sont utiles pour le profil utilisateur.\n")
            elif filename == 'churn_events.csv':
                f.write("C'est la variable cible (churn_date).\n")
            elif filename == 'feature_usage.csv':
                f.write("Très important : la fréquence d'utilisation des fonctionnalités est un indicateur clé de l'engagement.\n")
            elif filename == 'subscriptions.csv':
                f.write("Les types de plans et les montants peuvent indiquer le niveau d'investissement financier.\n")
            elif filename == 'support_tickets.csv':
                f.write("Le volume et la priorité des tickets peuvent signaler une insatisfaction.\n")
            f.write("\n---\n\n")
