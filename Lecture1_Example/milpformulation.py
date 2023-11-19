import gurobipy as gp

class Arc:
    def __init__(self,origin, destination, cost, capacity):
        self.From   = origin
        self.To     = destination
        self.Cost   = cost
        self.Capac  = capacity

class Commodity:
    def __init__(self,origin, destination, quantity):
        self.From   = origin
        self.To     = destination
        self.Quant  = quantity

class Node:
    def __init__(self):
        self.InLinks  = [ ]         #List of Nodes connected to self via a direct link
        self.OutLinks = [ ]         #List of Nodes connected from self via a direct link
    
    def addInLink(self,Node):
        self.InLinks.append(Node)       
    
    def addOutLink(self,Node):
        self.OutLinks.append(Node)

n_arcs = 7
n_commodities = 4
n_nodes = 5

arcs_data = {
    "i": [1,1,2,2,3,3,4],
    "j": [2,3,3,4,4,5,5],
    "cost": [1,1,2,4,8,5,3],
    "capacity": [20,10,10,20,40,10,30],
}

commodities_data = {
    "#": [1,2,3,4],
    "origin": [1,1,2,3],
    "destination": [4,5,5,5],
    "quantity": [15,5,10,5],
}

arcs = [0]*n_arcs
commodities = [0]*n_commodities
nodes = [Node() for _ in range(n_nodes)]

for i in range(n_arcs):
    arcs[i] = Arc(arcs_data['i'][i], arcs_data['j'][i], 
                  arcs_data['cost'][i], arcs_data['capacity'][i])
    
for i in range(n_commodities):
    commodities[i] = Commodity(commodities_data['origin'][i], 
                               commodities_data['destination'][i], 
                               commodities_data['quantity'][i])

for id, node in enumerate(nodes, start=1):
    
    for arc in arcs:
        
        if arc.From == id:
            node.addOutLink(arc.To)
        if arc.To == id:
            node.addInLink(arc.From)

# Observing data storage
# for arc in arcs:
#     print(arc.__dict__)

# for node in nodes:
#     print(node.__dict__)

# for commo in commodities:
#     print(commo.__dict__)


## The MILP model

model = gp.Model("MILP_1")

# Define variables
x = {}
for k in range(1, len(commodities) + 1):
    for arc in arcs:
        x[k, arc.From, arc.To] = model.addVar(obj= arc.Cost, vtype ="C",
                                              name = "x(%d,%d,%d)"%(k,arc.From,arc.To))
        
model.update()

# Define constraints

capacity = {}

for id, arc in enumerate(arcs, start=1):
    x[arc.From, arc.To] = model.addConstr(gp.quicksum(x[k,arc.From,arc.To] for k in range(1,len(commodities)+1)),
                                          "<=",arc.Capac,name="Capacity(%d)"%id)

continuity = {}

for idc, commodity in enumerate(commodities, start=1):
    for idn, node in enumerate(nodes,start=1):
        if idn == commodity.From:
            continuity[idc,idn] = model.addConstr(gp.quicksum(x[idc,idn,p] for p in node.OutLinks) - gp.quicksum(x[idc,p,idn] for p in node.InLinks),
                                    '=', commodity.Quant, name ='Continuity(%d,%d)' %(idc,idn) )
        elif idn == commodity.To:
            continuity[idc,idn] = model.addConstr(gp.quicksum(x[idc,idn,p] for p in node.OutLinks) - gp.quicksum(x[idc,p,idn] for p in node.InLinks),
                                    '=', -commodity.Quant, name ='Continuity(%d,%d)' %(idc,idn) )
        else:
            continuity[idc,idn] = model.addConstr(gp.quicksum(x[idc,idn,p] for p in node.OutLinks) - gp.quicksum(x[idc,p,idn] for p in node.InLinks),
                                    '=', 0, name ='Continuity(%d,%d)' %(idc,idn) )
            
model.update()
model.write("MCF_Model.lp")
model.optimize()

print
for arc in arcs:
    Flow = 0
    for m in range(1,len(commodities)+1):
        Flow += x[m,arc.From,arc.To].X
    if int(Flow)>0:
        print ("Arc(%d,%d) \t" %(arc.From + 1,arc.To + 1), int(Flow))
        print
print
print ("Objective Function =", model.ObjVal/1.0)
print ("------------------------------------------------------------------------")