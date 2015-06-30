#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ArbizAl
#
# Created:     16/06/2015
# Copyright:   (c) ArbizAl 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
#Create the Model Container
NFL=Model()
#specify model type
NFL.modelSense=GRB.MAXIMIZE
#
NFL.update()

#use Teams for find every home game, then iterate over every week
games={}
For t in teams:
    For a in homeGames[t]:#call every away opponent in list teams
        For w in WEEKS:#calls
            games[a,t,w,]=NFL.addVar(obj=1,vtype=GRB.BINARY, name a+'_'+t+'_'+cstr(w))#a is name away team, t is name of home team and w is week
NFL.update
#create a dictionary to hold all the contraints
myconstraint={}
#each game played once
for t in teams:
    for a in homeGames[t]:
        constrName='Game_'+a+'_'+t
        myconstraint[constrName]=NFL.addConstr(quicksum(games[a,t,w]for w in weeks)<=1)
        name=constrName)
NFL.update()
NFL.write('modelname')
NFL.optimize()

#Every team must play once a week for each week of the season
for t in teams:#iterate over each team and each week
    for w in weeks:
        constrName=t+'_'+plays+cstr(w)#cstr turns a number into a string, necessary for concatenation
        myconstraint[constrName]=NFL.addConstr(quicksum(games[a,t,w]
            for a in homegames[t])
            +quicksum(games[t,h,w] for h in away games[t])<=1,name=constrName)#when a team is away, opponent MUST be home
NFL.update()