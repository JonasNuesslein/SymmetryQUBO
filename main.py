from symmetricQUBO import get_symmetry_free_QUBO
import maxClique
import hamiltonCycles
import graphColoring
import vertexCover
import graphIsomorphism
import utils


problem = maxClique.MAXCLIQUE(V=30, E=87)
#problem = graphIsomorphism.GRAPHISOMORPHISM(V=6, E=10)
#problem = vertexCover.VERTEXCOVER(V=30, E=131)
#problem = graphColoring.GRAPHCOLORING(V=10, E=31, n_colors=3)
#problem = hamiltonCycles.HAMILTONCYCLES(V=6, E=10)

new_Q = get_symmetry_free_QUBO(problem.Q, n_min_symmetries=3, max_additional_qubits=25)

n, n_couplers, _, depth = utils.print_info(problem.Q, reps=3, solve=False, shots=1024)
print("Data for Q:")
print("   n_qubits: ", n)
print("   depth: ", depth)
print("   n_couplers: ", n_couplers, "\n")

n, n_couplers, _, depth = utils.print_info(new_Q, reps=3, solve=False, shots=1024)
print("Data for Q_mod:")
print("   n_qubits: ", n)
print("   depth: ", depth)
print("   n_couplers: ", n_couplers)
