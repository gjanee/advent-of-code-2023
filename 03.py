# --- Day 3: Gear Ratios ---
#
# You and the Elf eventually reach a gondola lift station; he says the
# gondola lift will take you up to the water source, but this is as
# far as he can bring you.  You go inside.
#
# It doesn't take long to find the gondolas, but there seems to be a
# problem: they're not moving.
#
# "Aaah!"
#
# You turn around to see a slightly-greasy Elf with a wrench and a
# look of surprise.  "Sorry, I wasn't expecting anyone!  The gondola
# lift isn't working right now; it'll still be a while before I can
# fix it."  You offer to help.
#
# The engineer explains that an engine part seems to be missing from
# the engine, but nobody can figure out which one.  If you can add up
# all the part numbers in the engine schematic, it should be easy to
# work out which part is missing.
#
# The engine schematic (your puzzle input) consists of a visual
# representation of the engine.  There are lots of numbers and symbols
# you don't really understand, but apparently any number adjacent to a
# symbol, even diagonally, is a "part number" and should be included
# in your sum.  (Periods (.) do not count as a symbol.)
#
# Here is an example engine schematic:
#
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
#
# In this schematic, two numbers are not part numbers because they are
# not adjacent to a symbol: 114 (top right) and 58 (middle right).
# Every other number is adjacent to a symbol and so is a part number;
# their sum is 4361.
#
# Of course, the actual engine schematic is much larger.  What is the
# sum of all of the part numbers in the engine schematic?
#
# --------------------
#
# The first part of this puzzle is written to support part 2, which
# asks a very different question.  Part numbers are repeated in the
# input.  We accommodate the possibility that two instances of a part
# number are adjacent to the same symbol (though this never happens in
# our input).

from collections import defaultdict
from functools import reduce
import re

pattern = re.compile(r"\d+")

def is_symbol(c):
    return not (c.isdigit() or c == ".")

grid = [line.strip() for line in open("03.in")]
R, C = len(grid), len(grid[0])  # grid dimensions

# Adjacency sparse matrix: maps a symbol location (row, col) to a set
# of adjacent part numbers, each described by
# (row, start_col, end_col).
adj = defaultdict(lambda: set())

for r in range(R):
    i = 0
    while True:
        m = pattern.search(grid[r], pos=i)
        if m == None:
            break
        for nr in [r-1, r, r+1]:
            for nc in range(m.start()-1, m.end()+1):
                if nr in range(R) and nc in range(C):
                    if is_symbol(grid[nr][nc]):
                        adj[(nr, nc)].add((r, m.start(), m.end()))
        i = m.end()

print(
    sum(
        int(grid[row][start_col:end_col])
        for row, start_col, end_col in reduce(set.union, adj.values())
    )
)

# --- Part Two ---
#
# The engineer finds the missing part and installs it in the engine!
# As the engine springs to life, you jump in the closest gondola,
# finally ready to ascend to the water source.
#
# You don't seem to be going very fast, though.  Maybe something is
# still wrong?  Fortunately, the gondola has a phone labeled "help",
# so you pick it up and the engineer answers.
#
# Before you can explain the situation, she suggests that you look out
# the window.  There stands the engineer, holding a phone in one hand
# and waving with the other.  You're going so slowly that you haven't
# even left the station.  You exit the gondola.
#
# The missing part wasn't the only issue - one of the gears in the
# engine is wrong.  A gear is any * symbol that is adjacent to exactly
# two part numbers.  Its gear ratio is the result of multiplying those
# two numbers together.
#
# This time, you need to find the gear ratio of every gear and add
# them all up so that the engineer can figure out which gear needs to
# be replaced.
#
# Consider the same engine schematic again:
#
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
#
# In this schematic, there are two gears.  The first is in the top
# left; it has part numbers 467 and 35, so its gear ratio is 16345.
# The second gear is in the lower right; its gear ratio is 451490.
# (The * adjacent to 617 is not a gear because it is only adjacent to
# one part number.)  Adding up all of the gear ratios produces 467835.
#
# What is the sum of all of the gear ratios in your engine schematic?

from operator import mul

print(
    sum(
        reduce(
            mul,
            [
                int(grid[row][start_col:end_col])
                for row, start_col, end_col in s
            ]
        )
        for (r, c), s in adj.items()
        if grid[r][c] == "*" and len(s) == 2
    )
)
