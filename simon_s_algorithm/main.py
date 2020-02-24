import qiskit as qk
import sys
sys.path.append('../')
import simulation as sim

s = '11'
n = len(s)
barriers = True


def build_circuit():
    simonCircuit = qk.QuantumCircuit(n*2)

    simonCircuit.h(range(n))

    if barriers:
        simonCircuit.barrier()

    # Oracle
    # Step 1: copy content
    for i in range(n):
        simonCircuit.cx(i, n+i)

    # Step 2: create mapping
    j = s.find('1')
    if j >= 0:
        for i in range(n):
            if s[i] == '1':
                simonCircuit.cx(j, n+i)

    # Step 3: randomize the function

    if barriers:
        simonCircuit.barrier()

    simonCircuit.h(range(n))
    simonCircuit.measure_all()

    simonCircuit.draw(output='mpl').savefig('circuit.svg')
    print('Circuit built. Circuit image saved locally.')
    
    return simonCircuit

def custom_analysis(result):
    categorized_result = {}
    for measresult in result.keys():
        result_input = measresult[-1:n-1:-1]
        categorized_result[result_input] = (
                categorized_result.get(result_input, 0) + 
                result[measresult])
    print(categorized_result)

    if '1' in s:
        correct = True
        for y in categorized_result.keys():
            ip = 0
            for b in zip(s, y):
                ip += int(b[0])*int(b[1])
            if (ip % 2) :
                correct = False
        if correct:
            print('The result is correct.')
        else:
            print('The result is incorrect.')
    else:
        if len(categorized_result) == 2**n:
            print('The result is correct.')
        else:
            print('The result is incorrect.')

    qk.visualization.plot_histogram(categorized_result).savefig('local_sim.svg')
    
if __name__ == "__main__":
    sim.local_sim(build_circuit())

