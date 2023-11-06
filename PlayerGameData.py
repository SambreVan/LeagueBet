import requests
import json

API_KEY = 'RGAPI-4188fb6a-e6db-454b-8b26-8bb3fa221877'
PLAYER_NAME = 'Swishee'
REGION = 'euw1'

def get_player_id(player_name):
    response = requests.get(
        f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={API_KEY}'
    )
    return response.json().get('id')

def get_current_game_info(summoner_id):
    response = requests.get(
        f'https://{REGION}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={API_KEY}'
    )
    return response.json()

def get_ranked_stats(summoner_id):
    response = requests.get(
        f'https://{REGION}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={API_KEY}'
    )
    return response.json()

def calculate_winrate(player_ranked_stats):
    for queue in player_ranked_stats:
        if queue.get('queueType') == 'RANKED_SOLO_5x5':
            wins = queue.get('wins', 0)
            losses = queue.get('losses', 0)
            total_games = wins + losses
            return wins / total_games if total_games > 0 else 0
    return 0


def calculate_team_chances(team_100_winrate, team_200_winrate):
    total_winrate = team_100_winrate + team_200_winrate
    if total_winrate == 0:
        return 50, 50

    chance_team_100 = (team_100_winrate / total_winrate) * 100
    chance_team_200 = (team_200_winrate / total_winrate) * 100
    return round(chance_team_100, 2), round(chance_team_200, 2)

def get_game_players_info():
    summoner_id = get_player_id(PLAYER_NAME)
    current_game_info = get_current_game_info(summoner_id)
    team_100_winrate = []
    team_200_winrate = []
    game_data = {'players': [], 'team_100_avg_winrate': 0, 'team_200_avg_winrate': 0, 'team_chances': {}}

    for player in current_game_info.get('participants', []):
        player_summoner_id = get_player_id(player.get('summonerName'))
        player_ranked_stats = get_ranked_stats(player_summoner_id)
        winrate = calculate_winrate(player_ranked_stats)

        player_info = {
            'name': player.get('summonerName'),
            'teamId': player.get('teamId'),
            'rank': player_ranked_stats[0].get('tier') if player_ranked_stats else 'Unranked',
            'winrate': round(winrate * 100, 2) if winrate else 0
        }
        game_data['players'].append(player_info)

        if player_info['teamId'] == 100:
            team_100_winrate.append(player_info['winrate'])
        else:
            team_200_winrate.append(player_info['winrate'])

    game_data['team_100_avg_winrate'] = round(sum(team_100_winrate) / len(team_100_winrate), 2) if team_100_winrate else 0
    game_data['team_200_avg_winrate'] = round(sum(team_200_winrate) / len(team_200_winrate), 2) if team_200_winrate else 0

    team_100_chance, team_200_chance = calculate_team_chances(game_data['team_100_avg_winrate'], game_data['team_200_avg_winrate'])
    game_data['team_chances'] = {'team_100': team_100_chance, 'team_200': team_200_chance}

    return game_data

def save_data_to_json(data, filename='game_data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

game_data = get_game_players_info()
save_data_to_json(game_data)

print(f"Chances de victoire estimées - Équipe 100: {game_data['team_chances']['team_100']}%, Équipe 200: {game_data['team_chances']['team_200']}%")