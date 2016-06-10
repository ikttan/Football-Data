# Copyright (c) 2016, Ian Tan
# Data Science Institute, Multimedia University
#
# An experimental prediction application for EURO 2016

import httplib
import json

# awayTeam = ""
# homeTeam = ""
# For Euro, this code
# Gets the match id of the two teams given
# Do a head to head comparison to get past scores
# Do a independent form for each for last 5 - 10 matches

# Make a matrix
# ID:awayGoals:homeGoals:homeOrAwayOrNeutral:<vector of away form>:<vector of home form>
# try to get 5x13 matrix


# Define the parameters for the API
season = '424'

try:
    conn = httplib.HTTPConnection("api.football-data.org")
    # You don't actually need the authentication token
    headers = { 'X-Auth-Token': 'add6aabec52f418a8d261a140dc970d6', 'X-Response-Control': 'minified' }

    # Get the right teams from the season in question
    #conn.request('GET', '/v1/soccerseasons/' + season + '/teams', None, headers )
    #conn.request('GET', '/v1/soccerseasons/424/fixtures', None, headers)
    #response = conn.getresponse()
    #data = json.loads(response.read())
    #print json.dumps(data, sort_keys=True, indent=2)

    # Extract the ID of the team by iterating it over the total number of teams until found
    # For testing, we know 0 is France, the host
    #print data['teams']
    #teamID = '773'

    # # Get the fixtures for the team
    conn.request('GET', '/v1/fixtures/149855?head2head=15', None, headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    print json.dumps(data, sort_keys=True, indent=2)

    conn.close()
except Exception as e:
    print("[Error]")
