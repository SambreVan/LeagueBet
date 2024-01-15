import json
import os

def calculate_stats_at_max_level(base_stats):
    max_level_stats = {}
    for stat, value in base_stats.items():
        if "perlevel" in stat:
            base_stat = stat.replace("perlevel", "")
            max_level_stats[base_stat] = base_stats[base_stat] + (base_stats[stat] * 17)
    return max_level_stats

def clean_champion_data(champion):
    stats_at_max_level = calculate_stats_at_max_level(champion["stats"])
    return {
        "id": champion["id"],
        "name": champion["name"],
        "title": champion["title"],
        "tags": champion["tags"],
        "base_stats": champion["stats"],
        "stats_at_level_18": stats_at_max_level
    }

def process_json_files(directory):
    output_dir = "Json/Cleaned/13.22.1"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)

            champions = data["data"]
            cleaned_data = {champ: clean_champion_data(details) for champ, details in champions.items()}

            for champ, details in cleaned_data.items():
                with open(f"{output_dir}/{champ}.json", 'w') as outfile:
                    json.dump(details, outfile, indent=4)

# Exemple d'utilisation
process_json_files("Json/13.22.1")
