### Airline Planning and Optimisation ###
# Fleet network model

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

Parameters_A310 = {
    "cask":     0.12,
    "lf":       0.80,
    "seats":    240,
    "range":    9600,
    "speed":    900,
    "lto":      20/60,
    "bt":       14*7,
    "fleet":    2,
    "cost":     ???,
}

Parameters_A320 = {
    "cask":     0.11,
    "lf":       0.80,
    "seats":    160,
    "range":    5400,
    "speed":    870,
    "lto":      12/60,
    "bt":       12*7,
    "fleet":    2,
    "cost":     ???,
}

Yield = 0.16
Budget = ???

Parameters = [Parameters_A310, Parameters_A320]

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
        for k in range(2):
            z[i, j, k] = model.addVar(vtype =gp.GRB.INTEGER,name = "z(%d,%d,%d)"%(i,j,k))
        w[i, j] = model.addVar(vtype =gp.GRB.INTEGER,name = "w(%d,%d)"%(i,j))

ac = {}
for i in range(2):
    ac[i] = model.addVar(vtype =gp.GRB.INTEGER,name = "ac(%d)"%(i))

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
        c2[i,j] = model.addConstr(x[i,j] + gp.quicksum(w[i,m]*(1-G[j]) for m in range(6)) + 
                                  gp.quicksum(w[m,j]*(1-G[i]) for m in range(6)), "<=", 
                                  gp.quicksum(z[i,j,k]*Parameters[k]['seats']*Parameters[k]['lf'] for k in range(2)),
                                  name="C2(%d,%d)"%(i,j))

c3 = {}   
for i in range(6):
    for k in range(2):
        c3[i,k] = model.addConstr(gp.quicksum(z[i,j,k] for j in range(6)),"=",gp.quicksum(z[j,i,k] for j in range(6)),name="C3(%d,%d)"%(i,k))

c4 = {}
for k in range(2):
    c4[0] = model.addConstr(gp.quicksum(((Distance[i][j] / Parameters[k]['speed'])+Parameters[k]['lto'])*z[i,j,k] for i in range(6) for j in range(6)),
                            '<=',Parameters[k]['bt']*ac[k], name="C4(%d)"%(k))
    
c5 = {}
for i in range(6):
    for j in range(6):
        for k in range(2):
            if Distance[i][j] <= Parameters[k]['range']:
                c5[i,j,k] = model.addConstr(z[i,j,k],"<=",10000, name="C5(%d%d%d)"%(i,j,k))
            else:
                c5[i,j,k] = model.addConstr(z[i,j,k],"<=",0 ,name="C5(%d%d%d)"%(i,j,k))

c6 = {}
c6[0] = model.addConstr(gp.quicksum(Parameters[k]['cost']*Parameters[k]['fleet'] for k in range(2)), "<=",
                        Budget, name="C6(0)")

## Define objective
obj = gp.LinExpr()

for i in range(6):
    for j in range(6):
        obj += (Yield*Distance[i][j]*(x[i,j]+w[i,j]) - 
                gp.quicksum(Parameters[k]['cask']*Parameters[k]['seats']*Distance[i][j]*z[i,j,k] for k in range(2)))


model.setObjective(obj,gp.GRB.MAXIMIZE)

model.update()
model.write("Airline_Networks/MCF_Model_HandS.lp")
model.optimize()

# Display solutions
for v in model.getVars():
    print(v.varName,v.x)