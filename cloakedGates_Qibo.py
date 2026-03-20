import time
import random
from qibo import Circuit, gates
import qibo

qibo.set_backend("numpy")

def preprocess_qasm(qasm_input: str, keywords: list[str] = None) -> str:
    """
    Preprocess QASM code for Qibo compatibility by commenting out unsupported keyword lines
    and adding measurement gates if missing.

    Lines starting with keywords (e.g., 'barrier', 'int') are prefixed with '//' to preserve
    line numbers. If no measurement gates are present, measurements are added for all qubits
    to ensure Qibo's execute_circuit returns frequencies.

    Args:
        qasm_input (str): QASM code as a string.
        keywords (list[str], optional): Keywords to comment out (e.g., ['barrier']). 
                                       Defaults to ['barrier', 'int', 'float', 'for'].

    Returns:
        str: Preprocessed QASM code with commented keywords and added measurements.

    Raises:
        ValueError: If qasm_input is empty or not a string.
    """
    if not isinstance(qasm_input, str) or not qasm_input.strip():
        raise ValueError("Input QASM must be a non-empty string")

    # Default keywords for Qibo 0.2.18 unsupported statements
    keywords = keywords or ['barrier', 'int', 'float', 'for']
    keyword_set = set(k.lower() for k in keywords)

    # Initialize variables
    lines = qasm_input.splitlines()
    cleaned_lines = []
    qregs = {}  # {name: size, ...}, e.g., {'q': 8, 'a': 1}
    cregs = {}  # {name: size, ...}, e.g., {'c': 8}
    has_measurements = False
    is_qasm_3 = any(line.strip().startswith('OPENQASM 3') for line in lines)

    # Parse lines for registers and measurements, comment out keywords
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('//'):
            cleaned_lines.append(line)
            continue

        # Check for quantum registers
        if stripped_line.startswith(('qreg ', 'qubit[')):
            parts = stripped_line.split()
            if len(parts) >= 2:
                reg_name = parts[1].split('[')[0]
                size = int(parts[1].split('[')[1].split(']')[0]) if '[' in parts[1] else 1
                qregs[reg_name] = size
            cleaned_lines.append(line)
            continue

        # Check for classical registers
        if stripped_line.startswith(('creg ', 'bit[')):
            parts = stripped_line.split()
            if len(parts) >= 2:
                reg_name = parts[1].split('[')[0]
                size = int(parts[1].split('[')[1].split(']')[0]) if '[' in parts[1] else 1
                cregs[reg_name] = size
            cleaned_lines.append(line)
            continue

        # Check for measurements
        if 'measure' in stripped_line.lower():
            has_measurements = True
            cleaned_lines.append(line)
            continue

        # Comment out lines starting with keywords
        first_word = stripped_line.split()[0].lower() if stripped_line.split() else ''
        if first_word in keyword_set:
            cleaned_lines.append(f'// {line}')
        else:
            cleaned_lines.append(line)

    # Add measurements if none exist
    if not has_measurements and qregs:
        # Find or create a classical register
        creg_name = next(iter(cregs), 'meas')
        total_qubits = sum(qregs.values())
        if creg_name not in cregs:
            creg_size = total_qubits
            creg_line = f"bit[{creg_size}] {creg_name};" if is_qasm_3 else f"creg {creg_name}[{creg_size}];"
            cleaned_lines.insert(2, creg_line)  # After OPENQASM and include
            cregs[creg_name] = creg_size
        else:
            creg_size = cregs[creg_name]

        # Add measurements for all qubits
        meas_lines = []
        qubit_idx = 0
        for qreg_name, qreg_size in qregs.items():
            for i in range(qreg_size):
                if qubit_idx < creg_size:  # Ensure enough classical bits
                    meas_line = (
                        f"{creg_name}[{qubit_idx}] = measure {qreg_name}[{i}];"
                        if is_qasm_3 else
                        f"measure {qreg_name}[{i}] -> {creg_name}[{qubit_idx}];"
                    )
                    meas_lines.append(meas_line)
                    qubit_idx += 1
        if meas_lines:
            cleaned_lines.append('')  # Add blank line for readability
            cleaned_lines.extend(meas_lines)

    return '\n'.join(cleaned_lines)

