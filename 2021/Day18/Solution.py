##### Day 18 #####
# https://adventofcode.com/2021/day/18

# ------------------------------------------------
# imports
# ------------------------------------------------
from math import ceil, floor
import pandas as pd
import numpy as np
import re

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

# data = pd.read_csv("input.csv", delim_whitespace=True, header=None)
#
with open("input_test_2.csv", "r") as file:
    lines = file.readlines()

input_list = [x.replace("\n", "") for x in lines]

# expected for the sum of input_test.csv is
# summed: [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
# magnitude: 3488

# expected for the sum of input_test_2.csv is
# summed: [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
# magnitude: 4140
# largest magnitude for the sum of 2 numbers: 3993

sample_addition_inputs = [
    [
        "[1,1]",
        "[2,2]",
        "[3,3]",
        "[4,4]",
        "[5,5]",
        "[6,6]",
    ]  # final sum : [[[[5,0],[7,4]],[5,5]],[6,6]]]
]
sample_explode_inputs = [
    "[[[[[9,8],1],2],3],4]",  # [[[[0,9],2],3],4]
    "[7,[6,[5,[4,[3,2]]]]]",  # [7,[6,[5,[7,0]]]]
    "[[6,[5,[4,[3,2]]]],1]",  # [[6,[5,[7,0]]],3]
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",  # [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",  # [[3,[2,[8,0]]],[9,[5,[7,0]]]]
]

sample_magnitude_inputs = [
    "[[1,2],[[3,4],5]]",  # becomes 143.
    "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",  # becomes 1384.
    "[[[[1,1],[2,2]],[3,3]],[4,4]]",  # becomes 445.
    "[[[[3,0],[5,3]],[4,4]],[5,5]]",  # becomes 791.
    "[[[[5,0],[7,4]],[5,5]],[6,6]]",  # becomes 1137.
    "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",  # becomes 3488
]
# ------------------------------------------------
# Solution
# ------------------------------------------------


def get_left_digit_loc(digit_loc, all_digits_loc):
    left_in_locations = np.where(all_digits_loc == digit_loc)[0][0] - 1
    if left_in_locations == -1:
        left_digit_loc = None
    else:
        left_digit_loc = all_digits_loc[left_in_locations]
    return left_digit_loc


def get_right_digit_loc(digit_loc, all_digits_loc):
    right_in_locations = np.where(all_digits_loc == digit_loc)[0][0] + 1
    if right_in_locations == len(all_digits_loc):
        right_digit_loc = None
    else:
        right_digit_loc = all_digits_loc[right_in_locations]
    return right_digit_loc


def number_to_df(snailfish_number):
    sh = re.compile("(\[|,|\])")
    snailfish_number_lst = list(filter(None, sh.split(snailfish_number)))
    # snailfish_number_lst = sh.split(snailfish_number) # list(snailfish_number)
    snailfish_number_df = pd.DataFrame({"raw_number": snailfish_number_lst})
    snailfish_number_df["symbol"] = [
        "digit" if x.isdigit() else x for x in snailfish_number_lst
    ]
    snailfish_number_df["value"] = [
        int(x) if x.isdigit() else 0 for x in snailfish_number_lst
    ]
    snailfish_number_df = pd.get_dummies(snailfish_number_df, columns=["symbol"])
    snailfish_number_df["symbol_digit"] = (
        snailfish_number_df["value"] * snailfish_number_df["symbol_digit"]
    )

    return additional_cols(snailfish_number_df)


def additional_cols(snailfish_number_df):
    snailfish_number_df["raw_number"] = snailfish_number_df["raw_number"].astype(str)
    snailfish_number_df["cumsum_["] = snailfish_number_df["symbol_["].cumsum()
    snailfish_number_df["cumsum_]"] = snailfish_number_df["symbol_]"].cumsum()
    snailfish_number_df["is_digit"] = [
        x.isdigit() for x in snailfish_number_df["raw_number"]
    ]
    snailfish_number_df["explode_loc"] = (
        (snailfish_number_df["is_digit"])  # a digit
        & (
            snailfish_number_df["cumsum_["] - snailfish_number_df["cumsum_]"] > 4
        )  # after 5 still open brackets
        & (snailfish_number_df["is_digit"].shift(-2))
    )
    return snailfish_number_df.reset_index(drop=True)


