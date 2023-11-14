import requests
import json
import os

API_KEY = 'RGAPI-8626f8fe-2f63-4e6d-98f4-245b8dd1d3e4'  # Votre clé API
PLAYER_NAME = 'tbw bboy'  # Nom du joueur
REGION = 'euw1'  # Région

def get_summoner_info(api_key, region, player_name):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_match_history(api_key, region, account_id):
    url = f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def save_to_json(data, filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print(f"Le fichier {filename} existe déjà.")

try:
    summoner_info = get_summoner_info(API_KEY, REGION, PLAYER_NAME)
    account_id = summoner_info['accountId']

    match_history = get_match_history(API_KEY, REGION, account_id)
    save_to_json(match_history, 'match_history.json')

    print("L'historique des matchs a été enregistré avec succès.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")
