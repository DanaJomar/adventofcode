##### Day 15 #####
# https://adventofcode.com/2021/day/15

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np
from heapq import heappop, heappush

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()
lines = [list(x.replace("\n", "")) for x in lines]
MAP = np.array(lines, dtype=int)
start = (0, 0)
end = tuple([x - 1 for x in MAP.shape])

# ------------------------------------------------
# Solution
# ------------------------------------------------
def getNeighbours(node, size_factor):
    neighbours = []
    if node[1] < MAP.shape[1] * size_factor - 1:
        neighbours += [(node[0], node[1] + 1)]
    if node[0] < MAP.shape[0] * size_factor - 1:
        neighbours += [(node[0] + 1, node[1])]
    if node[1] > 0:
        neighbours += [(node[0], node[1] - 1)]
    if node[0] > 0:
        neighbours += [(node[0] - 1, node[1])]
    return neighbours


def getRisks(coordinates_lst):
    risks = np.array([])
    x_lim = MAP.shape[0]
    y_lim = MAP.shape[1]
    for idx1, idx2 in coordinates_lst:
        cave_risk = MAP[idx1 % x_lim, idx2 % y_lim] + idx1 // x_lim + idx2 // y_lim
        risks = np.append(risks, (cave_risk - 1) % 9 + 1)
    return risks


def getPath(start, end, size_factor=1):
    risk_heap = []
    heappush(risk_heap, (0, start))
    risk_to_cave = {start: 0}
    visited = set()
    neighbours = []
    while end not in neighbours:
        risk_so_far, current_cave = heappop(risk_heap)
        if current_cave in visited:
            continue
        neighbours = getNeighbours(current_cave, size_factor)
        neighbours_risks = getRisks(neighbours)
        for i in range(len(neighbours)):
            if neighbours[i] in visited:
                continue
            risk_to_neighbour = min(
                risk_to_cave.get(neighbours[i], np.Inf),
                risk_so_far + neighbours_risks[i],
            )
            risk_to_cave[neighbours[i]] = risk_to_neighbour
            heappush(
                risk_heap,
                (
                    risk_to_neighbour,
                    neighbours[i],
                ),
            )
        visited.add(current_cave)
    return risk_to_cave[end]


# ---------------- part 1 ----------------
print(getPath(start, end))

# ---------------- part 2 ----------------
print(getPath(start, tuple([x * 5 - 1 for x in MAP.shape]), 5))


##