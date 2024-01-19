# --- Day 23: A Long Walk ---
#
# The Elves resume water filtering operations!  Clean water starts
# flowing over the edge of Island Island.
#
# They offer to help you go over the edge of Island Island, too!  Just
# hold on tight to one end of this impossibly long rope and they'll
# lower you down a safe distance from the massive waterfall you just
# created.
#
# As you finally reach Snow Island, you see that the water isn't
# really reaching the ground: it's being absorbed by the air itself.
# It looks like you'll finally have a little downtime while the
# moisture builds up to snow-producing levels.  Snow Island is pretty
# scenic, even without any snow; why not take a walk?
#
# There's a map of nearby hiking trails (your puzzle input) that
# indicates paths (.), forest (#), and steep slopes (^, >, v, and <).
#
# For example:
#
# #.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#
#
# You're currently on the single path tile in the top row; your goal
# is to reach the single path tile in the bottom row.  Because of all
# the mist from the waterfall, the slopes are probably quite icy; if
# you step onto a slope tile, your next step must be downhill (in the
# direction the arrow is pointing).  To make sure you have the most
# scenic hike possible, never step onto the same tile twice.  What is
# the longest hike you can take?
#
# In the example above, the longest hike you can take is marked with
# O, and your starting position is marked S:
#
# #S#####################
# #OOOOOOO#########...###
# #######O#########.#.###
# ###OOOOO#OOO>.###.#.###
# ###O#####O#O#.###.#.###
# ###OOOOO#O#O#.....#...#
# ###v###O#O#O#########.#
# ###...#O#O#OOOOOOO#...#
# #####.#O#O#######O#.###
# #.....#O#O#OOOOOOO#...#
# #.#####O#O#O#########v#
# #.#...#OOO#OOO###OOOOO#
# #.#.#v#######O###O###O#
# #...#.>.#...>OOO#O###O#
# #####v#.#.###v#O#O###O#
# #.....#...#...#O#O#OOO#
# #.#########.###O#O#O###
# #...###...#...#OOO#O###
# ###.###.#.###v#####O###
# #...#...#.#.>.>.#.>O###
# #.###.###.#.###.#.#O###
# #.....###...###...#OOO#
# #####################O#
#
# This hike contains 94 steps.  (The other possible hikes you could
# have taken were 90, 86, 82, 82, and 74 steps long.)
#
# Find the longest hike you can take through the hiking trails listed
# on your map.  How many steps long is the longest hike?
#
# --------------------
#
# We abstract the network of hiking trails into a directed graph.  Our
# parsing relies on arrows appearing adjacent to junctions in the
# network exactly and only in those places; junctions correspond to
# graph nodes.  We use a brute force approach because it will be
# needed in part 2, but since the graph is directed in this part, we
# could also have found the longest path by topologically sorting the
# nodes and computing the length from the sorted list.

from common import neighbors4

grid = {
    (r, c): v
    for r, line in enumerate(open("23.in"))
    for c, v in enumerate(line.strip())
}
R = max(r for r, c in grid) + 1  # grid dimensions
C = max(c for r, c in grid) + 1

start = next(filter(lambda loc: loc[0] == 0 and grid[loc] == ".", grid))
end = next(filter(lambda loc: loc[0] == R-1 and grid[loc] == ".", grid))

class Node:

    all = {}  # loc => Node

    def __init__(self, loc):
        self.loc = loc
        self.edges = set()  # {(node, distance), ...}
        Node.all[loc] = self

    @staticmethod
    def get(loc):
        if loc in Node.all:
            return Node.all[loc]
        else:
            return Node(loc)

    @staticmethod
    def reset():
        for node in Node.all.values():
            node.visited = False

movable_dirs = [
    " ^ ",
    "<*>",
    " v "
]

todo = [(Node.get(start), (start[0]+1, start[1]))]
while len(todo) > 0:
    from_node, loc = todo.pop()
    prev_loc = from_node.loc
    # Walk to the next junction.
    dist = 1
    while True:
        next_locs = [
            next_loc
            for next_loc in neighbors4(loc, R, C)
            if grid[next_loc] in ".<>^v" and next_loc != prev_loc
        ]
        if len(next_locs) != 1:
            break
        dist += 1
        prev_loc, loc = loc, next_locs[0]
    # Reached a junction or the end.
    to_node = Node.get(loc)
    from_node.edges.add((to_node, dist))
    for next_loc in next_locs:
        dr, dc = next_loc[0]-loc[0], next_loc[1]-loc[1]
        if grid[next_loc] == movable_dirs[dr+1][dc+1]:
            todo.append((to_node, next_loc))

def longest_path_length():
    lpl = 0
    def dfs(node, dist):
        nonlocal lpl
        if node.loc == end:
            lpl = max(lpl, dist)
            return
        node.visited = True
        for n, d in node.edges:
            if not n.visited:
                dfs(n, dist+d)
        node.visited = False
    Node.reset()
    dfs(Node.all[start], 0)
    return lpl

print(longest_path_length())

# --- Part Two ---
#
# As you reach the trailhead, you realize that the ground isn't as
# slippery as you expected; you'll have no problem climbing up the
# steep slopes.
#
# Now, treat all slopes as if they were normal paths (.).  You still
# want to make sure you have the most scenic hike possible, so
# continue to ensure that you never step onto the same tile twice.
# What is the longest hike you can take?
#
# In the example above, this increases the longest hike to 154 steps:
#
# #S#####################
# #OOOOOOO#########OOO###
# #######O#########O#O###
# ###OOOOO#.>OOO###O#O###
# ###O#####.#O#O###O#O###
# ###O>...#.#O#OOOOO#OOO#
# ###O###.#.#O#########O#
# ###OOO#.#.#OOOOOOO#OOO#
# #####O#.#.#######O#O###
# #OOOOO#.#.#OOOOOOO#OOO#
# #O#####.#.#O#########O#
# #O#OOO#...#OOO###...>O#
# #O#O#O#######O###.###O#
# #OOO#O>.#...>O>.#.###O#
# #####O#.#.###O#.#.###O#
# #OOOOO#...#OOO#.#.#OOO#
# #O#########O###.#.#O###
# #OOO###OOO#OOO#...#O###
# ###O###O#O###O#####O###
# #OOO#OOO#O#OOO>.#.>O###
# #O###O###O#O###.#.#O###
# #OOOOO###OOO###...#OOO#
# #####################O#
#
# Find the longest hike you can take through the surprisingly dry
# hiking trails listed on your map.  How many steps long is the
# longest hike?

for node in Node.all.values():
    for n, d in node.edges:
        n.edges.add((node, d))

print(longest_path_length())
