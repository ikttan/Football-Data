# Copyright (c) 2016, Ian Tan
# Data Science Institute, Multimedia University

# Importing some standard libraries that I may or may not use
import numpy as np  # Numerical Python
import pandas as pd  # To use the DataFrame structure
import matplotlib.pyplot as plt  # Plotting library

import requests  # Using this library for my HTTP requests
import json  # I work mainly with JSON formatted data
import pymongo  # I plan to work predominantly with MongoDB to store JSON data


# Just a routine to pause for keyboard input
def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")


# Data structures basics with NumPy basics (ndarrays) and pandas (DataFrame)
# Data gathering - loading, storage and file formats

base_url = 'http://api.football-data.org'
headers = {'X-Auth-Token': 'add6aabec52f418a8d261a140dc970d6', 'X-Response-Control': 'minified'}

## Get the seasons
uri = '/v1/soccerseasons/'
filter = {'season': '2015'}
try:
    response = requests.get(base_url + uri, params=filter, headers=headers)
    # print response.url
    seasons = pd.DataFrame(response.json(), columns=['id', 'caption'])
    seasons['Season'] = filter.get('season')
    # print seasons
except Exception as e:
    print("[Seasons Errno {0}] {1}".format(e.args, e.message))

# For 2015/2016 season
# Bundesliga 394
# Premier League 398
# Serie A 401
# Ligue 1 396
# Primeira Luga 402
# Eredivisie 404

# Just using NumPy to create an array of list :P
leagues = np.array([['Bundesliga', 394],
                    ['Premier League', 398],
                    ['Serie A', 401],
                    ['Ligue 1', 396],
                    ['Primeira Liga', 402],
                    ['Eredivisie', 404]])

filter = ''

leagueGoals = pd.DataFrame()

for index in leagues[:, 1]:
    uri = '/v1/soccerseasons/' + index + '/leagueTable'
    try:
        response = requests.get(base_url + uri, params=filter, headers=headers)
        # print response.url
        # print json.dumps(response.json(), sort_keys=True, indent=2)
        league = response.json()['leagueCaption']
        # This next line is tricky :P
        goals = pd.DataFrame(response.json()['standing'], columns=['goals'])
        # As the DataFrame now only contains the number of goals, I simply just sum up the whole DataFrame
        # or you can specify the column 'goals'
        totalGoals = goals['goals'].sum()
        # print totalGoals
        # print 'Total goals for ' + league + ' are: ' + str(totalGoals)
        leagueGoals = leagueGoals.append({'league': league, 'goals': totalGoals}, ignore_index=True)
    except Exception as e:
        print("[League Errno {0}] {1}".format(e.args, e.message))

# Data marshalling - clean transform, merge and reshape{'league': league, 'goals': totalGoals}

print leagueGoals.to_string()

# Plotting and visualization with matplotlib
# The line below is because I am using PyCharm non-interactive mode, else the plot will not show - Doesn't WORK!
plt.interactive(False)
# Haven't figured out how to relabel the ticks on the x-axis
# plt.xticks()
# leagueGoals.plot.bar(x='League', y='Number of Goals', title='Total Goals Scored in Major European Leagues')
ax = leagueGoals.plot.bar(title='Total Number of Goals Scored in Major European Leagues')
ax.set_xlabel('League', fontsize=12)
ax.set_ylabel('No. of Goals', fontsize=12)

plt.show()
# pause()
