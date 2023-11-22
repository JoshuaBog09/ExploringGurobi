### Airline Planning and Optimisation ###
# Hub and spoke network model

import gurobipy as gp

Distance = [[0,1461,1536,975,4545,3888],
            [1461,0,336,973,5790,5177],
            [1536,336,0,1244,5671,5081],
            [975,973,1244,0,5515,4851],
            [4545,5790,5671,5515,0,691],
            [3888,5177,5081,4851,691,0]]

Demand = [[0,2509,1080,558,770,713],
          [2509,0,216,112,360,333],
          [1080,216,0,78,46,43],
          [558,112,78,0,32,30],
          [770,360,46,32,0,70],
          [713,333,43,30,70,0]]

Parameters = {
    "cask":     0.12,
    "yield":    0.16,
    "lf":       0.80,
    "seats":    150,
    "speed":    890,
    "lto":      20/60,
    "bt":       13*7,
    "fleet":    4,
}

G = [0,1,1,1,1,1]

model = gp.Model('MILP-Hub and Spoke Network')

## Define decision variables
# To define x,z,w |--> direct flow, number flights, flow with transfer at hub

x = {}
z = {}
w = {}
for i in range(6):
    for j in range(6):
        x[i, j] = model.addVar(vtype =gp.GRB.INTEGER,name = "x(%d,%d)"%(i,j))
        z[i, j] = model.addVar(vtype =gp.GRB.INTEGER,name = "z(%d,%d)"%(i,j))
        w[i, j] = model.addVar(vtype =gp.GRB.INTEGER,name = "w(%d,%d)"%(i,j))

model.update()

## Define constraints

c1 = {}
for i in range(6):
    for j in range(6):
        c1[i,j] = model.addConstr(x[i,j]+w[i,j],"<=",Demand[i][j],name="C1(%d,%d)"%(i,j))

c1star = {}
for i in range(6):
    for j in range(6):
        c1star[i,j] = model.addConstr(w[i,j],"<=",Demand[i][j]*G[i]*G[j],name="C1Star(%d,%d)"%(i,j))

c2 = {}
for i in range(6):
    for j in range(6):
        c2[i,j] = model.addConstr(x[i,j] + gp.quicksum(w[i,m] * (1-G[j]) for m in range(6))
                                  + gp.quicksum(w[m,j] * (1-G[i]) for m in range(6)),"<=",
                                   z[i,j]*Parameters['seats']*Parameters['lf'],name="C2(%d,%d)"%(i,j))
        
c3={}
for i in range(6):
    c3[i] = model.addConstr(gp.quicksum(z[i,j] for j in range(6)),"=",gp.quicksum(z[j,i] for j in range(6)),name="C3(%d)"%(i))

c4={}
c4[0] = model.addConstr(gp.quicksum(((Distance[i][j] / Parameters['speed'])+Parameters['lto'])*z[i,j] for i in range(6) for j in range(6)),
                        '<=',Parameters['bt']*Parameters['fleet'],name="C4(0)")

## Define objective
obj = gp.LinExpr()

for i in range(6):
    for j in range(6):
        obj += (Parameters['yield']*Distance[i][j]*(x[i,j]+w[i,j]) - Parameters['cask']*Parameters['seats']*Distance[i][j]*z[i,j])


model.setObjective(obj,gp.GRB.MAXIMIZE)

model.update()
model.write("Airline_Networks/MCF_Model_HandS.lp")
model.optimize()

# Display solutions
for v in model.getVars():
    print(v.varName,v.x)