import qiskit as qk
import math

def qft(n, draw=False):
    # the upper bit is the MSB
    qreg = qk.QuantumRegister(n)
    qc = qk.QuantumCircuit(qreg)
    for i in range(n):
        qc.h(i)
        for j in range(2, n-i+1):
            qc.cu1(2*math.pi/(2**j), i+j-1, i)
        # qc.barrier()
    # qc.draw(output='mpl')
    if draw:
        print(qc)
    gate = qc.to_gate()
    gate.name = 'QFT'

    return gate

 
