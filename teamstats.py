import json
import os

def load_champion_data(champion_name, directory="Json/Cleaned/13.22.1"):
    try:
        with open(f"{directory}/{champion_name}.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Champion '{champion_name}' not found.")
        return None

def sum_team_stats(team):
    team_stats = {
        "total_hp": 0,
        "total_armor": 0,
        "total_spellblock": 0,
        # Ajoutez ici d'autres statistiques si nécessaire
    }
    for champion_name in team:
        champion_data = load_champion_data(champion_name)
        if champion_data:
            team_stats["total_hp"] += champion_data["stats_at_level_18"]["hp"]
            team_stats["total_armor"] += champion_data["stats_at_level_18"]["armor"]
            team_stats["total_spellblock"] += champion_data["stats_at_level_18"]["spellblock"]
    return team_stats

def main():
    team1 = []
    team2 = []

    print("Enter the names of champions for Team 1:")
    for i in range(5):
        team1.append(input(f"Champion {i+1}: ").capitalize())

    print("\nEnter the names of champions for Team 2:")
    for i in range(5):
        team2.append(input(f"Champion {i+1}: ").capitalize())

    team1_stats = sum_team_stats(team1)
    team2_stats = sum_team_stats(team2)

    print("\nTeam 1 Stats:", team1_stats)
    print("Team 2 Stats:", team2_stats)

if __name__ == "__main__":
    main()
