import qiskit as qk
import matplotlib.pyplot as plt 

secret_unitary = 'hz'

print('loading account...')
qk.IBMQ.load_account()

print('getting provider...')
provider = qk.IBMQ.get_provider(hub='ibm-q')

# use NTU hub


# for be in provider.backends():
    # print(be)

def apply_secret_unitary(secret_unitary, qubit, quantum_circuit, dagger):
    functionmap = {
            'x': quantum_circuit.x,
            'y': quantum_circuit.y,
            'z': quantum_circuit.z,
            'h': quantum_circuit.h,
            't': quantum_circuit.t
            }

    if dagger:
        functionmap['t'] = quantum_circuit.tdg
        [functionmap[unitary](qubit) for unitary in secret_unitary]
    else:
        [functionmap[unitary](qubit) for unitary in secret_unitary[::-1]]

def local_sim():
    qc = qk.QuantumCircuit(3, 3)

    # q[0]: qubit to be teleported. Given to Alice after the secret unitary is
    #    applied.
    # q[1]: Alice's second qubit. Her piece of Bell pair.
    # q[2]: Bob's qubit. destination of the teleportation.

    # apply the secret unitary
    apply_secret_unitary(secret_unitary, qc.qubits[0], qc, dagger=False)
    qc.barrier()

    # generate the entangled pair
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # apply the teleportation protocol
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)

    # call Bob the result and Bob apply the corresponding gates
    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.barrier()

    # If the teleportation works, then q[2] = secret_unitary |0>. Therefore
    # we can apply its inverse to recover q[2] = |0>
    apply_secret_unitary(secret_unitary, qc.qubits[2], qc, dagger=True)
    qc.measure(2, 2)

    
    # save circuit image
    qc.draw(output='mpl').savefig('teleportation_circuit_local.png')

    # local simulation

    backend = qk.Aer.get_backend('qasm_simulator')
    job_sim = qk.execute(qc, backend)
    sim_result = job_sim.result()

    measurement_result = sim_result.get_counts(qc)
    print(measurement_result)
    qk.visualization.plot_histogram(measurement_result).savefig(
            'transportation_local_sim.png')

    # c[2] = 0 means our teleportation protocol has worked.

def ibm_sim():

    print('start building circuit...')

    qc = qk.QuantumCircuit(3, 3)

    # q[0]: qubit to be teleported. Given to Alice after the secret unitary is
    #    applied.
    # q[1]: Alice's second qubit. Her piece of Bell pair.
    # q[2]: Bob's qubit. destination of the teleportation.

    # apply the secret unitary
    apply_secret_unitary(secret_unitary, qc.qubits[0], qc, dagger=False)
    qc.barrier()

    # generate the entangled pair
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # apply the teleportation protocol
    qc.cx(0, 1)
    qc.h(0)

    # call Bob the result and Bob apply the corresponding gates
    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.barrier()

    # If the teleportation works, then q[2] = secret_unitary |0>. Therefore
    # we can apply its inverse to recover q[2] = |0>
    apply_secret_unitary(secret_unitary, qc.qubits[2], qc, dagger=True)

    qc.barrier()
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)

    
    print('circuit built.')

    # save circuit image
    qc.draw(output='mpl').savefig('teleportation_circuit_ibm.png')
    print('circuit image saved locally.')
    
    print('preparing backend...')
    backend = qk.providers.ibmq.least_busy(provider.backends(filters=
        lambda b: b.configuration().n_qubits >= 3 and
        not b.configuration().simulator and b.status().operational==True))

    print('using backend:', backend)

    print('job started...')
    job_exp = qk.execute(qc, backend=backend, shots=8192)
    exp_result = job_exp.result()

    print('result obtained.')

    exp_measurement_result = exp_result.get_counts(qc)
    print('result:', exp_measurement_result)
    
    qk.visualization.plot_histogram(exp_measurement_result).savefig(
            'transportation_exp_result.png')
    print('result saved locally.')


    error_rate = ( sum([exp_measurement_result[result] for result in 
        exp_measurement_result.keys() if result[0]=='1']) 
        / sum(list(exp_measurement_result.values())) )
    print('error rate : ', error_rate)


if __name__ == "__main__":
    ibm_sim()
