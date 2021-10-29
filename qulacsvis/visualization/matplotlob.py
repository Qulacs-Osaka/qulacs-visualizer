from qulacs import QuantumCircuit

WID = 0.65
HIG = 0.65


class MatplotlibDrawer:
    def __init__(self, circuit: QuantumCircuit):
        self.qubit_count = circuit.get_qubit_count()
        self.gate_info = [[] for _ in range(self.qubit_count)]
        self.layer_width = []

        self.gate_dict = {
            "I": r"$I$",
            "X": r"$X$",
            "Y": r"$Y$",
            "Z": r"$Z$",
            "H": r"$H$",
            "S": r"$S$",
            "Sdag": r"$S^\dag$",
            "T": r"$T$",
            "Tdag": r"$T^\dag$",
            "sqrtX": r"$\sqrt{X}$",
            "sqrtXdag": r"$\sqrt{X^\dag}$",
            "sqrtY": r"$\sqrt{Y}$",
            "sqrtYdag": r"$\sqrt{Y^\dag}$",
            "Projection-0": r"$P0$",
            "Projection-1": r"$P1$",
            "U1": r"$U1$",
            "U2": r"$U2$",
            "U3": r"$U3$",
            "X-rotation": r"$RX$",
            "Y-rotation": r"$RY$",
            "Z-rotation": r"$RZ$",
            "Pauli": r"$Pauli$",
            "Pauli-rotation": r"$PR$",
            "CZ": r"$CZ$",
            "CNOT": r"$\targ$",
            "SWAP": r"$SWAP$",
            "Reflection": r"$Ref$",
            "ReversibleBoolean": r"$ReB$",
            "DenseMatrix": r"$DeM$",
            "DinagonalMatrix": r"$DiM$",
            "SparseMatrix": r"$SpM$",
            "Generic gate": r"$GeG$",
            "ParametricRX": r"$pRX$",
            "ParametricRY": r"$pRY$",
            "ParametricRZ": r"$pRZ$",
            "ParametricPauliRotation": r"$pPR$",
        }
        self._char_list = {
            " ": (0.0958, 0.0583),
            "!": (0.1208, 0.0729),
            '"': (0.1396, 0.0875),
            "#": (0.2521, 0.1562),
            "$": (0.1917, 0.1167),
            "%": (0.2854, 0.1771),
            "&": (0.2333, 0.1458),
            "'": (0.0833, 0.0521),
            "(": (0.1167, 0.0729),
            ")": (0.1167, 0.0729),
            "*": (0.15, 0.0938),
            "+": (0.25, 0.1562),
            ",": (0.0958, 0.0583),
            "-": (0.1083, 0.0667),
            ".": (0.0958, 0.0604),
            "/": (0.1021, 0.0625),
            "0": (0.1875, 0.1167),
            "1": (0.1896, 0.1167),
            "2": (0.1917, 0.1188),
            "3": (0.1917, 0.1167),
            "4": (0.1917, 0.1188),
            "5": (0.1917, 0.1167),
            "6": (0.1896, 0.1167),
            "7": (0.1917, 0.1188),
            "8": (0.1896, 0.1188),
            "9": (0.1917, 0.1188),
            ":": (0.1021, 0.0604),
            ";": (0.1021, 0.0604),
            "<": (0.25, 0.1542),
            "=": (0.25, 0.1562),
            ">": (0.25, 0.1542),
            "?": (0.1583, 0.0979),
            "@": (0.2979, 0.1854),
            "A": (0.2062, 0.1271),
            "B": (0.2042, 0.1271),
            "C": (0.2083, 0.1292),
            "D": (0.2312, 0.1417),
            "E": (0.1875, 0.1167),
            "F": (0.1708, 0.1062),
            "G": (0.2312, 0.1438),
            "H": (0.225, 0.1396),
            "I": (0.0875, 0.0542),
            "J": (0.0875, 0.0542),
            "K": (0.1958, 0.1208),
            "L": (0.1667, 0.1042),
            "M": (0.2583, 0.1604),
            "N": (0.225, 0.1396),
            "O": (0.2354, 0.1458),
            "P": (0.1812, 0.1125),
            "Q": (0.2354, 0.1458),
            "R": (0.2083, 0.1292),
            "S": (0.1896, 0.1188),
            "T": (0.1854, 0.1125),
            "U": (0.2208, 0.1354),
            "V": (0.2062, 0.1271),
            "W": (0.2958, 0.1833),
            "X": (0.2062, 0.1271),
            "Y": (0.1833, 0.1125),
            "Z": (0.2042, 0.1271),
            "[": (0.1167, 0.075),
            "\\": (0.1021, 0.0625),
            "]": (0.1167, 0.0729),
            "^": (0.2521, 0.1562),
            "_": (0.1521, 0.0938),
            "`": (0.15, 0.0938),
            "a": (0.1854, 0.1146),
            "b": (0.1917, 0.1167),
            "c": (0.1646, 0.1021),
            "d": (0.1896, 0.1188),
            "e": (0.1854, 0.1146),
            "f": (0.1042, 0.0667),
            "g": (0.1896, 0.1188),
            "h": (0.1896, 0.1188),
            "i": (0.0854, 0.0521),
            "j": (0.0854, 0.0521),
            "k": (0.1729, 0.1083),
            "l": (0.0854, 0.0521),
            "m": (0.2917, 0.1812),
            "n": (0.1896, 0.1188),
            "o": (0.1833, 0.1125),
            "p": (0.1917, 0.1167),
            "q": (0.1896, 0.1188),
            "r": (0.125, 0.0771),
            "s": (0.1562, 0.0958),
            "t": (0.1167, 0.0729),
            "u": (0.1896, 0.1188),
            "v": (0.1771, 0.1104),
            "w": (0.2458, 0.1521),
            "x": (0.1771, 0.1104),
            "y": (0.1771, 0.1104),
            "z": (0.1562, 0.0979),
            "{": (0.1917, 0.1188),
            "|": (0.1, 0.0604),
            "}": (0.1896, 0.1188),
        }

        gate_info_part = [
            {"raw_text": "wire", "width": WID} for _ in range(self.qubit_count)
        ]
        gate_num = circuit.get_gate_count()

        for i in range(gate_num):
            gate = circuit.get_gate(i)
            if len(gate.get_target_index_list()) == 0:
                print(
                    """CAUTION: The {}-th Gate you added is skipped.\
                    This gate does not have "target_qubit_list".""".format(
                        i
                    )
                )
                continue
            target_index_list = gate.get_target_index_list()
            control_index_list = gate.get_control_index_list()
            gate_name = gate.get_name()
            name_latex = self.gate_dict[gate_name]

            if len(control_index_list) > 0:
                for qubit in range(self.qubit_count):
                    self.gate_info[qubit].append(gate_info_part[qubit])
                    gate_info_part[qubit] = {"raw_text": "wire", "width": WID}

                for target_index in target_index_list:
                    if target_index == target_index_list[0]:
                        gate_info_part[target_index]["raw_text"] = gate_name
                        gate_info_part[target_index]["text"] = name_latex
                        gate_info_part[target_index]["width"] = self.get_text_width(
                            gate_name
                        )
                        gate_info_part[target_index]["height"] = HIG
                        gate_info_part[target_index]["target_bit"] = target_index_list
                        gate_info_part[target_index]["control_bit"] = control_index_list
                    else:
                        gate_info_part[target_index]["width"] = self.get_text_width(
                            gate_name
                        )
                        gate_info_part[target_index]["raw_text"] = "ghost"

                for qubit in range(self.qubit_count):
                    self.gate_info[qubit].append(gate_info_part[qubit])
                    gate_info_part[qubit] = {"raw_text": "wire", "width": WID}

                continue

            conflict = False
            for target_index in target_index_list:
                if gate_info_part[target_index]["raw_text"] != "wire":
                    conflict = True

            if conflict:
                for qubit in range(self.qubit_count):
                    self.gate_info[qubit].append(gate_info_part[qubit])
                    gate_info_part[qubit] = {"raw_text": "wire", "width": WID}

            for target_index in target_index_list:
                if target_index == target_index_list[0]:
                    gate_info_part[target_index]["raw_text"] = gate_name
                    gate_info_part[target_index]["text"] = name_latex
                    gate_info_part[target_index]["width"] = self.get_text_width(
                        gate_name
                    )
                    gate_info_part[target_index]["height"] = HIG
                    gate_info_part[target_index]["target_bit"] = target_index_list
                    gate_info_part[target_index]["control_bit"] = control_index_list
                else:
                    gate_info_part[target_index]["width"] = self.get_text_width(
                        gate_name
                    )
                    gate_info_part[target_index]["raw_text"] = "ghost"
        for qubit in range(self.qubit_count):
            self.gate_info[qubit].append(gate_info_part[qubit])

        self.layer_width = [WID for _ in range(len(self.gate_info))]
        for i in range(len(self.gate_info)):
            for j in range(self.qubit_count):
                self.layer_width[i] = max(
                    self.layer_width[i], self.gate_info[j][i]["width"]
                )

    def get_text_width(self, text: str) -> int:
        width = 0
        if "sqrt" in text:
            width += 0.0583
            text = text.replace("sqrt", "")
        if "dag" in text:
            width += 0.0583
            text = text.replace("dag", "")
        for character in text:
            width += self._char_list[character][1]
        return width
