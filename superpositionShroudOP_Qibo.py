import ast
import random

def ssop_obfuscate_and_execute_qibo(code_content):
    # Parse the code into an AST
    parsed_code = ast.parse(code_content)

    # Extract import statements and functions
    imports = []
    other_nodes = []
    function_defs = []

    for node in parsed_code.body:
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            imports.append(node)
        elif isinstance(node, ast.FunctionDef):
            function_defs.append(node)
        else:
            other_nodes.append(node)

    # Select two random functions from the parsed code
    if len(function_defs) < 2:
        raise ValueError("The input code must contain at least two functions.")

    selected_functions = random.sample(function_defs, 2)

    # Remove the selected functions from other_nodes
    other_functions = [node for node in function_defs if node not in selected_functions]

    # Convert AST nodes back to code
    def ast_to_code(nodes):
        return "\n".join([ast.unparse(node) for node in nodes])

    # Create the code for the selected functions
    function_1_code = ast_to_code([selected_functions[0]])
    function_2_code = ast_to_code([selected_functions[1]])
    other_functions_code = ast_to_code(other_functions)
    other_code = ast_to_code(other_nodes)
    imports_code = ast_to_code(imports)

    # Ensure the function codes are properly formatted
    function_1_code = "\n    ".join(function_1_code.split("\n"))
    function_2_code = "\n    ".join(function_2_code.split("\n"))
    other_functions_code = "\n".join(other_functions_code.split("\n"))
    other_code = "\n".join(other_code.split("\n"))

    # Create the obfuscated code with Qibo
    obfuscated_code = f"""
{imports_code}
from qibo import Circuit, gates
import qibo

# Create a quantum circuit with one qubit
circuit = Circuit(1)
circuit.add(gates.H(0))  # Put the qubit in superposition using a Hadamard gate

# Set the backend to statevector simulation
qibo.set_backend("numpy")

# Execute the circuit to get the statevector
statevector = circuit()

# Decision based on quantum statevector
if abs(statevector.state()[0]) > 0:
    # This branch shall always execute
    {function_1_code}
if abs(statevector.state()[1]) > 0:
    # This branch shall never execute
    # The statevector for [1] is always 0
    {function_2_code}
    
{other_functions_code}
{other_code}
"""
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

    result = ssop_obfuscate_and_execute_qibo(sample_code)
    print("\n===== Obfuscated Code =====")
    print(result['obfuscated_code'])