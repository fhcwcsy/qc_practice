import qiskit as qk
import time
import matplotlib.pyplot as plt

def local_sim(qc, figname='local_sim.svg', printresult=True, shots=1024):
    print('Local simulation started.')
    backend = qk.Aer.get_backend('qasm_simulator') 
    job_sim = qk.execute(qc, backend,shots=shots)
    sim_result = job_sim.result()
    print('Simulation finished.')
    measurement_result = sim_result.get_counts(qc)

    if printresult:
        print('Simulation result:', measurement_result)
        qk.visualization.plot_histogram(measurement_result).savefig(figname)
        print('Simulation plotted and saved locally.')

    return measurement_result

def quantumComputerExp(qc, figname='exp_result.svg', accuracy_func=None,
        shots=1024, mode='least_busy', printresult=True, commentstr=None):

    print('Experiment started.')
    print('Loading account...')
    account = qk.IBMQ.load_account()
    ntu_provider = qk.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal',
            project='default')
    print('Account loaded')

    if mode == 'least_busy':
        print('Finding backend...')
        backend = qk.providers.ibmq.least_busy(ntu_provider.backends(filters=lambda x:
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

    # sort result
    bitlen = qc.cregs[0].size
    result_list = [('{b:0{l}b}'.format(b=i, l=bitlen), 
        result_count.get('{b:0{l}b}'.format(b=i, l=bitlen), 0)) for i in range(2**bitlen)]
    
    with open('exp_data.txt', 'a') as f:
        f.write('\n\n\n')
        f.write('Record start\n')
        f.write('Time: '+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n')
        f.write('Backend: '+backend._configuration.backend_name+'\n')
        f.write('Qubits: '+str(backend._configuration.n_qubits)+'\n')
        f.write('Basis gates: '+', '.join(backend._configuration.basis_gates)+'\n')
        f.write('Shots: '+str(shots)+'\n')
        f.write('Max shots: '+str(backend._configuration.max_shots)+'\n')
        f.write('creg size: '+str(qc.cregs[0].size)+'\n')
        f.write('qreg size: '+str(qc.qregs[0].size)+'\n')
        f.write('\n')
        for b, c in result_list:
            f.write(b+': '+str(c)+'\n')
        f.write('\n')
        f.write('Record end\n')
        f.write('\n\n\n')

    return result_count


def sort_by_key(result):
    bitlen = len(next(iter(result.keys())))
    sorted_result = [('{n:0{b}b}'.format(n=i, b=bitlen), 
        result.get('{n:0{b}b}'.format(n=i, b=bitlen), 0)) 
        for i in range(2**bitlen)]
    return sorted_result

def sort_by_prob(result):
    return sorted([(k, result[k]) for k in result.keys()], key=lambda x: x[1], 
            reverse=True)

