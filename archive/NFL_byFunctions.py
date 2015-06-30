# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:27:36 2015

Author: Andrew
"""

from gurobipy import *

def createGurobiModel(modelName, sense):
    myModel = Model(modelName)
    myModel.modelSense = sense
    myModel.update()
    return myModel
    
def getData():
    pass

def makeVariables(myModel):
    pass

def makeConstraints(myModel, myVars):
    pass

def main():
    newModel = createGurobiModel('NFL_scheduling', GRB.MAXIMIZE)
    # = getData()
    # = makeVariables()
    # = makeConstraints()
    newModel.optimize()
    
    for var in myVars:
        if myVars[var].x > 0:
            print var, myVars[var].x

if __name__ == '__main__':
    main()