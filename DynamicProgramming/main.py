## Usign DP to solve a simple network (Shortest Path) ##

# DATA 

network = [
    ["A", "B", 2],
    ["A", "C", 4],
    ["A", "D", 3],
    ["B", "E", 7],
    ["B", "F", 4],
    ["B", "G", 6],
    ["C", "E", 3],
    ["C", "F", 2],
    ["C", "G", 4],
    ["D", "E", 4],
    ["D", "F", 1],
    ["D", "G", 5],
    ["E", "H", 1],
    ["E", "I", 4],
    ["F", "H", 6],
    ["F", "I", 3],
    ["G", "H", 3],
    ["G", "I", 3],
    ["H", "J", 3],
    ["I", "J", 4]
]

levels = [
    ["A"],
    ["B", "C", "D"],
    ["E", "F", "G"],
    ["H", "I"],
    ["J"],
]

class Arc:

    def __init__(self, fr, to, cost):
        self.fr: str    = fr
        self.to: str    = to
        self.cost: int  = cost

class Node:
    def __init__(self, node):
        self.node           = node
        self.current_cost   = 1e6
        self.level          = None
        self.InLinks        = [ ]
        self.OutLinks       = [ ]
    
    def addInLink(self,Node):
        self.InLinks.append(Node)       
    
    def addOutLink(self,Node):
        self.OutLinks.append(Node)

    def addLevel(self, level):
        self.level = level
    
    def adjustCost(self, cost):
        if cost < self.current_cost:
            self.current_cost = cost

arcs = []
node_names = []
nodes = []

# Creating arcs
for line in network:
    arcs.append(Arc(line[0], line[1], line[2]))
    node_names.extend([line[0], line[1]])

node_names = sorted(set(node_names))

for name in node_names: 
    nodes.append(Node(name))

# Creating node links
for node in nodes:
    
    for idx, arc in enumerate(arcs):
        
        if arc.fr == node.node:
            node.addOutLink([idx, arc.to])

        if arc.to == node.node:
            node.addInLink([idx, arc.fr])

# Setting level
for node in nodes:
    if node.node in ["A"]:
        node.addLevel(0)
    elif node.node in ["B", "C", "D"]:
        node.addLevel(1)
    elif node.node in ["E", "F", "G"]:
        node.addLevel(2)
    elif node.node in ["H", "I"]:
        node.addLevel(3)
    elif node.node in ["J"]:
        node.addLevel(4)

# Set initial node to zero (start from last node)
nodes[-1].current_cost = 0

# Solve
for level in levels[::-1]:
    
    # Level |---> the elements contained within a level
    for node in nodes:
        
        # Find the nodes which are currently in evaluation
        if node.node in level:
            
            # Look at the options
            for link in node.InLinks:

                # Find the cost of the link and addapt cost of next node
                new_cost = arcs[link[0]].cost + node.current_cost
                nodes[int(ord(link[1])-ord('A'))].adjustCost(new_cost)

# Backtracking to find the correct path

path = ['A']

for level in levels:

    found_cp = False
    
    # Level |---> the elements contained within a level
    for node in nodes:
        
        # Find the nodes which are currently in evaluation
        if node.node in level and node.node == path[-1]:

            # Look at the options
            for link in node.OutLinks:
                
                # Compute the cost the previous node should have
                old_cost = node.current_cost - arcs[link[0]].cost

                # Find if the current link is the correct link
                if old_cost == nodes[int(ord(link[1])-ord('A'))].current_cost:
                    
                    # Add link and break to next level
                    path.append(link[1])
                    found_cp = True
                    
                    break
        
        if found_cp:
            break

print(path)

for node in nodes:
    print(node.__dict__)
