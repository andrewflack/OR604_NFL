# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 21:46:03 2015

Author: Andrew
"""

import sqlite3

myConnection = sqlite3.connect('NFL_scheduling.db')
myCursor = myConnection.cursor()

#List: teams = all 32 teams in the NFL
sqlString = "SELECT team FROM team_info"
myCursor.execute(sqlString)

teams = []
b = myCursor.fetchall()

#for row in b:
#    print row[0]
#
#print '\n\n'

for row in b:
    if row[0] not in teams:
        teams.append(row[0])
#print(teams)

#List: week = a list of the number of weeks in the season
week = []
week = range(1, 18)
#print(week)

#Dictionary: Home games = use the team name as the key and use a list of home 
#games for each team as the value
sqlString = """
            SELECT a.team, b.away_team 
            FROM team_info as a JOIN announced_games as b ON a.team = b.home_team
            """

myCursor.execute(sqlString)

b = myCursor.fetchall()

#for row in b:
#    print row[0], row[1]
#
#print '\n\n'

home_games = {}    
for row in b:
    if row[0] not in home_games:      
        home_games[row[0]]=[]          
    home_games[row[0]].append(row[1])  

#print home_games 

#Dictionary: Away games = use the team name as the key and use a list of away 
#games for each team as the value
sqlString = """
            SELECT a.team, b.home_team 
            FROM team_info as a JOIN announced_games as b ON a.team = b.away_team
            """

myCursor.execute(sqlString)

b = myCursor.fetchall()

#for row in b:
#    print row[0], row[1]
#
#print '\n\n'

away_games = {}    
for row in b:
    if row[0] not in away_games:      
        away_games[row[0]]=[]          
    away_games[row[0]].append(row[1])  

#print away_games 


#Dictionary: Conference = all teams by conference – AFC or NFC
sqlString = """
            SELECT conference, team
            FROM team_info
            """
myCursor.execute(sqlString)

b = myCursor.fetchall()

#for row in b:
#    print row[0], row[1]
#
#print '\n\n'

conference = {}
for row in b:
    if row[0] not in conference:      
        conference[row[0]] = []          
    conference[row[0]].append(row[1])
    
#print(conference)

#Dictionary: Division = all teams by conference and division 
#HINT:  this can be done with a dictionary within a dictionary
sqlString = """
            SELECT conference, division, team
            FROM team_info
            """
myCursor.execute(sqlString)

b = myCursor.fetchall()

#for row in b:
#    print row[0], row[1], row[2]
#
#print '\n\n'

division = {}
for row in b:
    if row[0] not in division:
        division[row[0]] = {}
    if row[1] not in division[row[0]]:
        division[row[0]][row[1]] = []
    division[row[0]][row[1]].append(row[2])

#print(division)

early_bye = ['ARI', 'CIN', 'CLE', 'DEN', 'SEA', 'STL']

intl_series = {'DET': 8, 'BUF': 7, 'MIA': 4, 'NYJ': 4, 'JAX': 7, 'KC': 8}

myCursor.close()
myConnection.close()