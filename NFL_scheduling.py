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
"""

from gurobipy import *
import build_NFL_data_structures

# Create a model object that will contain the variables and constraints
# of the LP formulation
NFL_sched = Model()

# Set the model sense and update
NFL_sched.modelSense = GRB.MAXIMIZE
NFL_sched.update()

# Prepare data


# Create the variable
games = {}

for h in teams:
    for a in home_games[h]:
        for w in week:
            games[a,h,w] = NFL_sched.addVar(obj = 1, vtype = GRB.BINARY, 
            name = a +'_'+ h + '_' + str(w))
            
NFL_sched.update()

# Create a dictionary to hold contraints
myConsts = {}

### CONSTRAINTS ###

# 1 - Each game will be played exactly once during the season
for h in teams:
    for a in home_games[h]:
        constrName = 'game_' + a + '_' + h
        myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w] 
        for w in week) <= 1, name = constrName)
        
NFL_sched.update()

## 2 - Every team must play once a week for each week of the season
#for t in teams:
#    for w in week:
#        constrName = t + '_plays_'+ str(w)
#        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,t,w] for a in home_games[t])
#            + quicksum(games[t,h,w] for h in away_games[t])) <= 1, name = constrName)
#
#NFL_sched.update()
#
## 3 - BYE games can only happen during weeks 4 through the week before 
## Thanksgiving. In 2015, Thanksgiving is week 12, therefore BYE games can only 
## be played from week 4 through week 11).
#for h in teams:
#    constrName = h + '_BYE_'
#    myConsts[constrName] = NFL_sched.addConstr((quicksum(games['BYE',h,w] for w in range(1,4)) + quicksum(games['BYE',h,w] for w in range(12,18))) == 0, name = constrName)
#
#NFL_sched.update()
#
## 4 - No team that had an early BYE week (week 4) the previous season will 
## have an early BYE (week 4) in the present season
#for e in early_bye:
#    constrName = e + 'early_BYE'
#    myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',h,4] for h in teams) == 0, name = constrName)
#
#NFL_sched.update()
#
## 5 - Teams having an international game will have their BYE game the 
## following week
#for t in intl_series:
#    constrName = t + '_BYE_following_week'
#    myConsts[constrName] = NFL_sched.addConstr(games['BYE',t,intl_series[t] + 1] == 1, name = constrName)
#
#NFL_sched.update()
#
## 6 - Teams playing an international game will be at home the week before the 
## international game 
#for t in intl_series:
#    constrName = t + '_home_before_intl'
#    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,t,intl_series[t] - 1] for a in home_games[t]) == 1, name = constrName)
#
#NFL_sched.update()
#
## 7 - Two teams cannot play back to back games or play against each other the 
## week before and the week after a BYE
#for c in division:
#    for d in division[c]:
#        for t1 in range(0,3):
#            for t2 in range(t1+1,4):
#                team1 = division[c][d][t1]
#                team2 = division[c][d][t2]
#                for i in range(1,17):
#                    constrName = team1 + '_' + team2 + '_' + str(i)
#                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w] for w in [i,i+1]) + 
#                    quicksum(games[team2,team1,w] for w in [i,i+1])) <= 1, name = constrName)
#
#NFL_sched.update()
#
#for c in division:
#    for d in division[c]:
#        for t1 in range(0,3):
#            for t2 in range(t1+1,4):
#                team1 = division[c][d][t1]
#                team2 = division[c][d][t2]
#                for i in range(1,16):
#                    constrName = team1 + '_BYE_' + str(i)
#                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w] for w in [i,i+2]) + 
#                    quicksum(games[team2,team1,w] for w in [i,i+2]) + games['BYE',team1,i+1]) <= 2, name = constrName)
#
#NFL_sched.update()
#
#for c in division:
#    for d in division[c]:
#        for t1 in range(0,3):
#            for t2 in range(t1+1,4):
#                team1 = division[c][d][t1]
#                team2 = division[c][d][t2]
#                for i in range(1,16):
#                    constrName = team2 + '_BYE_' + str(i)
#                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w] for w in [i,i+2]) + 
#                    quicksum(games[team2,team1,w] for w in [i,i+2]) + games['BYE',team2,i+1]) <= 2, name = constrName)
#
#NFL_sched.update()

# 8 - No team plays 4 away/home games consecutively during the season

# 9 - No team plays 3 consecutive home/away games during weeks 1,2,3,4,5 
# and 15,16,17

# 10 - Week 17 games will consist only of divisional games

# 11 - No team plays more than two road games against teams coming off their BYE
# see pg 71 in notebook

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
            if games[a,h,w].x > 0:
                print a, h, w, games[a,h,w].x