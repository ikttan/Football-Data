# Copyright (c) 2016, Ian Tan
# Data Science Institute, Multimedia University

import numpy as np  # Numerical Python
import pandas as pd  # To use the DataFrame structure
import matplotlib.pyplot as plt  # Plotting library

import requests  # Using this library for my HTTP requests
import json  # I work mainly with JSON formatted data

base_url = 'http://api.football-data.org'
headers = {'X-Auth-Token': 'add6aabec52f418a8d261a140dc970d6', 'X-Response-Control': 'minified'}

## Get the seasons
uri = '/v1/soccerseasons/'
filter = {'season': '2015'}
try:
    response = requests.get(base_url + uri, params=filter, headers=headers)
    seasons = pd.DataFrame(response.json(), columns=['id', 'caption'])
    seasons['Season'] = filter.get('season')
except Exception as e:
    print("[Seasons Errno {0}] {1}".format(e.args, e.message))

# For 2015/2016 season

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
        league = response.json()['leagueCaption']
        # This next line is tricky :P
        goals = pd.DataFrame(response.json()['standing'], columns=['goals'])
        totalGoals = goals['goals'].sum()
        # print 'Total goals for ' + league + ' are: ' + str(totalGoals)
        leagueGoals = leagueGoals.append({'league': league, 'goals': totalGoals}, ignore_index=True)
    except Exception as e:
        print("[League Errno {0}] {1}".format(e.args, e.message))

print leagueGoals.to_string()

# Plotting and visualization with matplotlib
plt.interactive(False)
# Haven't figured out how to relabel the ticks on the x-axis
# plt.xticks()
ax = leagueGoals.plot.bar(title='Total Number of Goals Scored in Major European Leagues')
ax.set_xlabel('League', fontsize=12)
ax.set_ylabel('No. of Goals', fontsize=12)
plt.show()
