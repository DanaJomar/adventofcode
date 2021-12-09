##### Day 8 #####
# https://adventofcode.com/2021/day/8

# ------------------------------------------------
# imports
# ------------------------------------------------
import re

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    input = file.readlines()

# input = [
#     "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf\n",
# ]
right_mapping = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}
right_mapping_reversed = {x: y for y, x in right_mapping.items()}
# letter_count:number
unique_len_mappings = {2: 1, 3: 7, 4: 4, 7: 8}
letters = ["a", "b", "c", "d", "e", "f", "g"]
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------

part1_input = [x.split(" | ")[1].replace("\n", "").split(" ") for x in input]
result = {}
for i in unique_len_mappings:
    result[i] = [x for y in part1_input for x in y if len(x) == i]
final_sum = 0
for x in result:
    final_sum += len(result.get(x))
print(final_sum)
## 440

# ---------------- part 2 ----------------
def get_correction_mapping(observed):
    for string in observed:
        if len(string) == 2:
            cf = string
        if len(string) == 3:
            acf = string
        if len(string) == 4:
            bcdf = string
        if len(string) == 7:
            abcdefg = string
    a = re.sub("|".join(list(cf)), "", acf)
    bd = re.sub("|".join(list(cf)), "", bcdf)
    eg = re.sub("|".join(list(bcdf) + [a]), "", abcdefg)
    # if len == 2 --> cf 1
    # if len == 3 --> acf 7
    # if len == 4 --> bcdf 4
    # if len == 7 --> abcdfeg 8
    # if len == 6
    # abcefg 0 (acf, eg, b/d) --> b
    # abdefg 6 (a, bd, eg, c/f) --> f
    # abcdfg 9 (a, bcdf, e/g) or (acf, bd, e/g) --> g

    corr_map = {}
    corr_map[a] = "a"
    for string in observed:
        if len(string) == 6:
            if all(elem in list(string) for elem in list(acf + eg)):
                remaining_char = re.sub("|".join(list(acf + eg)), "", string)
                corr_map[remaining_char] = "b"
                corr_map[bd.replace(remaining_char, "")] = "d"
            if all(elem in list(string) for elem in list(a + bd + eg)):
                remaining_char = re.sub("|".join(list(a + bd + eg)), "", string)
                corr_map[remaining_char] = "f"
                corr_map[cf.replace(remaining_char, "")] = "c"
            if all(elem in list(string) for elem in list(a + bcdf)):
                remaining_char = re.sub("|".join(list(a + bcdf)), "", string)
                corr_map[remaining_char] = "g"
                corr_map[eg.replace(remaining_char, "")] = "e"
    return corr_map


def correct(output, correction_mapping):
    corrected = []
    for error_value in output:
        value_corrected = [
            correction_mapping.get(i) if correction_mapping.get(i) is not None else i
            for i in error_value
        ]
        value_corrected.sort()
        corrected.append("".join(value_corrected))
    return corrected


def get_number(corrected_output, right_mapping_reversed=right_mapping_reversed):
    numbers = []
    for string in corrected_output:
        numbers.append(str(right_mapping_reversed.get(string)))
    return "".join(numbers)


output_values = [x.split(" | ")[1].replace("\n", "").split(" ") for x in input]
observed_values = [x.split(" | ")[0].replace("\n", "").split(" ") for x in input]

final_sum = 0
for i in range(len(observed_values)):
    observed = observed_values[i]
    output = output_values[i]
    corr_map = get_correction_mapping(observed)
    final_sum += int(get_number(correct(output, corr_map)))
print(final_sum)
## 1046281

#  aaaa
# b    c
# b    c
#  dddd
# e    f
# e    f
#  gggg
