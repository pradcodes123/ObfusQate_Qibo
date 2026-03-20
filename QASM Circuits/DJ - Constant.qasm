OPENQASM 2.0;
// Deutsch-Jozsa constant function f(x)=0
include "qelib1.inc";

qreg q[4];  // 3 input qubits + 1 ancilla
creg c[3];

// Initialize ancilla to |1> and apply H
x q[3];
h q[3];

// Apply Hadamard to input qubits
h q[0];
h q[1];
h q[2];

// Oracle for f(x)=0 -> do nothing

// Apply Hadamard again to input qubits
h q[0];
h q[1];
h q[2];

// Measure input qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
