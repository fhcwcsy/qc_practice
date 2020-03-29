import qiskit as qk
import math
import sys
import qft
import beauregard_modular_adder as adder
sys.path.append('../')
import simulation as sim
import extendedEuclideanAlgorithm as euclidalgo

def cmult_a_mod_N(bitlen, a, N):
    qreg = qk.QuantumRegister(2*bitlen+2) # control, x, b, ancilla
    qc = qk.QuantumCircuit(qreg)
    x_msb = 1
    b_msb = bitlen+1
    ancilla = 2*bitlen+1

    # prepare gates
    qft_gate = qft.qft(bitlen)
    adder.cc_phi_add_a_mod_N(bitlen, a, N)

    qc.append(qft_gate, qargs=qreg[b_msb:ancilla])

    for i in range(bitlen):
        qc.append(adder.cc_phi_add_a_mod_N(bitlen, 2**i * a, N), 
                qargs=[qreg[0]]+[qreg[bitlen-i]]+qreg[b_msb:])

    qc.append(qft_gate.inverse(), qargs=qreg[b_msb:ancilla])

    gate = qc.to_gate()
    gate.name = f'cmult{a}mod{N}'
    
    return gate

def cu_a(bitlen, a, N):
    qreg = qk.QuantumRegister(2*bitlen+2) # control, x, b, ancilla
    qc = qk.QuantumCircuit(qreg)
    x_msb = 1
    b_msb = bitlen+1
    ancilla = 2*bitlen+1
    cmulta = cmult_a_mod_N(bitlen, a, N)
    ainv = euclidalgo.egcd(a, N)[1] % N
    # print(ainv)
    cmultainv = cmult_a_mod_N(bitlen, ainv, N)
    qc.append(cmulta, qargs=qreg)

    for i in range(bitlen):
        qc.cswap(0, i+1, bitlen+i+1)

    qc.append(cmultainv.inverse(), qargs=qreg)

    gate = qc.to_gate()
    gate.name = f'cu{a}mod{N}'
    return gate

def demonstrate_cua(x, a, N, c='1', simulation='sim'):
    bitlen = math.ceil(math.log2(N+1))+1 #???
    print(f'bitlen: {bitlen}')
    gate = cu_a(bitlen, a, N)


    qc = qk.QuantumCircuit(2*bitlen+2, 2*bitlen+2)

    # flip control
    if c == '1':
        qc.x(0)

    # initialize
    x_bin = '{n:0{bit}b}'.format(n=x, bit=bitlen)
    for i in range(bitlen):
        if x_bin[i] == '1':
            qc.x(i+1)

    qc.append(gate, qargs=qc.qregs[0])

    for i in range(bitlen*2+2):
        qc.measure(i, bitlen*2+1-i)

    # print(qc.draw())
    if simulation == 'sim':
        full_result = sim.sort_by_prob(
                sim.local_sim(qc, figname='cua_circuit.svg', printresult=False)
                )
        # print(full_result)
        top_result = full_result[0][0]
        if top_result[0] != c:
            raise Exception('ControlBitWasChanged')

        check = int(top_result[bitlen+1:], 2)
        if check > 0:
            raise Exception('AncillaBitNotClean')
        prod = int(top_result[1:bitlen+1], 2)
        print('Calculated result:', prod)
        print('Correct result:', x*a % N)
        
    else:
        raise Exception('UnsupportedSimulationMode')

if __name__ == "__main__":
    demonstrate_cua(4, 5, 7, c='1')

