from qiskit.circuit import QuantumCircuit, QuantumRegister, Parameter, ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator, BackendSampler
from qiskit.circuit.library import EfficientSU2
from qiskit_algorithms import VQD, VQE, SamplingVQE, NumPyEigensolver
from qiskit_algorithms.optimizers import COBYLA, SPSA, SLSQP
from qiskit_algorithms.gradients import DerivativeType, LinCombQGT, LinCombEstimatorGradient
from qiskit_algorithms.state_fidelities import BaseStateFidelity, ComputeUncompute

from qiskit_nature.second_q.hamiltonians.lattices import LineLattice, BoundaryCondition
from qiskit_nature.second_q.hamiltonians.ising_model import IsingModel
from qiskit.quantum_info import Operator
# from qiskit.quantum_info.operators.base_operator import BaseOperator

import matplotlib.pyplot as plt

from qiskit import Aer
import numpy as np


simulator = Aer.get_backend('aer_simulator')
counts = []
values = []
steps = []
# aer_backend = BackendEstimator(simulator, options={"shots": 500})
# machine = 'H1-2E'
# backend_emu = QuantinuumBackend(device_name=machine)
# backend_emu.login()
# qis_backend = TketBackend(backend_emu, backend_emu.default_compilation_pass(optimisation_level=2))
# qestimator = BackendEstimator(qis_backend, options={"shots": 100})

class Params:
    def __init__(self, num_qubits: int, no_of_states_to_compute: int, use_quant, 
                 uniform_interaction, uniform_onsite_potential,
                 max_vqe_iterations, optimizer):
        self.num_qubits = num_qubits
        self.no_of_states_to_compute = no_of_states_to_compute
        self.hamiltonian_op = self.__get_hamiltonian__(uniform_interaction, uniform_onsite_potential)
        self.max_vqe_iterations = max_vqe_iterations
        self.use_quant = use_quant
        self.optimizer = optimizer
            
    
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
        # print('numpy soln', np.linalg.eigvals(ham_operator))
        return SparsePauliOp.from_operator(ham_operator)


def callback(eval_count, params, value, meta, step):
    counts.append(eval_count)
    values.append(value)
    steps.append(step)

if __name__ == "__main__":
    # TODO: which on has to be less than 1?
    optimizer_slsqp = SLSQP(maxiter=50)
    optimizer_cobyla = COBYLA(maxiter=50)
    estimator = Estimator()
    params = Params(num_qubits = 3, no_of_states_to_compute = 3, use_quant = False, 
                 uniform_interaction=-1.0, uniform_onsite_potential=-0.4,
                 max_vqe_iterations=50, optimizer=optimizer_slsqp)
    ansatz = EfficientSU2(params.num_qubits, entanglement="linear")
    
    sampler = BackendSampler(simulator)
    fidelity = ComputeUncompute(sampler)


    # vqd = VQD(estimator, fidelity, ansatz, optimizer, k=params.no_of_states_to_compute, betas=[33]*params.no_of_states_to_compute, callback=callback)
    vqd = VQD(estimator, fidelity, ansatz, params.optimizer, k=params.no_of_states_to_compute, callback=callback)
    result = vqd.compute_eigenvalues(params.hamiltonian_op)
    print('VQD res: ', result.eigenvalues)

    exact_solver = NumPyEigensolver(k=params.num_qubits)
    exact_result = exact_solver.compute_eigenvalues(params.hamiltonian_op)
    ref_values = exact_result.eigenvalues
    print('NumPyEigensolver res: ', ref_values)


