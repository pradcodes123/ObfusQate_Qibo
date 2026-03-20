OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];    // Single register: q[0]-q[2] for input, q[3]-q[5] for output
creg c[3];    // Classical register for measurements

// Step 1: Apply Hadamard gates to the input register (q[0]-q[2])
h q[0];
h q[1];
h q[2];

// Step 2: Oracle function - Copy input (q[0]-q[2]) to output (q[3]-q[5])
cx q[0], q[3];
cx q[1], q[4];
cx q[2], q[5];

// Step 3: Oracle - Apply XOR operations for s='101'
// (Flips bits in q[3], q[5] when q[0]=1, since s has 1s in positions 0 and 2)
cx q[0], q[3];
cx q[0], q[5];

// Step 4: Measure the output register (q[3]-q[5], optional but included)
measure q[3] -> c[0];
measure q[4] -> c[1];
measure q[5] -> c[2];

// Step 5: Apply Hadamard gates to the input register again (q[0]-q[2])
h q[0];
h q[1];
h q[2];

// Step 6: Measure the input register (q[0]-q[2], overwrites c)
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];