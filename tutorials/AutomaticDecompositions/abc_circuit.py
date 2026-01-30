import tequila as tq
import math
import random
import matplotlib.pyplot as plt
import time

from circuit_with_graph import split_2
import ab_circuit as ab


def convert_to_pauli(U: tq.gates.ExpPauli):
    """
    Converts an Exponential Pauli U of form e^(-i*angle/2 *P) to: angle and PauliGate P.

    Restrictions:
    - only one or no angle allowed
    """

    map = U.make_parameter_map()

    angle_parameters = list(map.keys())

    if len(angle_parameters) > 1 or len(U.gates) > 1:
        return None

    if len(angle_parameters) == 0:
        angle = None
    else:
        angle = tq.Variable(angle_parameters[0])

    return angle, tq.gates.PauliGate(U.gates[0].paulistring)


def calculate_abc(H, A, B, C):
    """
    Calculates the Expectation Value for the given Hamiltonian H and the Unitary U = A*B*C
    with the ABC-Formula.
    """
    # Do the decomposition
    psi, P = convert_to_pauli(B)
    ac_up, ac_down = split_2(A+C)
    apc_up, apc_down = split_2(A+P+C)

    # Calculation of every part:
    a = (0.5*psi).apply(tq.numpy.cos)
    b = (0.5*psi).apply(tq.numpy.sin)
    
    a_term = ab.calculate_ab(circuits=[ac_up, ac_down], H=H) #before tq.ExpectationValue(H=H, U=A+C) / A+P+C
    b_term = ab.calculate_ab(circuits=[apc_up, apc_down], H=H)

    local_term = (a**2) * a_term + (b**2) * b_term 

    _, img = small_braket(ac_up, ac_down, apc_up, apc_down, H)
    cross_term = 2*a*b*(img)

    return local_term + cross_term

def small_braket(bra_up, bra_down, ket_up, ket_down, H):
    """
    Calculates Overlap of the form <|(AC)^{\dagger} H APC|> or <|(ACP)^{\dagger} H AC|>.
    Assumes A and C to be horizontally splitable.
    """
    result_r = 0
    result_i = 0
    for ps in H.paulistrings:
        up_ps = {}
        down_ps = {}
        for p in ps.qubits:
            if p in ket_up.qubits or p in bra_up.qubits:
                up_ps[p] = ps[p]
            if p in ket_down.qubits or p in bra_down.qubits:
                down_ps[p] = ps[p]

        coeff = float(ps.coeff.real)
        h_up = tq.QubitHamiltonian.from_paulistrings([tq.PauliString(up_ps)])
        h_down = tq.QubitHamiltonian.from_paulistrings([tq.PauliString(down_ps)])

        a_real, a_img = tq.BraKet(bra=bra_up, ket=ket_up, operator=h_up)
        b_real, b_img = tq.BraKet(bra=bra_down, ket=ket_down, operator=h_down)
        c_real, c_img = tq.BraKet(bra=ket_up, ket=bra_up, operator=h_up)
        d_real, d_img = tq.BraKet(bra=ket_down, ket=bra_down, operator=h_down)

        result_r += 0.5*(a_real*b_real - a_img*b_img) + 0.5*(c_real*d_real - c_img*d_img)

        if len(down_ps) == 0: # Hamiltonian only acts on the upper parts
            result_i += 0.5*a_img + 0.5*c_img
            continue
        if len(up_ps) == 0: # " - lower parts
            result_i += 0.5*b_img + 0.5*d_img
            continue

        result_ac = 0.5 * a_img + 0.5 * c_img
        result_bd = 0.5 * b_img + 0.5 * d_img
        result_i += coeff * (result_ac * result_bd)

    return result_r, result_i


