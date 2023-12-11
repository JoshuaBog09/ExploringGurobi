import numpy as np
import pandas as pd
import gurobipy as gp
import sqlite3
import datetime
import matplotlib.pyplot as plt

# connection = sqlite3.connect("FleetAssignment/Flights.db")
# cursor = connection.cursor()

# # Code to create database run once and the database will be created

# df = np.genfromtxt("FleetAssignment/data.txt", delimiter=", ", dtype="unicode", skip_header=1)

# cursor.execute("DROP TABLE Flights")
# cursor.execute("CREATE TABLE Flights (Flight TEXT, FromL TEXT, ToL TEXT, Departure DATETIME, Arrival DATETIME, Demand INTEGER)")

# for id in range(df.shape[0]):
   
#     cursor.execute(f'INSERT INTO Flights VALUES ("{df[id,0]}", "{df[id,1]}", "{df[id,2]}", "{df[id,3]}", "{df[id,4]}", "{df[id,5]}")')

# connection.commit()

# # END code to create database

data = pd.read_csv('FleetAssignment/data.txt', sep=", ")

data['Departure'] = pd.to_datetime(data['Departure'], format='%H:%M')
data['Arrival'] = pd.to_datetime(data['Arrival'], format='%H:%M')

class Node:

    def __init__(self, location, time, TAT):
        # Storage Adress
        self.airport = location
        self.time = time + datetime.timedelta(minutes=TAT)
        self.InLinks  = [ ]     # List of Nodes connected to self via a direct link
        self.OutLinks = [ ]     # List of Nodes connected from self via a direct link

    def addInLink(self,Node):
        self.InLinks.append(Node)       
    
    def addOutLink(self,Node):
        self.OutLinks.append(Node)


class Arc:

    def __init__(self, flight, From, To, Departure, Arrival, TAT):
        self.Flight = flight
        self.From  = From
        self.To    = To
        self.Departure = Departure
        self.Arrival = Arrival + datetime.timedelta(minutes=TAT)


Nodes_O = []
Nodes_I = []

Arcs = []

for index, line in data.iterrows():

    Flight = line["Flight"]
    From = line["From"]
    To = line["To"]
    Departure = line["Departure"]
    Arrival = line["Arrival"]
    Demand = line["Demand"]
    
    Nodes_O.append(Node(From, Departure, 0))
    Nodes_I.append(Node(To, Arrival, 10))

    Arcs.append(Arc(Flight, From, To, Departure, Arrival, 10))

Nodes_all = Nodes_O + Nodes_I

unique_objects = set()
unique_objects_list = []

for obj in Nodes_all:

    obj_identifier = (obj.airport, obj.time)

    if obj_identifier not in unique_objects:

        unique_objects.add(obj_identifier)
        unique_objects_list.append(obj)

Nodes_all = unique_objects_list

Nodes_all = sorted(Nodes_all, key=lambda x: x.time, reverse=False)

for node in Nodes_all:
    
    for arc in Arcs:
        
        if arc.From == node.airport and arc.Departure == node.time:
            node.addOutLink(arc.To)
        
        if arc.To == node.airport and arc.Arrival == node.time:
            node.addInLink(arc.From)

airport = ['PDL', 'LIS', 'OPO', 'FNC', 'YTO', 'BOS']
color = ["b", "g", "r", "c", "m", "y"]

for node in Nodes_all:
    y = airport.index(node.airport)
    x = node.time

    plt.scatter(x,y, color=color[y])

for arc in Arcs:
    x1 = arc.Departure
    x2 = arc.Arrival
    y1 = airport.index(arc.From)
    y2 = airport.index(arc.To)

    plt.plot([x1, x2], [y1, y2], color="k")

plt.show()

for node in Nodes_all:
    print(node.__dict__)

# for node in Nodes_all_sorted:
#     print(node.__dict__)