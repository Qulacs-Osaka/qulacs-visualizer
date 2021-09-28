from qulacs import QuantumCircuit

def _generate_latex_source(circuit) -> str:
    gate_dict = {"I" : r"\gate{I}",
                "X" : r"\gate{X}",
                "Y" : r"\gate{Y}",
                "Z" : r"\gate{Z}",
                "H" : r"\gate{H}",
                "S" : r"\gate{S}",
                "Sdag"     : r"\gate{S^\dag}",
                "T"        : r"\gate{T}",
                "Tdag"     : r"\gate{T^\dag}",
                "sqrtX"    : r"\gate{\sqrt{X}}",
                "sqrtXdag" : r"\gate{\sqrt{X^\dag}}",
                "sqrtY"    : r"\gate{\sqrt{Y}}",
                "sqrtYdag" : r"\gate{\sqrt{Y^\dag}}",
                "Projection-0" : r"\gate{P0}",
                "Projection-1" : r"\gate{P1}",
                "U1" : r"\gate{U1}",
                "U2" : r"\gate{U2}",
                "U3" : r"\gate{U3}",
                "X-rotation" : r"\gate{RX}",
                "Y-rotation" : r"\gate{RY}",
                "Z-rotation" : r"\gate{RZ}",
                "Pauli" : r"\gate{Pauli}",
                "Pauli-rotation" : r"\gate{PR}",
                "CZ" : r"\gate{CZ}",
                "CNOT" : r"\targ",
                "SWAP" : r"\gate{SWAP}",
                "Reflection" : r"\gate{Ref}",
                "ReversibleBoolean" : r"\gate{ReB}",
                "DenseMatrix" : r"\gate{DeM}",
                "DinagonalMatrix" : r"\gate{DiM}",
                "SparseMatrix" : r"\gate{SpM}",
                "Generic gate" : r"\gate{GeG}",
                "ParametricRX" : r"\gate{pRX}",
                "ParametricRY" : r"\gate{pRY}",
                "ParametricRZ" : r"\gate{pRZ}",
                "ParametricPauliRotation" : r"\gate{pPR}"
                }
    depth = circuit.calculate_depth()
    qubit_count = circuit.get_qubit_count()

    gate_latex = [[r"\nghost{ {q}_{"+str(i)+r"} : }",r"\lstick{ {q}_{"+str(i)+r"} :  }"] for i in range(qubit_count)]
    gate_latex_part = [r"\qw" for _ in range(qubit_count)]

    gate_num = circuit.get_gate_count()
    for i in range(gate_num):
        gate = circuit.get_gate(i)
        if len(gate.get_target_index_list())==0:
            print("CAUTION: The {}-th Gate you added is skipped. This gate does not have \"target_qubit_list\".".format(i))
            continue
        target_index_list = gate.get_target_index_list()
        control_index_list = gate.get_control_index_list()
        name_latex = gate_dict[gate.get_name()]
        
        if len(control_index_list)>0:
            for qubit in range(qubit_count):
                gate_latex[qubit].append(gate_latex_part[qubit])
                gate_latex_part[qubit] = r"\qw"

            for target_index in target_index_list:
                gate_latex_part[target_index] = name_latex

            target_index = target_index_list[0]
            for control_index in control_index_list:
                gate_latex_part[control_index] = r"\ctrl{"+str(target_index-control_index)+r"}"

            for qubit in range(qubit_count):
                gate_latex[qubit].append(gate_latex_part[qubit])
                gate_latex_part[qubit] = r"\qw"

            continue

        conflict = False
        for target_index in target_index_list:
            if gate_latex_part[target_index] != r"\qw":
                conflict = True
        
        if conflict:
            for qubit in range(qubit_count):
                gate_latex[qubit].append(gate_latex_part[qubit])
                gate_latex_part[qubit] = r"\qw"
        
        for target_index in target_index_list:
            gate_latex_part[target_index] = name_latex
    
    for qubit in range(qubit_count):
        gate_latex[qubit].append(gate_latex_part[qubit])
        gate_latex[qubit].append(r"\qw")
    
    circuit_latex_part = [" & ".join(gate_latex[i]) for i in range(qubit_count)]
    circuit_latex = (r" \\"+"\n").join(circuit_latex_part)


    res = r'''\documentclass[border=2px]{standalone}
    \usepackage[braket, qm]{qcircuit}
    \usepackage{graphicx}

    \begin{document}
    \scalebox{1.0}{
    \Qcircuit @C=1.0em @R=0.2em @!R { \\
    '''
    res+=circuit_latex
    res+=r'''
    \\ }}
    \end{document}
    '''

    return res
