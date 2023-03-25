We receive a very interesting looking file with an `.qasm` extension.

![image](https://user-images.githubusercontent.com/80063008/227546021-906fb26b-5510-4dc4-ab0f-3518075cb857.png)

Reading it we see OPENQASM 2.0 being mentioned:

![image](https://user-images.githubusercontent.com/80063008/227546150-18e89cc0-7ed4-48cb-9394-c4c755532a91.png)

Some research later, we find we can open it using the `qiskit` python library:

```bash
pip install qiskit
```

With ChatGPT's help, we reached this script:

```python
from qiskit import QuantumCircuit, Aer, execute

# Load the qasm file using from_qasm_file() method
qasm_file = 'quantum_artifact.qasm'
qc = QuantumCircuit.from_qasm_file(qasm_file)

# Set up the backend and execute the circuit
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()

# Print the result
print(result.get_counts(qc))
```
The output of this script gives us a binary string:
![image](https://user-images.githubusercontent.com/80063008/227546843-41131e9c-5a89-4aae-b579-a87f17a0730a.png)

Decoded it in Cyberchef to:

HTB{a_gl1mps3_0f_h0p3}