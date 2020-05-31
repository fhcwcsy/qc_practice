import sys
sys.path.append('../')
sys.path.append('../shor_s_algorithm')
import simulation as sim
import qft
import matplotlib.pyplot as plt
import math
import numpy as np
# Import measurement calibration functions
import qiskit as qk
from qiskit.providers.aer import noise
from qiskit.tools.visualization import plot_histogram
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, tensored_meas_cal,
                                                 CompleteMeasFitter, TensoredMeasFitter) 
 

 
 
if __name__ == "__main__":
    print('program started')

    bename = 'ibmq_cambridge'

    # account setup

    account = qk.IBMQ.load_account()
    ntu_provider = qk.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal',
            project='default')
    _backend = ntu_provider.get_backend(bename)

    # account setup finished

    qreg = qk.QuantumRegister(7)
    layout = {qreg[0]: 4, 
              qreg[1]: 6,
              qreg[2]: 13, 
              qreg[3]: 12, 
              qreg[4]: 11, 
              qreg[5]: 17, 
              qreg[6]: 23}
     

    ########## mitigation circuit ##########

    meas_calibs, state_labels = complete_meas_cal(
            qubit_list=[0, 1, 2], qr=qreg, circlabel='mcal') 
    job = qk.execute(meas_calibs, backend=_backend, shots=8192, initial_layout=layout)
    qk.tools.monitor.job_monitor(job)
    cal_results = job.result()
    meas_fitter = CompleteMeasFitter(cal_results, state_labels, circlabel='mcal')
    
    ##########  a = 7  ##########
    creg = qk.ClassicalRegister(3)
    qc7 = qk.QuantumCircuit(qreg, creg, name='7')

    # initialize
    qc7.x(6) 
    qc7.h([0, 1, 2])

    # multiplier
    qc7.cx(2, 4)
    qc7.cx(2, 5)

    # ccx
    qc7.cry(-math.pi/2, 1, 3)
    qc7.cz(5, 3)
    qc7.cry(math.pi/2, 1, 3)

    qc7.x(4)

    # ccx
    qc7.cry(-math.pi/2, 1, 6)
    qc7.cz(4, 6)
    qc7.cry(math.pi/2, 1, 6)

    inv_qft = qft.qft(3)
    qc7.append(inv_qft, qargs=qreg[:3])
    for i in range(3):
        qc7.measure(i, i)

    ##########  a = 11  ##########

    qc11 = qk.QuantumCircuit(qreg, creg, name='11')

    # initialize
    qc11.x(6) 
    qc11.h([0, 1, 2])

    # multiplier
    qc11.cx(2, 3)
    qc11.cx(2, 4)
    qc11.cx(2, 6)

    inv_qft = qft.qft(3)
    qc11.append(inv_qft, qargs=qreg[:3])
    for i in range(3):
        qc11.measure(i, i)

    ##########  run circuits  ##########
    
    for qc in [qc7, qc11]:

        job = qk.execute(qc, backend=_backend, shots=8192, initial_layout=layout)
        qk.tools.monitor.job_monitor(job)
        raw_results = job.result()
        raw_counts = raw_results.get_counts()

        ########## error mitigation ##########
        meas_filter = meas_fitter.filter
        mitigated_results = meas_filter.apply(raw_results)
        mitigated_counts = mitigated_results.get_counts(0)
        qk.tools.visualization.plot_histogram(
                [raw_counts, mitigated_counts], legend=['raw', 'mitigated'], 
                title=f'a = {qc.name}')
        plt.savefig(f'./results/error_mitigation_{qc.name}_cambridge2.svg')
        plt.show()
    
