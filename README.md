[Advent of Code 2023](https://adventofcode.com/2023) solutions in Python.

## Puzzle summary

| Day | Puzzle essence | The hitch or twist | The insight |
|--:|---|---|---|
| [1](https://adventofcode.com/2023/day/1) | Find digits in strings | The last digit in `oneight` is 8, not 1 | |
| [2](https://adventofcode.com/2023/day/2) | Maintain counts in different buckets | | Perfect application of `Counter` |
| [3](https://adventofcode.com/2023/day/3) | Find numbers (strings of digits) diagonally adjacent to symbols in a grid | It's 2D, and the symbol-number association is one-to-many | Scan for numbers row by row, but store the associations by symbol |
| [4](https://adventofcode.com/2023/day/4) | Count winning lottery cards | There are lots of them | |
| [5](https://adventofcode.com/2023/day/5) | Map values through a sequence of linear functions | The functions are piecewise linear and discontinuous | Mapping a range of values through a piecewise linear function produces a set of ranges; repeat |
| [6](https://adventofcode.com/2023/day/6) | Solve a time-distance problem | | It's just a quadratic equation |
| [7](https://adventofcode.com/2023/day/7) | Play poker | Jacks are wild | If hands are represented as descending card counts (e.g., a full house is \[3, 2]), then lexicographic order matches hand order |
| [8](https://adventofcode.com/2023/day/8) | Simultaneously follow multiple paths in a directed graph | The paths all fall into cycles | The least common multiple of the cycle lengths works because of the special way the paths were constructed |
| [9](https://adventofcode.com/2023/day/9) | Run a difference engine | Run it backwards | Backwards is the same as forwards: subtracting a negative delta is the same as adding a positive delta |
| [10](https://adventofcode.com/2023/day/10) | Follow segments that make up a loop on a 2D map | Calculate the area of the loop's interior, but oops, loop segments can be directly adjacent | Use a scanline approach and track loop crossings |
| [11](https://adventofcode.com/2023/day/11) | Manhattan distance | Some rows/columns are special | |
| [12](https://adventofcode.com/2023/day/12) | An ugly pattern matching problem | | Dynamic programming with caching: break off a piece of the problem, recurse |
| [13](https://adventofcode.com/2023/day/13) | Find lines of reflection in grids | There are imperfections | Hamming distance = 1 |
| [14](https://adventofcode.com/2023/day/14) | Move objects on a grid with obstacles | | Another cycle detection puzzle |
| [15](https://adventofcode.com/2023/day/15) | Hashing | | |
| [16](https://adventofcode.com/2023/day/16) | Follow a path on a grid | The path splits and cycles | |
| [17](https://adventofcode.com/2023/day/17) | Find a lowest-cost path on a grid | Turns are both restricted and required | Consider any admissible number of steps in the same direction to be a single move |
| [18](https://adventofcode.com/2023/day/18) | Calculate the area of a polygon | The polygon is huge | Shoelace formula |
| [19](https://adventofcode.com/2023/day/19) | A hierarchical linear programming problem | What is the size of the solution space? | Each constraint cuts a 4D cuboid along a face |
| [20](https://adventofcode.com/2023/day/20) | Simulate a circuit and pulses | When does it terminate? | Reverse engineer the circuit |
| [21](https://adventofcode.com/2023/day/21) | Count reachable cells in a grid | The grid is infinite, there's an alternating parity pattern, and the grid repeat pattern is complex | Another specially crafted input that works for reasons not entirely clear; count square tiles in a rhombus pattern |
| [22](https://adventofcode.com/2023/day/22) | Locate dominator nodes in a directed graph | | |
| [23](https://adventofcode.com/2023/day/23) | Find a longest path in a graph | NP-hard! | Brute force DFS, but the problem is small enough that heuristics are not needed |
| [24](https://adventofcode.com/2023/day/24) | Determine when moving particles collide | There are hundreds of particles; add one more | Cast the problem as a system of linear equations; notice that 3 particles are sufficient to find a solution |
| [25](https://adventofcode.com/2023/day/25) | Find a minimum cut in a graph | | Ford-Fulkerson maximum flow algorithm |
