import qiskit as qk
import sys
sys.path.append('../')
import simulation as sim

shots = 256
bits = '01'

# Build circuit
def build_circuit():
    qc = qk.QuantumCircuit(2, 2)
    qc.barrier()

    # prepare bell states
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # encode
    if bits == '11':
        qc.z(0)
        qc.x(0)

    elif bits == '01':
        qc.z(0)

    elif bits == '10':
        qc.x(0)

    qc.barrier()

    # Alice send the qubit to Bob

    # Bob receives qubit 0. Applies the recovery protocol
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    # take final measurements to see if the result is correct
    qc.measure(0, 0)
    qc.measure(1, 1)

    # print circuit
    qc.draw(output='mpl').savefig('circuit.png')
    print('Circuit built. Circuit image saved locally.')

    return qc

def accuracy(result_count):
    return result_count[bits]/float(shots)

if __name__ == "__main__":
    sim.leastBusy_device_exp(build_circuit(), shots=shots, accuracy_func=accuracy)
    
