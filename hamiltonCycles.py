import numpy as np



class HAMILTONCYCLES:

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
        for p_i in range(self.V):
            for v_i in range(self.V):
                for p_j in range(self.V):
                    for v_j in range(self.V):
                        q_i = p_i * self.V + v_i
                        q_j = p_j * self.V + v_j
                        if q_i < q_j:
                            if p_i == p_j or v_i == v_j or (p_j == p_i + 1 and self.graph[v_i][v_j] == 0) \
                                    or (p_j == self.V - 1 and p_i == 0 and self.graph[v_i][v_j] == 0):
                                Q[(q_i, q_j)] = 3
                        elif q_i == q_j:
                            Q[(q_i, q_j)] = -1
        return Q
