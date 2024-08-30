import gurobipy as gp
from gurobipy import GRB

round_2 = [0x0, 0x4, 0x8, 0xc, 0x1, 0x5, 0x9, 0xd, 0x2, 0x6, 0xa, 0xe, 0x3, 0x7, 0xb, 0xf]

num_of_rounds = int(input("Enter the number of rounds: "))

# Create a new Gurobi model
model = gp.Model("sypher")

# Create binary variables
x = {}
for i in range(num_of_rounds + 1):
    for j in range(16):
        x[(i, j)] = model.addVar(vtype=GRB.BINARY, name=f"x{i}{hex(j)[2:]}")

# Update model to include new variables
model.update()

# Create integer variables
a = {}
for i in range(num_of_rounds):
    for j in range(4):
        a[(i, j)] = model.addVar(vtype=GRB.INTEGER, name=f"a{i}{hex(j)[2:]}")

#   Creating Minimize equation
expr0 = gp.LinExpr()
for i in range(num_of_rounds):
    for j in range(4):
        expr0 += a[(i,j)]
model.setObjective(expr0, GRB.MINIMIZE) 


#   Adding constraints 

#   First Constraint
for i in range(num_of_rounds):
    for j in range(4):
        for k in range(4):
            if i==0:
                model.addConstr(x[(i, 4 * j + k)] - a[(i, j)] >= 0)
            else:
                model.addConstr(x[(i, round_2[4 * j + k])] - a[(i, j)] >= 0)

#   Second Constraint
expr1 = gp.LinExpr()
for i in range(num_of_rounds):
    expr1 = 0
    for j in range(4):
        expr1 += a[i, j]
    model.addConstr(expr1 >= 1)


#   Third Constraint
expr2 = gp.LinExpr()
for i in range(num_of_rounds):
    for j in range(4):
        expr2 = 0
        for k in range(4):
            if i==0:
                if k<3:
                    expr2 += x[i, 4*j + k]
                else:
                    expr2 += x[i, 4*j + k] - a[i, j]
            else:
                if k<3:
                    expr2 += x[(i, round_2[4 * j + k])]
                else:
                    expr2 += x[(i, round_2[4 * j + k])] - a[i,j]
        model.addConstr(expr2 >= 0)


#   Fourth Constraint
expr3 = gp.LinExpr()
expr4 = gp.LinExpr()
for i in range(num_of_rounds):
    for j in range(4):
        expr3 = 0
        expr4 = 0
        for k in range(4):
            if i == 0:
                expr3 += 4 * x[i, 4*j + k] - x[i+1, round_2[4*j + k]]
                expr4 += 4 * x[i+1, round_2[4*j + k]] - x[i, 4*j + k]
            else:
                expr3 += 4 * x[i, round_2[4*j + k]] - x[i+1, round_2[4*j + k]]
                expr4 += 4 * x[i+1, round_2[4*j + k]] - x[i, round_2[4*j + k]]
        model.addConstr(expr3 >= 0)
        model.addConstr(expr4 >= 0)

# Optimize the model
model.optimize()

# Save the LP file
model.write("sypher004_gurobipy.lp")
