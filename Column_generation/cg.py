import numpy as np
import gurobipy as gp


flights = np.genfromtxt("Column_generation/flight.txt", delimiter="\t", dtype="unicode")
itineraries = np.genfromtxt("Column_generation/itineraries.txt", delimiter="\t", dtype="unicode")
recapture = np.genfromtxt("Column_generation/recapture.txt", delimiter="\t")

model = gp.Model("MILP_ColumnGeneration")

## iteration 0
r = 0
fare_r = 0

# Define variables
t = {}
for i in range(itineraries.shape[0]):
    t[i,0] = model.addVar(vtype =gp.GRB.INTEGER,name = "t(%d,r)"%(i+1))

model.update()

# Define constraints

demand = {}
for i in range(flights.shape[0]):
    const = gp.linExpr()
    
    for p in range(itineraries.shape[0]):
        
        if flights[i,0] in itineraries[i,6:7]:
            delta = 1
        else:
            delta = 0
        
        const += delta * t[i,0]
    
    demand[i] = model.addConstr(const, ">=", ...)

# objective function

obj = gp.LinExpr()

for p in range(itineraries.shape[0]):
    obj += (itineraries[p,4])*t[p]


model.setObjective(obj,gp.GRB.MINIMIZE)

model.update()
model.write("Column_generation/cg.lp")
model.optimize()

