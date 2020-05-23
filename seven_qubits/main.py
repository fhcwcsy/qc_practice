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


import numpy as np
# Import measurement calibration functions
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, tensored_meas_cal,
                                                 CompleteMeasFitter, TensoredMeasFitter) 

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

    inv_qft = qft.qft(3)
    qc.append(inv_qft, qargs=qreg[:3])
    for i in range(3):
        qc.measure(i, i)

    # print(qc)

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

    # print(qc)

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

    print(qc)

    return qc

if __name__ == "__main__":
    
    circuit = a_7()
    # sim.local_sim(circuit)
    # result = sim.quantumComputerExp(circuit, backend='ibmq_16_melbourne')
    # circuit = a_11()
    # result = sim.quantumComputerExp(circuit, backend='ibmq_rochester')

    for i in range(4):
        result = sim.quantumComputerExp(circuit, backend='ibmq_paris',
                note=f'optimize={i}', optimize=i)

    for i in range(4):
        result = sim.quantumComputerExp(circuit, backend='ibmq_almaden',
                note=f'optimize={i}', optimize=i)
