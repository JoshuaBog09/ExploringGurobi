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
for p in range(recaptures.shape[0]):
    for r in range(recaptures.shape[0]):
        for recapture in recaptures[:,1:]:
            if p == int(recapture[0]) - 1 and r == int(recapture[1]) - 1:
                b[p, r] = float(recapture[2])
            else:
                b[p, r] = 0


capacity = {}
for i in range(flights.shape[0]):
    capacity[i] = model.addConstr(gp.quicksum(delta[i, r]*x[p, r] for p in range(itineraries.shape[0]) for r in range(itineraries.shape[0])),
                                  "<=", int(flights[i,-1]), name=f"Capacity({i})")


ucdemand = {}
for p in range(itineraries.shape[0]):

    constr = gp.LinExpr()
    
    for r in range(itineraries.shape[0]):
        try:
            constr += x[p, r]/b[p, r]
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
model.write("Mix_flow/Model_MF.lp") # 1.422000000000e+05
model.optimize()