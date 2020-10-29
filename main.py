from seatings import compute_seating_cost, generate_seating
from simulated_annealing import SimulatedAnnealing, MyState


def generate_sample_families(*args):
    from random import shuffle

    result = []
    fam_id = 100
    for amount, members in args:
        for _ in range(amount):
            result.append({"count": members, "id": "%s" % fam_id})
            fam_id += 1
    shuffle(result)
    return result


def main():
    """ROWS = 36
    COLUMNS = 36

    sa = SimulatedAnnealing(1000, MyState(generate_sample_families((400, 1), (400, 2), (400, 4))), compute_seating_cost,
                            rows=ROWS, columns=COLUMNS)
    state, cost, cost_trace = sa.run_simulation(return_cost_trace=True)
    print(cost_trace)
    print("first: %s\nlast: %s\nmax: %s\nmin: %s"
          % (cost_trace[0], cost_trace[-1], max(cost_trace), min(cost_trace)))
    print(cost)
    print(state.placing_order)
    stadium = generate_seating(state.placing_order, rows=ROWS, columns=COLUMNS)
    stadium.get_heatmap_plot().show()
    print(stadium.graphic(labeled=True))"""

    ROWS = 10
    COLUMNS = 100
    sa = SimulatedAnnealing(500000, MyState(generate_sample_families((50, 1), (75, 2), (75, 3), (50, 4))), compute_seating_cost,
                            rows=ROWS, columns=COLUMNS)
    state, cost, cost_trace = sa.run_simulation(return_cost_trace=True)
    print(cost_trace)
    print("first: %s\nlast: %s\nmax: %s\nmin: %s"
          % (cost_trace[0], cost_trace[-1], max(cost_trace), min(cost_trace)))
    print(cost)
    print(state.placing_order)
    stadium = generate_seating(state.placing_order, rows=ROWS, columns=COLUMNS)
    stadium.get_heatmap_plot().show()
    print(stadium.graphic(labeled=True))

    import matplotlib.pyplot as plt
    plt.plot(cost_trace)
    plt.show()


if __name__ == "__main__":
    main()
