import os
import json
import requests

version = "13.1.1"
source = "https://cdn.merakianalytics.com/riot/lol/resources/old/en-US/1700987404_champions.json"

# Fonction pour télécharger le fichier JSON
def telecharger_json(url, nom_fichier):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write(reponse.text)
    else:
        print(f"Échec du téléchargement depuis {url}")


# Télécharger le fichier JSON
os.makedirs("Json/" + version + "/data/en_US/champion", exist_ok=True)
nom_fichier = os.path.join("Json/" + version + "/data/en_US/", "champions.json")
telecharger_json(source, nom_fichier)
print(f"Téléchargé : {nom_fichier}")

# Lire le fichier JSON et créer un fichier par champion
with open(nom_fichier, "r", encoding="utf-8") as fichier:
    champions = json.load(fichier)

# Créer un fichier pour chaque champion
for champ, details in champions.items():
    nom_fichier_champion = os.path.join(
        "Json/" + version + "/data/en_US/champion", f"{champ}.json"
    )
    with open(nom_fichier_champion, "w", encoding="utf-8") as fichier_champ:
        json.dump(details, fichier_champ, ensure_ascii=False, indent=4)
