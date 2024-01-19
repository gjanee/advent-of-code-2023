# --- Day 24: Never Tell Me The Odds ---
#
# It seems like something is going wrong with the snow-making process.
# Instead of forming snow, the water that's been absorbed into the air
# seems to be forming hail!
#
# Maybe there's something you can do to break up the hailstones?
#
# Due to strong, probably-magical winds, the hailstones are all flying
# through the air in perfectly linear trajectories.  You make a note
# of each hailstone's position and velocity (your puzzle input).  For
# example:
#
# 19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3
#
# Each line of text corresponds to the position and velocity of a
# single hailstone.  The positions indicate where the hailstones are
# right now (at time 0).  The velocities are constant and indicate
# exactly how far each hailstone will move in one nanosecond.
#
# Each line of text uses the format px py pz @ vx vy vz.  For
# instance, the hailstone specified by 20, 19, 15 @ 1, -5, -3 has
# initial X position 20, Y position 19, Z position 15, X velocity 1, Y
# velocity -5, and Z velocity -3.  After one nanosecond, the hailstone
# would be at 21, 14, 12.
#
# Perhaps you won't have to do anything.  How likely are the
# hailstones to collide with each other and smash into tiny ice
# crystals?
#
# To estimate this, consider only the X and Y axes; ignore the Z axis.
# Looking forward in time, how many of the hailstones' paths will
# intersect within a test area?  (The hailstones themselves don't have
# to collide, just test for intersections between the paths they will
# trace.)
#
# In this example, look for intersections that happen with an X and Y
# position each at least 7 and at most 27; in your actual data, you'll
# need to check a much larger test area.  Comparing all pairs of
# hailstones' future paths produces the following results:
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 18, 19, 22 @ -1, -1, -2
# Hailstones' paths will cross inside the test area (at x=14.333,
# y=15.333).
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 20, 25, 34 @ -2, -2, -4
# Hailstones' paths will cross inside the test area (at x=11.667,
# y=16.667).
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 12, 31, 28 @ -1, -2, -1
# Hailstones' paths will cross outside the test area (at x=6.2,
# y=19.4).
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for hailstone A.
#
# Hailstone A: 18, 19, 22 @ -1, -1, -2
# Hailstone B: 20, 25, 34 @ -2, -2, -4
# Hailstones' paths are parallel; they never intersect.
#
# Hailstone A: 18, 19, 22 @ -1, -1, -2
# Hailstone B: 12, 31, 28 @ -1, -2, -1
# Hailstones' paths will cross outside the test area (at x=-6, y=-5).
#
# Hailstone A: 18, 19, 22 @ -1, -1, -2
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for both hailstones.
#
# Hailstone A: 20, 25, 34 @ -2, -2, -4
# Hailstone B: 12, 31, 28 @ -1, -2, -1
# Hailstones' paths will cross outside the test area (at x=-2, y=3).
#
# Hailstone A: 20, 25, 34 @ -2, -2, -4
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for hailstone B.
#
# Hailstone A: 12, 31, 28 @ -1, -2, -1
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for both hailstones.
#
# So, in this example, 2 hailstones' future paths cross inside the
# boundaries of the test area.
#
# However, you'll need to search a much larger test area if you want
# to see if any hailstones might collide.  Look for intersections that
# happen with an X and Y position each at least 200000000000000 and at
# most 400000000000000.  Disregard the Z axis entirely.
#
# Considering only the X and Y axes, check all pairs of hailstones'
# future paths for intersections.  How many of these intersections
# occur within the test area?
#
# --------------------
#
# Hailstone paths are lines defined parametrically as functions of
# time.  In this part we are interested if two *lines* intersect; if
# there is an intersection, the hailstones may pass through the
# intersection point at different times.  Thus to answer this part,
# for paths a and b we seek if there are two times t_a and t_b such
# that
#
# { dx_a*t_a + px_a = dx_b*t_b + px_b
# { dy_a*t_a + py_a = dy_b*t_b + py_b
#
# This is a linear system of two equations with two unknowns.  We
# could solve it using NumPy, but in the spirit of running these
# puzzle solutions on stock Python, we write our own Gaussian
# elimination solver.

from collections import namedtuple
from fractions import Fraction as F
import re