def small_braket_custom(A, B, C, H):
    """
    Calculates Overlap of the form <|(AC)^{\dagger} H APC|> or <|(ACP)^{\dagger} H AC|>.
    Assumes A and C to be horizontally splitable.
    """
    psi, P = convert_to_pauli(B)
    bra_up, bra_down = split_2(A+C)
    ket_up, ket_down = split_2(A+P+C)


    result_r = 0
    result_i = 0
    for ps in H.paulistrings:
        up_ps = {}
        down_ps = {}
        for p in ps.qubits:
            if p in ket_up.qubits or p in bra_up.qubits:
                up_ps[p] = ps[p]
            if p in ket_down.qubits or p in bra_down.qubits:
                down_ps[p] = ps[p]

        coeff = float(ps.coeff.real)
        h_up = tq.QubitHamiltonian.from_paulistrings([tq.PauliString(up_ps)])
        h_down = tq.QubitHamiltonian.from_paulistrings([tq.PauliString(down_ps)])

        a_real, a_img = tq.BraKet(bra=bra_up, ket=ket_up, operator=h_up)
        b_real, b_img = tq.BraKet(bra=bra_down, ket=ket_down, operator=h_down)
        c_real, c_img = tq.BraKet(bra=ket_up, ket=bra_up, operator=h_up)
        d_real, d_img = tq.BraKet(bra=ket_down, ket=bra_down, operator=h_down)

        result_r += 0.5*(a_real*b_real - a_img*b_img) + 0.5*(c_real*d_real - c_img*d_img)

        if len(down_ps) == 0: # Hamiltonian only acts on the upper parts
            result_i += 0.5*a_img + 0.5*c_img
            continue
        if len(up_ps) == 0: # " - lower parts
            result_i += 0.5*b_img + 0.5*d_img
            continue

        result_ac = 0.5 * a_img + 0.5 * c_img
        result_bd = 0.5 * b_img + 0.5 * d_img
        result_i += coeff * (result_ac * result_bd)

    return result_r, result_i


# -----------------------------------------Testing---------------------------------------------------------

def correct_check():
    data = []
    num = 10

    H = tq.QubitHamiltonian("Z(0)Z(1) + 3.0Z(0)Z(1)Z(2)Z(3) + 3.0Z(2)Z(3) + 3.0X(0)X(1)X(2)X(3)")

    A = tq.gates.H(0) + tq.gates.CRz(0,1, angle="psi") + tq.gates.Ry(angle=2, target=1, control=0) + tq.gates.H(2)
    C = tq.gates.H(0) + tq.gates.CNOT(0,1) + tq.gates.Ry(angle=2, target=1, control=0) + tq.gates.H(2)

    #B = tq.gates.Ry(angle="psi", target=1) + tq.gates.Ry(angle="psi", target=2)
    B = tq.gates.ExpPauli(paulistring="Y(1)Y(2)", angle="psi")

    #tq.draw(A+B+C)

    for i in range(num): # check for some angles
        angle = random.uniform(0, 4* math.pi) # 4 pi because everything is angle/2

     
        E = tq.ExpectationValue(H=H, U=A+B+C)
        actual = tq.simulate(E,  variables={"psi": angle})


        ourValue = calculate_abc(H, A, B, C)
        our = tq.simulate(ourValue, variables={"psi": angle})

        data.append((angle, actual - our))

    x_values, y_values = zip(*data)
    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, color='blue', s=7,label='Data Points')

    plt.xlabel("'Angle for psi")
    plt.ylabel('Error of Expectation Value against tequila calc')
    plt.title('Error Detail of our Calc-Method')
    plt.legend()
    plt.grid(True)

    if abs(max(y_values)) < 0.1: # otherwise we are Zoomed in to much
        plt.ylim(-1, 1)

    plt.show()


