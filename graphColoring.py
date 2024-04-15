import numpy as np


class GRAPHCOLORING:

    def __init__(self, V, E, n_colors):
        self.V = V
        self.E = E
        self.n_colors = n_colors
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
        for v_i in range(self.V):
            for c_i in range(self.n_colors):
                for v_j in range(self.V):
                    for c_j in range(self.n_colors):
                        q_i = v_i * self.n_colors + c_i
                        q_j = v_j * self.n_colors + c_j
                        if q_i < q_j:
                            if v_i == v_j or (self.graph[v_i][v_j] == 1 and c_i == c_j):
                                Q[(q_i, q_j)] = 3
                        elif q_i == q_j:
                            Q[(q_i, q_j)] = -1
        return Q

