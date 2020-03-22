import qiskit as qk
import math
import sys
import qft
sys.path.append('../')
import simulation as sim
import os

def adder(a, b):
    required_bits = math.ceil(math.log2(max(a, b)+1))+1

    a_bin = '{n:0{bit}b}'.format(n=a, bit=required_bits)
    b_bin = '{n:0{bit}b}'.format(n=b, bit=required_bits)

    qreg = qk.QuantumRegister(2*required_bits)
    creg = qk.ClassicalRegister(required_bits)
    qc = qk.QuantumCircuit(qreg, creg)

    qft_qc = qft.qft(required_bits)
    qft_dagger = qft_qc.inverse()


    # initialize

    for i in range(required_bits):
        if a_bin[i] == '1':
            qc.x(i)

    for i in range(required_bits):
        if b_bin[i] == '1':
            qc.x(required_bits+i)

    # first QFT
    qc.append(qft_qc, qargs=qreg[required_bits : 2*required_bits])

    # add 
    for i in range(required_bits):
        for j in range(1, required_bits-i+1):
            qc.cu1(2*math.pi/(2**j), i+j-1, required_bits+i)
        qc.barrier()


    # second QFT
    qc.append(qft_dagger, qargs=qreg[required_bits : 2*required_bits])

    for i in range(required_bits):
        qc.measure(i+required_bits, required_bits-i-1)
    print(qc.draw())
    qc.draw(output='mpl').savefig('draperadder_circuit.svg')
    return qc

def phi_add(bitlen, a):

    a_bin = '{n:0{bit}b}'.format(n=a, bit=bitlen)

    qreg = qk.QuantumRegister(bitlen, name='phi_add')
    qc = qk.QuantumCircuit(qreg)

    qft_qc = qft.qft(bitlen)
    qft_dagger = qft_qc.inverse()

    # first QFT
    # qc.append(qft_qc, qargs=qreg)

    # add 
    for i in range(bitlen):
        for j in range(1, bitlen-i+1):
            if a_bin[i+j-1] == '1':
                qc.u1(2*math.pi/(2**j), i)
        # qc.barrier()

    # qc2 = qk.QuantumCircuit(qreg)
    # qc2 = gcc(qc, qreg[0])
     
    # print(qc2.draw())

    # second QFT
    # qc.append(qft_dagger, qargs=qreg)
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


def demonstrate_adder():
    a = 30
    b = 33
    # result = sim.sort_by_prob(sim.local_sim(adder(a, b), printresult=False))
    # ans = int(result[0][0], 2)
    # print(ans)
    # print(ans == a+b)
    simresult = sim.quantumComputerExp(adder(a, b), printresult=True, shots=8192)
    print('sort 1')
    probsort = sim.sort_by_prob(simresult)
    print('sort 2')
    keysort = sim.sort_by_key(simresult)
    print('#################################################')
    print('prob sort')
    l1 = len(probsort)
    l2 = len(keysort)
    print(l1, l2)
    
    for i in range(l1):
        print(i, probsort[i])
    print('key sort')
    for i in range(l2):
        print(i, keysort[i])


if __name__ == "__main__":
    demonstrate_adder()
