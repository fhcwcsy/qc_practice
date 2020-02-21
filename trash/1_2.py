from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt 
# %config InlineBackend.figure_format = 'svg' # Makes the images look nice
 

n = 8
n_q = 8
n_b = 8
qc_output = QuantumCircuit(n_q,n_b)

for j in range(n):
    qc_output.measure(j,j)

# plot configuration
# fig = qc_output.draw(output='mpl')
# fig.show()

qc_encode = QuantumCircuit(n)
qc_encode.x(7) 
qc_encode.x(2) 

qc = qc_encode + qc_output
qc.draw(output='mpl')

#simulate
# replace 'Aer.get_backend('qasm_simulator')' with another device if you want
# to use another one.

counts = execute(qc, Aer.get_backend('qasm_simulator')).result().get_counts() 

#plot the result
plot_histogram(counts)
plt.subplots_adjust(bottom=0.25) 
plt.show()

# plt.savefig("test.svg") 
 

