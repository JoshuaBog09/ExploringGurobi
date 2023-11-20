\ Model MILP_1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  2 x(0) + 3 x(1)
Subject To
 Const1: - 3 x(0) + x(1) <= 1
 Const2: 4 x(0) + 2 x(1) <= 20
 Const3: 4 x(0) - x(1) <= 10
 Const4: - x(0) + 2 x(1) <= 5
Bounds
End
