##### Day 9 #####
# https://adventofcode.com/2021/day/9

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np
import pandas as pd
import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    input = file.readlines()

data = pd.DataFrame([list(x.replace("\n", "")) for x in input]).astype(int)

# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
## solution from: https://stackoverflow.com/a/3986876/4905565
def detect_local_minima(arr):
    # https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array/3689710#3689710
    """
    Takes an array and detects the troughs using the local maximum filter.
    Returns a boolean mask of the troughs (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    # define an connected neighborhood
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#generate_binary_structure
    neighborhood = morphology.generate_binary_structure(len(arr.shape), 2)
    # apply the local minimum filter; all locations of minimum value
    # in their neighborhood are set to 1
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.filters.html#minimum_filter
    local_min = filters.minimum_filter(arr, footprint=neighborhood) == arr
    # local_min is a mask that contains the peaks we are
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.
    #
    # we create the mask of the background
    background = arr == 0
    #
    # a little technicality: we must erode the background in order to
    # successfully subtract it from local_min, otherwise a line will
    # appear along the background border (artifact of the local minimum filter)
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#binary_erosion
    eroded_background = morphology.binary_erosion(
        background, structure=neighborhood, border_value=1
    )
    #
    # we obtain the final mask, containing only peaks,
    # by removing the background from the local_min mask
    detected_minima = local_min ^ eroded_background
    return np.where(detected_minima)


local_minima_locations = detect_local_minima(data.values)
print(sum(data.values[local_minima_locations] + 1))
## 600

# ---------------- part 2 ----------------
def get_neighbours(point, df):
    x = point[0]  # row number
    y = point[1]  # col number
    nrow, ncol = df.shape
    neighbours = []
    values = []
    if x < (nrow - 1):
        neighbours.append((x + 1, y))
        values.append(df.iloc[x + 1, y])
    if x > 0:
        neighbours.append((x - 1, y))
        values.append(df.iloc[x - 1, y])
    if y < (ncol - 1):
        neighbours.append((x, y + 1))
        values.append(df.iloc[x, y + 1])
    if y > 0:
        neighbours.append((x, y - 1))
        values.append(df.iloc[x, y - 1])
    return (neighbours, values)


def find_basin(min_point, df):
    basin = []
    to_check = [min_point]
    max_value = 9
    while len(to_check) > 0:
        point = to_check.pop(0)
        point_value = df.iloc[point[0], point[1]]
        neighbours, values = get_neighbours(point, data)
        in_basin_locs = np.where(values > point_value)[0].tolist()
        for x in in_basin_locs:
            if values[x] != max_value:
                basin.append(neighbours[x])
                to_check.append(neighbours[x])
    return basin + [min_point]


basins = []
basin_lengths = []
for point in zip(local_minima_locations[0], local_minima_locations[1]):
    basin = find_basin(point, data)
    basins = basins + [basin]
    basin_lengths.append(len(set(basin)))

basin_lengths.sort()
print(np.prod(basin_lengths[-3:]))
## 987840

# visualise
data.style.background_gradient(cmap="viridis")
