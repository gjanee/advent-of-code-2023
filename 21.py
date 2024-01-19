# --- Day 21: Step Counter ---
#
# You manage to catch the airship right as it's dropping someone else
# off on their all-expenses-paid trip to Desert Island!  It even
# helpfully drops you off near the gardener and his massive farm.
#
# "You got the sand flowing again!  Great work!  Now we just need to
# wait until we have enough sand to filter the water for Snow Island
# and we'll have snow again in no time."
#
# While you wait, one of the Elves that works with the gardener heard
# how good you are at solving problems and would like your help.  He
# needs to get his steps in for the day, and so he'd like to know
# which garden plots he can reach with exactly his remaining 64 steps.
#
# He gives you an up-to-date map (your puzzle input) of his starting
# position (S), garden plots (.), and rocks (#).  For example:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
#
# The Elf starts at the starting position (S) which also counts as a
# garden plot.  Then, he can take one step north, south, east, or
# west, but only onto tiles that are garden plots.  This would allow
# him to reach any of the tiles marked O:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#O#....
# .##.OS####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
#
# Then, he takes a second step.  Since at this point he could be at
# either tile marked O, his second step would allow him to reach any
# garden plot that is one step north, south, east, or west of any tile
# that he could have reached after the first step:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#O..#..
# ....#.#....
# .##O.O####.
# .##.O#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
#
# After two steps, he could be at any of the tiles marked O above,
# including the starting position (either by going north-then-south or
# by going west-then-east).
#
# A single third step leads to even more possibilities:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#.O.#..
# ...O#O#....
# .##.OS####.
# .##O.#...#.
# ....O..##..
# .##.#.####.
# .##..##.##.
# ...........
#
# He will continue like this until his steps for the day have been
# exhausted.  After a total of 6 steps, he could reach any of the
# garden plots marked O:
#
# ...........
# .....###.#.
# .###.##.O#.
# .O#O#O.O#..
# O.O.#.#.O..
# .##O.O####.
# .##.O#O..#.
# .O.O.O.##..
# .##.#.####.
# .##O.##.##.
# ...........
#
# In this example, if the Elf's goal was to get exactly 6 more steps
# today, he could use them to reach any of 16 garden plots.
#
# However, the Elf actually needs to get 64 steps today, and the map
# he's handed you is much larger than the example map.
#
# Starting from the garden plot marked S on your map, how many garden
# plots could the Elf reach in exactly 64 steps?

from common import neighbors4

grid = [line.strip() for line in open("21.in")]
R, C = len(grid), len(grid[0])  # grid dimensions

sr = next(filter(lambda r: "S" in grid[r], range(R)))
sc = grid[sr].index("S")

plots = set([(sr, sc)])
for _ in range(64):
    plots = {
        (nr, nc)
        for r, c in plots
        for nr, nc in neighbors4(r, c, R, C)
        if grid[nr][nc] in ".S"
    }

print(len(plots))

