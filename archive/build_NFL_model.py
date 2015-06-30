# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:11:50 2015

Author: Andrew
"""

from gurobipy import *
#from build_NFL_variables import *
#from build_NFL_constraints import *

def make_gurobi_model(modelName, sense):
    myModel = Model(modelName)
    myModel.modelSense = sense
    myModel.update()
    return myModel
    
def main():
    newModel = make_gurobi_model('NFL_sched', GRB.MAXIMIZE)
    # = make_db()    
    # = make_data_structures()
    # = make_variables()
    # = make_constraints()
    newModel.optimize()
    
    # Write the LP file
    newModel.write('NFL_sched.lp')
    
    # Solve the optimization model
    newModel.optimize()
    
    # Extract the solution
    newModel.write('NFL_sched.sol')
    
    # Print scheduled games with scores
    print('')
    for h in teams:
        for a in home_games[h]:
            for w in week:
                if games[h,a,w].x > 0:
                    print h, a, w, games[h,a,w].x

if __name__ == '__main__':
    main()