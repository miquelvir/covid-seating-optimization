import math
from copy import deepcopy
import random
import numpy as np


class State:
    def __init__(self):
        raise NotImplementedError

    def mutate(self):
        raise NotImplementedError


class MyState(State):
    def __init__(self, placing_order):
        self.placing_order = placing_order

    @staticmethod
    def _swap_two(list_, max_attempts=15):
        a = random.randint(0, len(list_) - 1)
        b = random.randint(0, len(list_) - 1)
        # attempts = 0
        while b == a or list_[a]["count"] == list_[b]["count"]:   # and attempts < max_attempts:  # or list_[b]["count"] == list_[a]["count"]
            # attempts += 1
            b = random.randint(0, len(list_) - 1)
        temp_a = list_[a]
        list_[a] = list_[b]
        list_[b] = temp_a

    def _mutate_recursive(self, placing_order, mutations=0, max_mutations=1):
        new_placing_order = deepcopy(placing_order)

        self._swap_two(new_placing_order)
        mutations += 1

        if mutations >= max_mutations:
            return MyState(new_placing_order)
        else:
            return self._mutate_recursive(new_placing_order, mutations, max_mutations)

    def mutate(self, max_mutations=1):
        return self._mutate_recursive(self.placing_order, max_mutations=max_mutations)


class SimulatedAnnealing:
    def __init__(self, max_iterations, initial_state, cost_function, *args, p=None, **kwargs):
        self._max_iterations = max_iterations  # time budget
        self._current_iteration = self._max_iterations
        self._cost_function = cost_function
        self._p = p if p else self._default_p
        self._args = args
        self._kwargs = kwargs

        # initial guess
        self._solution_state = initial_state
        self._solution_cost = self._cost_function(self._solution_state, *self._args, **self._kwargs)

    def _current_temperature(self):
        return (self._current_iteration + 1) / self._max_iterations  # time budget fraction

    @staticmethod
    def _default_p(solution_cost, neighbour_cost, current_temperature, maxk, k, *args, **kwargs):
        if neighbour_cost < solution_cost:
            return 1

        return np.exp(-(neighbour_cost - solution_cost) / current_temperature)

    def iteration(self):
        # select a random neighbour performing a small random mutation to the current state
        neighbour_state = self._solution_state.mutate(1)
        neighbour_cost = self._cost_function(neighbour_state, *self._args, **self._kwargs)

        # accept the mutation according to the p function
        if random.uniform(0, 1) <= self._p(self._solution_cost, neighbour_cost, self._current_temperature(), self._max_iterations, self._current_iteration,
                                          *self._args, **self._kwargs):
            self._solution_state, self._solution_cost = neighbour_state, neighbour_cost

    def run_simulation(self, return_cost_trace=False, return_state_trace=False):
        if return_cost_trace:
            cost_trace = [self._solution_cost]
        if return_cost_trace:
            state_trace = [str(self._solution_state)]

        while self._current_iteration > 1:
            self.iteration()
            self._current_iteration -= 1

            if return_cost_trace:
                cost_trace.append(self._solution_cost)
            if return_cost_trace:
                state_trace.append(str(self._solution_state))

        if return_cost_trace and return_state_trace:
            return self._solution_state, self._solution_cost, cost_trace, state_trace
        if return_cost_trace:
            return self._solution_state, self._solution_cost, cost_trace
        if return_state_trace:
            return self._solution_state, self._solution_cost, state_trace
        return self._solution_state, self._solution_cost
