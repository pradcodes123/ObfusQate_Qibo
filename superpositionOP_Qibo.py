import ast
import random
import qibo
from qibo import Circuit, gates

# Set numpy backend
qibo.set_backend('numpy')

def extract_random_function_and_imports(code_content):
    tree = ast.parse(code_content)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    return random.choice(functions) if functions else None, imports, tree.body

def indent_function_body(function_code):
    lines = function_code.split('\n')
    indented_lines = [lines[0]] + ['    ' + line if line else line for line in lines[1:]]
    return '\n'.join(indented_lines)

def modularize_opaque_pred(sample_code_path, opaque_pred_code):
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
    sample_code = "\n".join(ast.unparse(node) for node in sample_code_body if not isinstance(node, (ast.Import, ast.ImportFrom)))

    # Integrate everything into the new obfuscated code
    new_code = f"""
{imports_code}

{opaque_pred_code}

initial_circuit = create_initial_circuit()
counts = execute_circuit(initial_circuit)
selected_path = pather(counts)

if selected_path == '01':
    def prime_numbers(limit=25):
        print(f"Prime Numbers up to {{limit}}:")
        primes = []
        for num in range(2, limit + 1):
            is_prime = True
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        print(primes)
elif selected_path == '11':
    {random_function_code}
elif selected_path == '10':
    def fibonacci_sequence(n=20):
        print(f"Fibonacci Sequence up to {{n}} terms:")
        fib = [0, 1]
        while len(fib) < n:
            fib.append(fib[-1] + fib[-2])
        print(fib)
elif selected_path == '00':
    def factorial_calculator(n=10):
        print(f"Factorials up to {{n}}:")
        factorials = {{}}
        for i in range(1, n + 1):
            factorials[i] = 1 if i == 1 else i * factorials[i - 1]
        for key, value in factorials.items():
            print(f"{{key}}! = {{value}}")
            
{sample_code}            
"""
    return new_code

def sop_obfuscate_and_execute_qibo(code_content):
    opaque_pred_code = """
import qibo
from qibo import Circuit, gates

def create_initial_circuit():
    circuit = Circuit(5, density_matrix=True)
    # Apply Hadamard gates to all qubits to create superposition
    circuit.add(gates.H(q) for q in range(5))
    circuit.add(gates.Z(4))
    circuit.add(gates.CNOT(2, 4))
    circuit.add(gates.H(0))
    circuit.add(gates.CNOT(3, 4))
    circuit.add(gates.H(2))
    circuit.add(gates.H(1))
    circuit.add(gates.X(1))
    circuit.add(gates.Y(2))
    circuit.add(gates.H(1))
    circuit.add(gates.S(2))
    circuit.add(gates.Z(1))
    circuit.add(gates.Y(2))
    circuit.add(gates.H(1))
    circuit.add(gates.X(1))
    circuit.add(gates.H(3))
    circuit.add(gates.M(*range(4), collapse=False))
    return circuit

def execute_circuit(circuit):
    result = circuit(nshots=1024)
    if not hasattr(result, 'frequencies'):
        raise ValueError("Circuit execution returned QuantumState instead of CircuitResult. Ensure measurements are included.")
    counts = result.frequencies(binary=True)
    return counts

def pather(counts):
    selection = max(counts, key=counts.get)
    return selection[2:4]

qibo.set_backend('numpy')
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
    result = sop_obfuscate_and_execute_qibo(sample_code)
    print(result['obfuscated_code'])

