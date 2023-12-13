import json
import psycopg2
from psycopg2.extras import execute_values
import os


# Paramètres de connexion à la base de données
dbname = "LeagueBet"
user = "Ivan"
password = "r6sOtXPV5ugzD4q9958"
host = "bdd.ilovebeemo.com"
port = 35475

# Chemin vers le dossier contenant les fichiers JSON
json_folder_path = "Json/13.24.1"
roles_file_path = "championrates.json"


def remove_name_from_abilities(abilities):
    for ability_type in abilities.values():
        for ability in ability_type:
            del ability["name"]
            del ability["icon"]
            for effect in ability.get("effects", []):
                del effect["description"]
            del ability["notes"]
            del ability["blurb"]
    return abilities


# Lecture des postes des champions
with open(roles_file_path, "r") as file:
    champions_data = json.load(file)
    champions_roles = champions_data["data"]


# Connexion à la base de données
conn = psycopg2.connect(
    dbname=dbname, user=user, password=password, host=host, port=port
)
cur = conn.cursor()

# Requêtes SQL pour insérer les données
insert_champion_query = """
INSERT INTO champions (id, key, name, title, resource, attack_type, health_flat, health_perlevel, healthRegen_flat, healthRegen_perlevel, mana_flat, mana_perlevel, manaRegen_flat, manaRegen_perlevel, armor_flat, armor_perlevel, magicResistance_flat, magicResistance_perlevel, attackDamage_flat, attackDamage_perlevel, movespeed_flat, acquisitionRadius_flat, selectionRadius_flat, pathingRadius_flat, gameplayRadius_flat, criticalStrikeDamage_flat, criticalStrikeDamageModifier_flat, attackSpeed_flat, attackSpeed_perlevel, attackSpeedRatio_flat, attackCastTime_flat, attackTotalTime_flat, attackDelayOffset_flat, attackRange_flat, roles, ability_p, ability_q, ability_w, ability_e, ability_r, role)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

# Lister tous les fichiers JSON dans le dossier spécifié
json_files = [f for f in os.listdir(json_folder_path) if f.endswith(".json")]

# Seuil de playRate pour considérer un poste
play_rate_threshold = 0.1

# Traiter chaque fichier JSON
for json_file in json_files:
    with open(os.path.join(json_folder_path, json_file), "r", encoding="utf-8") as file:
        data = json.load(file)

        # Obtenir les postes du champion actuel
        champion_id = str(
            data["id"]
        )  # Assurez-vous que l'ID est sous forme de chaîne si nécessaire
        champion_roles_data = champions_roles.get(champion_id, {})

        # Filtrer les postes basés sur le playRate
        champion_roles = [
            role
            for role, details in champion_roles_data.items()
            if details["playRate"] >= play_rate_threshold
        ]

        # Supprimez les champs de chaque compétence
        data["abilities"] = remove_name_from_abilities(data["abilities"])
        print(data["abilities"])
        exit()
        # Insérer les informations du champion
        for role in champion_roles:
            cur.execute(
                insert_champion_query,
                (
                    data["id"],
                    data["key"],
                    data["name"],
                    data["title"],
                    data["resource"],
                    data["attackType"],
                    data["stats"]["health"]["flat"],
                    data["stats"]["health"]["perLevel"],
                    data["stats"]["healthRegen"]["flat"],
                    data["stats"]["healthRegen"]["perLevel"],
                    data["stats"]["mana"]["flat"],
                    data["stats"]["mana"]["perLevel"],
                    data["stats"]["manaRegen"]["flat"],
                    data["stats"]["manaRegen"]["perLevel"],
                    data["stats"]["armor"]["flat"],
                    data["stats"]["armor"]["perLevel"],
                    data["stats"]["magicResistance"]["flat"],
                    data["stats"]["magicResistance"]["perLevel"],
                    data["stats"]["attackDamage"]["flat"],
                    data["stats"]["attackDamage"]["perLevel"],
                    data["stats"]["movespeed"]["flat"],
                    data["stats"]["acquisitionRadius"]["flat"],
                    data["stats"]["selectionRadius"]["flat"],
                    data["stats"]["pathingRadius"]["flat"],
                    data["stats"]["gameplayRadius"]["flat"],
                    data["stats"]["criticalStrikeDamage"]["flat"],
                    data["stats"]["criticalStrikeDamageModifier"]["flat"],
                    data["stats"]["attackSpeed"]["flat"],
                    data["stats"]["attackSpeed"]["perLevel"],
                    data["stats"]["attackSpeedRatio"]["flat"],
                    data["stats"]["attackCastTime"]["flat"],
                    data["stats"]["attackTotalTime"]["flat"],
                    data["stats"]["attackDelayOffset"]["flat"],
                    data["stats"]["attackRange"]["flat"],
                    data["roles"],
                    [json.dumps(ability) for ability in data["abilities"]["P"]],
                    [json.dumps(ability) for ability in data["abilities"]["Q"]],
                    [json.dumps(ability) for ability in data["abilities"]["W"]],
                    [json.dumps(ability) for ability in data["abilities"]["E"]],
                    [json.dumps(ability) for ability in data["abilities"]["R"]],
                    role,
                ),
            )

# Valider les changements
conn.commit()

# Fermer le curseur et la connexion
cur.close()
conn.close()

print("Transférer des donnée terminée")
