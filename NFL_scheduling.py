# -*- coding: utf-8 -*-
"""
Name: NFL_scheduling
Purpose: Optimization model to create 2015 NFL schedule
Created: Sun Jun 21 19:41:05 2015
Author: Andrew Flack
Copyright: (c) Andrew Flack 2015
"""

"""
TO DO:
- clean up constraint names
- try to reformulate constraints 3-6 to remove equalities
- constraint 7 introduces zero half cuts
- constraint family 7 introduces constraints with the same name
"""

from gurobipy import *
import build_NFL_data_structures

# Create a model object that will contain the variables and constraints
# of the LP formulation
NFL_sched = Model()

# Set the model sense and update
NFL_sched.modelSense = GRB.MAXIMIZE
NFL_sched.update()

# Create the variable
games = {}

for h in teams:
    for a in home_games[h]:
        for w in week:
            for s in slots:
                games[a,h,w,s] = NFL_sched.addVar(obj = team_priority[h]*team_priority[a]*week_priority[w]*slot_priority[s], vtype = GRB.BINARY, 
                    name = a +'_'+ h + '_' + str(w) + s)
                
NFL_sched.update()

# Create a dictionary to hold contraints
myConsts = {}

####### CORE MODEL CONSTRAINTS #######

# 1 - Each game will be played exactly once during the season
for h in teams:
    for a in home_games[h]:
        constrName = 'GamePlayedOnce' + a + '_' + h + '_' + s
        myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,s] for w in week for s in slots) <= 1, name = constrName)
        
NFL_sched.update()

# 2 - Every team must play once a week for each week of the season
for t in teams:
    for w in week:
        constrName = t + '_PlaysOnceInWeek_'+ str(w)
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,t,w,s] for a in home_games[t] for s in slots) + 
                                                    quicksum(games[t,h,w,s] for h in away_games[t] for s in slots)) >= 1, name = constrName)

NFL_sched.update()

# 3 - BYE games can only happen during weeks 4 through the week before 
# Thanksgiving. In 2015, Thanksgiving is week 12, therefore BYE games can only 
# be played from week 4 through week 11).
for h in teams:
    constrName = h + '_BYE_Week4-11'
    myConsts[constrName] = NFL_sched.addConstr((quicksum(games['BYE',h,w,s] for w in range(1,4) for s in slots) + 
                                                quicksum(games['BYE',h,w,s] for w in range(12,18) for s in slots)) == 0, name = constrName)

NFL_sched.update()

# 4 - No team that had an early BYE week (week 4) the previous season will 
# have an early BYE (week 4) in the present season
constrName = 'HadEarlyBYE'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',h,4,s] for h in early_bye for s in slots) == 0, name = constrName)

NFL_sched.update()

# 5 - Teams having an international game will have their BYE game the 
# following week
for t in intl_series:
    constrName = t + '_HasByeAfterIntl'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',t,intl_series[t] + 1,s] for s in slots) >= 1, name = constrName)

NFL_sched.update()

# 6 - Teams playing an international game will be at home the week before the 
# international game 
for t in intl_series:
    constrName = t + '_HomeBeforeIntl'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,t,intl_series[t] - 1,s] for a in home_games[t] for s in slots) >= 1, name = constrName)

NFL_sched.update()

# 7 - Two teams cannot play back to back games or play against each other the 
# week before and the week after a BYE
for c in division:
    for d in division[c]:
        for t1 in range(0,3):
            for t2 in range(t1+1,4):
                team1 = division[c][d][t1]
                team2 = division[c][d][t2]
                for i in range(1,17):
                    constrName = team1 + '_' + team2 + '_NoBackToBack'
                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w,s] for w in [i,i+1] for s in slots) + 
                                                                quicksum(games[team2,team1,w,s] for w in [i,i+1] for s in slots)) <= 1, name = constrName)

NFL_sched.update()

for c in division:
    for d in division[c]:
        for t1 in range(0,3):
            for t2 in range(t1+1,4):
                team1 = division[c][d][t1]
                team2 = division[c][d][t2]
                for i in range(1,16):
                    constrName = team1 + '_BackBYEBack_' + str(i)
                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w,s] for w in [i,i+2] for s in slots) + 
                                                                quicksum(games[team2,team1,w,s] for w in [i,i+2] for s in slots) + 
                                                                quicksum(games['BYE',team1,i+1,s] for s in slots)) <= 2, name = constrName)

NFL_sched.update()

for c in division:
    for d in division[c]:
        for t1 in range(0,3):
            for t2 in range(t1+1,4):
                team1 = division[c][d][t1]
                team2 = division[c][d][t2]
                for i in range(1,16):
                    constrName = team2 + '_BackBYEBack_' + str(i)
                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w,s] for w in [i,i+2] for s in slots) + 
                                                                quicksum(games[team2,team1,w,s] for w in [i,i+2] for s in slots) + 
                                                                quicksum(games['BYE',team2,i+1,s] for s in slots)) <= 2, name = constrName)

