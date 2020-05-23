import qiskit as qk
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, tensored_meas_cal,
                                                 CompleteMeasFitter, TensoredMeasFitter) 
 

if __name__ == "__main__":
    qreg = qk.QuantumRegister(7, 'q0')
    layout = {qreg[0]: 12, 
              qreg[1]: 11,
              qreg[2]: 13, 
              qreg[3]: 17, 
              qreg[4]: 14, 
              qreg[5]: 12, 
              qreg[6]: 6}
     
    account = qk.IBMQ.load_account()
    ntu_provider = qk.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal',
            project='default')
    bename = 'ibmq_cambridge'
    _backend = ntu_provider.get_backend(bename)
     
    qreg = qk.QuantumRegister(7, 'q0')
    meas_calibs, state_labels = complete_meas_cal(qubit_list=[0, 1, 2], qr=qreg, circlabel='mcal') 
    qk.compiler.transpile(meas_calibs, backend=_backend, initial_layout=layout)
     


