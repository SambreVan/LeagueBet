import requests
from urllib.parse import quote
import json
import os

# Votre clé d'API personnelle de Riot Games
api_key = 'RGAPI-4413a60d-9d1d-47a7-ad3c-d84da47e46fe'

# Le nom d'utilisateur du joueur, encodé pour être utilisé dans une URL
summoner_name = 'TBW Bboy'
encoded_summoner_name = quote(summoner_name)

# L'URL de base pour l'API de la région EUW
url_base = 'https://euw1.api.riotgames.com/lol/'

# Construire l'URL pour obtenir l'ID de l'invocateur
url_summoner = f'{url_base}summoner/v4/summoners/by-name/{encoded_summoner_name}'

# Faire la requête pour obtenir l'ID de l'invocateur
response_summoner = requests.get(url_summoner, headers={"X-Riot-Token": api_key})

# Vérifier si la requête a réussi
if response_summoner.status_code == 200:
    # Convertir la réponse en JSON
    summoner_data = response_summoner.json()
    
    # Utiliser l'ID de l'invocateur pour obtenir plus de données, par exemple les stats classées
    summoner_id = summoner_data['id']
    url_ranked_stats = f'{url_base}league/v4/entries/by-summoner/{summoner_id}'
    
    # Faire la requête pour obtenir les stats classées
    response_ranked_stats = requests.get(url_ranked_stats, headers={"X-Riot-Token": api_key})
    
    if response_ranked_stats.status_code == 200:
        ranked_stats_data = response_ranked_stats.json()
        
        # Le chemin vers le fichier JSON où vous voulez enregistrer les données
        file_path = 'player_data.json'
        
        # Vérifier si le fichier JSON existe déjà
        if os.path.isfile(file_path):
            # Lire les données existantes
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            # Créer un nouveau dictionnaire si le fichier n'existe pas
            data = {}
        
        # Mettre à jour ou ajouter les données du joueur
        data[summoner_name] = ranked_stats_data
        
        # Écrire les données mises à jour dans le fichier JSON
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Les données du joueur {summoner_name} ont été mises à jour dans {file_path}.")
    else:
        print(f"Erreur lors de la récupération des statistiques classées: {response_ranked_stats.status_code}")
        print(response_ranked_stats.text)
else:
    print(f"Erreur lors de la récupération des données de l'invocateur: {response_summoner.status_code}")
    print(response_summoner.text)

# Note: Ce script ne gère pas les erreurs de manière exhaustive et ne prend pas en compte les limites de taux de l'API.
