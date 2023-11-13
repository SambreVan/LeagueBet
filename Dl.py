import os
import requests

# URL de base et liste des noms de champions
version = "13.22.1"
chemin_fichier = "Champ.txt"
base_url = (
    "https://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/champion/"
)


def lire_noms_champions(chemin_fichier):
    with open(chemin_fichier, "r") as fichier:
        return [ligne.strip() for ligne in fichier]


def telecharger_json(url, nom_fichier):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(nom_fichier, "w") as fichier:
            fichier.write(reponse.text)
    else:
        print(f"Échec du téléchargement depuis {url}")


def main():
    # Créer le dossier 'Json' s'il n'existe pas
    if not os.path.exists("Json"):
        os.makedirs("Json")

    for nom in lire_noms_champions(chemin_fichier):
        url_complet = base_url + nom + ".json"
        nom_fichier = os.path.join(
            "Json", f"{nom}.json"
        )  # Chemin dans le dossier 'Json'
        telecharger_json(url_complet, nom_fichier)
        print(f"Téléchargé : {nom_fichier}")


if __name__ == "__main__":
    main()
