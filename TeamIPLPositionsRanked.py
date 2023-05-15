import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
# import html5lib
import seaborn as sns
import pandas as pd

""""
IPL teams Ranked Scorecard 2023
"""

url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/points-table-standings"
# fetch the scorecard of IPL teams
keys = ['Total_match', 'Won_match', 'Lost_match', 'Tie_match', 'No_result', 'Net Run Rate']

# Create an empty dictionary
list_of_dicts = [] # create an empty list to hold the dictionaries

resp = requests.get(url)
soup = BeautifulSoup(resp.content,'html5lib')

# find the table element inside the first div
table = soup.find('tbody', attrs= {"class":'ds-text-center'})

# Create an empty dictionary to store the information for each team
team_dict = {}

# Find all the team names
team_names = table.findAll("span", attrs={"class":"ds-text-tight-s ds-font-bold ds-uppercase ds-text-left"})

# Iterate over each row in the table
for row in table.find_all("tr", attrs={"class":"ds-text-tight-s"}):
    # Create a dictionary to store the information for this row
    row_dict = {}
    # Get the data cells for this row
    data = row.find_all("td", attrs={"class":"ds-w-0 ds-whitespace-nowrap ds-min-w-max"})
    # Iterate over the keys and the data cells
    for i in range(len(keys)):
        # Set the dictionary value to the current data cell's text
        row_dict[keys[i]] = data[i].text.strip()
    # Get the team name for this row
    team_name = team_names.pop(0).text.strip()
    # Add the row dictionary to the team dictionary with the team name as the key
    team_dict[team_name] = row_dict

# result team
# print(team_dict)
# # write IPL data to a JSON file
# with open('IPLTeamRanked.json', 'w') as file:
#     json.dump(team_dict, file, indent=4)

#define x-axis and y-axis data
teams = list(team_dict.keys())
won_match = [int(team_dict[team]['Won_match']) for team in teams]
total_match = [int(team_dict[team]['Total_match']) for team in teams]
lost_match = [int(team_dict[team]['Lost_match']) for team in teams]
net_run_rate = [float(team_dict[team]['Net Run Rate']) for team in teams]

# plot data
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(teams, won_match, color='blue',alpha=1,label='Won Matches')
ax.bar(teams, total_match, color='orange',label='Total Matches')
ax.bar(teams, lost_match, color='red',label='Lost Matches')

# Add Net Run Rate data as a separate histogram
ax2 = ax.twinx()
ax2.plot(teams, net_run_rate, color='green',marker='o',label='Net Run Rate',markersize=8)

ax2.set_ylim([-1, 1])
ax2.set_ylabel('Net Run Rate')

# Annotate markers with net run rate value
for i, rate in enumerate(net_run_rate):
    ax2.annotate(str(rate), (i, rate), ha='left', va='bottom', fontsize=8)

ax.set_xlabel('Teams')
ax.set_ylabel('Matches')
ax.set_title('Matches Won vs Total Matches')
ax.legend()

# Set x-axis labels rotation angle and adjust other properties
ax.set_xticklabels(teams, rotation=45, ha='right', fontsize=8)
plt.subplots_adjust(bottom=0.2)

plt.show()
