OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

// Step 1: Hadamard on control
h q[0];

// Step 2: Target qubit in |1>
x q[1];

// Step 3: Controlled-Z (phase kickback)
cz q[0], q[1];

// Step 4: Hadamard to control to see interference
h q[0];

// Step 5: Measure
measure q -> c;
