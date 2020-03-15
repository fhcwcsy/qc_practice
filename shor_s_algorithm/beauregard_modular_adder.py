import qiskit as qk
import draper_adder
import qft
import math
import sys
sys.path.append('../')
import simulation as sim

def cc_phi_add_a_mod_N(bitlen, a, N):
    # gargs: c, c, x[bitlen], ancilla

    a = a % N
    qreg = qk.QuantumRegister(bitlen+3) 
    qc = qk.QuantumCircuit(qreg)
    ancilla = bitlen+2
    msb = 2

    # prepare gates
    cc_phi_add_a = draper_adder.cc_phi_add_a(bitlen, a)
    phi_add_N = draper_adder.phi_add(bitlen, N).to_gate()
    qft_gate = qft.qft(bitlen)

    qc.append(cc_phi_add_a, qargs=qreg[:-1])
    qc.append(phi_add_N.inverse(), qargs=qreg[2:ancilla])
    qc.append(qft_gate.inverse(), qargs=qreg[2:ancilla])
    qc.cx(msb, ancilla)
    qc.append(qft_gate, qargs=qreg[2:ancilla])
    qc.append(phi_add_N.control(), qargs=[qreg[-1]]+qreg[2:ancilla])
    qc.append(cc_phi_add_a.inverse(), qargs=qreg[:-1])
    qc.append(qft_gate.inverse(), qargs=qreg[2:ancilla])
    qc.x(msb)
    qc.cx(msb, ancilla)
    qc.x(msb)
    qc.append(qft_gate, qargs=qreg[2:ancilla])
    qc.append(cc_phi_add_a, qargs=qreg[:-1])

    qc.draw(output='mpl').savefig('cc_phi_add_mod_N_circuit.svg')
    # print(qc.draw())
    gate = qc.to_gate()
    gate.name = f'ccPhiAdd{a}Mod{N}'
    return gate


def demonstrating_cc_phi_add_a_mod_N(a, b, N, control='11', simulation='local'):
    bitlen = math.ceil(math.log2(max(a+1, b+1)))+1
    print(f'bitlen: {bitlen}')
    modadd = cc_phi_add_a_mod_N(bitlen, a, N)
    qft_gate = qft.qft(bitlen)
    qc = qk.QuantumCircuit(bitlen+3, bitlen)

    # flip controls
    for i in range(2):
        if control[i] == '1':
            qc.x(i)

    a_bin = '{n:0{bit}b}'.format(n=a, bit=bitlen)
    b_bin = '{n:0{bit}b}'.format(n=b, bit=bitlen)

    for i in range(bitlen):
        if b_bin[i] == '1':
            qc.x(i+2)
    
    qc.append(qft_gate, qargs=qc.qregs[0][2:bitlen+2])
    qc.append(modadd, qargs=qc.qregs[0])
    qc.append(qft_gate.inverse(), qargs=qc.qregs[0][2:bitlen+2])
    for i in range(bitlen):
        qc.measure(i+2, bitlen-i-1)
    # print(qc.draw())
    
    if simulation == 'local':
        ans = int(sim.sort_by_prob(sim.local_sim(qc, printresult=False))[0][0], 2)
        print(f'{a}+{b} mod {N} = {ans}, control: {control}')
        print('actual ans:', (a+b)%N)
    elif simulation == 'exp':
        result = sim.sort_by_prob(sim.quantumComputerExp(qc, shots=8192))
        print(result)
    elif simulation == None:
        pass
    else:
        raise Exception('InvalidSimulationMode')



if __name__ == "__main__":
    demonstrating_cc_phi_add_a_mod_N(5, 5, 7, control='11', simulation='local')
    # cc_phi_add_mod_N(4, 2, 5)



