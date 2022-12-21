##### Day 21 #####
# https://adventofcode.com/2022/day/21

# ------------------------------------------------
# imports
# ------------------------------------------------
import re
from sympy import symbols, solve

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
ops = dict()
waiting = []
with open("input.csv", "r") as f:
    for line in f:
        name, job = line.replace("\n", "").split(": ")
        ops[name] = job
        if not job.isnumeric():
            waiting.append((name, job))

# ------------------------------------------------
# Solution
# ------------------------------------------------
def replace_with_value(symbol, current_ops):
    new_val = current_ops.get(symbol)
    if new_val is None:
        return symbol
    else:
        try:
            new_val = str(eval("( " + new_val + " )"))
        except NameError:
            new_val = "( " + new_val + " )"
        return new_val


# ---------------- part 1 ----------------
ops_copy = ops.copy()
while len(waiting) > 0:
    name, job = waiting.pop()
    job_split = job.split(" ")
    new_job = []
    for symbol in job_split:
        new_job.append(replace_with_value(symbol, ops_copy))
    new_job = " ".join(new_job)
    try:
        new_job = str(eval(new_job))
    except NameError:
        waiting.append((name, new_job))
    ops_copy[name] = new_job

ops_copy["root"]
# ---------------- part 2 ----------------
ops_copy = ops.copy()

# get and remove the root operation
root_op = ops_copy["root"].split(" ")
root_op
ops_copy.pop("root")
ops_copy.pop("humn")

# populate the waiting list
for name, job in ops_copy.items():
    if not job.isnumeric():
        waiting.append((name, job))
pattern = "|".join(ops_copy.keys())

while (
    len(re.findall(pattern, ops_copy.get(root_op[0])))
    + len(re.findall(pattern, ops_copy.get(root_op[-1])))
    > 0
):
    name, job = waiting.pop(0)
    job_split = job.split(" ")
    new_job = []
    for symbol in job_split:
        new_job.append(replace_with_value(symbol, ops_copy))
    new_job = " ".join(new_job)
    try:
        new_job = str(eval(new_job))
    except NameError:
        waiting.append((name, new_job))
    ops_copy[name] = new_job

## solve equation
humn = symbols("humn")
expr = ops_copy.get(root_op[0]) + " - " + ops_copy.get(root_op[-1])
humn_val = solve(expr)[0]
print(round(humn_val))
eval(
    (ops_copy.get(root_op[0]) + " == " + ops_copy.get(root_op[-1])).replace(
        "humn", str(round(humn_val))
    )
)