def explode_pair(explode_loc, snailfish_number_df):
    explode_digit_left = snailfish_number_df.loc[explode_loc, "symbol_digit"]
    explode_digit_right = snailfish_number_df.loc[explode_loc + 2, "symbol_digit"]

    digits_loc = np.where((snailfish_number_df["is_digit"]))[0]
    left_loc = get_left_digit_loc(explode_loc, digits_loc)
    right_loc = get_right_digit_loc(explode_loc + 2, digits_loc)

    if left_loc is not None:
        snailfish_number_df.loc[left_loc, "symbol_digit"] += explode_digit_left
        snailfish_number_df.loc[left_loc, "raw_number"] = snailfish_number_df.loc[
            left_loc, "symbol_digit"
        ]
    if right_loc is not None:
        snailfish_number_df.loc[right_loc, "symbol_digit"] += explode_digit_right
        snailfish_number_df.loc[right_loc, "raw_number"] = snailfish_number_df.loc[
            right_loc, "symbol_digit"
        ]

    snailfish_number_df = snailfish_number_df.drop(
        range(explode_loc - 1, (explode_loc + 2) + 2), axis=0
    )

    snailfish_number_df.loc[explode_loc - 1] = np.zeros(
        snailfish_number_df.shape[1], dtype=int
    )
    return additional_cols(snailfish_number_df.sort_index())


def split_number(split_loc, snailfish_number_df):
    digit = snailfish_number_df.loc[split_loc, "symbol_digit"]
    digit_by_2 = digit / 2
    snailfish_number_df = pd.concat(
        [
            snailfish_number_df.loc[: (split_loc - 1)],
            number_to_df(
                "[" + str(floor(digit_by_2)) + "," + str(ceil(digit_by_2)) + "]"
            ),
            snailfish_number_df.loc[(split_loc + 1) :],
        ]
    )
    return additional_cols(snailfish_number_df)


def reduce_number(number):
    snailfish_number = number_to_df(number)
    start_number = number
    end_number = ""
    while end_number != start_number:
        start_number = end_number
        explodes_loc = np.where(snailfish_number["explode_loc"])[0]
        while len(explodes_loc) > 0:
            current_explode_loc = explodes_loc[0]
            snailfish_number = explode_pair(current_explode_loc, snailfish_number)
            explodes_loc = np.where(snailfish_number["explode_loc"])[0]
        splits_loc = np.where(snailfish_number["symbol_digit"] >= 10)[0]
        if len(splits_loc) > 0:
            current_split_loc = splits_loc[0]
            snailfish_number = split_number(current_split_loc, snailfish_number)
            splits_loc = np.where(snailfish_number["symbol_digit"] >= 10)[0]
        end_number = snailfish_number.sort_index()["raw_number"].astype(str).str.cat()
    return end_number


def add_numbers(number_1, number_2):
    to_reduce = "[" + number_1 + "," + number_2 + "]"
    return reduce_number(to_reduce)


def magnitude(lst):
    left = lst[0]
    right = lst[1]
    if (type(left) == int) & (type(right) == int):
        return 3 * left + 2 * right
    elif type(left) == list:
        left = magnitude(left)
    elif type(right) == list:
        right = magnitude(right)
    return magnitude([left, right])


# ---------------- part 1 ----------------

input_list_copy = input_list.copy()
summed = add_numbers(input_list_copy.pop(0), input_list_copy.pop(0))
while len(input_list_copy) > 0:
    summed = add_numbers(summed, input_list_copy.pop(0))
print(summed)
print(magnitude(eval(summed)))


# ---------------- part 2 ----------------
input_list_copy = input_list.copy()
max_mag = 0
while len(input_list_copy) > 0:
    number_1 = input_list_copy.pop(0)
    for number_2 in input_list_copy:
        summed_1 = add_numbers(number_1, number_2)
        summed_2 = add_numbers(number_2, number_1)
        mag_1 = magnitude(eval(summed_1))
        mag_2 = magnitude(eval(summed_2))
        max_mag = max([max_mag, mag_1, mag_2])
print(max_mag)
# 4727 ### too much time ~ 27 min

# for input in sample_magnitude_inputs:
#     print(input)
#     print(magnitude(eval(input)))
#
# ##### reduction test cases
# # should result:
# # [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
# reduce_number(
#     "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
# )
# # should result:
# # [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
# reduce_number(
#     "[[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]"
# )
# # should result:
# # [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
# reduce_number(
#     "[[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]"
# )
#
# # should result:
# # [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
# reduce_number(
#     "[[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]"
# )
#
# # should result:
# # [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
# reduce_number(
#     "[[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],[[2,[2,2]],[8,[8,1]]]]"
# )
#
# # should result:
# # [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
# reduce_number("[[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],[2,9]]")
#
# # should result:
# # [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
# reduce_number(
#     "[[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],[1,[[[9,3],9],[[9,0],[0,7]]]]]"
# )
#
# # should result:
# # [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
# reduce_number(
#     "[[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],[[[5,[7,4]],7],1]]"
# )
#
# # should result:
# # [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
# reduce_number(
#     "[[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],[[[[4,2],2],6],[8,7]]]"
# )