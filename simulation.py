import qiskit as qk

def local_sim(qc, figname='local_sim.svg', printresult=True):
    print('Local simulation started.')
    backend = qk.Aer.get_backend('qasm_simulator') 
    job_sim = qk.execute(qc, backend)
    sim_result = job_sim.result()
    print('Simulation finished.')
    measurement_result = sim_result.get_counts(qc)

    if printresult:
        print('Simulation result:', measurement_result)
        qk.visualization.plot_histogram(measurement_result).savefig(figname)
        print('Simulation plotted and saved locally.')
    return measurement_result

def quantumComputerExp(qc, figname='exp_result.svg', accuracy_func=None,
        usehub='ibm-q', shots=1024, mode='least_busy', printresult=True):

    print('Experiment started.')
    print('Loading account...')
    account = qk.IBMQ.load_account()
    print('Account loaded')

    if mode == 'least_busy':
        print('Finding backend...')
        provider = qk.IBMQ.get_provider(hub=usehub)
        backend = qk.providers.ibmq.least_busy(provider.backends(filters=lambda x:
            x.configuration().n_qubits >= qc.qregs[0].size and
            not x.configuration().simulator and 
            x.status().operational==True))

    elif mode == 'simulate':
        backend = account.get_backend('ibmq_qasm_simulator') 

    else:
        raise Exception('InvalidExpMode')

    print('Using backend:', backend)
    print('Job started.')
    job = qk.execute(qc, backend=backend, shots=shots)
    qk.tools.monitor.job_monitor(job)
    result = job.result()
    result_count = result.get_counts()

    if printresult:
        print('Result:', result_count)
        qk.visualization.plot_histogram(result_count).savefig('exp_result.svg')
        if accuracy_func != None:
            print('Accuracy:', accuracy_func(result_count))

    return result_count
 
