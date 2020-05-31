import qiskit as qk
import sys
sys.path.append('../')
import simulation as sim
import random
import math
import time
import matplotlib.pyplot as plt

from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error 

size = 6
max_gate = 20
shots = 8192
sim_shots = 100000
bename = 'ibmq_almaden'
layout = [9, 8, 7, 6, 5, 10]
account = qk.IBMQ.load_account()
ntu_provider = qk.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal',
        project='default')
backend = ntu_provider.get_backend(bename)

print('setup finished.')

def get_noise(p_meas,p_gate):

    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = depolarizing_error(p_gate, 1)
    error_gate2 = error_gate1.tensor(error_gate1)

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure") # measurement error is applied to measurements
    noise_model.add_all_qubit_quantum_error(error_gate1, ["x"]) # single qubit gate error is applied to x gates
    noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"]) # two qubit gate error is applied to cx gates
        
    return noise_model 

def create_circuits():
    qc_list = []
    for length in range(1, max_gate+1):
        if length < max_gate/3:
            iteration = 10
        elif length < max_gate*2/3:
            iteration = 30
        else:
            iteration = 60
        for j in range(iteration):
            qc = qk.QuantumCircuit(size, size)

            def xwrapper(qc):
                t = random.randint(0, size-1)
                qc.x(t)

            def hwrapper(qc):
                t = random.randint(0, size-1)
                qc.h(t)
            
            def cxwrapper(qc):
                c = random.randint(0, size-1)
                t = random.randint(0, size-1)
                while c == t:
                    t = random.randint(0, size-1)
                qc.cx(c, t)

            def crxwrapper(qc):
                c = random.randint(0, size-1)
                t = random.randint(0, size-1)
                while c == t:
                    t = random.randint(0, size-1)
                k = random.randint(0, 5)
                qc.crx(math.pi/2**k, c, t)
            
            gatelist = [xwrapper, hwrapper, cxwrapper, crxwrapper]

            qc.x(random.sample(list(range(size)), math.ceil(size/2)))

            for i in range(length):
                random.choice(gatelist)(qc)

            for i in range(size):
                qc.measure(i, i)

            transpiled = qk.compiler.transpile(
                    qc, 
                    backend=backend, 
                    initial_layout=layout,
                    optimization_level=3
                    )
            qc_list.append({
                'qc':transpiled, 
                'depth':transpiled.depth()
                })

    
    return qc_list
    
def getans(qc_list):
    simbe = qk.Aer.get_backend('qasm_simulator')
    for qcdata in qc_list:

        simjob = qk.execute(
                qcdata['qc'], 
                backend=simbe, 
                shots=sim_shots,
                optimization_level=0
                )

        qcdata['sim_result'] = simjob.result().get_counts(qcdata['qc'])

def exp(qc_list):
    # noise_model = get_noise(0.01,0.01) 
    onlyqc = [data['qc'] for data in qc_list]
    # backend = ntu_provider.get_backend('ibmq_qasm_simulator')
    backend = qk.Aer.get_backend('qasm_simulator')
    job = qk.execute(
            onlyqc, 
            backend=backend, 
            shots=shots, 
            optimization_level=0,
            noise_model=noise_model 
            )
    qk.tools.monitor.job_monitor(job)

    result = job.result()
    for qcdata in qc_list:
        qcdata['exp_result'] = result.get_counts(qcdata['qc'])
        diff = 0
        for bitstring in qcdata['sim_result']:
            diff += abs(qcdata['exp_result'].get(bitstring, 0) 
                    - qcdata['sim_result'][bitstring] * shots/sim_shots)
            qcdata['error'] = diff/shots
            qcdata['accuracy'] = 1-qcdata['error']

def plotaccuracy(qc_list):
    shorttime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    depth = [data['depth'] for data in qc_list]
    acc = [data['accuracy'] for data in qc_list]
    err = [data['error'] for data in qc_list]
    plt.plot(depth, acc, 'o')
    plt.xlabel('depth')
    plt.ylabel('crude accuracy')
    plt.savefig(f'./results/accuracy_{shorttime}.pdf')
    plt.clf()
    plt.plot(depth, err, 'o')
    plt.xlabel('depth')
    plt.ylabel('crude error')
    plt.savefig(f'./results/error_{shorttime}.pdf')
    with open(f'./results/result.txt_{shorttime}', 'w') as f:
        for data in qc_list:
            f.write(f'{data["depth"]} {data["error"]}\n')
            print(f'{data["depth"]} {data["error"]}')
    

if __name__ == "__main__":
    qclist = create_circuits()
    print('qc ready')
    getans(qclist)
    print('ans ready')
    exp(qclist)
    print('done')
    plotaccuracy(qclist)
    # for qc in qclist:
        # print(qc['error'])
        # print()

