import qiskit as qk
import sys
import math
sys.path.append('../')
import simulation as sim

reg_size = 5
theta = math.pi*2/3

def build_circuit():
    qpe = qk.QuantumCircuit(reg_size+1, reg_size)
    qpe.x(reg_size)
    for qubit in range(reg_size):
        qpe.h(qubit)

    qpe.barrier()

    repetitions = 2**(reg_size-1)
    for counting_qubit in range(reg_size):
        for i in range(repetitions):
            qpe.cu1(theta, counting_qubit, reg_size) # This is C-U
        repetitions //= 2

    qpe.barrier()

    qft_dagger(qpe, reg_size)

    # measure
    for i in range(reg_size):
        qpe.measure(i, reg_size-i-1)

    # qpe.draw(output='mpl').savefig('circuit.svg')
    return qpe

def qft_dagger(qc, n):
    # Remember to swap the qubits
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n, 0, -1):
        k = n - j
        for m in range(k):
            qc.cu1(-math.pi/float(2**(k-m)), n-m-1, n-k-1) 
        qc.h(n-k-1)

if __name__ == "__main__":
    result = sim.local_sim(build_circuit(), shots=8192)
    maximum = max(result.values())
    for keys in result:
        if result[keys] == maximum:
            print(int(keys, 2)/(2**reg_size))
