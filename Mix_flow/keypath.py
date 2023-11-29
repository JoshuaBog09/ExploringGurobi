import numpy as np
import gurobipy as gp


flights = np.genfromtxt("Mix_flow/flight.txt", delimiter="\t", dtype="unicode")
itineraries = np.genfromtxt("Mix_flow/itineraries.txt", delimiter="\t", dtype="unicode")
recaptures = np.genfromtxt("Mix_flow/recapture.txt", delimiter="\t")

model = gp.Model("MILP_KeyPath")

# define decision variables
t = {}
for p in range(itineraries.shape[0]):
    for r in range(itineraries.shape[0]):
        t[p,r] = model.addVar(vtype = gp.GRB.INTEGER, name = f"t({p},{r})")

model.update()

# define delta constant
delta = {}
for i, flight in enumerate(flights[:,0]):
    for p, path in enumerate(itineraries[:,6:]):
        if flight in path:
            d = 1
        elif flight not in path:
            d = 0
        delta[i, p] = d

# define b constant
b = {}
for p in range(recaptures.shape[0]):
    for r in range(recaptures.shape[0]):
        for recapture in recaptures[:,1:]:
            if p == int(recapture[0]) - 1 and r == int(recapture[1]) - 1:
                b[p, r] = float(recapture[2])
            else:
                b[p, r] = 0

Q = {}
for i in range(flights.shape[0]):
    Q[i] = gp.quicksum(delta[i, p]*int(itineraries[p, 3]) for p in range(itineraries.shape[0]))

CAP = {}
for i in range(flights.shape[0]):
    CAP[i] = int(flights[i,5])

# Constraint one
c1 = {}
for i in range(flights.shape[0]):
    c1[i] = model.addConstr(gp.quicksum(delta[i, p]*t[p, r] for p in range(itineraries.shape[0]) for r in range(itineraries.shape[0])) - 
                            gp.quicksum(delta[i, p]*b[r, p]*t[r, p] for r in range(itineraries.shape[0]) for p in range(itineraries.shape[0])),
                              ">=", Q[i] - CAP[i], name=f"C1({i})")

# Constraint two
c2 = {}
for p in range(itineraries.shape[0]):
    c2[p] = model.addConstr(gp.quicksum(t[p, r] for r in range(itineraries.shape[0])), "<=", 
                            int(itineraries[p, 3]), name=f"C2({p})")
    
## Define objective
obj = gp.LinExpr()

for p in range(itineraries.shape[0]):
    for r in range(itineraries.shape[0]):
        obj += (int(itineraries[p,4].strip().replace("$","")) - b[p, r]* int(itineraries[r,4].strip().replace("$","")))*t[p, r]


model.setObjective(obj,gp.GRB.MINIMIZE)

model.update()
model.write("Mix_flow/Model_KP.lp")
model.optimize()