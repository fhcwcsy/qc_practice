import qiskit as qk
import sys
sys.path.append('../')
import simulation as sim
from qiskit.ignis.mitigation.measurement import (complete_meas_cal,CompleteMeasFitter) 

qr = qk.QuantumRegister(3)
meas_calibs, state_labels = complete_meas_cal(qr=qr, circlabel='mcal') 


