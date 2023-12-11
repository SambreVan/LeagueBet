import json
import psycopg2
import os

# Paramètres de connexion à la base de données
dbname = "LeagueBet"
user = "Ivan"
password = "r6sOtXPV5ugzD4q9958"
host = "bdd.ilovebeemo.com"
port = 35475

# Chemin vers le dossier contenant les fichiers JSON
json_folder_path = "Json/13.22.1"

# Connexion à la base de données
conn = psycopg2.connect(
    dbname=dbname, user=user, password=password, host=host, port=port
)
cur = conn.cursor()

# Requêtes SQL pour insérer les données
insert_champion_query = """
INSERT INTO champions (id, key, name, title, resource, attack_type, roles)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

insert_stats_query = """
INSERT INTO champion_stats (champion_id, health, health_regen, mana, mana_regen, armor, magic_resistance, attack_damage, movespeed, acquisition_radius, selection_radius, pathing_radius, gameplay_radius, critical_strike_damage, critical_strike_damage_modifier, attack_speed, attack_speed_ratio, attack_cast_time, attack_total_time, attack_delay_offset, attack_range)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

insert_abilities_query = """
INSERT INTO champion_abilities (champion_id, ability_type, description)
VALUES (%s, %s, %s)
ON CONFLICT (champion_id, ability_type) DO NOTHING;
"""

# Lister tous les fichiers JSON dans le dossier spécifié
json_files = [f for f in os.listdir(json_folder_path) if f.endswith(".json")]

# Traiter chaque fichier JSON
for json_file in json_files:
    with open(os.path.join(json_folder_path, json_file), "r", encoding="utf-8") as file:
        data = json.load(file)

        # Insérer les informations du champion
        cur.execute(
            insert_champion_query,
            (
                data["id"],
                data["key"],
                data["name"],
                data["title"],
                data["resource"],
                data["attackType"],
                data["roles"],
                # data["Lane"],
                data["stats"]["health"]["flat"],
                data["stats"]["health"]["perLevel"],
                data["stats"]["healthRegen"]["flat"],
                data["stats"]["healthRegen"]["perLevel"],
                data["stats"]["mana"]["flat"],
                data["stats"]["mana"]["perLevel"],
                data["stats"]["manaRegen"]["flat"],
                data["stats"]["manaRegen"]["perLevel"],
                data["stats"]["armor"]["flat"],
                ata["stats"]["armor"]["perLevel"],
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
                data["abilities"]["P"],
                data["abilities"]["Q"],
                data["abilities"]["W"],
                data["abilities"]["E"],
                data["abilities"]["R"],
            ),
        )

# Valider les changements
conn.commit()

# Fermer le curseur et la connexion
cur.close()
conn.close()

print("Transférer des donnée terminée")
