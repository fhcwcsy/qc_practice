from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt 
 
ha = QuantumCircuit(4, 2)

# input
ha.x(0)
ha.x(1)
ha.barrier()

# XOR on bit 1
ha.cx(0, 2)
ha.cx(1, 2)
ha.barrier()

# output
ha.measure(2, 0)
ha.measure(3, 1)
ha.draw(output='mpl')

# simulate
counts = execute(ha, Aer.get_backend('qasm_simulator')).result().get_counts() 

# plot the result
plot_histogram(counts)
plt.subplots_adjust(bottom=0.25) 
 
plt.show()
