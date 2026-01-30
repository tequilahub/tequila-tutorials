import tequila as tq
import networkx as nx


def decompose_unitary(U):
    """
    Deconstructs a Unitary into list of independent sub circuits.
    """
    connections = U.to_networkx()
    qubits = list(nx.connected_components(connections))

    circuits = []
    for c in qubits:
        sub_circuit_gates = [gate for gate in U.gates if all(q in c for q in gate.qubits)]
        sub_circuit = tq.QCircuit(gates=sub_circuit_gates)
        circuits.append(sub_circuit)
    return circuits