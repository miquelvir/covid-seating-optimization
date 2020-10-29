import math
from copy import deepcopy
import random
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class Seat:
    occupant: str = None
    blocked: bool = False

    def available(self):
        return self.occupant is None and not self.blocked

    def simple_graphic(self):
        return "-" if self.blocked else "_" if not self.occupant else "x"

    def complete_graphic(self):
        return "----------" if self.blocked else "__________" if not self.occupant else self.occupant.id_()

    def graphic(self, simple=True):
        if simple:
            return self.simple_graphic()
        return self.complete_graphic()

    def __eq__(self, other):
        if not isinstance(other, Seat):
            return False
        return self.occupant == other.occupant


@dataclass
class Person:
    family_id: str
    family_member_id: int

    def id_(self):
        return self.family_id, self.family_member_id

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.id_ == other.id_


class Stadium:
    def graphic(self, simple=True):
        representation = "*stadium*\n"
        for row in self.matrix:
            representation += " ".join([str(x.graphic(simple=simple)) for x in row]) + "\n"
        return representation

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.array([Seat() for _ in range(rows*columns)], dtype=Seat).reshape(rows, columns)

    def __getitem__(self, item):
        return self.matrix[item]

    def __len__(self):
        return len(self.matrix)


def follows_covid_guidelines(stadium, x, y, current_family):
    if x - 1 >= 0 and not (stadium[y][x - 1].occupant is None or
                           stadium[y][x - 1].occupant.family_id == current_family["id"]):
        return False
    if x - 2 >= 0 and not (stadium[y][x - 2].occupant is None or
                           stadium[y][x - 2].occupant.family_id == current_family["id"]):
        return False
    if y - 1 >= 0 and not (stadium[y - 1][x].occupant is None or
                           stadium[y - 1][x].occupant.family_id == current_family["id"]):
        return False
    if y + 1 < len(stadium) and not (stadium[y + 1][x].occupant is None or
                                     stadium[y + 1][x].occupant.family_id == current_family["id"]):
        return False
    return True


def generate_seating(state):
    def next_seat():
        nonlocal x
        nonlocal y
        if x + 1 < stadium.columns:
            x += 1
        elif y + 1 < stadium.rows and 0 < stadium.rows:
            y += 1
            x = 0
        else:
            return False
        return True

    stadium = Stadium(6, 6)
    stadium[3][3] = Seat(blocked=True)

    y, x = 0, 0
    for family in state:
        for member_id in range(family["count"]):
            while not follows_covid_guidelines(stadium, x, y, family):
                # advance seat
                if not next_seat():
                    return stadium

            stadium[y][x].occupant = Person(family["id"], member_id)
            if not next_seat():
                return stadium

    return stadium


def get_cost(state):
    """Calculates cost of the argument state for your solution."""
    stadium = generate_seating(state)

    cost = 0
    for row in stadium:
        for seat in row:
            if seat.occupant is not None:
                cost -= 1
    return cost, stadium


def get_neighbors(state, recursion=0):
    """Returns neighbors of the argument state for your solution."""
    new_state = deepcopy(state)
    a = random.randint(0, len(new_state) - 1)
    b = random.randint(0, len(new_state) - 1)
    while b == a:
        b = random.randint(0, len(new_state) - 1)
    temp = new_state[a]
    new_state[a] = new_state[b]
    new_state[b] = temp
    if recursion >= 0:
        return new_state
    else:
        return get_neighbors(new_state, recursion + 1)


def heatmap(stadium):
    data = np.full((len(stadium), len(stadium[0])), 99, dtype=int)
    for y, row in enumerate(stadium):
        for x, seat in enumerate(row):
            if seat.blocked:
                data[y][x] = 50
            elif seat.occupant is not None:
                data[y][x] = 0
    plt.imshow(data, cmap='gray')
    plt.show()


def simulated_annealing(initial_state):
    """Peforms simulated annealing to find a solution
        Let s = s0
        For k = 0 through kmax (exclusive):
        T ← temperature( (k+1)/kmax )
        Pick a random neighbour, snew ← neighbour(s)
        If P(E(s), E(snew), T) ≥ random(0, 1):
        s ← snew
        Output: the final state s
    """
    initial_temp = 100
    final_temp = 0
    schedule_alpha = .1

    current_temp = initial_temp

    # Start by initializing the current state with the initial state
    solution = initial_state
    solution_cost, solution_stadium = get_cost(initial_state)

    trace = [solution_cost]
    while current_temp > final_temp:
        neighbor = get_neighbors(solution)
        neighbor_cost, neighbor_stadium = get_cost(neighbor)
        # Check if neighbor is best so far

        cost_diff = neighbor_cost - solution_cost

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = neighbor
        # if the new solution is not better, accept it with a probability of e^(-cost_diff/temp)
        else:
            if random.uniform(0, 1) < math.exp(cost_diff / current_temp):
                solution, solution_cost, solution_stadium = neighbor, neighbor_cost, neighbor_stadium
                trace.append(solution_cost)
        # decrement the temperature
        current_temp -= schedule_alpha

    print(solution_cost)
    print(trace)
    print("max: %s\nmin: %s\nfirst: %s\nlast: %s" % (max(trace), min(trace), trace[0], trace[-1]))
    heatmap(solution_stadium)
    return solution


def generate_sample_families(*args):
    result = []
    fam_id = 100
    for fam, count in args:
        for _ in range(fam):
            result.append({"count": count, "id": "%s" % fam_id})
            fam_id += 1
    random.shuffle(result)
    return result


if __name__ == "__main__":
    res = simulated_annealing(generate_sample_families((20, 1), (20, 2), (20, 4)))
    print(res)