NFL_sched.update()

# 8 - No team plays 4 home/away games consecutively during the season
for h in teams:
    for w in range(1,15):
        constrName = 'NoFourConsecutive_' + h + '_' + str(w) + '_HomeGames'
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for a in home_games[h] for s in slots)+
                                                    quicksum(games[a,h,w+1,s] for a in home_games[h] for s in slots)+
                                                    quicksum(games[a,h,w+2,s] for a in home_games[h] for s in slots)+
                                                    quicksum(games[a,h,w+3,s] for a in home_games[h] for s in slots))<= 3, name = constrName)

NFL_sched.update()

for a in teams:
    for w in range(1,15):
        constrName = 'NoFourConsecutive_' + a + '_' + str(w) + '_AwayGames'
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for h in away_games[a] for s in slots)+
                                                    quicksum(games[a,h,w+1,s] for h in away_games[a] for s in slots)+
                                                    quicksum(games[a,h,w+2,s] for h in away_games[a] for s in slots)+
                                                    quicksum(games[a,h,w+3,s] for h in away_games[a] for s in slots))<= 3, name = constrName)

NFL_sched.update()

# 9 - No team plays 3 consecutive home/away games during weeks 1,2,3,4,5 
# and 15,16,17
for h in teams:
    for w in [1,2,3,15]:
        constrName = 'NoThreeConsecutive_' + h + '_HomeGames'
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for a in home_games[h] for s in slots)+
                                                    quicksum(games[a,h,w+1,s] for a in home_games[h] for s in slots)+
                                                    quicksum(games[a,h,w+2,s] for a in home_games[h] for s in slots))<= 2, name = constrName)

NFL_sched.update()

for a in teams:
    for w in [1,2,3,15]:
        constrName = 'NoThreeConsecutive_' + h + '_AwayGames'
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for h in away_games[a] for s in slots)+
                                                    quicksum(games[a,h,w+1,s] for h in away_games[a] for s in slots)+
                                                    quicksum(games[a,h,w+2,s] for h in away_games[a] for s in slots))<= 2, name = constrName)

NFL_sched.update()

# 10 - Week 17 games will consist only of divisional games
for c in division:
    for d in division[c]:
        constrName = str(c) + '_' + str(d) + '_' + '_Week17DivGame'
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[division[c][d][t1],division[c][d][t2],17,s] for t1 in range(0,3) for t2 in range(t1+1,4) for s in slots) + 
                                                    quicksum(games[division[c][d][t2],division[c][d][t1],17,s] for t1 in range(0,3) for t2 in range(t1+1,4) for s in slots)) >= 2, name = constrName)

NFL_sched.update()

####### ENHANCEMENT 1 CONSTRAINTS #######

# 11 - No team plays more than two road games against teams coming off their BYE
# see pg 71 in notebook

# 12 - New York Teams don’t want to play late home games on Yom Kippur and 
# Rosh Hashanah

# 13 - There are two Monday night games on week 1

# 14 - There is only one Monday night game during weeks 2 through 16

# 15 - The home team for the late Monday night game on week 1 will be a team 
# one of the following five teams (ARI, SD, SF, OAK, SEA)

# 16 - There is only one Thursday night game during weeks 1 through 16

# 17 - There is only one Sunday night game scheduled during weeks 1 through 16

# 18 - There will be two Saturday Night games, one each night in weeks 15 
# and 16 (The Saturday rule depends on how many Saturdays there are in 
# December and in which month week 17 falls.  Basically, if Thanksgiving 
# is week 12, then there are Saturday Night games during weeks 15 and 16.  
# If Thanksgiving occurs in week 13, there are two Saturday games - one early 
# and one late - that happen during week 16).

# 19 - Superbowl champion opens the season at home on Thursday night of week 1

# 20 - There are two Thanksgiving Day games: DET hosts the early game and 
# DAL hosts the late game.  (The networks alternate each year who gets the 
# early game and who gets the late game)


### END CONSTRAINTS ###

# Write the LP file
NFL_sched.write('NFL_sched.lp')

# Solve the optimization model
NFL_sched.optimize()

# Extract the solution
NFL_sched.write('NFL_sched.sol')

# Print scheduled games with scores
print('')
for h in teams:
    for a in home_games[h]:
        for w in week:
            for s in slots:
                if games[a,h,w,s].x > 0:
                    print a, h, w, s, games[a,h,w,s].x*team_priority[h]*team_priority[a]*week_priority[w]*slot_priority[s]