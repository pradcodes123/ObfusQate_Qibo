OPENQASM 2.0;
include "qelib1.inc";

// 7 qubits: 3 control (q[0]-q[2]), 4 work (q[3]-q[6])
qreg q[7];
creg c[3]; // Measure control qubits for period

// Step 1: Initialize control register in superposition
h q[0];
h q[1];
h q[2];

// Step 2: Initialize work register to |1> (q[6]=1)
x q[6];

// Step 3: Controlled-U operations (a^k mod N)
// Controlled-U (7^1 mod 15 = 7)
cx q[0], q[5];
cx q[5], q[4];
cx q[4], q[5];
cx q[5], q[4];
cx q[4], q[3];
cx q[3], q[4];
cx q[4], q[3];
cx q[5], q[3];
cx q[3], q[5];
cx q[5], q[3];

// Controlled-U^2 (7^2 mod 15 = 49 mod 15 = 4)
cx q[1], q[4];
cx q[4], q[3];
cx q[3], q[4];
cx q[4], q[3];
cx q[5], q[3];
cx q[3], q[5];
cx q[5], q[3];

// Controlled-U^4 (7^4 mod 15 = 2401 mod 15 = 1, identity, skip)

// Step 4: Inverse QFT on control qubits (q[0]-q[2])
swap q[0], q[2]; // Swap to reverse qubit order for QFT
h q[0];
cp(-pi/2) q[1], q[0];
h q[1];
cp(-pi/4) q[2], q[0];
cp(-pi/2) q[2], q[1];
h q[2];

// Step 5: Measure control qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];