OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];    // Single 6-qubit register for compatibility
creg c[2];    // Classical register for measurements (2 qubits used)

// Step 1: Prepare variational ansatz on q[0] and q[1]
ry(0.5) q[0];  // Placeholder parameter θ₀ = 0.5 radians
ry(0.3) q[1];  // Placeholder parameter θ₁ = 0.3 radians

// Step 2: Add entanglement
cx q[0], q[1]; // CNOT for entanglement

// Step 3: Second layer of parameterized RY rotations
ry(0.7) q[0];  // Placeholder parameter θ₂ = 0.7 radians
ry(0.4) q[1];  // Placeholder parameter θ₃ = 0.4 radians

// Step 4: Measure q[0] and q[1] for <Z0Z1>
measure q[0] -> c[0];
measure q[1] -> c[1];