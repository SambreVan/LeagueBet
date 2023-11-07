import requests

API_KEY = "RGAPI-4475970f-ad94-4fa2-b4c2-0d6e42451056"
REGION = "euw1"  # Mettez "euw1" pour la région Europe Ouest


def get_champion_stats(champion_id):
    url = f"https://{REGION}.api.riotgames.com/lol/platform/v3/champion-rotations"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        champion_data = response.json()
        print(champion_data)
        exit()
        for champion in champion_data["champions"]:
            if champion["id"] == champion_id:
                return champion
        return "Champion not found."
    else:
        return f"Error {response.status_code} occurred."


# Remplacez 'YOUR_API_KEY' par votre propre clé API.
champion_id = 266  # Remplacez par l'ID du champion que vous recherchez. Par exemple, 266 correspond à Aatrox.
champion_stats = get_champion_stats(champion_id)
print(champion_stats)
