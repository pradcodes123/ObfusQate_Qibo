OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

// Create GHZ (5-qubit Bell-like) state
h q[0];
cx q[0], q[1];
cx q[1], q[2];
cx q[2], q[3];
cx q[3], q[4];

id q[0];
id q[1];
id q[2];
id q[3];
id q[4]

// Measure all qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
