import qiskit as qk
import sys
sys.path.append('../')
sys.path.append('../shor_s_algorithm/')
import draper_adder as adder
import qft
import simulation as sim
import random
import math
import time
import matplotlib.pyplot as plt

from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error 

bitlen = 6
bename = 'ibmq_16_melbourne'
layout = [0, 1, 2, 10, 11, 12] # 2*bitlen
shots = 8192
sim_shots = 100
 
account = qk.IBMQ.load_account()
ntu_provider = qk.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal',
        project='default')
backend = ntu_provider.get_backend(bename)
 
print('setup finished.')
 
def get_circuit():
    print('preparing circuits...')
    qc_list = []
    for i in range(1, 4):
        if i <= 3:
            rep = 15
        elif i < 5:
            rep = 8
        else:
            rep = 3

        for j in range(rep):
            x = random.randint(1, i)
            qr = qk.QuantumRegister(bitlen)
            cr = qk.QuantumRegister(bitlen)

            qc = adder.adder(i, x, custombitlen=bitlen)
            # qc.draw(output='mpl')
            # plt.show()
            
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

            print(f'depth of {x}+{i}: {transpiled.depth()}')
            # sim.local_sim(qc)
    print(f'{len(qc_list)} circuits generated.')
    return qc_list

def getans(qc_list):
    print('getting answers...')
    simbe = qk.Aer.get_backend('qasm_simulator')
    for qcdata in qc_list:

        simjob = qk.execute(
                qcdata['qc'], 
                backend=simbe, 
                shots=sim_shots,
                optimization_level=0
                )

        qcdata['sim_result'] = simjob.result().get_counts(qcdata['qc'])

    print('answers prepared.')

def exp(qc_list):
    print('conducting experiment...')

    # noise_model = get_noise(0.01,0.01) 
    onlyqc = [data['qc'] for data in qc_list]
    backend = ntu_provider.get_backend(bename)
    # backend = qk.Aer.get_backend('qasm_simulator')
    job = qk.execute(
            onlyqc, 
            backend=backend, 
            shots=shots, 
            optimization_level=0
            # noise_model=noise_model 
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
            if qcdata['depth'] > 40 and qcdata['error'] > 0.8:
                print(qcdata['sim_result'])
                print(qcdata['exp_result'])
    print('experiments finished.')

def plotaccuracy(qc_list):
    print('plotting...')
    shorttime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    depth = [data['depth'] for data in qc_list]
    acc = [data['accuracy'] for data in qc_list]
    err = [data['error'] for data in qc_list]
    plt.plot(depth, acc, 'o')
    plt.xlabel('depth')
    plt.ylabel('accuracy')
    plt.savefig(f'./results/adder_accuracy_{shorttime}.pdf')
    plt.clf()
    plt.plot(depth, err, 'o')
    plt.xlabel('depth')
    plt.ylabel('error')
    plt.savefig(f'./results/adder_error_{shorttime}.pdf')
    with open(f'./results/adder_result_{shorttime}.txt', 'w') as f:
        for data in qc_list:
            f.write(f'{data["depth"]} {data["error"]}\n')
            print(f'{data["depth"]} {data["error"]}')
    
def get_noise(p_meas,p_gate):
    # for testing only

    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = depolarizing_error(p_gate, 1)
    error_gate2 = error_gate1.tensor(error_gate1)

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure") # measurement error is applied to measurements
    noise_model.add_all_qubit_quantum_error(error_gate1, ["x"]) # single qubit gate error is applied to x gates
    noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"]) # two qubit gate error is applied to cx gates
        
    return noise_model 
 

if __name__ == "__main__":
    qclist = get_circuit()
    getans(qclist)
    exp(qclist)
    plotaccuracy(qclist)
    print('done')
    # for qc in qclist:
        # print(qc['error'])
        # print()

 

