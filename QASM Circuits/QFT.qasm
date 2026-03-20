OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];
// Quantum Fourier Transform for 4 qubits

// Optional: prepare input state |q3 q2 q1 q0> = |1 0 1 1> as example
x q[0];
x q[2];
x q[3];

// QFT
h q[0];
cu1(pi/2) q[1], q[0];
cu1(pi/4) q[2], q[0];
cu1(pi/8) q[3], q[0];

h q[1];
cu1(pi/2) q[2], q[1];
cu1(pi/4) q[3], q[1];

h q[2];
cu1(pi/2) q[3], q[2];

h q[3];

// Swap qubits to reverse order (QFT output is reversed)
swap q[0], q[3];
swap q[1], q[2];

// Measure all qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
