import qiskit as qk
import sys
sys.path.append('../')
sys.path.append('../shor_s_algorithm')
import simulation as sim
import qft
import matplotlib.pyplot as plt
import math
from qiskit.providers.aer import noise
from qiskit.tools.visualization import plot_histogram

def a_7():
    qreg = qk.QuantumRegister(7, 'q0')
    creg = qk.ClassicalRegister(3)
    qc = qk.QuantumCircuit(qreg, creg)

    # initialize
    qc.x(6) 
    qc.h([0, 1, 2])

    # multiplier
    qc.cx(2, 4)
    qc.cx(2, 5)

    # ccx
    qc.cry(-math.pi/2, 1, 3)
    qc.cz(5, 3)
    qc.cry(math.pi/2, 1, 3)

    qc.x(4)
    
    # ccx
    qc.cry(-math.pi/2, 1, 6)
    qc.cz(4, 6)
    qc.cry(math.pi/2, 1, 6)

    inv_qft = qft.qft(3).inverse()
    qc.append(inv_qft, qargs=qreg[2::-1])


    for i in range(3):
        qc.measure(i, i)

    # qc.draw(output='mpl')
    # plt.show()

    return qc
    
def a_11():
    qreg = qk.QuantumRegister(7)
    creg = qk.ClassicalRegister(3)
    qc = qk.QuantumCircuit(qreg, creg)

    # initialize
    qc.x(6) 
    qc.h([0, 1, 2])

    # multiplier
    qc.cx(2, 3)
    qc.cx(2, 4)
    qc.cx(2, 6)

    inv_qft = qft.qft(3)
    qc.append(inv_qft, qargs=qreg[:3])
    for i in range(3):
        qc.measure(i, i)

    # qc.draw(output='mpl')
    # plt.savefig('../presentation/20200528/figs/11circuit.pdf')

    return qc

def a_2():
    qreg = qk.QuantumRegister(7)
    creg = qk.ClassicalRegister(3)
    qc = qk.QuantumCircuit(qreg, creg)

    # initialize
    qc.x(6) 
    qc.h([0, 1, 2])

    # multiplier
    qc.cx(2, 5)
    qc.cx(2, 6)

    # ccx
    qc.cry(-math.pi/2, 1, 3)
    qc.cz(5, 3)
    qc.cry(math.pi/2, 1, 3)

    qc.cx(6, 4)

    # ccx
    qc.ccx(1, 4, 6)

    inv_qft = qft.qft(3)
    qc.append(inv_qft, qargs=qreg[:3])
    for i in range(3):
        qc.measure(i, i)


    return qc

def a_7_smaller():
    qreg = qk.QuantumRegister(6)
    creg = qk.ClassicalRegister(2)
    qc = qk.QuantumCircuit(qreg, creg)

    # initialize
    qc.x(5) 
    qc.h([0, 1])

    # multiplier
    qc.cx(1, 3)
    qc.cx(1, 4)

    qc.barrier()

    # ccx
    qc.cry(-math.pi/2, 0, 2)
    qc.cz(4, 2)
    qc.cry(math.pi/2, 0, 2)

    qc.barrier()

    qc.x(3)

    qc.barrier()

    # ccx
    qc.cry(-math.pi/2, 0, 5)
    qc.cz(3, 5)
    qc.cry(math.pi/2, 0, 5)

    inv_qft = qft.qft(2).inverse()
    qc.append(inv_qft, qargs=qreg[1::-1])
    # qc.measure(6, 0)
    for i in range(2):
        qc.measure(i, i)

    # qc.draw(output='mpl')
    # plt.show()

    return qc

if __name__ == "__main__":
    # circuit = a_7_smaller()
    # sim.local_sim(circuit)
    
    circuit = a_11()
    result = sim.quantumComputerExp(circuit, backend='ibmq_rochester', note='a=11')
    circuit = a_7()
    result = sim.quantumComputerExp(circuit, backend='ibmq_rochester', note='a=7')
    circuit = a_2()
    result = sim.quantumComputerExp(circuit, backend='ibmq_rochester', note='a=2')