Path = namedtuple("Path", "px py pz dx dy dz")

paths = [
    Path(*map(int, re.findall(r"-?\d+", line)))
    for line in open("24.in")
]

def solve(A, B):
    # Solve matrix equation Ax = B for square A by Gaussian
    # elimination and return True if successful.  A and B are both
    # modified; upon successful return, A is the identity matrix and B
    # holds the solution values.  False is returned if the matrix is
    # singular.  This function is written to preserve the type of the
    # entries (in particular, if the type is Fraction), not for
    # numerical stability.
    n = len(A)
    # Reduce to row echelon form.
    for i in range(n):
        if A[i][i] == 0:
            j = next(filter(lambda j: A[j][i] != 0, range(i, n)), None)
            if j == None:
                return False
            for c in range(i, n):
                A[i][c], A[j][c] = A[j][c], A[i][c]
            B[i], B[j] = B[j], B[i]
        for j in range(i+1, n):
            f = A[j][i]/A[i][i]
            for c in range(i, n):
                A[j][c] -= f*A[i][c]
            B[j] -= f*B[i]
    # Back substitute solution values.
    for i in range(n-1, -1, -1):
        B[i] /= A[i][i]
        A[i][i] /= A[i][i]
        for j in range(i):
            B[j] -= A[j][i]*B[i]
            A[j][i] -= A[j][i]
    return True

def intersects(path_a, path_b):
    LB, UB = 200000000000000, 400000000000000  # test area bounds
    A = [
        [F(path_a.dx), F(-path_b.dx)],
        [F(path_a.dy), F(-path_b.dy)]
    ]
    B = [
        F(path_b.px-path_a.px),
        F(path_b.py-path_a.py)
    ]
    success = solve(A, B)
    if not success:
        return False
    t_a, t_b = B
    return (
        t_a > 0 and t_b > 0
        and LB <= path_a.dx*t_a + path_a.px <= UB
        and LB <= path_a.dy*t_a + path_a.py <= UB
    )

print(
    sum(
        intersects(paths[i], paths[j])
        for i in range(len(paths))
        for j in range(i+1, len(paths))
    )
)

