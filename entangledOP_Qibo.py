import ast
import random
from qibo import Circuit, gates, set_backend

def extract_random_function_and_imports(code_content):
    tree = ast.parse(code_content)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    return random.choice(functions) if functions else None, imports, tree.body

def indent_function_body(function_code):
    lines = function_code.split('\n')
    indented_lines = [lines[0]] + ['    ' + line if line else line for line in lines[1:]]
    return '\n'.join(indented_lines)

def modularize_opaque_pred(sample_code, opaque_pred_code):
    random_function, imports, sample_code_body = extract_random_function_and_imports(sample_code)
    if random_function is None:
        raise ValueError("No function found in the sample code")

    # Remove repeated imports from the sample code imports list
    unique_imports = {}
    for node in imports:
        for alias in node.names:
            unique_imports[alias.name] = node

    # Convert the selected function and imports back to code
    random_function_code = indent_function_body(ast.unparse(random_function))
    imports_code = "\n".join(ast.unparse(node) for node in unique_imports.values())
    sample_code_body.remove(random_function)
    sample_code = "\n".join(ast.unparse(node) for node in sample_code_body if not isinstance(node, (ast.Import, ast.ImportFrom)))

    # Integrate everything into the new obfuscated code
    new_code = f"""
{imports_code}

{opaque_pred_code}

num_pairs = 8
counts = entangler(num_pairs)

if sum(int(bit) for bit in max(counts, key=counts.get)) == num_pairs * 2:
    def run_bell_state():
        # You may change this function to do something else entirely
        circuit = Circuit(2)
        circuit.add(gates.H(0))
        circuit.add(gates.CNOT(0, 1))
        circuit.add(gates.M(0, 1))
        print("Bell State Algorithm result")
        print([str(gate) for gate in circuit.queue])
        backend = NumpyBackend()
        result = backend.execute_circuit(circuit, nshots=1024)
        counts = result.frequencies(binary=True)
        print(counts)
else:
    {random_function_code}

{sample_code}
"""
    return new_code

def eop_obfuscate_and_execute_qibo(code_content):
    opaque_pred_code = """
from qibo import Circuit, gates
import qibo

def create_entangled_pairs(circuit, num_pairs):
    for i in range(0, num_pairs * 2, 2):
        circuit.add(gates.H(i))
        circuit.add(gates.CNOT(i, i + 1))

def measure_all(circuit, num_qubits):
    circuit.add(gates.M(*range(num_qubits)))

def execute_circuit(circuit, shots=1024):
    qibo.set_backend('numpy')
    result = circuit( nshots=shots)
    counts = result.frequencies(binary=True)
    return counts

def entangler(num_pairs):
    circuit = Circuit(num_pairs * 2)
    create_entangled_pairs(circuit, num_pairs)
    measure_all(circuit, num_pairs * 2)
    counts = execute_circuit(circuit, shots=1024)
    return counts

counts = entangler(8)
"""
    obfuscated_code = modularize_opaque_pred(code_content, opaque_pred_code)

    return {
        'original_code': code_content,
        'obfuscated_code': obfuscated_code,
    }

if __name__ == "__main__":
    sample_code = '''
import time
def pow(n, exp=2):
    return n ** exp

def sum(a, b):
    return a + b
start = time.time()
print(f"Square of 4 = {pow(4)}")
end = time.time()
print(f"Execution time: {end - start:.6f} seconds")
'''
    result = eop_obfuscate_and_execute_qibo(sample_code)
    print(result['obfuscated_code'])