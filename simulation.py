import qiskit as qk

def local_sim(qc, figname='local_sim.svg'):
    print('Local simulation started.')
    backend = qk.Aer.get_backend('qasm_simulator') 
    job_sim = qk.execute(qc, backend)
    sim_result = job_sim.result()
    print('Simulation finished.')

    measurement_result = sim_result.get_counts(qc)
    print('Simulation result:', measurement_result)
    qk.visualization.plot_histogram(measurement_result).savefig(figname)
    print('Simulation plotted and saved locally.')

def leastBusy_device_exp(qc, figname='exp_result.svg', accuracy_func=None,
        usehub='ibm-q', shots=1024):
    print('Experiment started.')
    print('Loading account...')
    qk.IBMQ.load_account()
    print('Account loaded')
    print('Finding backend...')
    provider = qk.IBMQ.get_provider(hub=usehub)
    backend = qk.providers.ibmq.least_busy(provider.backends(filters=lambda x:
        x.configuration().n_qubits >= qc.qregs[0].size and
        not x.configuration().simulator and 
        x.status().operational==True))
    print('Using backend:', backend)
    print('Job started.')
    job = qk.execute(qc, backend=backend, shots=shots)
    qk.tools.monitor.job_monitor(job)
    result = job.result()
    result_count = result.get_counts()
    print('Result:', result_count)
    qk.visualization.plot_histogram(result_count).savefig('exp_result.svg')
    if accuracy_func != None:
        print('Accuracy:', accuracy_func(result_count))
 
