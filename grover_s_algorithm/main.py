import qiskit as qk
import sys
sys.path.append('../')
import simulation as sim

def find_00():
    qr = qk.QuantumRegister(2)
    cr = qk.ClassicalRegister(2)

    groverCircuit = qk.QuantumCircuit(qr, cr)

    groverCircuit.x(qr)
    groverCircuit.cz(qr[0], qr[1])
    groverCircuit.x(qr)

    groverCircuit.h(qr)

    groverCircuit.z(qr)
    groverCircuit.cz(qr[0], qr[1])
    groverCircuit.h(qr)

    groverCircuit.draw(output='mpl').savefig('find00_circuit.svg')

    return groverCircuit

def find_101_110():

    def phase_oracle(circuit, register):
        circuit.cz(qr[2], qr[0])
        circuit.cz(qr[2], qr[1])

    def n_controlled_z(circuit, controls, target):
        if (len(controls) > 2):
            raise ValueError('The controlled Z with more than 2 controls is not\
                    implemented')
        elif (len(controls) == 1):
            circuit.h(target)
            circuit.cx(controls[0], target)
            circuit.h(target)
        elif (len(controls) == 2):
            circuit.h(target)
            circuit.ccx(controls[0], controls[1], target)
            circuit.h(target)
 

    def inversion_about_average(circuit, register, n):
        circuit.h(register)
        circuit.x(register)

        circuit.barrier()

        n_controlled_z(circuit, [register[j] for j in range(n-1)], register[n-1])

        circuit.barrier()
        
        circuit.x(register)
        circuit.h(register)

    qr = qk.QuantumRegister(3)
    cr = qk.ClassicalRegister(3)

    groverCircuit = qk.QuantumCircuit(qr, cr)
    groverCircuit.h(qr)

    groverCircuit.barrier()

    phase_oracle(groverCircuit, qr)

    groverCircuit.barrier()

    inversion_about_average(groverCircuit, qr, 3)

    groverCircuit.barrier()

    groverCircuit.measure_all()
    
    return groverCircuit



if __name__ == "__main__":
    sim.local_sim(find_101_110())
