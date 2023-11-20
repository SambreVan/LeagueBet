import os
import requests


def telecharger_json(url, nom_fichier):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write(reponse.text)
    else:
        print(f"Échec du téléchargement depuis {url}")


nom_fichier = os.path.join("Json/" + "champ.json")
telecharger_json(
    "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json",
    nom_fichier,
)
print(f"Téléchargé : {nom_fichier}")
