\ Model Northern Airline Company
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  1.08 x(0,0) + 1.095 x(0,1) + 1.11 x(0,2) + 1.125 x(0,3) + 1.11 x(1,1)
   + 1.125 x(1,2) + 1.14 x(1,3) + 1.1 x(2,2) + 1.115 x(2,3) + 1.13 x(3,3)
Subject To
 Production(0): x(0,0) + x(0,1) + x(0,2) + x(0,3) <= 25
 Production(1): x(1,1) + x(1,2) + x(1,3) <= 35
 Production(2): x(2,2) + x(2,3) <= 30
 Production(3): x(3,3) <= 10
 Demand(0): x(0,0) >= 10
 Demand(1): x(0,1) + x(1,1) >= 15
 Demand(2): x(0,2) + x(1,2) + x(2,2) >= 25
 Demand(3): x(0,3) + x(1,3) + x(2,3) + x(3,3) >= 20
Bounds
End
