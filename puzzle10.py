import logging
import pyomo.environ as pyo


logging.getLogger('pyomo.core').setLevel(logging.ERROR)


testing = False


# This is an optimization problem. Let's call n_b the number of times button b is
# activated, B^i_b the ith component of button b (=1 if index i in b, 0 otherwise),
# T^i the value at the ith index of target:
#
# minimize sum_b n_b
#
# subject to:
#   for all i: sum_b n_b * B^i_b = T^i
#   for all b: n_b >= 0, integer
#
# We will configure the LP relaxation and hope that it yields an integer solution.
#
m = pyo.AbstractModel()

m.num_positions = pyo.Param(within=pyo.PositiveIntegers)
m.num_buttons = pyo.Param(within=pyo.PositiveIntegers)
m.Positions = pyo.RangeSet(0, m.num_positions - 1)  # zero-indexed, inclusive
m.Buttons = pyo.RangeSet(0, m.num_buttons - 1)  # zero-indexed, inclusive

m.target = pyo.Param(m.Positions, within=pyo.NonNegativeIntegers)
m.button_indices = pyo.Param(m.Buttons, m.Positions, within=pyo.Binary)
m.n = pyo.Var(m.Buttons, domain=pyo.NonNegativeIntegers)

def button_presses_rule(m):
    return sum(m.n[b] for b in m.Buttons)
m.button_presses = pyo.Objective(rule=button_presses_rule)

def target_value_constraint(m, i):
    return sum(m.button_indices[b,i] * m.n[b] for b in m.Buttons) == m.target[i]
m.target_value = pyo.Constraint(m.Positions, rule=target_value_constraint)

# End of definition of the optimization model


def to_binary(button):
    return sum(1 << n for n in button)


def search_target(target, buttons, start=0, cost=0):
    # Application of a button an even number of times is equivalent to not applying it
    # Application of a button an odd number of times is equivalent to applying it once
    # At most one application of each button makes sense, order does not matter
    # So aim at finding a subset of buttons that applied results in the target
    # Do a tree search, branching on applying or not each button, minimizing cost.
    # Cost is subset cardinality, so each button has a cost of 1 to activate
    if target == start:
        return cost

    if not buttons:
        return 1e6  # i.e. infinity: this branch did not find a matching combination

    return min(
        # Apply first button
        search_target(target, buttons[1:], start ^ buttons[0], cost + 1),
        # Do not apply first button
        search_target(target, buttons[1:], start, cost)
    )


def apply(start, button, n):
    return tuple(x + n if idx in button else x for idx, x in enumerate(start))


def search_joltage(target, buttons, start=None, cost=0):
    # Build the instance data for the optimization problem
    data ={
        None: {
            'num_positions': {None: len(target)},
            'num_buttons': {None: len(buttons)},
            'target': dict(enumerate(target)),
            'button_indices': {
                (b, n): 1 if n in buttons[b] else 0
                for b in range(len(buttons))
                for n in range(len(target))
            }
        }
    }
    instance = m.create_instance(data)
    opt = pyo.SolverFactory('cbc')
    opt.solve(instance)
    return pyo.value(instance.button_presses)


class Machine():
    def __init__(self, target, buttons, joltages):
        self.target = target
        self.buttons = buttons
        self.binary_buttons = tuple(to_binary(button) for button in buttons)
        self.joltages = joltages

    def which_buttons1(self):
        return search_target(self.target, self.binary_buttons)

    def which_buttons2(self):
        return search_joltage(self.joltages, self.buttons)

    @staticmethod
    def target_from_spec(target_spec):
        target = 0
        # reverse the pattern so that bit significance matches the button specs (i.e. index 0
        # corresponds to the leftmost character; as a number, it's the rightmost digit (2^0))
        for c in reversed(target_spec[1 : -1]):  # Inside the brackets
            target <<= 1
            if c == '#':
                target |= 1
        return target

    @staticmethod
    def buttons_from_spec(buttons_spec):
        return tuple(
            tuple(int(n) for n in button[1 : -1].split(','))
            for button in buttons_spec
        )

    @staticmethod
    def joltages_from_spec(joltages_spec):
        # Minimal parsing, seems to be aligned with target (same number of positions)
        # To be reviewed for part two, may need to be reversed
        return tuple(int(n) for n in joltages_spec[1 : -1].split(','))  # Inside the braces

    @classmethod
    def from_line(cls, line):
        target_spec, *buttons_spec, joltages_spec = line.strip().split()
        target = cls.target_from_spec(target_spec)
        buttons = cls.buttons_from_spec(buttons_spec)
        joltages = cls.joltages_from_spec(joltages_spec)
        return cls(target, buttons, joltages)


def read_data():
    filename = f'puzzle10{'-test' if testing else ''}.in'
    with open(filename, 'r') as f:
        machines = [Machine.from_line(line) for line in f]
    return machines


def part_1():
    machines = read_data()
    return sum(m.which_buttons1() for m in machines)


def part_2():
    machines = read_data()
    return sum(m.which_buttons2() for m in machines)
