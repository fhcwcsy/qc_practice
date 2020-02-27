import qiskit as qk
import math
import sys
sys.path.append('../')
import simulation as sim

t = 4 # of counting qubits
n = 4 # of searching qubits

def build_circuit():
    qreg = qk.QuantumRegister(8) # 4 for counting, 4 for searching
    creg = qk.ClassicalRegister(4) 
    qc = qk.QuantumCircuit(qreg, creg)

    def example_grover_iteration():
        # a circuit with 5/16 solutions
        cccx = qk.aqua.circuits.gates.multi_control_toffoli_gate._cccx
        q = qk.QuantumRegister(4)
        qc = qk.QuantumCircuit(q)

        # Oracle
        qc.h(3)
        cccx(qc, q)
        qc.x(0)
        cccx(qc, q)
        qc.x(0)
        qc.x(1)
        cccx(qc, q)
        qc.x(1)
        qc.x(2)
        cccx(qc, q)
        qc.x(2)
        qc.x(1)
        qc.x(2)
        cccx(qc, q)
        qc.x(2)
        qc.x(1)
        qc.h(3)
        # Diffusion Operator
        qc.z(3)
        for qubit in q[:3]:
            qc.h(qubit)
            qc.x(qubit)
        cccx(qc, q)
        for qubit in q[:3]:
            qc.x(qubit)
            qc.h(qubit)
        qc.z(3)
        return qc
    
    # Create controlled-grover
    grit = example_grover_iteration().to_gate()
    cgrit = grit.control()

    def qft(n):
        # n-qubit qft on q in circ.
        q = qk.QuantumRegister(n)
        qc = qk.QuantumCircuit(q)
        for j in range(n):
            qc.h(q[j])
            for k in range(j+1, n):
                qc.cu1(math.pi/float(2**(k-j)), q[k], q[j])

        # Swaps!
        for i in range(n//2):
            qc.swap(q[i], q[n-i-1])
        return qc

    qft_dagger = qft(4).to_gate().inverse()

    qc.h(qreg)

    iterations = 1
    for qubit in reversed(qreg[:4]):
        for i in range(iterations):
            qc.append(cgrit, qargs=[qubit]+qreg[4:])
        iterations *= 2

    qc.append(qft_dagger, qargs=qreg[:4])
    qc.measure(qreg[:4], creg)
    qc.draw(output='mpl').savefig('circuit.svg')
    print('Circuit built.')

    return qc

if __name__ == "__main__":
    result = sim.local_sim(build_circuit())
    sorted_result = sorted(result.items(), key=lambda t: t[1], reverse=True)
    measured_int = min([
        int(sorted_result[0][0][::-1], 2), 
        int(sorted_result[1][0][::-1], 2)])
    print('Register output = ', measured_int)

    theta = (measured_int/(2**t))*math.pi*2
    print('theta =', theta)
    N = 2**n
    M = N * (math.sin(theta/2)**2)
    print('No of solutions =', N-M)



