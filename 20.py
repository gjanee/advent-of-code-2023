# --- Day 20: Pulse Propagation ---
#
# With your help, the Elves manage to find the right parts and fix all
# of the machines.  Now, they just need to send the command to boot up
# the machines and get the sand flowing again.
#
# The machines are far apart and wired together with long cables.  The
# cables don't connect to the machines directly, but rather to
# communication modules attached to the machines that perform various
# initialization tasks and also act as communication relays.
#
# Modules communicate using pulses.  Each pulse is either a high pulse
# or a low pulse.  When a module sends a pulse, it sends that type of
# pulse to each module in its list of destination modules.
#
# There are several different types of modules:
#
# Flip-flop modules (prefix %) are either on or off; they are
# initially off.  If a flip-flop module receives a high pulse, it is
# ignored and nothing happens.  However, if a flip-flop module
# receives a low pulse, it flips between on and off.  If it was off,
# it turns on and sends a high pulse.  If it was on, it turns off and
# sends a low pulse.
#
# Conjunction modules (prefix &) remember the type of the most recent
# pulse received from each of their connected input modules; they
# initially default to remembering a low pulse for each input.  When a
# pulse is received, the conjunction module first updates its memory
# for that input.  Then, if it remembers high pulses for all inputs,
# it sends a low pulse; otherwise, it sends a high pulse.
#
# There is a single broadcast module (named broadcaster).  When it
# receives a pulse, it sends the same pulse to all of its destination
# modules.
#
# Here at Desert Machine Headquarters, there is a module with a single
# button on it called, aptly, the button module.  When you push the
# button, a single low pulse is sent directly to the broadcaster
# module.
#
# After pushing the button, you must wait until all pulses have been
# delivered and fully handled before pushing it again.  Never push the
# button if modules are still processing pulses.
#
# Pulses are always processed in the order they are sent.  So, if a
# pulse is sent to modules a, b, and c, and then module a processes
# its pulse and sends more pulses, the pulses sent to modules b and c
# would have to be handled first.
#
# The module configuration (your puzzle input) lists each module.  The
# name of the module is preceded by a symbol identifying its type, if
# any.  The name is then followed by an arrow and a list of its
# destination modules. For example:
#
# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a
#
# In this module configuration, the broadcaster has three destination
# modules named a, b, and c.  Each of these modules is a flip-flop
# module (as indicated by the % prefix).  a outputs to b which outputs
# to c which outputs to another module named inv.  inv is a
# conjunction module (as indicated by the & prefix) which, because it
# has only one input, acts like an inverter (it sends the opposite of
# the pulse type it receives); it outputs to a.
#
# By pushing the button once, the following pulses are sent:
#
# button -low-> broadcaster
# broadcaster -low-> a
# broadcaster -low-> b
# broadcaster -low-> c
# a -high-> b
# b -high-> c
# c -high-> inv
# inv -low-> a
# a -low-> b
# b -low-> c
# c -low-> inv
# inv -high-> a
#
# After this sequence, the flip-flop modules all end up off, so
# pushing the button again repeats the same sequence.
#
# Here's a more interesting example:
#
# broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output
#
# This module configuration includes the broadcaster, two flip-flops
# (named a and b), a single-input conjunction module (inv), a
# multi-input conjunction module (con), and an untyped module named
# output (for testing purposes).  The multi-input conjunction module
# con watches the two flip-flop modules and, if they're both on, sends
# a low pulse to the output module.
#
# Here's what happens if you push the button once:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -high-> output
# b -high-> con
# con -low-> output
#
# Both flip-flops turn on and a low pulse is sent to output!  However,
# now that both flip-flops are on and con remembers a high pulse from
# each of its two inputs, pushing the button a second time does
# something different:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
#
# Flip-flop a turns off!  Now, con remembers a low pulse from module
# a, and so it sends only a high pulse to output.
#
# Push the button a third time:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -low-> output
# b -low-> con
# con -high-> output
#
# This time, flip-flop a turns on, then flip-flop b turns off.
# However, before b can turn off, the pulse sent to con is handled
# first, so it briefly remembers all high pulses for its inputs and
# sends a low pulse to output.  After that, flip-flop b turns off,
# which causes con to update its state and send a high pulse to
# output.
#
# Finally, with a on and b off, push the button a fourth time:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
#
# This completes the cycle: a turns off, causing con to remember only
# low pulses and restoring all modules to their original states.
#
# To get the cables warmed up, the Elves have pushed the button 1000
# times.  How many pulses got sent as a result (including the pulses
# sent by the button itself)?
#
# In the first example, the same thing happens every time the button
# is pushed: 8 low pulses and 4 high pulses are sent.  So, after
# pushing the button 1000 times, 8000 low pulses and 4000 high pulses
# are sent.  Multiplying these together gives 32000000.
#
# In the second example, after pushing the button 1000 times, 4250 low
# pulses and 2750 high pulses are sent.  Multiplying these together
# gives 11687500.
#
# Consult your module configuration; determine the number of low
# pulses and high pulses that would be sent after pushing the button
# 1000 times, waiting for all pulses to be fully handled after each
# push of the button.  What do you get if you multiply the total
# number of low pulses sent by the total number of high pulses sent?

