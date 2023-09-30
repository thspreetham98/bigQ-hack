from qiskit_algorithms import VQE, optimizers
from qiskit.circuit.library import EfficientSU2
from pytket.extensions.qiskit.tket_backend import TketBackend
from pytket.extensions.quantinuum import QuantinuumBackend

from qiskit import Aer
from qiskit.primitives import BackendEstimator
from qiskit_nature.second_q.hamiltonians.lattices import LineLattice, BoundaryCondition
from qiskit_nature.second_q.hamiltonians.ising_model import IsingModel
from qiskit.quantum_info import Operator


simulator = Aer.get_backend('aer_simulator')
aer_backend = BackendEstimator(simulator, options={"shots": 500})
machine = 'H1-2E'
backend_emu = QuantinuumBackend(device_name=machine)
backend_emu.login()
qis_backend = TketBackend(backend_emu, backend_emu.default_compilation_pass(optimisation_level=2))
qestimator = BackendEstimator(qis_backend, options={"shots": 100})

class Params:
    def __init__(self, num_qubits: int, use_quant, 
                 uniform_interaction, uniform_onsite_potential,
                 max_vqe_iterations):
        self.num_qubits = num_qubits
        self.hamiltonian_op = self.__get_hamiltonian__(uniform_interaction, uniform_onsite_potential)
        self.max_vqe_iterations = max_vqe_iterations
        self.use_quant = use_quant
            
    
    def __get_hamiltonian__(self, uniform_interaction, uniform_onsite_potential):
        line_lattice = LineLattice(num_nodes=self.num_qubits, boundary_condition=BoundaryCondition.OPEN)

        ising_model = IsingModel(
            line_lattice.uniform_parameters(
                uniform_interaction,
                uniform_onsite_potential
            ),
        )
        ham = ising_model.second_q_op()
        ham_operator = Operator(ham.to_matrix())
        return ham_operator


def vqe_solve(params: Params):
    optimizer = optimizers.COBYLA(maxiter=params.max_vqe_iterations)
    ansatz = EfficientSU2(params.num_qubits, entanglement="linear")
    if params.use_quant:
        estimator = qis_backend
    else:
        estimator = aer_backend
    vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)
    min = vqe.compute_minimum_eigenvalue(params.hamiltonian_op)
    return min.eigenvalue, min.optimal_circuit

if __name__ == "__main__":
    params = Params(num_qubits = 2, use_quant = True, 
                 uniform_interaction=-1.0, uniform_onsite_potential=-1.0,
                 max_vqe_iterations=5)
    ground_state_eigenvalue, ground_state_optimal_circuit = vqe_solve(params)
    print(ground_state_eigenvalue)

    