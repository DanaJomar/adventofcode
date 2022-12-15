##### Day 12 #####
# https://adventofcode.com/2022/day/12

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np
from string import ascii_lowercase
from heapq import heappop, heappush

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------


# ------------------------------------------------
# Solution
# ------------------------------------------------
def find_loc(map_array, value):
    locs = set()
    for i in range(len(map_array)):
        if value in map_array[i]:
            return i, map_array[i].index(value)


def map_to_numbers(map_array):
    S_loc = find_loc(map_array, "S")
    E_loc = find_loc(map_array, "E")
    map_array = np.char.replace(map_array, "S", "a")
    map_array = np.char.replace(map_array, "E", "z")
    numeric_array = np.array(
        list(map(lambda x: [ascii_lowercase.index(y.lower()) for y in x], map_array))
    )
    all_possible_starting_loc = np.where(numeric_array == 0)
    all_possible_starting_loc = set(
        [
            (x, y)
            for x, y in zip(all_possible_starting_loc[0], all_possible_starting_loc[1])
        ]
    )
    return numeric_array, S_loc, E_loc, all_possible_starting_loc


def nex_possible_moves(numeric_map, loc):
    x, y = loc
    value = numeric_map[loc]
    neighbours = set()
    if x > 0:
        neighbours.add((x - 1, y))
    if x < (numeric_map.shape[0] - 1):
        neighbours.add((x + 1, y))
    if y < (numeric_map.shape[1] - 1):
        neighbours.add((x, y + 1))
    if y > 0:
        neighbours.add((x, y - 1))
    for neighbour in neighbours.copy():
        if numeric_map[neighbour] > value + 1:
            neighbours.discard(neighbour)
    return neighbours


def find_path(path_to_input, all_possible_starts):
    data = np.loadtxt(path_to_input, dtype=str)
    numeric_map, S_loc, E_loc, all_possible_starting_loc = map_to_numbers(data)
    if not all_possible_starts:
        all_possible_starting_loc = set([S_loc])
    moves_queue = []
    for start_loc in all_possible_starting_loc:
        heappush(moves_queue, (0, (start_loc, start_loc)))
    visited = set()
    while len(moves_queue) > 0:
        steps_so_far, (start_loc, cur_loc) = heappop(moves_queue)
        if not (cur_loc in visited):
            neighbours = nex_possible_moves(numeric_map, cur_loc)
            if E_loc in neighbours:
                return steps_so_far + 1
            else:
                for neighbour in neighbours:
                    heappush(moves_queue, (steps_so_far + 1, (start_loc, neighbour)))
                    visited.add(cur_loc)


# ---------------- part 1 ----------------
find_path("input.csv", False)

# ---------------- part 2 ----------------
find_path("input.csv", True)