# --- Part Two ---
#
# Upon further analysis, it doesn't seem like any hailstones will
# naturally collide.  It's up to you to fix that!
#
# You find a rock on the ground nearby.  While it seems extremely
# unlikely, if you throw it just right, you should be able to hit
# every hailstone in a single throw!
#
# You can use the probably-magical winds to reach any integer position
# you like and to propel the rock at any integer velocity.  Now
# including the Z axis in your calculations, if you throw the rock at
# time 0, where do you need to be so that the rock perfectly collides
# with every hailstone?  Due to probably-magical inertia, the rock
# won't slow down or change direction when it collides with a
# hailstone.
#
# In the example above, you can achieve this by moving to position 24,
# 13, 10 and throwing the rock at velocity -3, 1, 2.  If you do this,
# you will hit every hailstone as follows:
#
# Hailstone: 19, 13, 30 @ -2, 1, -2
# Collision time: 5
# Collision position: 9, 18, 20
#
# Hailstone: 18, 19, 22 @ -1, -1, -2
# Collision time: 3
# Collision position: 15, 16, 16
#
# Hailstone: 20, 25, 34 @ -2, -2, -4
# Collision time: 4
# Collision position: 12, 17, 18
#
# Hailstone: 12, 31, 28 @ -1, -2, -1
# Collision time: 6
# Collision position: 6, 19, 22
#
# Hailstone: 20, 19, 15 @ 1, -5, -3
# Collision time: 1
# Collision position: 21, 14, 12
#
# Above, each hailstone is identified by its initial position and its
# velocity.  Then, the time and position of that hailstone's collision
# with your rock are given.
#
# After 1 nanosecond, the rock has exactly the same position as one of
# the hailstones, obliterating it into ice dust!  Another hailstone is
# smashed to bits two nanoseconds after that.  After a total of 6
# nanoseconds, all of the hailstones have been destroyed.
#
# So, at time 0, the rock needs to be at X position 24, Y position 13,
# and Z position 10.  Adding these three coordinates together produces
# 47.  (Don't add any coordinates from the rock's velocity.)
#
# Determine the exact position and velocity the rock needs to have at
# time 0 so that it perfectly collides with every hailstone.  What do
# you get if you add up the X, Y, and Z coordinates of that initial
# position?
#
# --------------------
#
# For more compact notation, rename variables as follows:
#
# dx -> a
# px -> b
# dy -> c
# py -> d
# dz -> e
# pz -> f
#
# We seek a path for the rock, defined parametrically by {A, B, C, D,
# E, F} as:
#
# { x = At + B
# { y = Ct + D
# { z = Et + F
#
# In this part we are interested when the hailstones and rock
# themselves intersect, not just their supporting lines.  Intersecting
# the rock path with a particular hailstone path {a, b, c, d, e, f}
# yields an intersection at some time t:
#
# { At + B = at + b
# { Ct + D = ct + d
# { Et + F = et + f
#
# Intersections with other hailstones will occur at other times.  To
# remove the aspect of time, and relate the rock's and hailstone's
# paths purely on their trajectories, eliminate t:
#
# (B-b)/(a-A) = (D-d)/(c-C) = (F-f)/(e-E)
#
# Or, avoiding division:
#
# (B-b)(c-C) = (D-d)(a-A)
# (D-d)(e-E) = (F-f)(c-C)
# (B-b)(e-E) = (F-f)(a-A)
#
# Multiplying out and reorganizing, we get:
#
# { AD-BC = dA - cB - bC + aD + bc-ad
# { CF-DE = fC - eD - dE + cF + de-cf
# { AF-BE = fA - eB - bE + aF + be-af
#
# Notice that the left sides of the equations are independent of the
# chosen hailstone path.  Thus if we select two hailstone paths and
# equate them using the above, we arrive at a system of 3 linear
# equations over our 6 unknowns A-F:
#
# (d1-d2)A - (c1-c2)B - (b1-b2)C + (a1-a2)D = b2*c2-a2*d2 - (b1*c1-a1*d1)
# (f1-f2)C - (e1-e2)D - (d1-d2)E + (c1-c2)F = d2*e2-c2*f2 - (d1*e1-c1*f1)
# (f1-f2)A - (e1-e2)B - (b1-b2)E + (a1-a2)F = b2*e2-a2*f2 - (b1*e1-a1*f1)
#
# By similarly equating the second hailstone path with a third, we
# arrive at a system of 6 equations and 6 unknowns.  (We're assuming
# the rock will hit the other 297 hailstones in the input, but then,
# the puzzle wouldn't make sense if it didn't.)

# Rename variables.
Path2 = namedtuple("Path2", "b d f a c e")

# Pick three arbitrary paths (we're assuming they're not parallel
# here).
j = Path2(*paths[0])
k = Path2(*paths[1])
l = Path2(*paths[2])

A = [
    [F(j.d-k.d), F(k.c-j.c), F(k.b-j.b), F(j.a-k.a),       F(0),       F(0)],
    [      F(0),       F(0), F(j.f-k.f), F(k.e-j.e), F(k.d-j.d), F(j.c-k.c)],
    [F(j.f-k.f), F(k.e-j.e),       F(0),       F(0), F(k.b-j.b), F(j.a-k.a)],
    [F(k.d-l.d), F(l.c-k.c), F(l.b-k.b), F(k.a-l.a),       F(0),       F(0)],
    [      F(0),       F(0), F(k.f-l.f), F(l.e-k.e), F(l.d-k.d), F(k.c-l.c)],
    [F(k.f-l.f), F(l.e-k.e),       F(0),       F(0), F(l.b-k.b), F(k.a-l.a)]
]

B = [
    F(k.b*k.c - j.b*j.c + j.a*j.d - k.a*k.d),
    F(k.d*k.e - j.d*j.e + j.c*j.f - k.c*k.f),
    F(k.b*k.e - j.b*j.e + j.a*j.f - k.a*k.f),
    F(l.b*l.c - k.b*k.c + k.a*k.d - l.a*l.d),
    F(l.d*l.e - k.d*k.e + k.c*k.f - l.c*l.f),
    F(l.b*l.e - k.b*k.e + k.a*k.f - l.a*l.f)
]

success = solve(A, B)
assert success

print(B[1]+B[3]+B[5])
