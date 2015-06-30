from gurobipy import *

# define our indexes
Ingredients = ('Scrap1', 'Scrap2', 'Scrap3', 'Scrap4', 'Ni', 'Cr', 'Mo')
Composition = ('C', 'Ni', 'Cr', 'Mo')

# define our data
PercentComp = {
                ('Scrap1', 'C'):0.008, 
                ('Scrap1', 'Ni'):0.18,
                ('Scrap1', 'Cr'):0.120,
                ('Scrap1', 'Mo'):0.0,
                ('Scrap2', 'C'):0.0070,
                ('Scrap2', 'Ni'):0.032,
                ('Scrap2', 'Cr'):0.011,
                ('Scrap2', 'Mo'):0.001,
                ('Scrap3', 'C'):0.0085,
                ('Scrap3', 'Ni'):0.0,
                ('Scrap3', 'Cr'):0.0,
                ('Scrap3', 'Mo'):0.0,
                ('Scrap4', 'C'):0.004,
                ('Scrap4', 'Ni'):0.0,
                ('Scrap4', 'Cr'):0.0,
                ('Scrap4', 'Mo'):0.0,
                ('Ni', 'C'):0.0,
                ('Ni', 'Ni'):1.0,
                ('Ni', 'Cr'):0.0,
                ('Ni', 'Mo'):0.0,
                ('Cr', 'C'):0.0,
                ('Cr', 'Ni'):0.0,
                ('Cr', 'Cr'):1.0,
                ('Cr', 'Mo'):0.0,
                ('Mo', 'C'):0.0,
                ('Mo', 'Ni'):0.0,
                ('Mo', 'Cr'):0.0,
                ('Mo', 'Mo'):1.0
              }

ResourceLimits = {
                    'Scrap1': 75,
                    'Scrap2': 250,
                    'Scrap3': GRB.INFINITY,
                    'Scrap4': GRB.INFINITY,
                    'Ni': GRB.INFINITY,
                    'Cr': GRB.INFINITY,
                    'Mo': GRB.INFINITY
                 }
                 
Cost = {
        'Scrap1': 16,
        'Scrap2': 10,
        'Scrap3': 8,
        'Scrap4': 9,
        'Ni': 48,
        'Cr': 60,
        'Mo': 53
       }

ProdLimit = 1000

MaxBlend = {
            'C': .0075,
            'Ni': .035,
            'Cr': .012,
            'Mo':.013
           }
           
MinBlend = {
            'C': .0065,
            'Ni': .030,
            'Cr': .010,
            'Mo':.011
           }
           
# create the modeling
steel = Model()
steel.modelSense = GRB.MINIMIZE
steel.update()


# create the variables
mix = {}
for ing in Ingredients:
    mix[ing] = steel.addVar(vtype = GRB.CONTINUOUS, obj = Cost[ing], 
                            ub = ResourceLimits[ing], name = ing)
    
steel.update()

# create the first constraint that limits the production to 1000 kg
steelConstrs = {}
constrName = 'Production_Limit'
steelConstrs[constrName] = steel.addConstr(quicksum(mix[i] for i in Ingredients) 
                                           == ProdLimit, name = constrName)
steel.update()

#create the blending constraints that add the upper bound on the composition
for comp in Composition:
    constrName = 'Max_Blend_' + comp
    steelConstrs[constrName] = steel.addConstr(quicksum(mix[i]*PercentComp[i,comp] 
                                               for i in Ingredients) 
                                               <= MaxBlend[comp]*quicksum(mix[i] 
                                               for i in Ingredients), 
                                               name = constrName)
steel.update()


#create the blending constraints that add the lower bound on the composition
for comp in Composition: 
    constrName = 'Min_Blend_' + comp
    steelConstrs[constrName] = steel.addConstr(quicksum(mix[i]*PercentComp[i,comp] 
                                               for i in Ingredients) 
                                               >= MinBlend[comp]*quicksum(mix[i] 
                                               for i in Ingredients), 
                                               name = constrName)
steel.update()

# write the LP file so you can at least see what the model looks like
steel.write('steel.lp')

# solve the optimization model
steel.optimize()

#extract the solution
steel.write('steel.sol')

for m in mix:
    if mix[m].x > 0:
        print m, mix[m].x


