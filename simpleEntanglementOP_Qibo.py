import ast
import random
import qibo
from qibo import Circuit, gates,set_backend

# Set numpy backend
set_backend('numpy')

def extract_random_function_and_imports(code_content):
    tree = ast.parse(code_content)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    return random.choice(functions) if functions else None, imports, tree.body

def indent_function_body(function_code):
    lines = function_code.split('\n')
    indented_lines = [lines[0]] + ['    ' + line if line else line for line in lines[1:]]
    return '\n'.join(indented_lines)

def modularize_simple_entanglement(sample_code_path, simple_entanglement_code):
    random_function, imports, sample_code_body = extract_random_function_and_imports(sample_code_path)
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
    sample_code = "\n".join(
        ast.unparse(node) for node in sample_code_body if not isinstance(node, (ast.Import, ast.ImportFrom)))

    # Integrate the obfuscated functions with the code
    new_code = f"""
{imports_code}

{simple_entanglement_code}

# Obfuscated quantum execution
qc = Circuit(2, density_matrix=True)
create_entangled_pair(qc, range(2))
measure_all(qc, range(2))
counts = execute_circuit(qc, shots=1024)

measured_result = [int(bit) for bit in max(counts, key=counts.get)]

if measured_result == [0, 0]:
    {random_function_code}

elif measured_result == [1, 1]:
    {random_function_code}

elif measured_result == [0, 1]:
    def run_bell_state():
        # You may change this function to do something else entirely
        qc = Circuit(2, density_matrix=True)
        qc.add(gates.H(0))
        qc.add(gates.CNOT(0, 1))
        qc.add(gates.M(0, 1, collapse=False))
        print("Bell State Algorithm result")
        print(qc.draw())  # Note: Qibo's draw() is text-based; no matplotlib equivalent available

elif measured_result == [1, 0]:
    def fibonacci_sequence(n=20):
        print(f"Fibonacci Sequence up to {{n}} terms:")
        fib = [0, 1]
        while len(fib) < n:
            fib.append(fib[-1] + fib[-2])
        print(fib)

{sample_code}
"""
    return new_code

def seop_obfuscate_and_execute_qibo(code_content):
    simple_entanglement_code = """
import qibo
from qibo import Circuit, gates

def create_entangled_pair(qc, qubits):
    qc.add(gates.H(qubits[0]))
    qc.add(gates.CNOT(qubits[0], qubits[1]))

def measure_all(qc, qubits):
    qc.add(gates.M(*qubits, collapse=False))

def execute_circuit(qc, shots=1024):
    result = qc(nshots=shots)
    if not hasattr(result, 'frequencies'):
        raise ValueError("Circuit execution returned QuantumState instead of CircuitResult. Ensure measurements are included.")
    counts = result.frequencies(binary=True)
    print(counts)
    return counts

qibo.set_backend('numpy')
"""
    obfuscated_code = modularize_simple_entanglement(code_content, simple_entanglement_code)

    return {
        'original_code': code_content,
        'obfuscated_code': obfuscated_code,
    }



if __name__ == "__main__":
    # Sample input code to be obfuscated
    sample_code = '''
import time    
def pow(n, exp=2):
    return n ** exp

def sum(a, b):
  return a + b

start  = time.time()
print(f"Square of 4 = {pow(4)}")
end = time.time()
print(f"Execution time: {end - start:.6f} seconds")    
'''

    result = seop_obfuscate_and_execute_qibo(sample_code)
    print("\n===== Obfuscated Code =====")
    print(result['obfuscated_code'])


