##### Day 20 #####
# https://adventofcode.com/2022/day/20

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
data = np.loadtxt("input.csv", dtype=int)
original_order = [(i, data[i]) for i in range(len(data))]
# ------------------------------------------------
# Solution
# ------------------------------------------------
def mix(current_order, original_order):
    data_copy = current_order.copy()
    for val_id, value in original_order:
        # (val_id, value) = (0, 1)
        # print(val_id, value)
        idx = data_copy.index((val_id, value))
        data_copy.pop(idx)
        new_idx = (idx + value) % len(data_copy)
        data_copy.insert(new_idx, (val_id, value))
        # print([y for x, y in data_copy])
    return data_copy


# ---------------- part 1 ----------------

mixed_data = mix(original_order, original_order)
zero_index = [y for x, y in mixed_data].index(0)
sum(
    [
        mixed_data[(zero_index + 1000) % len(data)][1],
        mixed_data[(zero_index + 2000) % len(data)][1],
        mixed_data[(zero_index + 3000) % len(data)][1],
    ]
)
# ---------------- part 2 ----------------
dec_key = 811589153
decrypted_data = [(x, y * dec_key) for x, y in original_order]
mixed_data = decrypted_data.copy()
for i in range(10):
    mixed_data = mix(mixed_data, decrypted_data)

zero_index = [y for x, y in mixed_data].index(0)
sum(
    [
        mixed_data[(zero_index + 1000) % len(data)][1],
        mixed_data[(zero_index + 2000) % len(data)][1],
        mixed_data[(zero_index + 3000) % len(data)][1],
    ]
)
