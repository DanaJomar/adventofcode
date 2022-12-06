##### Day 4 #####
# https://adventofcode.com/2022/day/4

# ------------------------------------------------
# imports
# ------------------------------------------------

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
def read_input(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    pairs_assignments = [line.replace("\n", "").split(",") for line in lines]
    return pairs_assignments


# ------------------------------------------------
# Solution
# ------------------------------------------------
def get_range(assignment):
    assignment = assignment.split("-")
    return set(range(int(assignment[0]), int(assignment[1]) + 1))


# ---------------- part 1 ----------------
pairs_assignments = read_input("input.csv")
count = 0
for assignment_1, assignment_2 in pairs_assignments:
    assignment_1 = get_range(assignment_1)
    assignment_2 = get_range(assignment_2)
    intersection = assignment_1.intersection(assignment_2)
    if (assignment_1 == intersection) | (assignment_2 == intersection):
        count += 1
print(count)

# ---------------- part 2 ----------------
pairs_assignments = read_input("input.csv")
count = 0
for assignment_1, assignment_2 in pairs_assignments:
    assignment_1 = get_range(assignment_1)
    assignment_2 = get_range(assignment_2)
    intersection = assignment_1.intersection(assignment_2)
    if len(intersection) > 0:
        count += 1
print(count)