# --- Part Two ---
#
# The Elf seems confused by your answer until he realizes his mistake:
# he was reading from a list of his favorite numbers that are both
# perfect squares and perfect cubes, not his step counter.
#
# The actual number of steps he needs to get today is exactly
# 26501365.
#
# He also points out that the garden plots and rocks are set up so
# that the map repeats infinitely in every direction.
#
# So, if you were to look one additional map-width or map-height out
# from the edge of the example map above, you would find that it keeps
# repeating:
#
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##...####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##..S####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##...####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
#
# This is just a tiny three-map-by-three-map slice of the
# inexplicably-infinite farm layout; garden plots and rocks repeat as
# far as you can see.  The Elf still starts on the one middle tile
# marked S, though - every other repeated S is replaced with a normal
# garden plot (.).
#
# Here are the number of reachable garden plots in this new infinite
# version of the example map for different numbers of steps:
#
# - In exactly 6 steps, he can still reach 16 garden plots.
# - In exactly 10 steps, he can reach any of 50 garden plots.
# - In exactly 50 steps, he can reach 1594 garden plots.
# - In exactly 100 steps, he can reach 6536 garden plots.
# - In exactly 500 steps, he can reach 167004 garden plots.
# - In exactly 1000 steps, he can reach 668697 garden plots.
# - In exactly 5000 steps, he can reach 16733044 garden plots.
#
# However, the step count the Elf needs is much larger!  Starting from
# the garden plot marked S on your infinite map, how many garden plots
# could the Elf reach in exactly 26501365 steps?
#
# --------------------
#
# An unsatisfying solution to an extremely frustrating puzzle.
# Unsatisfying because the solution, while satisfyingly simple, relies
# on the input grid having been very specially crafted, and the exact
# characteristics that give rise to a simple solution (or to any
# solution at all for that matter) are unclear.  Frustrating because
# the patterns that both repeat and evolve are hard to tease out, and
# especially hard to extrapolate from small numbers, without
# generating off-by-one and other kinds of errors.  (We attempted to
# solve the puzzle by counting rhombi, but gave up because the
# accounting was too fiddly to get right.  The solution below is based
# on counting square grid tiles.)
#
# The grid (hereinafter "tile" since it repeats) is square with side
# dimension 131 which, significantly, is odd.  The starting plot is
# exactly in the center, at (65, 65).  It is equally significant that
# the number of steps from the center to the tile edges is odd.  The
# four cardinal directions from the starting plot to the tile edges
# are entirely clear of rocks.  Thus, as the Elf moves it reaches the
# four edges of the tile at the same time and its set of possible
# positions fills out a rhombus pattern (more on this later).  As the
# Elf continues to move, the rhombus grows and the Elf's set of
# possible positions encompasses more tiles:
#
#         +-*-+
#         |/ \|
#         /   \
#        /|   |\
#     +-/-+---+-\-+
#     |/  |   |  \|
#     /   |   |   \
#    /|   |   |   |\
# +-/-+---+---+---+-\-+
# |/  |   |   |   |  \|
# *   |   |   |   |   *
# |\  |   |   |   |  /|
# +-\-+---+---+---+-/-+
#    \|   |   |   |/
#     \   |   |   /
#     |\  |   |  /|
#     +-\-+---+-/-+
#        \|   |/
#         \   /
#         |\ /|
#         +-*-+
#
# Complicating this picture is the role of parity, of both individual
# plots and entire tiles.  Once reached, a plot can only be entered
# after either an even number of steps or an odd number, not both.
# This gives each plot a kind of parity.  As the Elf moves, any given
# plot alternates between being reachable or not, blinking in a way
# that is reminiscent of oscillators in the Game of Life.
#
# Further, parity extends to whole tiles.  Each tile can be
# partitioned into the plots reachable by an even number of steps and
# those reachable by an odd number.  Because the side dimension is
# odd, adjacent tiles have opposite parity.  This effect can be seen
# in the following example of a 3x3 grid of 3x3 tiles, where "O" marks
# the plots reachable after an odd number of steps on the left, and an
# even number of steps on the right:
#
# +---+---+---+  +---+---+---+
# |.O.|O.O|.O.|  |O.O|.O.|O.O|
# |O.O|.O.|O.O|  |.O.|O.O|.O.|
# |.O.|O.O|.O.|  |O.O|.O.|O.O|
# +---+---+---+  +---+---+---+
# |O.O|.O.|O.O|  |.O.|O.O|.O.|
# |.O.|OSO|.O.|  |O.O|.S.|O.O|
# |O.O|.O.|O.O|  |.O.|O.O|.O.|
# +---+---+---+  +---+---+---+
# |.O.|O.O|.O.|  |O.O|.O.|O.O|
# |O.O|.O.|O.O|  |.O.|O.O|.O.|
# |.O.|O.O|.O.|  |O.O|.O.|O.O|
# +---+---+---+  +---+---+---+
#
# Understand that both adjacent plots and adjacent tiles alternate
# parity; and that reachability of a given plot and overall
# reachability of a tile alternate with each step of the Elf.  A busy
# picture!
#
# The number of steps asked for, 26501365, is magical because
# 26501365 = 65 + 202300*131.  I.e., the Elf travels to the edge of
# the starting tile, and then fully across an even number of tiles
# after that.  Call the parity that results from the Elf traveling to
# the edge of the starting tile (i.e., traveling 65 steps) "even", and
# the other parity "odd".  Because 65 is odd, this means even tile
# parity is the parity that does *not* include the starting plot.
# Because the Elf travels an even number of full tile widths after
# that (and an even number of steps overall after that), the rhombus
# will have the following consistent structure (2 full tile widths of
# steps are shown here, with E/O indicating even/odd):
#
#         +-*-+
#         |/ \|
#       O / E \ O
#        /|   |\
#     +-/-+---+-\-+
#     |/  |   |  \|
#   O / E | O | E \ O
#    /|   |   |   |\
# +-/-+---+---+---+-\-+
# |/  |   |   |   |  \|
# * E | O | E | O | E *
# |\  |   |   |   |  /|
# +-\-+---+---+---+-/-+
#    \|   |   |   |/
#   O \ E | O | E / O
#     |\  |   |  /|
#     +-\-+---+-/-+
#        \|   |/
#       O \ E / O
#         |\ /|
#         +-*-+
#
# So, how many plots are reachable?  If the Elf travels across n full
# grid tiles after the starting tile then the number of tiles wholly
# or mostly covered (as indicated in the diagram above) is given by
# 2n^2 + 2n + 1.  Of these, assuming the Elf has traveled a number of
# steps such that the parity is shown as above, (n+1)^2 are even and
# n^2 are odd.  That leaves the tile corners at the rhombus edges to
# either include or exclude:
#
#         +-*-+
#         |/ \|
#       O / E \ O
#        /|   |\
#     +-/-+   +-\-+
#     |/         \|
#   O / E       E \ O
#    /|           |\
# +-/-+           +-\-+
# |/                 \|
# * E               E *
# |\                 /|
# +-\-+           +-/-+
#    \|           |/
#   O \ E       E / O
#     |\         /|
#     +-\-+   +-/-+
#        \|   |/
#       O \ E / O
#         |\ /|
#         +-*-+
#
# A tile corner consists of those plots that are of distance greater
# than 65 from the center of the tile in a particular quadrant.  But
# because each corner comes into play equally in considering the
# different sides of the rhombus, we don't need to count the plots in
# individual corners, but can calculate just the sum of all reachable
# plots in all corners of a tile.  With this simplification, the
# corners of n odd tiles must be added, and the corners of n+1 even
# tiles must be subtracted.
#
# With all that analysis, the only real computation we need to do is
# figure out how many plots of each parity can be reached in one tile.
# For this it is sufficient to travel far enough that one tile is
# completely examined, i.e., the maximum distance the Elf can travel
# in a tile, or 65+65 = 130 steps.

