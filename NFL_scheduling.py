# -*- coding: utf-8 -*-
"""
Name: NFL_scheduling
Purpose: Optimization model to create 2015 NFL schedule
Created: Sun Jun 21 19:41:05 2015
Author: Andrew Flack
Copyright: (c) Andrew Flack 2015
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
                games[a,h,w,s] = NFL_sched.addVar(obj = team_priority[h]+team_priority[a]+week_priority[w]+slot_priority[s], 
                    vtype = GRB.BINARY, ub = 1, name = a +'_'+ h + '_' + str(w) + s)
                
NFL_sched.update()

Y = {}

for h in teams:
    for a in home_games[h]:
        for w in week:
            Y[a,h,w] = NFL_sched.addVar(obj = 1, vtype = GRB.BINARY, name = 'Y_' + a +'_'+ h + '_' + str(w))

NFL_sched.update()

# Create a dictionary to hold contraints
myConsts = {}

####### CORE MODEL CONSTRAINTS #######

# 1 - Each game will be played exactly once during the season
for h in teams:
    for a in home_games[h]:
        constrName = 'GamePlayedOnce' + a + '_' + h + '_' + s
        myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,s] for w in week for s in slots) == 1, name = constrName)
        
NFL_sched.update()

# 2 - Every team must play once a week for each week of the season
for t in teams:
    for w in week:
        constrName = t + '_PlaysOnceInWeek_'+ str(w)
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,t,w,s] for a in home_games[t] for s in slots) + 
                                                    quicksum(games[t,h,w,s] for h in away_games[t] for s in slots)) == 1, name = constrName)

NFL_sched.update()

# 3 - BYE games can only happen during weeks 4 through the week before 
# Thanksgiving. In 2015, Thanksgiving is week 12, therefore BYE games can only 
# be played from week 4 through week 11). And BYE games can only happen 
# during SunE slot.
constrName = 'BYE_SunE'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',h,w,s] for s in slots if s != 'SunE' for h in teams for w in week) <= 0, name = constrName)

NFL_sched.update()        

for h in teams:
    constrName = h + '_BYE_Week4-11'
    myConsts[constrName] = NFL_sched.addConstr((quicksum(games['BYE',h,w,'SunE'] for w in range(1,4)) + 
                                                quicksum(games['BYE',h,w,'SunE'] for w in range(12,18))) <= 0, name = constrName)

NFL_sched.update()

# 4 - No team that had an early BYE week (week 4) the previous season will 
# have an early BYE (week 4) in the present season
constrName = 'HadEarlyBYE'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',h,4,s] for h in early_bye for s in slots) <= 0, name = constrName)

NFL_sched.update()

# 5 - Teams having an international game will have their BYE game the 
# following week
for w in intl_series:
    constrName = str(w) + '_ByeAfterIntl_away'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',intl_series[w][0],w + 1,s] for s in slots) >= 1, name = constrName)

NFL_sched.update()

for w in intl_series:
    constrName = str(w) + '_ByeAfterIntl_home'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games['BYE',intl_series[w][1],w + 1,s] for s in slots) >= 1, name = constrName)

NFL_sched.update()

# 6 - Teams playing an international game will be at home the week before the 
# international game 
for w in intl_series:
    constrName = str(w) + '_HomeBeforeIntl_away'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,intl_series[w][0],w-1,s] for a in home_games[intl_series[w][0]] for s in slots) >= 1, name = constrName)

NFL_sched.update()

for w in intl_series:
    constrName = str(w) + '_HomeBeforeIntl_home'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,intl_series[w][1],w-1,s] for a in home_games[intl_series[w][1]] for s in slots) >= 1, name = constrName)

NFL_sched.update()

# 6a - International series games are correct
for w in intl_series:
    constrName = str(w) + '_IntlGame'
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[intl_series[w][0],intl_series[w][1],w,s] for s in slots) >= 1, name = constrName)

NFL_sched.update()

## 7 - Two teams cannot play back to back games or play against each other the 
## week before and the week after a BYE
#for c in division:
#    for d in division[c]:
#        for t1 in range(0,3):
#            for t2 in range(t1+1,4):
#                team1 = division[c][d][t1]
#                team2 = division[c][d][t2]
#                for i in range(1,17):
#                    constrName = team1 + '_' + team2 + '_NoBackToBack'
#                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w,s] for w in [i,i+1] for s in slots) + 
#                                                                quicksum(games[team2,team1,w,s] for w in [i,i+1] for s in slots)) <= 1, name = constrName)
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
#                    constrName = team1 + '_BackBYEBack_' + str(i)
#                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w,s] for w in [i,i+2] for s in slots) + 
#                                                                quicksum(games[team2,team1,w,s] for w in [i,i+2] for s in slots) + 
#                                                                quicksum(games['BYE',team1,i+1,s] for s in slots)) <= 2, name = constrName)
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
#                    constrName = team2 + '_BackBYEBack_' + str(i)
#                    myConsts[constrName] = NFL_sched.addConstr((quicksum(games[team1,team2,w,s] for w in [i,i+2] for s in slots) + 
#                                                                quicksum(games[team2,team1,w,s] for w in [i,i+2] for s in slots) + 
#                                                                quicksum(games['BYE',team2,i+1,s] for s in slots)) <= 2, name = constrName)
#
#NFL_sched.update()
#
## 8 - No team plays 4 home/away games consecutively during the season
#for h in teams:
#    for w in range(1,15):
#        constrName = 'NoFourConsecutive_' + h + '_' + str(w) + '_HomeGames'
#        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for a in home_games[h] for s in slots)+
#                                                    quicksum(games[a,h,w+1,s] for a in home_games[h] for s in slots)+
#                                                    quicksum(games[a,h,w+2,s] for a in home_games[h] for s in slots)+
#                                                    quicksum(games[a,h,w+3,s] for a in home_games[h] for s in slots))<= 3, name = constrName)
#
#NFL_sched.update()
#
#for a in teams:
#    for w in range(1,15):
#        constrName = 'NoFourConsecutive_' + a + '_' + str(w) + '_AwayGames'
#        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for h in away_games[a] for s in slots)+
#                                                    quicksum(games[a,h,w+1,s] for h in away_games[a] for s in slots)+
#                                                    quicksum(games[a,h,w+2,s] for h in away_games[a] for s in slots)+
#                                                    quicksum(games[a,h,w+3,s] for h in away_games[a] for s in slots))<= 3, name = constrName)
#
#NFL_sched.update()
#
## 9 - No team plays 3 consecutive home/away games during weeks 1,2,3,4,5 
## and 15,16,17
#for h in teams:
#    for w in [1,2,3,15]:
#        constrName = 'NoThreeConsecutive_' + h + '_HomeGames'
#        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for a in home_games[h] if a != 'BYE' for s in slots)+
#                                                    quicksum(games[a,h,w+1,s] for a in home_games[h] if a != 'BYE' for s in slots)+
#                                                    quicksum(games[a,h,w+2,s] for a in home_games[h] if a != 'BYE' for s in slots))<= 2, name = constrName)
#
#NFL_sched.update()
#
#for a in teams:
#    for w in [1,2,3,15]:
#        constrName = 'NoThreeConsecutive_' + h + '_AwayGames'
#        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[a,h,w,s] for h in away_games[a] if a != 'BYE' for s in slots)+
#                                                    quicksum(games[a,h,w+1,s] for h in away_games[a] if a != 'BYE' for s in slots)+
#                                                    quicksum(games[a,h,w+2,s] for h in away_games[a] if a != 'BYE' for s in slots))<= 2, name = constrName)
#
#NFL_sched.update()

# 10 - Week 17 games will consist only of divisional games
for c in division:
    for d in division[c]:
        constrName = str(c) + '_' + str(d) + '_' + '_Week17DivGame'
        myConsts[constrName] = NFL_sched.addConstr((quicksum(games[division[c][d][t1],division[c][d][t2],17,s] for t1 in range(0,3) for t2 in range(t1+1,4) for s in slots) + 
                                                    quicksum(games[division[c][d][t2],division[c][d][t1],17,s] for t1 in range(0,3) for t2 in range(t1+1,4) for s in slots)) >= 2, name = constrName)

NFL_sched.update()

####### ENHANCEMENT 1 CONSTRAINTS #######

# 11 - No team plays more than two road games against teams coming off their BYE
for a in teams:
    for h in away_games[a]:
        for w in range(4,12):
            constrName = a + '_RoadGamesAgainstTeamsOffBye_' + h + '_' + str(w) 
            myConsts[constrName] = NFL_sched.addConstr((games['BYE',h,w,'SunE'] + quicksum(games[a,h,w+1,s] for s in slots)) <= 1 + Y[a,h,w+1], name = constrName)
    constrName = a + '_NoMoreThan2_' + h
    myConsts[constrName] = NFL_sched.addConstr(quicksum(Y[a,h,w+1] for h in away_games[a] for w in range(4,12)) <= 2, name = constrName)
    
NFL_sched.update()

# 12 - New York Teams don’t want to play late home games on Yom Kippur and 
# Rosh Hashanah
constrName = 'NYJ_NoLateGamesJewishHolidays'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,'NYJ',w,s] for a in home_games['NYJ'] for w in jewish_holiday_weeks for s in late_slots) == 0, name = constrName)

NFL_sched.update()

constrName = 'NYG_NoLateGamesJewishHolidays'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,'NYG',w,s] for a in home_games['NYG'] for w in jewish_holiday_weeks for s in late_slots) == 0, name = constrName)

NFL_sched.update()

# 13 - There are two Monday night games on week 1
constrName = 'TwoMonNWeek1'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,1,'MonN2'] for h in teams for a in home_games[h]) >= 1, name = constrName)

NFL_sched.update()

# 14 - There is only one Monday night game during weeks 2 through 16
for w in range(1,17):
    constrName = 'OneMonNWeek2-16' + '_' + str(w)
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,'MonN1'] for h in teams for a in home_games[h]) >= 1, name = constrName)

NFL_sched.update()

# 15 - The home team for the late Monday night game on week 1 will be a team 
# one of the following five teams (ARI, SD, SF, OAK, SEA)
constrName = 'MonN2week1'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,1,'MonN2'] for h in MonN2week1 for a in home_games[h]) >= 1, name = constrName)

NFL_sched.update()

# 16 - There is only one Thursday night game during weeks 1 through 16
for w in range(1,17):
    constrName = 'OneThursWeek1-16' + '_' + str(w)
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,'ThurN'] for h in teams for a in home_games[h]) >= 1, name = constrName)

NFL_sched.update()

# 17 - There is only one Sunday night game scheduled during weeks 1 through 16
for w in range(1,17):
    constrName = 'OneSunNWeek1-16' + '_' + str(w)
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,'SunN'] for h in teams for a in home_games[h]) == 1, name = constrName)

NFL_sched.update()

# 18 - There will be two Saturday Night games, one each night in weeks 15 
# and 16.
for w in range(15,17):
    constrName = 'SatN_week_' + str(w)
    myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,'SatN'] for h in teams for a in home_games[h]) == 1, name = constrName)
    
NFL_sched.update()

# 19 - Superbowl champion opens the season at home on Thursday night of week 1
constrName = 'ChampOpensThurN'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,SBchamp,1,'ThurN'] for a in home_games[SBchamp]) >= 1, name = constrName)

NFL_sched.update()

# 20 - There are two Thanksgiving Day games: DET hosts the early game and 
# DAL hosts the late game.
constrName = 'DET_earlyThanksgiving'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,'DET',12,'ThurE'] for a in home_games['DET']) == 1, name = constrName)

NFL_sched.update()

constrName = 'DAL_lateThanksgiving'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,'DAL',12,'ThurL'] for a in home_games['DAL']) == 1, name = constrName)

NFL_sched.update()

constrName = 'ThurE_only_week_12'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,'ThurE'] for h in teams for a in home_games[h] for w in range(1,18)) == 1, name = constrName)

NFL_sched.update()

constrName = 'ThurL_only_week_12'
myConsts[constrName] = NFL_sched.addConstr(quicksum(games[a,h,w,'ThurL'] for h in teams for a in home_games[h] for w in range(1,18)) == 1, name = constrName)

NFL_sched.update()

####### ENHANCEMENT 2 CONSTRAINTS #######

# 21 - All teams playing road Thursday Night games are home the previous week
# 22 - FOX and CBS each will get 8 doubleheaders from week 1 through 16; both networks have a double header on Week 17
# 23 - FOX and CBS cannot have more than two double headers in a row during weeks 1 through 16.
# 24 - Every team must play exactly one short week game during the season.  A short week is defined as a Sunday game in week “w” and a Thursday game in week “w+1”.  As a result, two of the six teams playing on Thanksgiving Day must play against each other the following Thursday night.
# 25 - No team playing on Monday night in week “w” can play Thursday during week “w+1” or Thursday “w+2”
# 26 - NYG and NYJ cannot play at home on the same day
# 27 - NYG and NYJ cannot play on the same network on Sunday afternoon
# 28 - OAK and SF cannot play on the same network on Sunday afternoon
# 29 - West Coast and Mountain Teams (SD, SF, OAK, SEA, ARI, DEN) cannot play at home during the Sunday early afternoon game (1:00 PM EST)
# 30 - CBS and FOX will have at least three 1PM Sunday afternoon games each week.
# 31 - Teams can play no more than 5 prime time games in a season (with no more than 4 of them being broadcast on NBC).  Thanksgiving Day games do not count as prime time games.  Only Thursday night, Saturday Night, Sunday Night, and Monday Night count as prime time games.

### END CONSTRAINTS ###

# Write the LP file
NFL_sched.write('NFL_sched.lp')

# Set parameters
NFL_sched.setParam('SolutionLimit',1)

# Solve the optimization model
NFL_sched.optimize()

#NFL_sched.computeIIS()
#NFL_sched.write('IIS.ilp')

# Extract the solution
NFL_sched.write('NFL_sched.sol')

# Print scheduled games with scores
print('')
for h in teams:
    for a in home_games[h]:
        for w in week:
            for s in slots:
                if games[a,h,w,s].x > 0:
                    print a, h, w, s, games[a,h,w,s].x*team_priority[h]+team_priority[a]+week_priority[w]+slot_priority[s]
                            