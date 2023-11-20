##Northern Airline Company problem:

import gurobipy as gp

# Cost values expressed in millions of dollar
unit_prod = [1.08, 1.11, 1.10, 1.13]
unit_storage = 0.015

# Maximum production
max_production = [25, 35, 30, 10]

# Sheduled demand
demand = [10, 15, 25, 20]

model = gp.Model("Northern Airline Company")

## Define variables
x = {}
for i in range(4):
    for j in range(4-i):
        x[i,j+i] = model.addVar(vtype ="C", name='x(%d,%d)'%(i,j+i))

model.update()

## Define constraints

# Production side
for i in range(4):
    model.addConstr(gp.quicksum(x[i,j+i] for j in range(4-i)),
                    "<=",max_production[i],name="Production(%d)"%i)

# demand side
for i in range(4):
    model.addConstr(gp.quicksum(x[j,i] for j in range(i+1)),
                    ">=",demand[i],name="Demand(%d)"%i)

## Define objective

obj = gp.LinExpr()

for i in range(4):
    for j in range(4-i):
        obj += (unit_prod[i] + j*unit_storage)*x[i,j+i]


model.setObjective(obj,gp.GRB.MINIMIZE)
model.update()

# Write LP formulation for tools such as LP solve or to DEBUG
model.write("basic_optimisation/NAC_MCF_Model.lp")

# Solve using gurobi
model.optimize()

# Display solutions
for v in model.getVars():
    print(v.varName,v.x)