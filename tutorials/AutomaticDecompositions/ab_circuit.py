import tequila as tq

import math
import random
import matplotlib.pyplot as plt
import time
from circuit_with_graph import split_2

def calculate_ab(H, circuits):
    """
    Maps Hamiltonian parts to a (sub) cuircuit as a local term or stores the cross terms and
    calculates the Expectation Values with each local and cross term.
    """
    local_terms = []
    cross_terms = []
    constant = 0.0

    for ps in H.paulistrings:
        qubits = ps.qubits
        isCross = True
        if len(qubits) == 0:
            constant += ps.coeff 
            continue

        for circuit in circuits:
            # check if local or cross term
            if set(qubits).issubset(set(circuit.qubits)):       
                local_terms.append((circuit, ps))
                isCross = False
                break 
        if isCross: cross_terms.append(ps)

    exp = float(constant.real)
    exp += calculate_local(local_terms)
    exp += calculate_cross(circuits, cross_terms)      
    return exp


def calculate_local(local_terms):
    """
    Calculates the Expectation Value for the local terms where the list local_terms containts tuples of 
    a (sub) curcuit and the corresponding Pauli-Strings of the Hamiltonian.
    """
    exp = 0.0
    for (circuit, ps) in local_terms:
        H = tq.QubitHamiltonian.from_paulistrings(ps)
        if not all(q in circuit.qubits for q in H.qubits):
            raise Exception("!!!")
        exp +=  tq.ExpectationValue(H=H, U=circuit)
    return exp

def calculate_cross(circuits, cross_terms):
    """
    Calculates the Expectation Value for the cross terms.
    Stores calculation results in dict to avoid the calculation of duplicates.
    """
    all_expvals = {}
    exp = 0.0

    for ps in cross_terms:
        parts = []
        used = {i:False for i in ps.qubits}
        tmp = float(ps.coeff.real)
        for circuit in circuits:
            lc = {}
            for q in ps.qubits:
                if q in circuit.qubits:
                    lc[q] = ps[q]
                    used[q] = True
            parts.append(lc) 

        if not all(used.values()): #not all the paulistrings qubits are being employed --> <0|A|0>
                care = [i for i in used if not used[i]]
                if not all([ps[q] =='Z' for q in care]):# <0|X|0> = <0|Y|0> = 0
                    continue

        for i in range(len(circuits)):
            ui = circuits[i]
            hi = tq.QubitHamiltonian.from_paulistrings(tq.PauliString(parts[i]))
            if len(hi) == 0:
                continue

            key = (str(hi), i)
            if key in all_expvals:
                ei = all_expvals[key]
            else:
                ei = tq.ExpectationValue(H=hi, U=ui)
                all_expvals[key] = ei

            tmp *= ei
        exp += tmp
    return exp


def time_check():
    max_qubits = 30
    data_classical = list()
    data_easy = list()

    U = tq.QCircuit()
    for qubits in range(8, max_qubits+1, 2):
        print(qubits)
        grouping = int(qubits/2)
        hamilstring = ""
        hamilstring += ''.join(f"Z({n})" for n in range(qubits))

        groups = [list(range(qubits))[i:i + grouping] for i in range(0, qubits, grouping)]
        for group in groups:
            hamilstring += ' + '
            hamilstring += ''.join(f"Z({n})" for n in group)

        U = tq.QCircuit()
        H = tq.QubitHamiltonian(hamilstring)

        angle = random.uniform(0, 2* math.pi)
        for i in range(0,qubits, grouping):
            U+= tq.gates.CNOT(list(range(i+1, i+grouping)),i) + tq.gates.H(list(range(i+grouping))) + tq.gates.CRy(angle=angle, target=list(range(i+1, i+grouping)), control=i)

        if qubits <= 28:
            start_time = time.time()
            E = tq.ExpectationValue(H=H, U=U+U)
            val = tq.simulate(E,variables={"psi": angle} )
            print(val)
            time_needed = time.time() - start_time
            data_classical.append((qubits, time_needed))


        circs= split_2(U+U)

        start_time = time.time()
        E = calculate_ab(H=H, circuits=circs)
        val = tq.simulate(E, variables={"psi": angle})
        print(val)
        time_needed = time.time() - start_time
        data_easy.append((qubits, time_needed))

    data_classical.append((30, 990))
        
    #tq.draw(U+B+U)
    qubits_classical, times_classical = zip(*data_classical)
    qubits_easy, times_easy = zip(*data_easy)
    plt.figure(figsize=(10, 6))

    plt.plot(qubits_classical, times_classical, label='full circuit', marker='o', linestyle='-', color='blue')
    plt.plot(qubits_easy, times_easy, label='decoupled method', marker='o', linestyle='--', color='red')

    # Add labels and title
    plt.yscale('log')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Full circuit vs decoupled circuit - calculation method')
    plt.legend()

    # Show grid and plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    


if __name__ == "__main__":
    #check for correct or time:
    #correct_check()

    time_check()