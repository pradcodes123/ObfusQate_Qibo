OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

// stateprep
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];

// optimized parameters (numeric)
 // gamma  = 0.8649379797
 // beta   = 0.4566039439
 // so RZ angle per edge = -gamma
 // and RX per qubit = 2*beta = 0.9132078879

// edges: (0,1),(1,2),(1,3),(3,4),(2,4)
// Cost unitary (per edge = CX - RZ(-gamma) - CX)
cx q[0], q[1];
rz(-0.8649379797) q[1];
cx q[0], q[1];

cx q[1], q[2];
rz(-0.8649379797) q[2];
cx q[1], q[2];

cx q[1], q[3];
rz(-0.8649379797) q[3];
cx q[1], q[3];

cx q[3], q[4];
rz(-0.8649379797) q[4];
cx q[3], q[4];

cx q[2], q[4];
rz(-0.8649379797) q[4];
cx q[2], q[4];

// Mixer
rx(0.9132078879) q[0];
rx(0.9132078879) q[1];
rx(0.9132078879) q[2];
rx(0.9132078879) q[3];
rx(0.9132078879) q[4];

// measure
measure q[0] -> c[4];
measure q[1] -> c[3];
measure q[2] -> c[2];
measure q[3] -> c[1];
measure q[4] -> c[0];