queue = []  # [(sender, receiver, pulse), ...]
num_pulses = {"L": 0, "H": 0}

class Module:

    all = {}  # maps names to modules
    def __class_getitem__(cls, name):
        return Module.all[name]

    def __init__(self, name, dests):
        self.name, self.dests = name, dests
        Module.all[name] = self

    def reset(self):
        pass

    @staticmethod
    def reset_all():
        for m in Module.all.values():
            m.reset()

    def send(self, pulse):
        for m in self.dests:
            queue.append((self.name, m, pulse))
            num_pulses[pulse] += 1

    def recv(self, sender, pulse):
        pass

class FlipFlop(Module):

    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.reset()

    def reset(self):
        self.state = False

    def recv(self, sender, pulse):
        if pulse == "H":
            return
        self.state = not self.state
        self.send("H" if self.state else "L")

class Conjunction(Module):

    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.inputs = {}  # initialized when reset later

    def reset(self):
        # This method both initializes and sets `inputs`.
        self.inputs = {
            m.name: "L"
            for m in Module.all.values()
            if self.name in m.dests
        }

    def trigger_hook(self):
        pass

    def recv(self, sender, pulse):
        self.inputs[sender] = pulse
        if all(v == "H" for v in self.inputs.values()):
            self.trigger_hook()
            self.send("L")
        else:
            self.send("H")

class Broadcaster(Module):

    def recv(self, sender, pulse):
        self.send(pulse)

class Sink(Module):

    def __init__(self, name):
        super().__init__(name, [])

for line in open("20.in"):
    name, dests = line.strip().split(" -> ")
    dests = dests.split(", ")
    if name == "broadcaster":
        Broadcaster(name, dests)
    elif name.startswith("%"):
        FlipFlop(name[1:], dests)
    elif name.startswith("&"):
        Conjunction(name[1:], dests)

# Add modules that are referenced as destinations but have no
# definition (e.g., rx in part 2).
for m in list(Module.all.values()):
    for d in m.dests:
        if d not in Module.all:
            Sink(d)

def push_button():
    queue.append(("button", "broadcaster", "L"))
    num_pulses["L"] += 1
    while len(queue) > 0:
        s, r, p = queue.pop(0)
        Module[r].recv(s, p)

Module.reset_all()
for _ in range(1000):
    push_button()

print(num_pulses["L"] * num_pulses["H"])

