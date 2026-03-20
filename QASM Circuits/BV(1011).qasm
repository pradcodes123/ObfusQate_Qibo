OPENQASM 2.0;
include "qelib1.inc";

// 4 input qubits + 1 ancilla
qreg q[5];
creg c[4];

// Initialize ancilla qubit to |1> and apply H
x q[4];
h q[4];

// Apply Hadamard to input qubits
h q[0];
h q[1];
h q[2];
h q[3];

// Oracle for a = 1011
cx q[0], q[4]; // a0 = 1
// a1 = 1
cx q[1], q[4];
// a2 = 0 -> no gate
// a3 = 1
cx q[3], q[4];

// Apply Hadamard again to input qubits
h q[0];
h q[1];
h q[2];
h q[3];

// Measure input qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
