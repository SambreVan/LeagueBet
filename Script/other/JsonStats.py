import json
import os

def process_champion_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        champion_name = list(data['data'].keys())[0]
        champion_data = data['data'][champion_name]

        base_ad = champion_data["stats"]["attackdamage"]
        ad_per_level = champion_data["stats"]["attackdamageperlevel"]
        ad_at_18 = base_ad + ad_per_level * 17  # Niveau maximal est 18, donc 17 niveaux de croissance

        base_ap = champion_data["info"]["magic"]  # Supposition : 'magic' représente l'AP de base
        # Note : L'AP ne croît généralement pas par niveau, donc nous utilisons la valeur de base

        scores = {
            "Name": champion_name,
            "BaseAD": base_ad,
            "ADatLevel18": ad_at_18,
            "BaseAP": base_ap
        }

        return scores

# Chemin du dossier contenant les fichiers JSON
input_folder = 'Json/13.22.1'
output_folder = 'JsonStats'

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(input_folder, filename)
        champion_scores = process_champion_file(file_path)

        output_file_path = os.path.join(output_folder, filename)
        with open(output_file_path, 'w') as outfile:
            json.dump(champion_scores, outfile, indent=4)

print("Traitement de tous les champions terminé.")