# --- Part Two ---
#
# The final machine responsible for moving the sand down to Island
# Island has a module attached named rx.  The machine turns on when a
# single low pulse is sent to rx.
#
# Reset all modules to their default states.  Waiting for all pulses
# to be fully handled after each button press, what is the fewest
# number of button presses required to deliver a single low pulse to
# the module named rx?
#
# --------------------
#
# The circuit seems to run forever, so we turn to analyzing it.  What
# we find is a clever mechanism of four binary counters that trigger
# low pulses every 3761, 3881, 3767, and 3779 button presses
# respectively (and otherwise send high pulses with every button
# press).  Those low pulses run through inverters and then into a
# single conjunction that waits for four high pulses to occur
# simultaneously before sending a low pulse to rx.  The counter cycle
# lengths are all prime, but in principle the number of button presses
# required will be the least common multiple of the counter cycle
# lengths.
#
# In more detail, each counter is implemented by a chained series of
# flip-flops, one per bit position, and an attached conjunction that
# acts as a firing trigger.  At the top of the circuit, the
# broadcaster sends a low pulse to the ones' position of each binary
# counter, thereby increasing each counter by 1 (in our diagrams
# below, flip-flops are in lowercase and conjunctions are uppercase):
#
# broadcaster ---+---> ls
#                |
#                +---> bv
#                |
#                +---> dc
#                |
#                +---> br
#
# Looking at just the ls counter (the other three are similar), 12
# flip-flops are connected in series.  The flip-flops by themselves
# form a binary counter, with on/off states corresponding to 1/0 bits.
# In addition to being chained, each flip-flop either sends a pulse to
# ZP or receives a pulse from ZP (the ones' position, ls, is special
# in that it both sends to and receives from ZP).
#
# broadcaster
#           |
#           v
#      2^0  ls <--> ZP
#           |
#           v
#      2^1  hs <--- ZP
#           |
#           v
#      2^2  fn <--- ZP
#           |
#           v
#      2^3  px <--- ZP
#           |
#           v
#      2^4  zx ---> ZP
#           |
#           v
#      2^5  zl ---> ZP
#           |
#           v
#      2^6  cl <--- ZP
#           |
#           v
#      2^7  mj ---> ZP
#           |
#           v
#      2^8  gp <--- ZP
#           |
#           v
#      2^9  md ---> ZP
#           |
#           v
#      2^10 ts ---> ZP
#           |
#           v
#      2^11 fc ---> ZP
#
# Continuing with the case of the ls counter above, when the
# flip-flops at bit positions 0, 4, 5, 7, 9, 10, and 11 are on, which
# first occurs after 2^0 + 2^4 + 2^5 + 2^7 + 2^9 + 2^10 + 2^11 = 3761
# button presses, ZP is triggered to send a low pulse.  ZP sends low
# pulses to all flip-flops that are complementary to the above, i.e.,
# to those that are off, which turns them on.  But ZP also sends a low
# pulse to ls, which is already on.  This causes ls to turn off, which
# in ripple effect turns all flip-flips in the counter off, thus
# resetting the counter.  Clever!
#
# At the bottom of the circuit, ZP and the conjunctions from the other
# counters get inverted and then routed into a final conjunction ZH.
#
# ZP ---> BH ---+
#               |
# NX ---> VD ---+
#               +---> ZH ---> rx
# DJ ---> NS ---+
#               |
# BZ ---> DL ---+
#
# The code below simulates pressing the button just until all four
# counters have triggered.  For slightly more input generality we
# avoid hard-coding the names of the {ZP, NX, DJ, BZ} conjunctions
# above and instead discover them by traversing backwards from rx.
# But fundamentally we are relying on the analysis above.

from math import lcm

zh = next(filter(lambda m: m.dests == ["rx"], Module.all.values()))
zp_etc = [list(Module[name].inputs)[0] for name in zh.inputs]

cycle_len = {name: None for name in zp_etc}
num_presses = 0

def hook(self):
    if self.name in cycle_len and cycle_len[self.name] == None:
        cycle_len[self.name] = num_presses
    if all(v != None for v in cycle_len.values()):
        raise StopIteration
Conjunction.trigger_hook = hook

Module.reset_all()
try:
    while True:
        num_presses += 1
        push_button()
except StopIteration:
    pass

print(lcm(*cycle_len.values()))