def time_check():
    max_qubits = 10
    data_classical = list()
    data_easy = list()

    U = tq.QCircuit()
    B = tq.QCircuit()
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
        print(H)

        angle = random.uniform(0, 2* math.pi)
        for i in range(0,qubits, grouping):
            U+= tq.gates.H(list(range(i+grouping))) +  tq.gates.CNOT(list(range(i+1, i+grouping)),i) + tq.gates.CRy(angle=angle, target=list(range(i+1, i+grouping)), control=i)

        ps = f"Y({grouping-1})Y({grouping})"
        B = tq.gates.ExpPauli(paulistring=ps, angle="psi")

        if qubits <= 28:
            start_time = time.time()
            E = tq.ExpectationValue(H=H, U=U+B+U)
            val = tq.simulate(E,variables={"psi": angle} )
            print(val)
            time_needed = time.time() - start_time
            data_classical.append((qubits, time_needed))

        start_time = time.time()
        E = calculate_abc(H=H, A=U, B=B, C=U)
        val = tq.simulate(E, variables={"psi": angle})
        print(val)
        time_needed = time.time() - start_time
        data_easy.append((qubits, time_needed))
        
    tq.draw(U+B+U)

    qubits_classical, times_classical = zip(*data_classical)
    qubits_easy, times_easy = zip(*data_easy)
    plt.figure(figsize=(10, 6))

    plt.plot(qubits_classical, times_classical, label='full circuit', marker='o', linestyle='-', color='blue')
    plt.plot(qubits_easy, times_easy, label='Weakly coupled method', marker='o', linestyle='--', color='red')

    # Add labels and title
    plt.yscale('log')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Classical vs Weakly coupled circuit calculation method')
    plt.legend()

    # Show grid and plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def recursive_test():
    max_qubits = 24
    data_classical = list()
    data_easy = list()

    U = tq.QCircuit()
    B = tq.QCircuit()
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
            U += tq.gates.CNOT(list(range(i+1, i+grouping)),i) + tq.gates.H(list(range(i+grouping))) + tq.gates.CRy(angle=angle, target=list(range(i+1, i+grouping)), control=i)

        ps = f"Y({grouping-1})Y({grouping})"
        B = tq.gates.ExpPauli(paulistring=ps, angle="psi")

        B2 = tq.gates.ExpPauli(paulistring=ps, angle="phi")

        if qubits <= 28:
            start_time = time.time()
            E = tq.ExpectationValue(H=H, U=U+B+U+B2+U)
            val = tq.simulate(E,variables={"psi": angle, "phi": angle/27} )
            time_needed = time.time() - start_time
            data_classical.append((qubits, time_needed))

        start_time = time.time()
        E = deeper_weakly(H=H, A=U, B=B, a=U, b=B2, c=U)
        val = tq.simulate(E, variables={"psi": angle, "phi": angle/27})
        time_needed = time.time() - start_time
        data_easy.append((qubits, time_needed))
        
    #tq.draw(U+B+U)
    data_classical.append((30, 1080))

    qubits_classical, times_classical = zip(*data_classical)
    qubits_easy, times_easy = zip(*data_easy)
    plt.figure(figsize=(10, 6))

    plt.plot(qubits_classical, times_classical, label='full circuit', marker='o', linestyle='-', color='blue')
    plt.plot(qubits_easy, times_easy, label='double weakly coupled method', marker='o', linestyle='--', color='red')

    # Add labels and title
    plt.yscale('log')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Classical vs Double weakly coupled circuit calculation method')
    plt.legend()

    # Show grid and plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()







def deeper_weakly(A, B, a,b,c, H):
    phi, p = convert_to_pauli(b)

    phi_1 = (0.5*phi).apply(tq.numpy.cos)
    phi_2 = (0.5*phi).apply(tq.numpy.sin)

    local_term = (phi_1**2) * calculate_abc(H=H, A=A, B=B, C=a+c) + (phi_2**2) * calculate_abc(H=H, A=A, B=B, C=a+p+c)

    _, img = small_braket_custom(A, B, a+p+c, H)

    cross_term = 2*phi_1*phi_2* img

    return local_term + cross_term



if __name__ == "__main__":
    #check for correct or time:
    correct_check()
    #recursive_test()
    time_check()