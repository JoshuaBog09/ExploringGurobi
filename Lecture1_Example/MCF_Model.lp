\ Model MILP_1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  x(1,1,2) + x(1,1,3) + 2 x(1,2,3) + 4 x(1,2,4) + 8 x(1,3,4) + 5 x(1,3,5)
   + 3 x(1,4,5) + x(2,1,2) + x(2,1,3) + 2 x(2,2,3) + 4 x(2,2,4)
   + 8 x(2,3,4) + 5 x(2,3,5) + 3 x(2,4,5) + x(3,1,2) + x(3,1,3)
   + 2 x(3,2,3) + 4 x(3,2,4) + 8 x(3,3,4) + 5 x(3,3,5) + 3 x(3,4,5)
   + x(4,1,2) + x(4,1,3) + 2 x(4,2,3) + 4 x(4,2,4) + 8 x(4,3,4)
   + 5 x(4,3,5) + 3 x(4,4,5)
Subject To
 Capacity(1): x(1,1,2) + x(2,1,2) + x(3,1,2) + x(4,1,2) <= 20
 Capacity(2): x(1,1,3) + x(2,1,3) + x(3,1,3) + x(4,1,3) <= 10
 Capacity(3): x(1,2,3) + x(2,2,3) + x(3,2,3) + x(4,2,3) <= 10
 Capacity(4): x(1,2,4) + x(2,2,4) + x(3,2,4) + x(4,2,4) <= 20
 Capacity(5): x(1,3,4) + x(2,3,4) + x(3,3,4) + x(4,3,4) <= 40
 Capacity(6): x(1,3,5) + x(2,3,5) + x(3,3,5) + x(4,3,5) <= 10
 Capacity(7): x(1,4,5) + x(2,4,5) + x(3,4,5) + x(4,4,5) <= 30
 Continuity(1,1): x(1,1,2) + x(1,1,3) = 15
 Continuity(1,2): - x(1,1,2) + x(1,2,3) + x(1,2,4) = 0
 Continuity(1,3): - x(1,1,3) - x(1,2,3) + x(1,3,4) + x(1,3,5) = 0
 Continuity(1,4): - x(1,2,4) - x(1,3,4) + x(1,4,5) = -15
 Continuity(1,5): - x(1,3,5) - x(1,4,5) = 0
 Continuity(2,1): x(2,1,2) + x(2,1,3) = 5
 Continuity(2,2): - x(2,1,2) + x(2,2,3) + x(2,2,4) = 0
 Continuity(2,3): - x(2,1,3) - x(2,2,3) + x(2,3,4) + x(2,3,5) = 0
 Continuity(2,4): - x(2,2,4) - x(2,3,4) + x(2,4,5) = 0
 Continuity(2,5): - x(2,3,5) - x(2,4,5) = -5
 Continuity(3,1): x(3,1,2) + x(3,1,3) = 0
 Continuity(3,2): - x(3,1,2) + x(3,2,3) + x(3,2,4) = 10
 Continuity(3,3): - x(3,1,3) - x(3,2,3) + x(3,3,4) + x(3,3,5) = 0
 Continuity(3,4): - x(3,2,4) - x(3,3,4) + x(3,4,5) = 0
 Continuity(3,5): - x(3,3,5) - x(3,4,5) = -10
 Continuity(4,1): x(4,1,2) + x(4,1,3) = 0
 Continuity(4,2): - x(4,1,2) + x(4,2,3) + x(4,2,4) = 0
 Continuity(4,3): - x(4,1,3) - x(4,2,3) + x(4,3,4) + x(4,3,5) = 5
 Continuity(4,4): - x(4,2,4) - x(4,3,4) + x(4,4,5) = 0
 Continuity(4,5): - x(4,3,5) - x(4,4,5) = -5
Bounds
End
