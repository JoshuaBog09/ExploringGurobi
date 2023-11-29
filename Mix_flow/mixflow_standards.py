import numpy as np
import gurobipy as gp


flights = np.genfromtxt("Mix_flow/flight.txt", delimiter="\t", dtype="unicode")
itineraries = np.genfromtxt("Mix_flow/itineraries.txt", delimiter="\t", dtype="unicode")
recaptures = np.genfromtxt("Mix_flow/recapture.txt", delimiter="\t")

model = gp.Model("MILP_MixFlow")

print(flights)
print(itineraries)
print(recaptures)

# define decision variables
x = {}
for p in range(itineraries.shape[0]):
    for r in range(itineraries.shape[0]):
        x[p,r] = model.addVar(vtype = gp.GRB.INTEGER, name = f"x({p},{r})")

model.update()

# define delta constant
delta = {}
for i, flight in enumerate(flights[:,0]):
    for p, path in enumerate(itineraries[:,6:]):
        if flight in path:
            d = 1
        elif flight not in path:
            d = 0
        delta[i,p] = d

# define b constant
b = {}
for recapture in recaptures[:,1:]:
    b[int(recapture[0])-1, int(recapture[1])-1] = float(recapture[2])


capacity = {}
for i in range(flights.shape[0]):
    capacity[i] = model.addConstr(gp.quicksum(delta[i, r]*x[p, r] for p in range(itineraries.shape[0]) for r in range(itineraries.shape[0])),
                                  "<=", int(flights[i,-1]), name=f"Capacity({i})")


ucdemand = {}
for p in range(itineraries.shape[0]):

    constr = gp.LinExpr()

    for r in recaptures[:,2].astype(int):
        try:
            constr += x[p, r-1]/b[p, r-1]
        except:
            constr += 0
    
    ucdemand[p] = model.addConstr(constr, "<=", int(itineraries[p,3]), name=f"ucDemand{p}")
    
## Define objective
obj = gp.LinExpr()

for p in range(itineraries.shape[0]):
    for r in range(itineraries.shape[0]):
        obj += x[p, r] * int(itineraries[r,4].strip().replace("$",""))


model.setObjective(obj,gp.GRB.MAXIMIZE)

model.update()
model.write("Mix_flow/Model_MF.lp")
model.optimize()