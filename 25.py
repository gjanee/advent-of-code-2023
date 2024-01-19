# --- Day 25: Snowverload ---
#
# Still somehow without snow, you go to the last place you haven't
# checked: the center of Snow Island, directly below the waterfall.
#
# Here, someone has clearly been trying to fix the problem.  Scattered
# everywhere are hundreds of weather machines, almanacs, communication
# modules, hoof prints, machine parts, mirrors, lenses, and so on.
#
# Somehow, everything has been wired together into a massive
# snow-producing apparatus, but nothing seems to be running.  You
# check a tiny screen on one of the communication modules: Error 2023.
# It doesn't say what Error 2023 means, but it does have the phone
# number for a support line printed on it.
#
# "Hi, you've reached Weather Machines And So On, Inc.  How can I help
# you?"  You explain the situation.
#
# "Error 2023, you say?  Why, that's a power overload error, of
# course!  It means you have too many components plugged in.  Try
# unplugging some components and--"  You explain that there are
# hundreds of components here and you're in a bit of a hurry.
#
# "Well, let's see how bad it is; do you see a big red reset button
# somewhere?  It should be on its own module.  If you push it, it
# probably won't fix anything, but it'll report how overloaded things
# are."  After a minute or two, you find the reset button; it's so big
# that it takes two hands just to get enough leverage to push it.  Its
# screen then displays:
#
# SYSTEM OVERLOAD!
# Connected components would require power equal to at least 100
# stars!
#
# "Wait, how many components did you say are plugged in?  With that
# much equipment, you could produce snow for an entire--"  You
# disconnect the call.
#
# You have nowhere near that many stars - you need to find a way to
# disconnect at least half of the equipment here, but it's already
# Christmas!  You only have time to disconnect three wires.
#
# Fortunately, someone left a wiring diagram (your puzzle input) that
# shows how the components are connected.  For example:
#
# jqt: rhn xhk nvd
# rsh: frs pzl lsr
# xhk: hfx
# cmg: qnr nvd lhk bvb
# rhn: xhk bvb hfx
# bvb: xhk hfx
# pzl: lsr hfx nvd
# qnr: nvd
# ntq: jqt hfx bvb xhk
# nvd: lhk
# lsr: lhk
# rzs: qnr cmg lsr rsh
# frs: qnr lhk lsr
#
# Each line shows the name of a component, a colon, and then a list of
# other components to which that component is connected.  Connections
# aren't directional; abc: xyz and xyz: abc both represent the same
# configuration.  Each connection between two components is
# represented only once, so some components might only ever appear on
# the left or right side of a colon.
#
# In this example, if you disconnect the wire between hfx/pzl, the
# wire between bvb/cmg, and the wire between nvd/jqt, you will divide
# the components into two separate, disconnected groups:
#
# - 9 components: cmg, frs, lhk, lsr, nvd, pzl, qnr, rsh, and rzs.
# - 6 components: bvb, hfx, jqt, ntq, rhn, and xhk.
#
# Multiplying the sizes of these groups together produces 54.
#
# Find the three wires you need to disconnect in order to divide the
# components into two separate groups.  What do you get if you
# multiply the sizes of these two groups together?
#
# --------------------
#
# We're being asked to find the minimum cut in the graph of components
# (we're assuming there's a unique minimum cut, and that there is no
# cut smaller than 3).  To do so we iterate over each pair of
# vertices, treating them as source and sink and applying the
# Ford-Fulkerson algorithm until we find a pair for which the maximum
# flow is 3.  (Because we use BFS to find so-called augmenting paths
# in the graph, the algorithm is technically known as Edmonds-Karp.)
# The minimum cut corresponds to the bottleneck that causes the
# maximum flow to be only 3.  The number of vertices on the source
# side of the minimum cut is recovered by counting vertices that are
# reachable from the source by edges that still have positive capacity
# in the Ford-Fulkerson residual graph.

from common import bfs, bfs_path
from itertools import combinations
import re

def ford_fulkerson(graph, source, sink):
    # Return the maximum flow between source and sink vertices in a
    # weighted, directed graph.  `graph` should be the graph in the
    # form of an adjacency matrix of edge weights; it is interpreted
    # as the residual graph by the algorithm and modified.  `source`
    # and `sink` should be indices into `graph`.
    def visit(node, prev, dist, accum, seen):
        if node == sink:
            raise StopIteration(bfs_path(sink, seen))
        return filter(lambda i: graph[node][i] > 0, range(len(graph)))
    max_flow = 0
    while True:
        path = bfs(source, visit)
        if path == None:
            break
        path_flow = min(
            graph[path[i]][path[i+1]]
            for i in range(len(path)-1)
        )
        for i in range(len(path)-1):
            graph[path[i]][path[i+1]] -= path_flow
            graph[path[i+1]][path[i]] += path_flow
        max_flow += path_flow
    return max_flow

input = open("25.in").read()
all_nodes = list(set(re.findall("[a-z]{3}", input)))
N = len(all_nodes)  # number of vertices

G = [[0]*N for _ in range(N)]  # adjacency matrix
for line in input.splitlines():
    nodes = re.findall("[a-z]{3}", line)
    i = all_nodes.index(nodes[0])
    for n in nodes[1:]:
        j = all_nodes.index(n)
        G[i][j] = G[j][i] = 1

for source, sink in combinations(range(N), 2):
    graph = [row[:] for row in G]
    max_flow = ford_fulkerson(graph, source, sink)
    if max_flow == 3:
        break

def visit(node, prev, dist, accum, seen):
    accum[0] += 1
    return filter(lambda i: graph[node][i] > 0, range(N))
size = bfs(source, visit, 0)

print(size*(N-size))

# --- Part Two ---
#
# You climb over weather machines, under giant springs, and narrowly
# avoid a pile of pipes as you find and disconnect the three wires.
#
# A moment after you disconnect the last wire, the big red reset
# button module makes a small ding noise:
#
# System overload resolved!
# Power required is now 50 stars.
#
# Out of the corner of your eye, you notice goggles and a
# loose-fitting hard hat peeking at you from behind an ultra crucible.
# You think you see a faint glow, but before you can investigate, you
# hear another small ding:
#
# Power required is now 49 stars.
#
# Please supply the necessary stars and push the button to restart the
# system.

print("DONE!")
