import tequila as tq
import networkx as nx

def split_2(U):
    """
    Deconstructs a splitable Unitary into list of independent sub circuits.
    If not splitable it will return [U]
    """
    connections = U.to_networkx()
    qubits = list(nx.connected_components(connections))

    circuits = []
    for c in qubits:
        sub_circuit_gates = [gate for gate in U.gates if all(q in c for q in gate.qubits)]
        sub_circuit = tq.QCircuit(gates=sub_circuit_gates)
        circuits.append(sub_circuit)

    return circuits

def split_n(U):
    """
    Tries to Split a Unitary in either 1 (unsplitable), 2 (AB-structure), 
    or 3 parts with ABC structure, where A and C are splitable but B is not.
    """
    A, rest = check_right(tq.QCircuit(gates=U.gates))

    if A is None: # Unitary is not splitable
        return [rest]

    C, rest = check_right(tq.QCircuit(gates=list(reversed(rest.gates))))
    B = tq.QCircuit(gates=list(reversed(rest.gates)))

    if C is None:
        return [A, B] 
    C = tq.QCircuit(gates=list(reversed(C.gates)))

    return [A, B, C]
   
def check_right(U):
    """
    Iterates through a QCircuit unitil it is splitable in reverse order.
    Returns either an Splitable and unsplitable part or None and unsplitable QCircuit.
    """
    test = tq.QCircuit(U.gates)
    seperable = None
    count = len(U.gates)

    while len(test.gates) != 0:
        test.gates.pop()
        count -= 1
        connections = test.to_networkx()
        qubits = list(nx.connected_components(connections))
        
        if(len(qubits) > 1):
            seperable = test
            break
    
    rest = tq.QCircuit(gates=U.gates[count:])

    return seperable, rest

if __name__ == "__main__":
    """
    Test and draw the Circuits
    """

    U = tq.gates.H(0) + tq.gates.CNOT(0,1)
    U+= tq.gates.H(2) + tq.gates.CNOT(2,3)
    U+=tq.gates.H(1) + tq.gates.CNOT(1,2)

    tq.draw(U, backend='circ')
    print('-'*20)
    print('try to split unitary should not work:', split_2(U))

    print('should show splitable A and unsplitable B')
    A, B = split_n(U)
    tq.draw(A, backend='circ')
    print('-'*20)
    tq.draw(B, backend='circ')
    print('-'*20)

    print('\n'*3)

    U+= tq.gates.H(0) + tq.gates.CNOT(0,1)
    U+= tq.gates.H(2) + tq.gates.CNOT(2,3)

    print('C should be circuit (ABC structure)')
    A, B, C = split_n(U)

    tq.draw(A, backend='circ')
    print('-'*20)
    tq.draw(B, backend='circ')
    print('-'*20)
    tq.draw(C, backend='circ')