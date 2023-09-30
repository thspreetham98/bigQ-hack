![Event Poster](img/bigqhack-chicago-2023.png)

# CQE Big Q Hack 2023 - Team GateHackers

## Team Information 
- Quantum Computing Platform Provider - Quantinuum (Mentored by Dr.Kathrin Spendier)
- Quantum Computing Use Case Provider - General Atomics (Dr. Matthew Cha & Dr.Pejman J.)
- Team Members : Ariadna Fernandez, Atharva Vidwans, Dhanvi Bharadwaj, Guillaume Remy and Preetham Tikkireddi


## Introduction
The collision processes and scattering physics of particles, atoms and molecules are crucial to our
understanding of the fundamental structure of matter. Fusion is the quantum nuclear reaction that
occurs when two light nuclei collide and fuse to create a single heavier nucleus with less mass than
the two original nuclei. The leftover mass is converted to energy and is responsible for the
generation of fusion energy. Harnessing practical fusion energy is identified as one of the Grand
Challenges for Engineering in the 21st Century.

Current fusion devices focus on deuterium-tritium (D-T) reaction [Kikuchi10], with two branches:
D + T → 5He∗
 → 4He(3.5 MeV) + n(14.1 MeV),
D +T → 5He∗
 → 5He+γ(16.75 MeV).


The fusion power gain in a large fusion device such as the International Thermonuclear
Experimental Reactor (ITER) or a Fusion Pilot Plant (FPP) is gauged by measuring neutron
production. However, the γ to n branching ratio is very small, somewhere between 1×10−5 and
3×10−4 with an uncertainty of about 50% [Kim12].

<i> Ab initio </i> approaches, such as the no-core shell model with continuum (NCSMC), represents the state
of the art for modeling D-T fusion [Hupin19]. To accurately model reactions, and in particular to
get the correct absolute values, the NCSMC includes as many scattering and reaction channels as
possible. Thus, not only is the relative motion of deuterium and tritium included, but also virtual
excited states as well, requiring a fully five-body quantum-mechanical wave function.
Numerical simulation could serve to guide and accelerate the time to experimental discovery in
quantum scattering. However, all known methods for classical simulation of fusion reaction, such as
renormalization group, quantum Monte Carlo, and tensor network methods, suffer from issues of
scalability, accuracy, and efficiency for quantum many-body systems, and introduce errors that are
difficult to gauge. Thus, the fusion reaction problem is an ideal candidate for demonstrating early
quantum advantage.

## Quantum Algorithms
Quantum computation has the potential for the efficient simulation of many body quantum systems.
This was demonstrated in polynomial time quantum algorithms, usually based on quantum phase
estimation (QPE), to solve the ground state and low-energy excited states for certain families of
quantum Hamiltonians with provable guarantees [Abrams99, Aspuru-Guzik05]. However, the QPE
algorithm requires resources that are out of reach for near term quantum hardware and it is
unclear when it will be achievable at scale. A variety of quantum algorithms for solving the ground
state problem on near-term noisy and early fault-tolerant quantum hardware have been proposed,
notably including the quantum metropolis algorithm, variational quantum eigensolver [Peruzzo14],
and quantum imaginary time evolution (QITE) [Jouzdani22]. 

Below, we highlight recent
demonstrations of quantum algorithms for the simulation of many body quantum Hamiltonians
towards quantum scattering:
- Scattering in the Ising model with the Quantum Lanczos Algorithm [Yeter21].
- Simulating excited states of the Lipkin model on a quantum computer [Manqoba23].
- Nuclear shell-model simulation in digital quantum computers [Perez23].

## Use Case Study
As a step towards applying quantum algorithms for the simulation of fusion reaction, we propose
the case study of quantum simulation of scattering of low-energy states in a model many body
quantum Hamiltonian. Such a study was performed for the Ising model on a 5-qubit IBM quantum
computer [Yeter21].
In this study, participants will first select a model quantum many body Hamiltonian. For example,
- the Lipkin model [Manqoba23],
- a simple nuclear Hamiltonian for proton-neutron interaction [Jouzdani22],
- the anisotropic 1-D XXZ-Heisenberg [VanDyke21].

Next, participants will demonstrate scattering of low-energy states. For example, in the 1-D
Heisenberg model in the ferromagnetic phase, low-energy excitations of an all up spin ground state
have blocks of down spins of down spins on neighboring sites and are called magnon bound states.
Scattering of magnon bound states have been shown to produce soliton-like behavior and have
been studied classically using DMRG and Bethe ansatz methods. Participants will use quantum
algorithms to determine physical quantities, such as scattering amplitudes, scattering phase, and
block length displacements, that describe the outcomes of scattering processes [Francis20]. For
example, a scattering amplitude, or transition probability, between an initial and final state may be
computed by

𝐴(𝑡) = 〈𝜓_final|𝜓_init(𝑡)〉 where |𝜓(𝑡)⟩ = 𝑒^iHt * |𝜓⟩

Various methods can be used when performing scattering calculations such as a Green’s function
approach through the Schwinger-Lipmann equation [Baker21] or dynamic approach with timeevolved two-point correlation functions [Yeter21].
