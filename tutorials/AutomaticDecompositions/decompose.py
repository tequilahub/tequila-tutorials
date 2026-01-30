import tequila as tq
import networkx as nx

import circuit_with_graph as cg

import ab_circuit as ab 

import abc_circuit as abc

import matplotlib.pyplot as plt
import math
import random
import time

def decompose(H, U):
    """
    Decomposes a Unitary U in (sub) circuits and calculates the Expectation Value in smaller steps.
    """
    unitary_circuits = cg.split_2(U)
    # The Unitary was split into smaller parts for easy calc
    if len(unitary_circuits) > 1:
        exp = ab.calculate_ab(H, unitary_circuits)
        return exp
    
    else: 
        # The Unitary was not splitable
        circuits = cg.split_n(U)
        if len(circuits) == 1:
            print("Could not split the Unitary")
            return tq.ExpectationValue(H=H, U=U)
        
        if len(circuits) == 2:
            A, B = circuits
            C = tq.QCircuit() # test with Identity
            abc.calculate_abc(H, A, B, C)

        if len(circuits) == 3:
            A, B, C = circuits
            abc.calculate_abc(H, A, B, C)

        print("Error: Could not calculate the Expectation Value")
        return None


if __name__ == "__main__":
    """
    Test and draw the Circuits
    """

    max_qubits = 30
    data_classical = list()
    data_easy = list()


    for qubits in range(8, max_qubits+1, 2):
        print("qubits:", qubits)
        grouping = int(qubits/4)
        hamilstring = ""
        hamilstring += ''.join(f"Z({n})" for n in range(qubits))
       

        groups = [list(range(qubits))[i:i + grouping] for i in range(0, qubits, grouping)]
        for group in groups:
            hamilstring += ' + '
            hamilstring += ''.join(f"Z({n})" for n in group)

        U = tq.QCircuit()
        H = tq.QubitHamiltonian(hamilstring)
        print(hamilstring)

        for i in range(0,qubits, grouping):
            angle = random.uniform(0, 2* math.pi)
            U+= tq.gates.CNOT(list(range(i+1, i+grouping)),i) + tq.gates.H(list(range(i+grouping))) + tq.gates.CRy(angle=angle, target=list(range(i+1, i+grouping)), control=i) #+ tq.gates.CRz(angle=angle*3, target=list(range(i+1, i+grouping)), control=i)

        if qubits <= 12:
            start_time = time.time()
            E = tq.ExpectationValue(H=H, U=U)
            val = tq.simulate(E)
            time_needed = time.time() - start_time
            data_classical.append((qubits, time_needed))

        start_time = time.time()
        E = decompose(H=H, U=U)
        val = tq.simulate(E)
        time_needed = time.time() - start_time
        data_easy.append((qubits, time_needed))
        

    data_classical.append((14, 3820))
    qubits_classical, times_classical = zip(*data_classical)
    qubits_easy, times_easy = zip(*data_easy)
    plt.figure(figsize=(10, 6))

    plt.plot(qubits_classical, times_classical, label='Classical', marker='o', linestyle='-', color='blue')
    plt.plot(qubits_easy, times_easy, label='Easy', marker='o', linestyle='--', color='red')

    # Add labels and title
    plt.yscale('log')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Comparison: Classical vs Easy')
    plt.legend()

    # Show grid and plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()




