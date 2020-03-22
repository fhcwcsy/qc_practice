import qiskit as qk
import beauregard_multiplier as multiplier
import qft
import math
import sys
sys.path.append('../')
import simulation as sim

def qpe(bitlen, a, N):

    # 0 ~ bitlen-1: counting qubits
    # bitlen ~ 3bitlen+1: oracle
    qreg = qk.QuantumRegister(3*bitlen+1) 

    qc = qk.QuantumCircuit(qreg)

    for i in range(bitlen):
        qc.h(i)

    for i in range(bitlen):
        qc.append(multiplier.cu_a(bitlen,((2**i * a) % N) , N),
                qargs=[qreg[bitlen-i-1]]+qreg[bitlen:])

    qc.append(qft.qft(bitlen), qargs=qreg[:bitlen])

    print(qc.draw())

if __name__ == "__main__":
    qpe(5, 5, 15)
