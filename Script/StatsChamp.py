import os
import requests

def get_all_versions(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des versions disponibles")
        return []

def telecharger_et_extraire_noms_champions(base_url):
    response = requests.get(base_url + "champion.json")
    if response.status_code == 200:
        data = response.json()

        # Accéder à la partie "data" du JSON
        data_section = data.get("data", {})

        # Récupérer toutes les clés (noms) dans la partie "data"
        list_noms = list(data_section.keys())
        return list_noms
    else:
        print("Erreur lors du téléchargement du fichier de liste des champions : Error", response.status_code)
        exit()

def lire_noms_champions(list_noms):
    with open(list_noms, "r") as fichier:
        return [ligne.strip() for ligne in fichier]

def telecharger_json(url, nom_fichier):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(nom_fichier, "w") as fichier:
            fichier.write(reponse.text)
    else:
        print(f"Échec du téléchargement depuis {url}")

def main():
    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    available_versions = get_all_versions(versions_url)

    if not available_versions:
        print("Impossible de récupérer les versions disponibles.")
        return

    latest_version = available_versions[0]

    while True:
        version = input(f"Veuillez entrer la version désirée (Dernière version: {latest_version}) : ")
        version = version if version else latest_version

        if version in available_versions:
            break
        else:
            print(f"Version '{version}' non disponible. Veuillez essayer à nouveau.")

    base_url = "https://ddragon.leagueoflegends.com/cdn/" + version + "/data/fr_FR/"

    # Créer le dossier 'Json' s'il n'existe pas
    if not os.path.exists("Json"):
        os.makedirs("Json")

    noms_champions = telecharger_et_extraire_noms_champions(base_url)

    if not os.path.exists("Json/" + version):
        os.makedirs("Json/" + version)

    for nom in noms_champions:
        url_complet = base_url + "champion/" + nom + ".json"
        nom_fichier = os.path.join("Json/" + version, f"{nom}.json")
        telecharger_json(url_complet, nom_fichier)
        print(f"Téléchargé : {nom_fichier}")

if __name__ == "__main__":
    main()