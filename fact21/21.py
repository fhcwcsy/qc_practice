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
 

def printtable():
    for i in [2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20]:
        for j in range(20):
            print('{:5d}'.format(i**(2**j)%21), end='')
        print()

def a_8():
    qreg = qk.QuantumRegister(8)
    creg = qk.ClassicalRegister(3)
    qc = qk.QuantumCircuit(qreg, creg)

    # initialize
    qc.x(7) 
    qc.h([0, 1, 2])

    # multiplier
    qc.cx(2, 7)
    qc.cx(2, 4)

    inv_qft = qft.qft(3)
    qc.append(inv_qft, qargs=qreg[:3])
    for i in range(3):
        qc.measure(i, i)

    # qc.draw(output='mpl')
    # plt.savefig('../presentation/20200528/figs/11circuit.pdf')

    return qc
 

if __name__ == "__main__":
    qc = a_8()
    sim.local_sim(qc)

