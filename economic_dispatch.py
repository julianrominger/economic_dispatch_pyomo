from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory

#We define an abstrac model
model = AbstractModel()

#Sets and parameters of the abstract model
model.t = Set() #time periods
model.g = Set() #conventional technologies
model.cos = Param(model.g) #marginal cost of generating units
model.cap = Param(model.g) #capacity of generating units
model.dem = Param(model.t) #demand level
model.shed_cost = Param(within=NonNegativeReals) #load shed cost

#Variables of the abstract model
model.gen = Var(model.g, model.t, domain=NonNegativeReals) #generation level
model.shed = Var(model.t, domain=NonNegativeReals) #load shedding

#Objective function of the abstract model
def obj_expression(model):
  return   sum(sum(model.cos[g]*model.gen[g,t]  for g in model.g) + model.shed_cost*model.shed[t] for t in model.t) 
model.OBJ = Objective(rule=obj_expression)

#Power balance constraint
def balance_rule(model,t):
  return sum(model.gen[g,t] for g in model.g) + model.shed[t] == model.dem[t]
model.balance = Constraint(model.t,rule=balance_rule)

#Max generation constraint
def max_gen_rule(model,g,t):
  return model.gen[g,t] <= model.cap[g]
model.max_gen = Constraint(model.g,model.t,rule=max_gen_rule)

#Max load shed constraint
def max_shed_rule(model,t):
  return model.shed[t] <= model.dem[t]
model.max_shed = Constraint(model.t,rule=max_shed_rule)

#We define the optimization solver. You can also use cplex, gurobi, etc
opt = SolverFactory('glpk')

#We open a DataPortal example
data = DataPortal() 

#We read all the data from different files
data.load(filename='scalars.dat')   
data.load(filename='dem_data.csv',format='set', set='t')
data.load(filename='gen_data.csv',format='set', set='g')
data.load(filename='gen_data.csv',index='g',param=['cos','cap'])
data.load(filename='dem_data.csv',index='t', param='dem')

#We create an instance  
instance = model.create_instance(data)

#We can display all the info of the instance
instance.pprint()

#We solve the optimization problem
results = opt.solve(instance,symbolic_solver_labels=True,tee=True) 

#We write some of the results in a csv file
f = open('gen_result.csv', 'w')
f.write("g,t,gen"+"\n")
for g in instance.g.value:
  for t in instance.t.value:
    f.write(str(g)+","+str(t)+","+str(instance.gen[g,t].value)+"\n")







