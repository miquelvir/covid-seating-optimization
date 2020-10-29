from seat import Seat
import numpy as np
import matplotlib.pyplot as plt


class Stadium:
    def graphic(self, labeled=False):
        representation = "*stadium*\n"
        for row in self.matrix:
            representation += " ".join([str(x.graphic(simple=not labeled)) for x in row]) + "\n"
        return representation

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.array([Seat() for _ in range(rows*columns)], dtype=Seat).reshape(rows, columns)

    def __getitem__(self, item):
        return self.matrix[item]

    def __len__(self):
        return len(self.matrix)

    def cost(self):
        cost = 0
        for row in self.matrix:
            for seat in row:
                if seat.has_occupant():
                    cost -= 1  # positive reward for each occupant

        return cost

    def get_heatmap_plot(self):
        data = np.full((self.rows, self.columns), 99, dtype=int)
        for y, row in enumerate(self.matrix):
            for x, seat in enumerate(row):
                if seat.blocked:
                    data[y][x] = 50
                elif seat.occupant is not None:
                    data[y][x] = 0
        plt.imshow(data, cmap='gray')
        return plt
