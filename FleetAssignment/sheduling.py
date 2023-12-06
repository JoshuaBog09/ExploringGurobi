import numpy as np
import gurobipy as gp
import sqlite3
import datetime

connection = sqlite3.connect("FleetAssignment/Flights.db")
cursor = connection.cursor()

## Code to create database run once and the database will be created
#
# df = np.genfromtxt("FleetAssignment/data.txt", delimiter=", ", dtype="unicode", skip_header=1)
# 
# cursor.execute("DROP TABLE Flights")
# cursor.execute("CREATE TABLE Flights (Flight TEXT, FromL TEXT, ToL TEXT, Departure TEXT, Arrival TEXT, Demand INTEGER)")
#
# for id in range(df.shape[0]):
#    
#     cursor.execute(f'INSERT INTO Flights VALUES ("{df[id,0]}", "{df[id,1]}", "{df[id,2]}", "{df[id,3]}", "{df[id,4]}", "{df[id,5]}")')
#
# connection.commit()
#
## END code to create database

class Node:

    def __init__(self, location, time, TAT):
        self.airport = location
        self.time = datetime.datetime.strptime(time, '%H:%M') + datetime.timedelta(minutes=TAT)

    
Nodes_O = []
Nodes_I = []

res = cursor.execute("SELECT Flight, FromL, ToL, Departure, Arrival, Demand FROM FLIGHTS")

for line in res:
    Nodes_O.append(Node(line[1], line[3], 0))
    Nodes_I.append(Node(line[2], line[4], 10))


# nodes = cursor.execute("SELECT DISTINCT FromL FROM FLIGHTS")

# airports = []

# for node in nodes:
#     airports.append(Node(node[0]))

print(Nodes_O[0].__dict__)
