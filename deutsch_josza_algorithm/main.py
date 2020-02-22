import qiskit as qk
import numpy as np
import sys
sys.path.append('../')
import simulation as sim

# length of the bitstring
n = 4

# function type, b for balanced and ('0'/'1') for constant
oracle = '0'

if oracle == 'b':
    b = np.random.randint(1, 2**n)
    # b = 3

# draw barriers
barriers = True

def build_circuit():
    djcircuit = qk.QuantumCircuit(n+1, n)

    # flip the second register
    djcircuit.x(n)

    if barriers:
        djcircuit.barrier()

    djcircuit.h(range(n+1))

    if barriers:
        djcircuit.barrier()
    
    # oracle

    if oracle == '0':
        djcircuit.iden(n)
    elif oracle == '1':
        djcircuit.x(n)
    elif oracle == 'b':
        # ???
        for i in range(n):
            if (b & (1 << i)):
                djcircuit.cx(i, n)
                print(f'applying: djcircuit.cx({i}, {n})')
    else:
        raise Exception('InvalidFunctionType')
    
    if barriers:
        djcircuit.barrier()

    djcircuit.h(range(n))

    djcircuit.measure(range(n), range(n))

    djcircuit.draw(output='mpl').savefig('circuit.svg')
    print('Circuit built. Image saved locally.')

    return djcircuit

if __name__ == "__main__":
    sim.leastBusy_device_exp(build_circuit())