# Gate substitution patterns
substitution_map = {
    'X': [
        ['H', 'Z', 'H'],
        ['S', 'Y', 'S'],
        ['H', 'Y', 'H'],
        ['Z', 'H', 'Z', 'H', 'Z'],
        ['SDG', 'Y', 'S'],
    ],
    'Z': [
        ['H', 'X', 'H'],
        ['S', 'S'],
        ['T', 'T', 'T', 'T'],
        ['X', 'H', 'X', 'H', 'X'],
    ],
    'S': [
        ['T', 'T'],
        ['X', 'T', 'X', 'T'],
        ['Z', 'T', 'Z', 'T'],
    ],
    'Y': [
        ['Z', 'X'],  # Corrected from ['X', 'Z']
        ['S', 'X', 'SDG'],
        ['T', 'X', 'TDG'],
    ]
}

# Gate class mapping
gate_mapping = {
    'X': gates.X,
    'Y': gates.Y,
    'Z': gates.Z,
    'H': gates.H,
    'S': gates.S,
    'SDG': gates.SDG,
    'T': gates.T,
    'TDG': gates.TDG
}

def get_gate(gate_name, qubit):
    g = gate_name.upper()
    if g == "SDG":
        return gates.S(qubit).dagger()
    elif g == "TDG":
        return gates.T(qubit).dagger()
    elif g in gate_mapping:
        return gate_mapping[g](qubit)
    raise ValueError(f"Unknown gate: {g}")

def substitute_gate(instr, qubit):
    name = instr.__class__.__name__.upper()
    if name in substitution_map:
        sequence = random.choice(substitution_map[name])
        return [get_gate(g, qubit) for g in sequence]
    return [instr]

def apply_dynamic_obfuscation(circuit):
    obf_circuit = Circuit(circuit.nqubits, density_matrix=True)
    for instr in circuit.queue:
        if isinstance(instr, gates.M) or len(instr.qubits) == 2:
            obf_circuit.add(instr)
        else:
            qubit = instr.qubits[0]
            substituted = substitute_gate(instr, qubit)
            for gate in substituted:
                obf_circuit.add(gate)
    return obf_circuit

def insert_obfuscation(circuit):
    new_circuit = Circuit(circuit.nqubits, density_matrix=True)
    measurements = []

    # Add original gates, substituting single-qubit gates
    for g in circuit.queue:
        if isinstance(g, gates.M):
            measurements.append(g)
        elif len(g.qubits) == 2:
            new_circuit.add(g)
        else:
            qubit = g.qubits[0]
            substituted = substitute_gate(g, qubit)
            for gate in substituted:
                new_circuit.add(gate)

    # Reapply measurements
    for m in measurements:
        new_circuit.add(gates.M(*m.qubits, collapse=False))

    return new_circuit

def execute_circuit(circuit, shots=1024, num_executions=10):
    execution_times = []
    final_result = None
    for _ in range(num_executions):
        start = time.time()
        result = circuit(nshots=shots)
        end = time.time()
        execution_times.append(end - start)
        final_result = result

    average_time = sum(execution_times) / len(execution_times)

    if not hasattr(final_result, 'frequencies'):
        raise ValueError("Missing measurements or invalid result object.")

    counts = final_result.frequencies(binary=True)
    return counts, average_time


