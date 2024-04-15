import copy
import numpy as np
import utils



def get_symmetry_free_QUBO(Q, n_min_symmetries=3, max_additional_qubits=99999, z=3):
    Q = copy.deepcopy(Q)
    n = utils.get_size_of_QUBO(Q)
    new_Q = copy.deepcopy(Q)
    new_n = n

    list_of_conflicting_qubits = get_list_of_conflicting_qubits(new_Q, new_n)

    print("Start factoring out semi-symmetries:")
    while len(list_of_conflicting_qubits) > 0:
        if new_n == n + max_additional_qubits:
            break
        symmetries, symmetric_qubit_pair = get_most_symmetric_pair(new_Q, new_n, list_of_conflicting_qubits)
        if len(symmetries) >= n_min_symmetries:
            new_Q = enhance_QUBO(new_Q, new_n, symmetric_qubit_pair, symmetries, z=z)
            new_n += 1
        else:
            break
        list_of_conflicting_qubits = remove_qubit_pair(list_of_conflicting_qubits, symmetric_qubit_pair)
        print(len(list_of_conflicting_qubits), symmetries, symmetric_qubit_pair)
        list_of_conflicting_qubits = get_list_of_conflicting_qubits(new_Q, new_n)
    print()

    new_Q_sparse = {}
    for key in new_Q.keys():
        if new_Q[key] != 0:
            new_Q_sparse[key] = new_Q[key]

    return new_Q_sparse


def get_list_of_conflicting_qubits(Q, n):
    list_of_conflicting_qubits = []

    max_negative_values = [0] * n
    for q1 in range(n):
        for q2 in range(n):
            v = get_value(Q, q1, q2)
            if v < 0:
                max_negative_values[q1] += v

    for q1 in range(n):
        for q2 in range(n):
            if q1 < q2 and get_coupler(Q, q1, q2) > -max_negative_values[q1] - max_negative_values[q2]:
                list_of_conflicting_qubits.append((q1,q2))

    return list_of_conflicting_qubits


def get_most_symmetric_pair(new_Q, new_n, list_of_conflicting_qubits, threshold=0.1):
    best_symmetric_qubit_pair = list_of_conflicting_qubits[0]
    best_symmetries = []
    for (q1,q2) in list_of_conflicting_qubits:
        symmetries = []
        for q3 in range(new_n):
            v1 = get_coupler(new_Q, q1, q3)
            v2 = get_coupler(new_Q, q2, q3)
            if v1 != 0 and v2 != 0 and np.abs(v1 - v2) < threshold:
                symmetries.append(q3)
        if len(symmetries) > len(best_symmetries):
            best_symmetries = symmetries
            best_symmetric_qubit_pair = (q1,q2)
    return best_symmetries, best_symmetric_qubit_pair


def get_coupler(new_Q, q1, q2):
    if q1 < q2:
        if (q1,q2) in new_Q.keys():
            return new_Q[(q1,q2)]
        else:
            return 0
    elif q1 > q2:
        if (q2,q1) in new_Q.keys():
            return new_Q[(q2,q1)]
        else:
            return 0
    else:
        return 0


def get_value(new_Q, q1, q2):
    if q1 < q2:
        if (q1,q2) in new_Q.keys():
            return new_Q[(q1,q2)]
        else:
            return 0
    elif q1 > q2:
        if (q2,q1) in new_Q.keys():
            return new_Q[(q2,q1)]
        else:
            return 0
    else:
        if (q1,q2) in new_Q.keys():
            return new_Q[(q1,q2)]
        else:
            return 0


def enhance_QUBO(new_Q, new_n, symmetric_qubit_pair, symmetries, z=7):
    q1, q2 = symmetric_qubit_pair
    new_Q = add(new_Q, q1, q1, z)
    new_Q = add(new_Q, q2, q2, z)
    new_Q = add(new_Q, q1, q2, 2*z)
    new_Q = add(new_Q, new_n, new_n, z)
    new_Q = add(new_Q, q1, new_n, -2*z)
    new_Q = add(new_Q, q2, new_n, -2*z)
    for q3 in symmetries:
        new_Q = add(new_Q, new_n, q3, get_coupler(new_Q, q1, q3))
        new_Q = add(new_Q, q1, q3, -get_coupler(new_Q, q1, q3))
        new_Q = add(new_Q, q2, q3, -get_coupler(new_Q, q2, q3))
    return new_Q


def remove_qubit_pair(list_of_conflicting_qubits, symmetric_qubit_pair):
    new_list_of_conflicting_qubits = []
    for i in range(len(list_of_conflicting_qubits)):
        if list_of_conflicting_qubits[i][0] != symmetric_qubit_pair[0] or \
                list_of_conflicting_qubits[i][1] != symmetric_qubit_pair[1]:
            new_list_of_conflicting_qubits.append(list_of_conflicting_qubits[i])
    return new_list_of_conflicting_qubits


def add(new_Q, q1, q2, value):
    if q1 > q2:
        q1, q2 = q2, q1
    if (q1,q2) in new_Q.keys():
        new_Q[(q1,q2)] += value
    else:
        new_Q[(q1,q2)] = value
    return new_Q
