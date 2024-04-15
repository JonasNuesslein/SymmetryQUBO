import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit_optimization import QuadraticProgram
import matplotlib.pyplot as plt


def get_size_of_QUBO(Q):
    n = 0
    for key in Q.keys():
        if key[0] > n:
            n = key[0]
        if key[1] > n:
            n = key[1]
    n += 1
    return n


def getValue(Q, solution):
    ones = [x for x in range(len(solution)) if solution[x] == 1]
    value = 0
    for x in ones:
        for y in ones:
            if (x, y) in Q.keys():
                value += Q[(x, y)]
    return value


def QUBO_to_QuadraticProgram(Q):
    quadr_program = QuadraticProgram()

    N = len(Q)
    for i in range(N):
        l = 'x' + str(i)
        quadr_program.binary_var(l)

    quad2 = {}
    for i in range(N):
        li = 'x' + str(i)
        for j in range(N):
            lj = 'x' + str(j)
            quad2.update({(li, lj): Q[i, j]})
    quadr_program.minimize(quadratic=quad2)
    return quadr_program


def solve_with_QAOA(Q, reps=3, print_circuit=False, solve=False, shots=128):

    n = get_size_of_QUBO(Q)

    Q_ = np.zeros((n,n))
    for (i,j) in Q.keys():
        Q_[i][j] = Q[(i,j)]

    H, _ = QUBO_to_QuadraticProgram(Q_).to_ising()
    ansatz = QAOAAnsatz(H, reps=reps).decompose()

    num_qubits = ansatz.num_qubits
    depth = ansatz.decompose().depth()
    used_gates = dict(ansatz.decompose().count_ops())

    if print_circuit:
        ansatz.decompose().draw(output="mpl", style="iqp")
        plt.savefig('circuit.pdf')
        plt.show()

    return num_qubits, depth, used_gates


def get_number_of_couplers(Q):
    c = 0
    for key in Q.keys():
        if Q[key] != 0 and key[0] != key[1]:
            c += 1
    return c


def print_info(Q, reps, solve, shots):
    n = get_size_of_QUBO(Q)
    num_qubits, depth, used_gates = solve_with_QAOA(Q, reps=reps, solve=solve, shots=shots)
    n_couplers = get_number_of_couplers(Q)
    density = n_couplers / (n * (n + 1) // 2)
    return n, n_couplers, density, depth

