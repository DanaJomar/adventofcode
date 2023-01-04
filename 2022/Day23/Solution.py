##### Day 23 #####
# https://adventofcode.com/2022/day/23

# ------------------------------------------------
# imports
# ------------------------------------------------
import matplotlib.pyplot as plt

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
elves_map = []
with open("input.csv", "r") as file:
    for line in file:
        elves_map.append(list(line.replace("\n", "")))

# ------------------------------------------------
# Solution
# ------------------------------------------------
def plot_map(elves_locs):
    xy_to_plot = list(zip(*elves_locs.values()))
    plt.gca().invert_yaxis()
    plt.scatter(xy_to_plot[1], xy_to_plot[0])
    plt.show()


def get_neighbours_loc(elf_loc):
    x, y = elf_loc
    n = (x - 1, y)
    s = (x + 1, y)
    e = (x, y + 1)
    w = (x, y - 1)
    se = (x + 1, y + 1)
    sw = (x + 1, y - 1)
    ne = (x - 1, y + 1)
    nw = (x - 1, y - 1)

    return {"n": n, "s": s, "e": e, "w": w, "ne": ne, "nw": nw, "se": se, "sw": sw}


def get_neighbours(neighbours_loc, locs):
    return {
        "n": locs.get(neighbours_loc.get("n"), "."),
        "s": locs.get(neighbours_loc.get("s"), "."),
        "e": locs.get(neighbours_loc.get("e"), "."),
        "w": locs.get(neighbours_loc.get("w"), "."),
        "ne": locs.get(neighbours_loc.get("ne"), "."),
        "nw": locs.get(neighbours_loc.get("nw"), "."),
        "se": locs.get(neighbours_loc.get("se"), "."),
        "sw": locs.get(neighbours_loc.get("sw"), "."),
    }


def move(loc, direction):
    if direction == "n":
        return (loc[0] - 1, loc[1])
    if direction == "s":
        return (loc[0] + 1, loc[1])
    if direction == "e":
        return (loc[0], loc[1] + 1)
    if direction == "w":
        return (loc[0], loc[1] - 1)


def moving_round(elves_locs, directions):
    elves_propositions = {}
    locs = {loc: "#" for _, loc in elves_locs.items()}
    movement = False
    for elf_id in elves_locs:
        # elf_id = 0
        elf_loc = elves_locs.get(elf_id)
        neighbours_loc = get_neighbours_loc(elf_loc)
        neighbours = get_neighbours(neighbours_loc, locs)
        # check if there's a neighbouring elf
        if "#" in neighbours.values():
            # check all possible moving directions
            for direction in directions:
                keys_to_check = [k for k in neighbours.keys() if direction in k]
                dir_neighbours = []
                for key in keys_to_check:
                    dir_neighbours.append(neighbours.get(key))
                # check if there is an elf neighbour in the direction
                if "#" not in dir_neighbours:
                    # make a proposition
                    elves_propositions[elf_id] = move(elf_loc, direction)
                    break
    # check the propositions
    elves_to_move = list(elves_propositions.keys())
    for elf_id in elves_to_move:
        if elf_id in elves_propositions.keys():
            proposition = elves_propositions.pop(elf_id)
            # move if only this elf proposed this position
            if proposition not in elves_propositions.values():
                movement = True
                locs.pop(elves_locs.get(elf_id))
                locs[proposition] = "#"
                elves_locs[elf_id] = proposition
            # else neither this elf nor the others which proposed this location could move to it
            else:
                same_prop_elves = [
                    k for k, v in elves_propositions.items() if v == proposition
                ]
                # rempve them from the propositions
                for elf_id in same_prop_elves:
                    elves_propositions.pop(elf_id)
    # permute directions
    first_dir = directions.pop(0)
    directions.append(first_dir)

    return elves_locs, directions, movement


# ---------------- part 1 ----------------

elves_locs = [
    (i, j) for i, x in enumerate(elves_map) for j, y in enumerate(x) if y == "#"
]
# elf_map_array = np.array(elf_map)
elves_locs = {elf_id: loc for elf_id, loc in enumerate(elves_locs)}
directions = ["n", "s", "w", "e"]

# %load_ext line_profiler
# %lprun -f moving_round moving_round(elves_locs, directions)

# plot_map(elves_locs)
for _ in range(10):
    elves_locs, directions, movement = moving_round(elves_locs, directions)
# plot_map(elves_locs)

locations = list(zip(*elves_locs.values()))
print(
    (max(locations[0]) - min(locations[0]) + 1)
    * (max(locations[1]) - min(locations[1]) + 1)
    - len(elves_locs)
)


# ---------------- part 2 ----------------
elves_locs = [
    (i, j) for i, x in enumerate(elves_map) for j, y in enumerate(x) if y == "#"
]
# elf_map_array = np.array(elf_map)
elves_locs = {elf_id: loc for elf_id, loc in enumerate(elves_locs)}
directions = ["n", "s", "w", "e"]

movement = True
i = 0
while movement:
    i = i + 1
    elves_locs, directions, movement = moving_round(elves_locs, directions)

print(i)
