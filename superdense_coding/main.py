import qiskit as qk

shots = 256
bits = '01'

# Build circuit
def build_circuit():
    qc = qk.QuantumCircuit(2, 2)
    qc.barrier()

    # prepare bell states
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # encode
    if bits == '11':
        qc.z(0)
        qc.x(0)

    elif bits == '01':
        qc.z(0)

    elif bits == '10':
        qc.x(0)

    qc.barrier()

    # Alice send the qubit to Bob

    # Bob receives qubit 0. Applies the recovery protocol
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    # take final measurements to see if the result is correct
    qc.measure(0, 0)
    qc.measure(1, 1)

    # print circuit
    qc.draw(output='mpl').savefig('circuit.png')
    print('Circuit built. Circuit image saved locally.')

    return qc

def local_sim(qc):
    print('Simulation started.')
    backend = qk.Aer.get_backend('qasm_simulator') 
    job_sim = qk.execute(qc, backend)
    sim_result = job_sim.result()
    print('Simulation finished.')

    measurement_result = sim_result.get_counts(qc)
    print('Simulation result:', measurement_result)
    qk.visualization.plot_histogram(measurement_result).savefig('local_sim.png')
    print('Simulation plotted and saved locally.')

def leastBusy_device_exp(qc):
    print('Experiment started.')
    print('Loading account...')
    qk.IBMQ.load_account()
    print('Account loaded')
    print('Finding backend...')
    provider = qk.IBMQ.get_provider(hub='ibm-q')
    backend = qk.providers.ibmq.least_busy(provider.backends(filters=lambda x:
        x.configuration().n_qubits >= 2 and
        not x.configuration().simulator and 
        x.status().operational==True))
    print('Using backend:', backend)
    print('Job started.')
    job = qk.execute(qc, backend=backend, shots=shots)
    qk.tools.monitor.job_monitor(job)
    result = job.result()
    result_count = result.get_counts()
    print('Result:', result_count)
    qk.visualization.plot_histogram(result_count).savefig('exp_result.png')
    print('Result plotted and saved locally.')
    accuracy = result_count[bits]/float(shots)
    print('Accuracy:', accuracy)

        

if __name__ == "__main__":
    leastBusy_device_exp(build_circuit())
    