def compute_tvd_dfc(original_results: dict, obfuscated_results: dict, shots: int = 1024) -> tuple[float, float]:
    """
    Compute Total Variation Distance (TVD) and Degree of Functional Corruption (DFC).

    Args:
        original_results (dict): Bitstring counts from original circuit (e.g., {'000': 500, '001': 524}).
        obfuscated_results (dict): Bitstring counts from obfuscated circuit.
        shots (int): Number of shots used in circuit execution (default: 1024).

    Returns:
        tuple[float, float]: (TVD, DFC) values.
    """
    if shots <= 0:
        raise ValueError("Number of shots must be positive")

    # Compute TVD: Σ|xi,obfus - xi,orig| / (2 * shots)
    all_keys = set(original_results).union(obfuscated_results)
    tvd_sum = sum(abs(original_results.get(key, 0) - obfuscated_results.get(key, 0)) for key in all_keys)
    tvd = tvd_sum / (2 * shots)

    # Compute DFC: (Count of correct output - Highest incorrect output) / shots
    # Correct output is the most frequent bitstring in original_results
    correct_bitstrings = set(original_results.keys())
    correct_count_sum = sum(obfuscated_results.get(bitstring, 0) for bitstring in correct_bitstrings)

    # Incorrect outputs are bitstrings in obfuscated_results not in correct_bitstrings
    incorrect_counts = [count for bitstring, count in obfuscated_results.items() 
                       if bitstring not in correct_bitstrings]
    max_incorrect_count = max(incorrect_counts, default=0)

    # DFC = (sum of correct counts - max incorrect count) / shots
    dfc = (correct_count_sum - max_incorrect_count) / shots if shots > 0 else 0

    return tvd, dfc        

def compare_results(original, obfuscated):
    # Normalize counts to probabilities
    total_orig = sum(original.values())
    total_obf = sum(obfuscated.values())
    if total_orig == 0 or total_obf == 0:
        return 0.0
    
    keys = set(original) | set(obfuscated)
    match = 0
    for k in keys:
        orig_prob = original.get(k, 0) / total_orig
        obf_prob = obfuscated.get(k, 0) / total_obf
        match += min(orig_prob, obf_prob)
    return 100 * match

def interpret_results(results):
    for key, value in results.items():
        print(f"Result: {key}, Count: {value}")

def clg_obfuscate_and_execute_qibo(input_qasm):
    input_qasm = input_qasm.strip()
    keywords_to_search = ['barrier']
    
    input_qasm = preprocess_qasm(input_qasm,keywords=keywords_to_search)
    
    if not input_qasm.startswith("OPENQASM 2"):
        raise ValueError("Invalid QASM version: Must start with 'OPENQASM 2.0;'")
    
    original_circuit = Circuit.from_qasm(input_qasm, density_matrix=True)

    obfuscated_circuit = insert_obfuscation(original_circuit)

    original_results, original_time = execute_circuit(original_circuit)
    obfuscated_results, obfuscated_time = execute_circuit(obfuscated_circuit)
    
    shots = 1024
    semantic_accuracy = compare_results(original_results, obfuscated_results)
    tvd, dfc = compute_tvd_dfc(original_results, obfuscated_results, shots=shots)


    return {
        "original_circuit": original_circuit,
        "obfuscated_circuit": obfuscated_circuit,
        "original_results": original_results,
        "obfuscated_results": obfuscated_results,
        "semantic_accuracy": semantic_accuracy,
        "tvd": tvd,
        "dfc": dfc,
        "original_time": original_time,
        "obfuscated_time": obfuscated_time,
    }

if __name__ == "__main__":
    file_path = "QASM Circuits/BV(1011).qasm"  # You may also select any other QASM file from the folder "QASM Circuit"
    with open(file_path, "r") as f:
            test_qasm = f.read() 
    print("Testing OpenQASM 2.0:")
    results_2 = clg_obfuscate_and_execute_qibo(test_qasm)
    
    print("\n--- Original Results (QASM 2.0) ---")
    interpret_results(results_2["original_results"])
    print("\n--- Obfuscated Results (QASM 2.0) ---")
    interpret_results(results_2["obfuscated_results"])
    print(f"\nSemantic Accuracy (QASM 2.0): {results_2['semantic_accuracy']:.2f}%")
    print(f"Original Time (QASM 2.0): {results_2['original_time']:.4f} s")
    print(f"Obfuscated Time (QASM 2.0): {results_2['obfuscated_time']:.4f} s")
    print(f"Total Variation Distance (TVD): {results_2['tvd']:.4f}")
    print(f"Degree of Functional Corruption (DFC): {results_2['dfc']:.4f}")