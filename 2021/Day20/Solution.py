##### Day 20 #####
# https://adventofcode.com/2021/day/20

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()
lines = [x.replace("\n", "") for x in lines]

sep_loc = lines.index("")
algorithm = "".join(lines[0:sep_loc])
image = lines[(sep_loc + 1) :]

# ------------------------------------------------
# Solution
# ------------------------------------------------
image_array = np.array([list(x) for x in image])
image_array = 0 + (image_array == "#")


def remove_padding(img, axis):
    all_lit = img.sum()
    detect_padding = (img.sum(axis=axis)).cumsum()

    padding_before = np.where(detect_padding == 0)[0]
    padding_after = np.where(detect_padding == all_lit)[0][1:]
    to_remove = np.append(padding_before, padding_after)
    return np.delete(img, to_remove, axis=1 - axis)


def binatodeci(binary):
    return sum(val * (2 ** idx) for idx, val in enumerate(reversed(binary)))


def get_or_default(df, loc_tuple, pad_val):
    if (
        (loc_tuple[0] < 0)
        | (loc_tuple[0] >= df.shape[0])
        | (loc_tuple[1] < 0)
        | (loc_tuple[1] >= df.shape[1])
    ):
        return pad_val
    return df[loc_tuple]


def get_neighbourhood(map, x, y, pad_val):
    return [
        get_or_default(map, (x - 1, y - 1), pad_val),
        get_or_default(map, (x - 1, y), pad_val),
        get_or_default(map, (x - 1, y + 1), pad_val),
        get_or_default(map, (x, y - 1), pad_val),
        get_or_default(map, (x, y), pad_val),
        get_or_default(map, (x, y + 1), pad_val),
        get_or_default(map, (x + 1, y - 1), pad_val),
        get_or_default(map, (x + 1, y), pad_val),
        get_or_default(map, (x + 1, y + 1), pad_val),
    ]


def get_new_val(pixel_loc):
    return 0 + (algorithm[pixel_loc] == "#")


def enhance(image, n):
    i = 0
    padding_val = 0
    while i < n:
        i = i + 1
        image_extended = np.pad(image, 2, mode="constant", constant_values=padding_val)
        enhanced_image = np.zeros(image_extended.shape, dtype=int)
        for x in range(image_extended.shape[0]):
            for y in range(image_extended.shape[1]):
                pixel_loc = binatodeci(
                    get_neighbourhood(image_extended, x, y, padding_val)
                )
                enhanced_image[x, y] = get_new_val(pixel_loc)

        enhanced_image = remove_padding(enhanced_image, 0)
        enhanced_image = remove_padding(enhanced_image, 1)
        enhanced_image = 1 - remove_padding(1 - enhanced_image, 0)
        enhanced_image = 1 - remove_padding(1 - enhanced_image, 1)
        image = enhanced_image.copy()
        padding_val = get_new_val(binatodeci(np.repeat([padding_val], 9)))
    return image


# ---------------- part 1 ----------------
enhanced_image = enhance(image_array, 2)
plt.imshow(pd.DataFrame(1 - enhanced_image), cmap="Greys")
enhanced_image.sum()

# ---------------- part 2 ----------------
enhanced_image = enhance(image_array, 50)
plt.imshow(pd.DataFrame(1 - enhanced_image), cmap="Greys")
enhanced_image.sum()