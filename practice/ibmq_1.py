import qiskit
import math
import matplotlib.pyplot as plt 
# from qiskit import IBMQ

# load account
# qiskit.IBMQ.save_account('9ce5ebd4ebc300a38c3ebd795bc80af580d53e16240f1c232a533b3a0611fb64fe22432e5f5442d23e9e553ea1deb06d47e0de8e682b1b4416f3a5112167c6ee') 
provider = qiskit.IBMQ.load_account()


# select device
# default_provider = qiskit.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal', project='default')
# backend = default_provider.get_backend('ibmq_boeblingen ')
backend = provider.get_backend('ibmq_essex')

# circuit setup

qc = qiskit.QuantumCircuit(1, 1)
 
# qc.h(0)
qc.u2(0, math.pi, 0)
qc.measure(0, 0)
qc.draw(output='mpl')
 
# simulate

result = qiskit.execute(qc, backend).result()
# print(result)
print(result.get_counts())
 
# plot
# qiskit.visualization.plot_histogram(counts)
# plt.subplots_adjust(bottom=0.25) 
plt.show()
 
