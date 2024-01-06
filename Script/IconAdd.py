#Import
import json
import os
import requests

# Paramètres de connexion à la base de données
dbname = "LeagueBet"
user = "Ivan"
password = "r6sOtXPV5ugzD4q9958"
host = "bdd.ilovebeemo.com"
port = 35475
options = "-c client_encoding=UTF8"

# Spécifiez le répertoire contenant les fichiers JSON
json_directory = "Json/13.24.1"  # Modifiez le répertoire selon vos besoins

# Liste pour stocker les noms des champions
champions = []

# Parcourez les fichiers JSON dans le répertoire
for root, _, files in os.walk(json_directory):
    for filename in files:
        if filename.endswith(".json"):
            with open(os.path.join(root, filename), "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                champion_name = data["key"].lower()
                champions.append(champion_name)

icons_base_url = "https://raw.communitydragon.org/latest/game/assets/characters"

# Créez le dossier "icons" s'il n'existe pas déjà
os.makedirs("icons", exist_ok=True)


# Fonction pour télécharger l'icône du champion
def telecharger_icone_champion(champion_id):
    icone_url = f"{icons_base_url}/{champion_id}/hud/{champion_id}_circle.png"
    icone_nom_fichier = os.path.join("Script/icons", f"{champion_id}.png")
    reponse = requests.get(icone_url)
    if reponse.status_code == 200:
        with open(icone_nom_fichier, "wb") as icone_fichier:
            icone_fichier.write(reponse.content)
        print(f"Téléchargé : {icone_nom_fichier}")
    else:
        print(f"Échec du téléchargement de l'icône pour {champion_id}")


# Téléchargez les icônes pour chaque champion
for champion in champions:
    telecharger_icone_champion(champion)

# Liste des fichiers d'icônes téléchargés
icon_files = os.listdir("icons")

# Vérification des champions manquants
champions_manquants = [
    champion for champion in champions if f"{champion}.png" not in icon_files
]

# Affichage des champions manquants
print("Champions manquants:")
for champion in champions_manquants:
    print(champion)
