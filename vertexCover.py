import numpy as np


class VERTEXCOVER:

    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.graph = self.create()
        self.Q = self.get_QUBO()

    def create(self):
        graph = np.zeros((self.V, self.V))
        edges = [(i, j) for i in range(self.V) for j in range(self.V) if i < j]
        selected_edges = np.random.choice(len(edges), size=self.E, replace=False)
        for e in selected_edges:
            i, j = edges[e]
            graph[i][j] = 1
            graph[j][i] = 1
        return graph

    def get_QUBO(self):
        Q = {}
        for i in range(self.V):
            for j in range(self.V):
                if i == j:
                    Q[(i, i)] = -1
                elif i < j and self.graph[i][j] == 1:
                    Q[(i, j)] = 3
        return Q

