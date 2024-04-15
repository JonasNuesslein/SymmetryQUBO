import numpy as np


class GRAPHISOMORPHISM:

    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.graph1 = self.create()
        self.graph2 = self.create()
        self.graph2 = self.graph1
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
        for v_i_1 in range(self.V):
            for v_i_2 in range(self.V):
                for v_j_1 in range(self.V):
                    for v_j_2 in range(self.V):
                        q_i = v_i_1 * self.V + v_i_2
                        q_j = v_j_1 * self.V + v_j_2
                        if q_i < q_j:
                            if v_i_1 == v_j_1 or v_i_2 == v_j_2 or (self.graph1[v_i_1][v_j_1] != self.graph2[v_i_2][v_j_2]):
                                Q[(q_i, q_j)] = 3
                        elif q_i == q_j:
                            Q[(q_i, q_j)] = -1
        return Q

