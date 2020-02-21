import qiskit
import numpy as np

#setup backend
backend = qiskit.Aer.get_backend('qasm_simulator')

# NOT gate
def not_gate(input_bit):

    q = qiskit.QuantumRegister(1) # a qubit to encode and manipulate the input
    c = qiskit.ClassicalRegister(1) # a bit to store the output
    qc = qiskit.QuantumCircuit(q, c)

    # initialize the bit with respect to the input bit
    if input_bit == '1':
        qc.x(q[0])

    # execute NOT

    qc.x(0)

    # extract output
    qc.measure(q[0], c[0])
    
    # run the circuit
    job = qiskit.execute(qc, backend, shots=1)
    output = list(job.result().get_counts().keys())[0]

    return output

if __name__ == "__main__":
    print(not_gate('1'))
