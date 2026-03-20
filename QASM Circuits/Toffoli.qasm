OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

// Set control qubits to |1⟩ to test Toffoli flip
x q[0];  // control 1
x q[1];  // control 2

// Toffoli gate decomposition
h q[2];
cx q[1], q[2];
tdg q[2];
cx q[0], q[2];
t q[2];
cx q[1], q[2];
tdg q[2];
cx q[0], q[2];
t q[1];
t q[2];
h q[2];
cx q[0], q[1];
t q[0];
tdg q[1];
cx q[0], q[1];

// Measurement
measure q -> c;
