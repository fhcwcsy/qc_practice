import qiskit as qk
import sys
sys.path.append('../')
import simulation as sim

nQubits = 2 # length of s
s = int('10', 2) # the hidden integer (s)
barriers = True
shots = 1024

if s >= 2**nQubits:
    raise Exception('SLengthError')

def place_barriers(qc):
    if barriers:
        qc.barrier()

def build_circuit():
    qr = qk.QuantumRegister(nQubits)
    cr = qk.ClassicalRegister(nQubits)

    bvCircuit = qk.QuantumCircuit(qr, cr)

    for i in range(nQubits):
        bvCircuit.h(qr[i])

    place_barriers(bvCircuit)

    # Apply the inner-product oracle
    for i in range(nQubits):
        if (s & (1 << i)):
            bvCircuit.z(qr[i])
        else:
            bvCircuit.iden(qr[i]) 

    place_barriers(bvCircuit)

    for i in range(nQubits):
        bvCircuit.h(qr[i])

    place_barriers(bvCircuit)

    bvCircuit.measure(qr, cr)

    bvCircuit.draw(output='mpl').savefig('circuit.svg')
    print('Circuit build. Circuit image saved locally.')

    return bvCircuit

def accuracy(result):
    correct_answer = '{0:0{1}b}'.format(s, nQubits) 
    print('Correct answer:', correct_answer)
    return result[correct_answer]/float(shots)

if __name__ == "__main__":
    sim.quantumComputerExp(build_circuit(), accuracy_func=accuracy,
            shots=1024, mode='least_busy')
