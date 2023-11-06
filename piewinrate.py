import json
import matplotlib.pyplot as plt

# Reading data from 'game_data.json'
with open('game_data.json', 'r') as file:
    data = json.load(file)

# Extracting average winrate for each team
team_100_winrate = data["team_100_avg_winrate"]
team_200_winrate = data["team_200_avg_winrate"]

# Labels for the pie chart
labels = 'Team 100', 'Team 200'

# Values for each section of the pie chart
sizes = [team_100_winrate, team_200_winrate]

# Setting up the pie chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')

# Displaying the pie chart
plt.title('Average Winrate of Each Team')
plt.show()
