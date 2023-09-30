from qiskit.circuit import QuantumCircuit, QuantumRegister, Parameter, ParameterVector
from qiskit_algorithms.gradients import DerivativeType, LinCombQGT
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms.gradients import LinCombEstimatorGradient
from qiskit.primitives import Estimator


# Instantiate the system Hamiltonian
h2_hamiltonian = SparsePauliOp.from_list([('II', -1.05),
                                          ('IZ',  0.39),
                                          ('ZI', -0.39),
                                          ('ZZ', -0.01)])

# This is the target energy
h2_energy = -1.85727503

# Define the Ansatz
wavefunction = QuantumCircuit(2)
params = ParameterVector('theta', length=8)
it = iter(params)
wavefunction.ry(next(it), 0)
wavefunction.ry(next(it), 1)
wavefunction.rz(next(it), 0)
wavefunction.rz(next(it), 1)
wavefunction.cx(0, 1)
wavefunction.ry(next(it), 0)
wavefunction.ry(next(it), 1)
wavefunction.rz(next(it), 0)
wavefunction.rz(next(it), 1)

#Make circuit copies for different VQEs
wavefunction_1 = wavefunction.copy()
wavefunction_2 = wavefunction.copy()

from qiskit_algorithms.optimizers import CG
from qiskit_algorithms import VQE, SamplingVQE

#Conjugate Gradient algorithm
optimizer = CG(maxiter=50)

# Gradient callable
estimator = Estimator()
grad = LinCombEstimatorGradient(estimator) # optional estimator gradient
vqe = VQE(estimator=estimator, ansatz=wavefunction, optimizer=optimizer, gradient=grad)

result = vqe.compute_minimum_eigenvalue(h2_hamiltonian)
print('Result of Estimator VQE:', result.optimal_value, '\nReference:', h2_energy)

from scipy.optimize import minimize

#Classical optimizer
vqe_classical = VQE(estimator=estimator, ansatz=wavefunction_2, optimizer=minimize, gradient=grad)

result_classical = vqe_classical.compute_minimum_eigenvalue(h2_hamiltonian)
print('Result of classical optimizer:', result_classical.optimal_value, '\nReference:', h2_energy)