import gurobipy as gp


cost = [2,3]

model = gp.Model("MILP_1")

x = {}

for i in range(2):
    x[i] = model.addVar(obj= cost[i], vtype ="C",
                        name = "x(%d)"%i, )

model.update()

model.addConstr(-3*x[0] + x[1],"<=",1,name="Const1")
model.addConstr(4*x[0] + 2*x[1],"<=",20,name="Const2")
model.addConstr(4*x[0] - x[1],"<=",10,name="Const3")
model.addConstr(-1*x[0] + 2*x[1],"<=",5,name="Const4")

obj = gp.LinExpr()
obj += cost[0]*x[0] + cost[1]*x[1]

model.setObjective(obj,gp.GRB.MAXIMIZE)
model.update()
model.write("basic_optimisation/MCF_Model.lp")
model.optimize()