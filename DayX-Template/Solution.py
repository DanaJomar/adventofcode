##### Day X #####
# <URL-TO-PUZZLE>

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

data = pd.read_csv("input.csv", delim_whitespace=True, header=None)

data = np.loadtxt("input_test.csv", dtype=str)

with open("input.csv", "r") as file:
    lines = file.readlines()

# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------


# ---------------- part 2 ----------------
