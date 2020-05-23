import qiskit as qk
import math
import sys
import qft
sys.path.append('../')
import simulation as sim

def adder(a, b):
    bitlen = math.ceil(math.log2(max(a, b)+1))+1

    a_bin = '{n:0{bit}b}'.format(n=a, bit=bitlen)
    b_bin = '{n:0{bit}b}'.format(n=b, bit=bitlen)

    qreg = qk.QuantumRegister(2*bitlen)
    creg = qk.ClassicalRegister(bitlen)
    qc = qk.QuantumCircuit(qreg, creg)

    qft_qc = qft.qft(bitlen)
    qft_dagger = qft_qc.inverse()


    # initialize

    for i in range(bitlen):
        if a_bin[i] == '1':
            qc.x(i)

    for i in range(bitlen):
        if b_bin[i] == '1':
            qc.x(bitlen+i)

    # first QFT
    qc.append(qft_qc, qargs=qreg[bitlen : 2*bitlen])

    # Add 
    # non-parallel version
    # for i in range(bitlen):
        # for j in range(1, bitlen-i+1):
            # qc.cu1(2*math.pi/(2**j), i+j-1, bitlen+i)
        # qc.barrier()

    # parallel version
    for i in range(1, bitlen+1):
        for j in range(bitlen-i+1):
            qc.cu1(2*math.pi/(2**i), i+j-1, bitlen+j)
        qc.barrier()

    # second QFT
    qc.append(qft_dagger, qargs=qreg[bitlen : 2*bitlen])

    for i in range(bitlen):
        qc.measure(i+bitlen, bitlen-i-1)

    return qc

def phi_add(bitlen, a):

    a_bin = '{n:0{bit}b}'.format(n=a, bit=bitlen)

    qreg = qk.QuantumRegister(bitlen, name='phi_add')
    qc = qk.QuantumCircuit(qreg)

    qft_qc = qft.qft(bitlen)
    qft_dagger = qft_qc.inverse()

    # Non-parallel version
    # add 
    # for i in range(bitlen):
        # for j in range(1, bitlen-i+1):
            # if a_bin[i+j-1] == '1':
                # qc.u1(2*math.pi/(2**j), i)
        # qc.barrier()
    
    # parallel version
    for i in range(1, bitlen+1):
        for j in range(bitlen-i+1):
            if a_bin[i+j-1] == '1':
                qc.u1(2*math.pi/(2**i), j)

    return qc

def c_phi_add(bitlen, a):
    controls = qk.QuantumRegister(1, name='control')
    qc = phi_add(bitlen, a)
    qc.add_register(controls)
    qc.qregs.reverse() # make control bits the first two qubits

    qc = qk.aqua.utils.controlled_circuit.get_controlled_circuit(qc, controls[0])

    gate = qc.to_gate()
    gate.name = f'cPhiAdd{a}'

    return gate

def cc_phi_add_a(bitlen, a):
    controls = qk.QuantumRegister(2, name='control')
    qc = phi_add(bitlen, a)
    qc.add_register(controls)
    qc.qregs.reverse() # make control bits the first two qubits

    qc = qk.aqua.utils.controlled_circuit.get_controlled_circuit(qc, controls[0])
    qc = qk.aqua.utils.controlled_circuit.get_controlled_circuit(qc, controls[1])
    # print(qc.draw())
    gate = qc.to_gate()
    gate.name = f'ccPhiAdd{a}'

    return gate


def demonstrate_adder(a, b, mode='sim'):
    if mode == 'sim':
        result = sim.sort_by_prob(sim.local_sim(adder(a, b), printresult=False))
        ans = int(result[0][0], 2)
        print(ans)
        print(ans == a+b)
    elif mode == 'exp':
        simresult = sim.quantumComputerExp(adder(a, b), printresult=True, shots=8192)
        probsort = sim.sort_by_prob(simresult)
        keysort = sim.sort_by_key(simresult)

        l1 = len(probsort)
        l2 = len(keysort)
        
        print('sorted by probability')
        for i in range(l1):
            print(i, probsort[i])
        print('sorted by keys')
        for i in range(l2):
            print(i, keysort[i])
    else: 
        raise Exception('InvalidMode')



if __name__ == "__main__":
    demonstrate_adder(1, 1, mode='exp')