assert R == C == 131
assert sr == sc == 65
assert 26501365%131 == 65 and (26501365//131)%2 == 0

odd, even = set([(65, 65)]), set()
s, s_other = odd, even
for _ in range(130):
    for r, c in s:
        for nr, nc in neighbors4(r, c, R, C):
            if grid[nr][nc] in ".S":
                s_other.add((nr, nc))
    s, s_other = s_other, s

def in_corner(t):
    r, c = t
    return abs(r-65)+abs(c-65) > 65

odd_corners = set(filter(in_corner, odd))
even_corners = set(filter(in_corner, even))

n = (26501365-65)//131

print(
    len(even)*(n+1)**2 + len(odd)*n**2
    - (n+1)*len(even_corners)
    + n*len(odd_corners)
)

# So there it is, simple yet unsatisfying.  Questions remain:
#
# - Are the rock-free avenues leading from the starting plot
#   essential, or do they just make the computation simpler?  That is,
#   is the growth neatly quadratic for every possible tile?
# - Is the rhombus that is visually inscribed into the tile
#   significant, or just a hint?  (It doesn't seem to impact our
#   analysis.)
# - Would anything change if there were obstructions such as walls or
#   spirals in the tile?  Or are we relying that the tile is
#   sufficiently open that the rhombus is maximally filled out once
#   the Elf reaches the tile edges?  (It seems that we are.)
#
# An alternative approach, because the growth is quadratic, is to
# sample the growth at three points and use a Lagrange interpolating
# polynomial to recover the quadratic equation.  We did this, sampling
# after the Elf travels 0, 2, and 4 full grid tiles, and got the right
# answer.  But if there were obstructions in the tile, would we need
# to sample farther out to get an accurate interpolation?
