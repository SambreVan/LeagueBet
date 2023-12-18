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
options = "-c client_encoding=UTF8"

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
    dbname=dbname, user=user, password=password, host=host, port=port, options=options
)
cur = conn.cursor()

# Requête SQL pour insérer les données
insert_champion_query = """
INSERT INTO champions (id, key, name, title, resource, attack_type, health_flat, health_perlevel, healthRegen_flat, healthRegen_perlevel, mana_flat, mana_perlevel, manaRegen_flat, manaRegen_perlevel, armor_flat, armor_perlevel, magicResistance_flat, magicResistance_perlevel, attackDamage_flat, attackDamage_perlevel, movespeed_flat, acquisitionRadius_flat, selectionRadius_flat, pathingRadius_flat, gameplayRadius_flat, criticalStrikeDamage_flat, criticalStrikeDamageModifier_flat, attackSpeed_flat, attackSpeed_perlevel, attackSpeedRatio_flat, attackCastTime_flat, attackTotalTime_flat, attackDelayOffset_flat, attackRange_flat, roles, ability_p, ability_q, ability_w, ability_e, ability_r, role)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

# Seuil de playRate pour considérer un poste
play_rate_threshold = 0.1

# Préparer une liste pour les insertions en masse
tuples_to_insert = []

# Traiter chaque fichier JSON
try:
    for json_file in os.listdir(json_folder_path):
        if json_file.endswith(".json"):
            with open(
                os.path.join(json_folder_path, json_file), "r", encoding="utf-8"
            ) as file:
                data = json.load(file)

                # Obtenir les postes du champion actuel
                champion_id = str(data["id"])
                champion_roles_data = champions_roles.get(champion_id, {})

                # Filtrer les postes basés sur le playRate
                champion_roles = [
                    role
                    for role, details in champion_roles_data.items()
                    if details["playRate"] >= play_rate_threshold
                ]

                # Supprimer les champs de chaque compétence
                data["abilities"] = remove_name_from_abilities(data["abilities"])

                # Préparer les données pour l'insertion
                for role in champion_roles:
                    tuples_to_insert.append(
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
                        )
                    )

    # Exécuter la requête avec execute_values pour une insertion en masse
    for record in tuples_to_insert:
        cur.execute(insert_champion_query, record)
    conn.commit()

except psycopg2.Error as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()

print("Transfert des données terminé.")
