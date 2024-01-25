# --- Day 18: Lavaduct Lagoon ---
#
# Thanks to your efforts, the machine parts factory is one of the
# first factories up and running since the lavafall came back.
# However, to catch up with the large backlog of parts requests, the
# factory will also need a large supply of lava for a while; the Elves
# have already started creating a large lagoon nearby for this
# purpose.
#
# However, they aren't sure the lagoon will be big enough; they've
# asked you to take a look at the dig plan (your puzzle input).  For
# example:
#
# R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)
#
# The digger starts in a 1 meter cube hole in the ground.  They then
# dig the specified number of meters up (U), down (D), left (L), or
# right (R), clearing full 1 meter cubes as they go.  The directions
# are given as seen from above, so if "up" were north, then "right"
# would be east, and so on.  Each trench is also listed with the color
# that the edge of the trench should be painted as an RGB hexadecimal
# color code.
#
# When viewed from above, the above example dig plan would result in
# the following loop of trench (#) having been dug out from otherwise
# ground-level terrain (.):
#
# #######
# #.....#
# ###...#
# ..#...#
# ..#...#
# ###.###
# #...#..
# ##..###
# .#....#
# .######
#
# At this point, the trench could contain 38 cubic meters of lava.
# However, this is just the edge of the lagoon; the next step is to
# dig out the interior so that it is one meter deep as well:
#
# #######
# #######
# #######
# ..#####
# ..#####
# #######
# #####..
# #######
# .######
# .######
#
# Now, the lagoon can contain a much more respectable 62 cubic meters
# of lava.  While the interior is dug out, the edges are also painted
# according to the color codes in the dig plan.
#
# The Elves are concerned the lagoon won't be large enough; if they
# follow their dig plan, how many cubic meters of lava could it hold?
#
# --------------------
#
# The lagoon, a polygon, will be huge in part 2, so we use the
# shoelace formula to calculate its area.  However, interpreting grid
# coordinates as points in the Cartesian plane will cause the outer
# edges of grid tiles on the polygon perimeter to be omitted.  The
# diagram below illustrates the problem.  Polygon vertices are marked
# with (V), edges with (=, !).  The quadrants of grid tiles not
# included by the shoelace formula are marked with (x).
#
#       0       1       2
#   +-------+-------+
#   | x   x | x   x |
# 0 |   V===============
#   | x !   |       |
#   +---!---+-------+
#   | x !   |
# 1 |   !   |      (polygon interior)
#   | x !   |
#   +---!---+-------+-------+
#   | x !   |       |       |
# 2 |   V===============V   |
#   | x   x | x   x | x !   |
#   +-------+-------+---!---+
#                   | x !   |
# 3                 |   !   |
#                   | x !   |
#                   +---!---+
#                       !
#
# Each grid tile on the polygon perimeter that is not a vertex
# contributes an additional 1/2 tile to the area.  Each grid tile that
# is an external (or convex) vertex contributes 3/4 of a tile, and
# each internal (or concave) vertex contributes 1/4.  To eliminate the
# need to figure out which vertices are convex and which are concave,
# observe that every polygon requires exactly 4 convex vertices to
# form a closed loop.  Every concave vertex must therefore be paired
# with an additional convex vertex.  Thus the 4 required convex
# vertices add 4*3/4 = 3 to the area, while the remaining vertices
# add, on average, 1/2 tile to the area each.  (This calculation
# assumes that adjacent edges are not collinear, i.e., that vertices
# always indicate turns.)

directives = []
colors = []
for line in open("18.in"):
    dir, n, color = line.split()
    directives.append((dir, int(n)))
    colors.append(color[2:-1])

def to_polygon(directives):
    # We use a Cartesian (x, y) coordinate system for this puzzle
    # instead of the (row, column) coordinate system used in previous
    # puzzles.
    dirs = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
    vertices = [(0, 0)]
    r, c = 0, 0
    for i, (d, n) in enumerate(directives[:-1]):
        r += dirs[d][0]*n
        c += dirs[d][1]*n
        if d != directives[i+1][0]:  # if at turn
            vertices.append((r, c))
    if directives[0][0] == directives[-1][0]:
        # If the first and last directions are the same, then the
        # first and last edges are collinear and the starting vertex
        # can be eliminated.
        del vertices[0]
    return vertices

def area(vertices):
    nv = len(vertices)
    area = 0
    perimeter = 0
    for i in range(nv):
        vi = vertices[i]
        vj = vertices[(i+1)%nv]
        area += vi[0]*vj[1] - vi[1]*vj[0]
        perimeter += abs(vj[0]-vi[0]) + abs(vj[1]-vi[1])
    # The shoelace formula assumes vertices are in counterclockwise
    # order.  If not, the area will simply be negative.
    return abs(area)//2 + (perimeter-nv)//2 + 3 + (nv-4)//2

print(area(to_polygon(directives)))

# --- Part Two ---
#
# The Elves were right to be concerned; the planned lagoon would be
# much too small.
#
# After a few minutes, someone realizes what happened; someone swapped
# the color and instruction parameters when producing the dig plan.
# They don't have time to fix the bug; one of them asks if you can
# extract the correct instructions from the hexadecimal codes.
#
# Each hexadecimal code is six hexadecimal digits long.  The first
# five hexadecimal digits encode the distance in meters as a
# five-digit hexadecimal number.  The last hexadecimal digit encodes
# the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means
# U.
#
# So, in the above example, the hexadecimal codes can be converted
# into the true instructions:
#
# - #70c710 = R 461937
# - #0dc571 = D 56407
# - #5713f0 = R 356671
# - #d2c081 = D 863240
# - #59c680 = R 367720
# - #411b91 = D 266681
# - #8ceee2 = L 577262
# - #caa173 = U 829975
# - #1b58a2 = L 112010
# - #caa171 = D 829975
# - #7807d2 = L 491645
# - #a77fa3 = U 686074
# - #015232 = L 5411
# - #7a21e3 = U 500254
#
# Digging out this loop and its interior produces a lagoon that can
# hold an impressive 952408144115 cubic meters of lava.
#
# Convert the hexadecimal color codes into the correct instructions;
# if the Elves follow this new dig plan, how many cubic meters of lava
# could the lagoon hold?

directives = [
    ("RDLU"[int(c[5])], int(c[:5], 16))
    for c in colors
]

print(area(to_polygon(directives)))
