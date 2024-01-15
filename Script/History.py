import requests

api_key = "RGAPI-4475970f-ad94-4fa2-b4c2-0d6e42451056"
summoner_name = "yiforce"
region = "euw1"

# Obtenir l'identifiant de compte
response = requests.get(
    f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
)


account_id = response.json()["accountId"]

# Récupérer l'historique des matchs
match_history = requests.get(
    f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key}"
)
print(match_history.json())
