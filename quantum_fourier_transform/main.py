import qiskit as qk
import sys
import math
sys.path.append('../')
import simulation as sim

n = 5

def input_state(qc, n):
    # Creates a special state that produce output 1 after the QFT
    for j in range(n):
        qc.h(j)
        qc.u1(-math.pi/float(2**(j)), j)

def build_circuit():
    qft_qc = qk.QuantumCircuit(n)

    input_state(qft_qc, n)
    qft_qc.draw(output='mpl').savefig('input_state.svg')

    qft_qc.barrier()
    
    # actual QFT circuit
    for j in range(n):
        qft_qc.h(j)
        for k in range(j+1, n):
            qft_qc.cu1(math.pi/float(2**(k-j)), k, j)
        qft_qc.barrier()

    for j in range(int(math.floor(n/2.))):
        qft_qc.swap(j, n-j-1)

    qft_qc.measure_all()

    qft_qc.draw(output='mpl').savefig('circuit.svg')
    print('Circuit built. Image saved locally.')

    return qft_qc

def acc(result):
    correct = '1'+'0'*(n-1)
    return result[correct]/1024.

if __name__ == "__main__":
    sim.quantumComputerExp(build_circuit(), accuracy_func=acc)


