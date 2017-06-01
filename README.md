# economic_dispatch_pyomo
This is the code to solve a simple economic dispatch model using pyomo.

You need to have installed in your computer python3, pyomo and the linear solver you want to use (glpk, cplex, gurobi, etc).

scalars.dat: Scalar data such as load shedding cost

gen_data.csv: Generation data such as marginal cost and capacity of generating units

dem_data.csv: Demand level data

economic_dispatch.py: Code to solve the economic dispatch problem. The optimal quantities to be produced are provided in the file gen_results.csv
