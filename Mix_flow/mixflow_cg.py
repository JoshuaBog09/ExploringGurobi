import gurobipy as gp
import numpy as np

Flight = np.genfromtxt("flight.txt", delimiter="\t", dtype="unicode")
Itineraries = np.genfromtxt("itineraries.txt", delimiter="\t", dtype="unicode")
Recapture = np.genfromtxt("recapture.txt", delimiter="\t", dtype="unicode")

r_set = [-1]

L = len(Flight)
P = len(Itineraries)

CAP = {}

for i in range(L):
    CAP[i] = int(Flight[i,5])

D = {}

for p in range(P):
    D[p] = int(Itineraries[p,3])

delta = {}

for idx_i, i in enumerate(Flight[:, 0]):
    for idx_p, p in enumerate(Itineraries[:, 6:8]):
        if i in p:
            delta[idx_i, idx_p] = 1
        else:
            delta[idx_i,idx_p] = 0

print(delta)

Q = {}

for i in range(L):
    Q[i] = sum([delta[i,p]*D[p] for p in range(P)])

b = {}

for line_r in Recapture[:,:]:
    b[int(line_r[1])-1, int(line_r[2])-1] = float(line_r[3])


for p1 in range(P):
    for p2 in range(P):
        if (p1, p2) not in b.keys():
            if p1 == p2:
                b[p1, p2] = 1
            else:
                b[p1, p2] = 0

for p in range(P):
    b[p,-1] = 1

for p in range(P):
    b[-1,p] = 0

fare = {}

for p in range(P):
    fare[p] = int(Itineraries[p,4].replace("$", ""))

fare[-1] = 0

model = gp.Model("")

## Decision variables
t = {}

for p in range(P):
    for r in r_set:
        t[p, r] = model.addVar(vtype=gp.GRB.INTEGER, name="t(%d,%d)"%(p,r))

model.update()

#unconstrained passenger demands by itinerary

C4 = {}
for i in range(L):
    C4[i] = model.addLConstr(gp.quicksum(delta[i, p]*t[p, r] for p in range(P) for r in r_set),
                             ">=", Q[i] - CAP[i], name='C4(%d)'%(i))


C5 = {}
for p in range(P):
    C5[p] = model.addLConstr(gp.quicksum(t[p, r] for r in r_set), "<=", D[p], name='C5(%d)'%(p))

##########################
### Objective Function ###
##########################
obj = gp.LinExpr()

for p in range(P):
    for r in r_set:
        obj += (fare[p] - b[p, r] * fare[r]) * t[p, r]

model.setObjective(obj,gp.GRB.MINIMIZE)
model.update()
# model.optimize()

relaxed_model = model.relax()
relaxed_model.optimize()

for id_t, val_t in t.items():
    print(f"{id_t} => {val_t}")

pis = []
for i in range(L):
    pis.append(relaxed_model.getConstrByName(f"C4({i})").Pi)

sigmas = []
for p in range(P):
    sigmas.append(relaxed_model.getConstrByName(f"C5({p})").Pi)

c = {}
for p in range(P):
    for r in range(P):
        c[p,r] = (fare[p] - sum([delta[i,p]*pis[i] for i in range(L)])) - b[p,r] * (fare[r] - sum([delta[i,r]*pis[i] for i in range(L)])) - sigmas[p]

print(c)

new_p = []
new_r = []

for p in range(P):
    for r in range(P):
        if c[p,r]<0:
            # columns to add -> t_p^r
            # Suggestion next to r = -1 add the indexes which belong to the various found values
            # Then loop over the newly created list of r values (repeat afterwards)

            # Question what to do with brp b(-1,p) to what is this equal
            print(f"({p},{r}) = ({c[p,r]})")
            
            new_p.append(p)
            new_r.append(r)

r_set.extend(new_r)
print(r_set)

# add t_1^0, t_2^3, t_11^10

for n_p, n_r in zip(new_p, new_r):
    t[n_p, n_r] = model.addVar(vtype=gp.GRB.INTEGER, name="t(%d,%d)"%(n_p,n_r))

model.update()

for i in range(L):
    model.remove(model.getConstrByName(f"C4({i})"))

for p in range(P):
    model.remove(model.getConstrByName(f"C5({p})"))
    

#unconstrained passenger demands by itinerary
C4 = {}
for i in range(L):

    expr1 = gp.LinExpr()
    expr2 = gp.LinExpr()

    for p in range(P):
        for r in r_set:
            try:
                expr1 += delta[i, p]*t[p, r]
            except:
                expr1 += 0

    for p in r_set:
        for r in range(P):
            try:
                expr2 += delta[i, p]*b[r, p]*t[r, p]
            except:
                expr2 += 0
    
    C4[i] = model.addLConstr(expr1-expr2,">=", Q[i] - CAP[i], name='C4(%d)'%(i))

# for i in range(L):
#     C4[i] = model.addLConstr(gp.quicksum(delta[i, p]*t[p, r] for p in range(P) for r in r_set) -
#                              gp.quicksum(delta[i, p]*b[p, r]*t[p, r] for p in range(P) for r in r_set),
#                              ">=", Q[i] - CAP[i], name='C4(%d)'%(i))

C5 = {}

for p in range(P):
    expr = gp.LinExpr()

    for r in r_set:
        try:
            expr += t[p, r]
        except:
            expr += 0
    
    C5[p] = model.addLConstr(expr, "<=", D[p], name='C5(%d)'%(p))

##########################
### Objective Function ###
##########################
obj = gp.LinExpr()

for p in range(P):
    for r in r_set:
        try:
            obj += (fare[p] - b[p, r] * fare[r]) * t[p, r]
        except:
            obj += 0

model.setObjective(obj,gp.GRB.MINIMIZE)
model.update()

relaxed_model = model.relax()
relaxed_model.update()
relaxed_model.optimize()
relaxed_model.write("cg.lp")

pis = []
for i in range(L):
    pis.append(relaxed_model.getConstrByName(f"C4({i})").Pi)

sigmas = []
for p in range(P):
    sigmas.append(relaxed_model.getConstrByName(f"C5({p})").Pi)

c = {}
for p in range(P):
    for r in range(P):
        c[p,r] = (fare[p] - sum([delta[i,p]*pis[i] for i in range(L)])) - b[p,r] * (fare[r] - sum([delta[i,r]*pis[i] for i in range(L)])) - sigmas[p]

new_p = []
new_r = []

for p in range(P):
    for r in range(P):
        if c[p,r]<0:
            # columns to add -> t_p^r
            # Suggestion next to r = -1 add the indexes which belong to the various found values
            # Then loop over the newly created list of r values (repeat afterwards)

            # Question what to do with brp b(-1,p) to what is this equal
            print(f"({p},{r}) = ({c[p,r]})")
            
            new_p.append(p)
            new_r.append(r)