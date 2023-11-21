### Airline Planning and Optimisation ###
# Point to point network model

import gurobipy as gp

N_aircraft  = 2
Revenue = 0.18

Aircraft = {
    "cask":     0.12,
    "lf":       0.75,
    "seats":    120,
    "speed":    870,
    "lto":      1/3,
    "bt":       70,
}

Demand = [[0,1000,200],
          [1000,0,300],
          [200,300,0 ]]

Distance = [[0,2236,3201],
            [2236,0,3500],
            [3201,3500,0]]


model = gp.Model("MILP_P2P")

# Define variables
x = {}
for i in range(3):
    for j in range(3):
        x[i, j] = model.addVar(vtype =gp.GRB.INTEGER,name = "x(%d,%d)"%(i,j))

z = {}
for i in range(3):
    for j in range(3):
        z[i, j] = model.addVar(vtype =gp.GRB.INTEGER,name = "z(%d,%d)"%(i,j))

model.update()

# Define constraints
demand = {}
for i in range(3):
    for j in range(3):
        demand[i,j] = model.addConstr(x[i,j],"<=",Demand[i][j],name="Demand(%d,%d)"%(i,j))

capacity = {}
for i in range(3):
    for j in range(3):
        capacity[i,j] = model.addConstr(x[i,j],"<=",z[i,j]*Aircraft["lf"]*Aircraft["seats"],
                                        name="Capacity(%d,%d)"%(i,j))


continuity = {}
for i in range(3):
    continuity[i] = model.addConstr(gp.quicksum(z[i,j] for j in range(3)),"=",
                                    gp.quicksum(z[j,i] for j in range(3)),
                                    name="Continuity(%d)"%(i))

productivity = {}
productivity[0] = model.addConstr(gp.quicksum(((Distance[i][j] / Aircraft['speed'])+Aircraft['lto'])*z[i,j] for i in range(3) for j in range(3)),
                                  "<=", Aircraft['bt']*N_aircraft, name="Productivity")

## Define objective
obj = gp.LinExpr()

for i in range(3):
    for j in range(3):
        obj += (Revenue*Distance[i][j]*x[i,j] - Aircraft['cask']*Aircraft['seats']*Distance[i][j]*z[i,j])


model.setObjective(obj,gp.GRB.MAXIMIZE)

model.update()
model.write("Airline_Networks/MCF_Model_P2P.lp")
model.optimize()

# Display solutions
for v in model.getVars():
    print(v.varName,v.x)