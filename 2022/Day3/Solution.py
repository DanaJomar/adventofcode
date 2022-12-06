##### Day 3 #####
# https://adventofcode.com/2022/day/3

# ------------------------------------------------
# imports
# ------------------------------------------------
from string import ascii_lowercase, ascii_uppercase

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

rucksacks_test = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
]

with open("input.csv", "r") as file:
    lines = file.readlines()
rucksacks_orig = [x.replace("\n", "") for x in lines]
# ------------------------------------------------
# Solution
# ------------------------------------------------
def get_intersection(rucksacks):
    intersection = set(list(rucksacks[0])).intersection(set(list(rucksacks[1])))
    for i in range(2, len(rucksacks)):
        rucksack = rucksacks[i]
        intersection = intersection.intersection(set(list(rucksack)))
    return intersection


def get_total_priority(rucksacks, splits):
    total_priority = 0
    for i in range(0, len(rucksacks), splits):
        comb_intersection = get_intersection(rucksacks[i : (i + splits)]).pop()
        if comb_intersection in ascii_lowercase:
            priority = ascii_lowercase.index(comb_intersection) + 1
        elif comb_intersection in ascii_uppercase:
            priority = (
                ascii_uppercase.index(comb_intersection) + len(ascii_lowercase) + 1
            )
        total_priority = total_priority + priority
    return total_priority


# ---------------- part 1 ----------------
rucksacks_splits = []
for rucksack in rucksacks_orig:
    midpoint = len(rucksack) // 2
    rucksacks_splits.append(rucksack[:midpoint])
    rucksacks_splits.append(rucksack[midpoint:])
get_total_priority(rucksacks_splits, 2)

# ---------------- part 2 ----------------
get_total_priority(rucksacks_orig, 3)
