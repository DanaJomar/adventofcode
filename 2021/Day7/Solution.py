##### Day 7 #####
# https://adventofcode.com/2021/day/7

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd
from pulp import *
from gekko import GEKKO

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
# input = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
input = pd.read_csv("input.csv", header=None)
input = input.values[0]
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
# 16 + x1 = y
# 1 + x2 = y
# 2 + x3 = y
# 0 + x4 = y
# 4 + x5 = y
# 2 + x6 = y
# 7 + x7 = y
# 1 + x8 = y
# 2 + x9 = y
# 14 + x10 = y
#
# z = sum(abs(x))

N = len(input)
x_vars = LpVariable.dicts("x", range(N))
x_vars_abs = LpVariable.dicts("x_abs", range(N))
x_vars_abs_1 = LpVariable.dicts("x_abs_1", range(N))
y_var = LpVariable("y")
prob = LpProblem("min_sum_abs", LpMinimize)

# OBJECTIVE
for i in range(N):
    prob += lpSum(x_vars_abs)

for i in range(N):
    # ABS CONSTRAINTS
    prob += x_vars_abs[i] >= x_vars[i]
    prob += x_vars_abs[i] >= -x_vars[i]
    # OTHER MODEL CONSTRAINTS
    prob += input[i] + x_vars[i] == y_var

prob.solve()

print("Status: " + str(LpStatus[prob.status]))
print("Objective: " + str(value(prob.objective)))

for v in prob.variables():
    print(v.name + " = " + str(v.varValue))

# Status: Optimal
# Objective: 352331.0
# y = 349.0

# ---------------- part 2 ----------------
#  z = sum((abs(x)*(abs(x)+1))/2)

# 16 + x1 = y
# 1 + x2 = y
# 2 + x3 = y
# 0 + x4 = y
# 4 + x5 = y
# 2 + x6 = y
# 7 + x7 = y
# 1 + x8 = y
# 2 + x9 = y
# 14 + x10 = y

m = GEKKO()  # Initialize gekko
m.options.SOLVER = 1  # APOPT is an MINLP solver

# optional solver settings with APOPT
m.solver_options = [
    "minlp_maximum_iterations 500",  # minlp iterations with integer solution
    "minlp_max_iter_with_int_sol 10",  # treat minlp as nlp
    "minlp_as_nlp 0",  # nlp sub-problem max iterations
    "nlp_maximum_iterations 50",  # 1 = depth first, 2 = breadth first
    "minlp_branch_method 1",  # maximum deviation from whole number
    "minlp_integer_tol 0.05",  # covergence tolerance
    "minlp_gap_tol 0.01",
]

# Initialize variables
variables = []
## constrains of the shape n_i + x_i = y
for i in range(N + 1):
    variables = variables + [m.Var(integer=True)]

for i in range(N):
    m.Equation(input[i] + variables[i] == variables[N])

m.Obj(
    m.sum(
        [
            a * b
            for a, b in zip(
                [m.abs(x) / 2 for x in variables[:-1]],
                [m.abs(x) + 1 for x in variables[:-1]],
            )
        ]
    )
)
m.solve(disp=False)


print("Results")
print(variables)
print("Objective: " + str(m.options.objfcnval))
