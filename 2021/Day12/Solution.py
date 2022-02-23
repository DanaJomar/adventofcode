##### Day 12 #####
# https://adventofcode.com/2021/day/12

# ------------------------------------------------
# imports
# ------------------------------------------------

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

with open("input.csv", "r") as file:
    lines = file.readlines()
lines = [l.replace("\n", "") for l in lines]

graph = {}
for line in lines:
    nodes = line.split("-")
    graph[nodes[0]] = graph.get(nodes[0], []) + [nodes[1]]
    graph[nodes[1]] = graph.get(nodes[1], []) + [nodes[0]]

# remove the links leaving the end or goining back to the start
graph.pop("end")
graph = {x: [y1 for y1 in y if y1 != "start"] for x, y in graph.items()}
# ------------------------------------------------
# Solution
# ------------------------------------------------
## Based on Dijakstra
def find_all_paths(graph, start, end, path=[], accepts_small_dupl=False):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if accepts_small_dupl:
            if (node in path) & (node.islower()):
                newpaths = find_all_paths(graph, node, end, path, False)
                for newpath in newpaths:
                    paths.append(newpath)
            else:
                newpaths = find_all_paths(graph, node, end, path, True)
                for newpath in newpaths:
                    paths.append(newpath)
        else:
            if (node not in path) | (node.isupper()):
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
    return paths


# ---------------- part 1 ----------------
paths = find_all_paths(graph, "start", "end")
len(paths)

# ---------------- part 2 ----------------
paths = find_all_paths(graph, "start", "end", [], True)
len(paths)