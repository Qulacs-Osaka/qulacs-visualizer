from typing import List, Tuple

from matplotlib import patches
from matplotlib import pyplot as plt
from qulacs import QuantumCircuit
from typing_extensions import Final, TypedDict

GATE_DEFAULT_WIDTH = 1
GATE_DEFAULT_HEIGHT = 1
GATE_MARGIN_RIGHT = 0.5


GateData = TypedDict(
    "GateData",
    {
        "text": str,
        "width": float,
        "height": float,
        "raw_text": str,
        "target_bit": List[int],
        "control_bit": List[int],
    },
)
CircuitData = List[List[GateData]]

PORDER_GATE: Final[int] = 5
PORDER_LINE: Final[int] = 3
PORDER_REGLINE: Final[int] = 2
PORDER_GRAY: Final[int] = 3
PORDER_TEXT: Final[int] = 6


class MPLCircuitlDrawer:
    def __init__(self, circuit: QuantumCircuit, *, scale: float = 1.0):
        self._figure = plt.figure()
        self._ax = self._figure.add_subplot(111)
        self._ax.axis("on")
        self._ax.grid()
        self._ax.set_aspect("equal")

        self._circuit = circuit
        self._parser = CircuitParser(circuit)
        # self._circuit_data = parse_circuit(self._circuit)
        self._circuit_data = self._parser.gate_info
        # 図の描画サイズの倍率
        self._fig_scale_factor = scale
        # 図の横幅(1個のゲートサイズ x 1行のゲート数)
        self._fig_width = len(self._circuit_data[0]) * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )
        # 図の縦幅(1個のゲートサイズ x qubit数)
        self._fig_height = self._parser.qubit_count * (
            GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT
        )
        # 比率を保ったまま拡大
        self._figure.set_size_inches(
            self._fig_width * self._fig_scale_factor,
            self._fig_height * self._fig_scale_factor,
        )

    def draw(self):  # type: ignore
        self._ax.set_xlim(-3, self._fig_width)
        self._ax.set_ylim(self._fig_height, -1)  # (max, min)にすると吊り下げになる

        # for col in range(10):
        #     for row in range(10):
        #         self._gate(col,row,0)
        GATE_RIGHT_MARGIN = 0.5
        max_line_length = (
            max([len(line) for line in self._circuit_data])
            * (GATE_DEFAULT_WIDTH + GATE_RIGHT_MARGIN)
            - GATE_RIGHT_MARGIN
        )
        for i, line in enumerate(self._circuit_data):
            line_ypos = i * (GATE_DEFAULT_HEIGHT + GATE_RIGHT_MARGIN)
            self._text(
                -2,
                line_ypos,
                "$q_{" + str(i) + "}$",
                fontsize=20,
            )

            self._line(
                (-1, line_ypos),
                (
                    max_line_length,
                    line_ypos,
                ),
            )

            for j, gate in enumerate(line):
                if gate["raw_text"] == "ghost":
                    continue
                elif gate["raw_text"] == "wire":
                    continue
                elif gate["raw_text"] == "CNOT":
                    self._cnot(gate, i, j)
                elif gate["raw_text"] == "SWAP":
                    self._swap(gate, i, j)
                elif len(gate["target_bit"]) > 1:
                    self._multi_gate(gate, i, j)
                else:
                    self._gate(gate, i, j)

        return self._figure

    def _line(
        self,
        from_xy: Tuple[float, float],
        to_xy: Tuple[float, float],
        lc: str = "k",
        ls: str = "-",
        lw: float = 2.0,
        zorder: int = PORDER_LINE,
    ) -> None:
        from_x, from_y = from_xy
        to_x, to_y = to_xy
        self._ax.plot(
            [from_x, to_x],
            [from_y, to_y],
            color=lc,
            linestyle=ls,
            linewidth=lw,
            zorder=zorder,
        )

    def _text(
        self,
        x: float,
        y: float,
        text: str,
        horizontalalignment: str = "center",
        verticalalignment: str = "center",
        fontsize: int = 13,
        color: str = "k",
        clip_on: bool = True,
        zorder: int = PORDER_TEXT,
    ) -> None:
        self._ax.text(
            x,
            y,
            text,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            fontsize=fontsize * self._fig_scale_factor,
            color=color,
            clip_on=clip_on,
            zorder=zorder,
        )

    def _gate(self, gate: GateData, col: int, row: int) -> None:
        ypos, xpos = col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT), row * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )
        box = patches.Rectangle(
            xy=(xpos - 0.5 * gate["width"], ypos - 0.5 * gate["height"]),
            width=gate["width"],
            height=gate["height"],
            facecolor="w",  # 塗りつぶし色
            edgecolor="k",  # 辺の色
            linewidth=3,
            zorder=PORDER_GATE,
        )
        self._ax.add_patch(box)

        self._text(xpos, ypos, gate["text"])

        self._control_bits(gate["control_bit"], (xpos, ypos))

    def _gate_with_size(
        self, gate: GateData, col: int, row: int, multi_gate_size: int
    ) -> None:
        ypos = (
            col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
            + (col + multi_gate_size - 1) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
        ) * 0.5
        xpos = row * (GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT)
        multi_gate_height = gate["height"] * multi_gate_size + GATE_MARGIN_RIGHT * (
            multi_gate_size - 1
        )
        box = patches.Rectangle(
            xy=(xpos - 0.5 * gate["width"], ypos - 0.5 * multi_gate_height),
            width=gate["width"],
            height=multi_gate_height,
            facecolor="w",
            edgecolor="k",
            linewidth=3,
            zorder=PORDER_GATE,
        )
        self._ax.add_patch(box)

        self._text(xpos, ypos, gate["text"])

    def _multi_gate(self, gate: GateData, col: int, row: int) -> None:
        ypos, xpos = col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT), row * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )
        multi_gate_data: GateData = {
            "text": gate["text"],
            "width": gate["width"],
            "height": gate["height"],
            "target_bit": [],
            "control_bit": [],
            "raw_text": gate["raw_text"],
        }

        gate["target_bit"].sort()
        connected_group = []
        connected_bit_list = []
        for target_bit in gate["target_bit"]:
            if connected_bit_list == []:
                connected_bit_list.append(target_bit)
                continue

            if target_bit - 1 in connected_bit_list:
                connected_bit_list.append(target_bit)
            else:
                connected_group.append(connected_bit_list)
                connected_bit_list = [target_bit]

        connected_group.append(connected_bit_list)

        # 名前付きで表示
        connected_bit_list = connected_group[0]
        self._gate_with_size(
            multi_gate_data, connected_bit_list[0], row, len(connected_bit_list)
        )
        # 名前無しで表示
        multi_gate_data["text"] = ""
        for connected_bit_list in connected_group[1:]:
            self._gate_with_size(
                multi_gate_data, connected_bit_list[0], row, len(connected_bit_list)
            )

        ypos = min(gate["target_bit"]) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
        to_ypos = max(gate["target_bit"]) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
        self._line((xpos, ypos), (xpos, to_ypos), lw=10, lc="gray")

        self._control_bits(gate["control_bit"], (xpos, ypos))

    def _cnot(self, gate: GateData, col: int, row: int) -> None:
        TARGET_QUBIT_RADIUS: Final[float] = 0.4
        ypos, xpos = col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT), row * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )

        if gate["control_bit"] is None:
            raise ValueError("control_bit is None")
        elif gate["control_bit"] == []:
            raise ValueError("control_bit is empty")

        target = patches.Circle(
            xy=(xpos, ypos),
            radius=TARGET_QUBIT_RADIUS,
            fc="w",
            ec="k",
            zorder=PORDER_GATE,
        )
        self._ax.add_patch(target)
        # draw target qubit's "+" mark
        # |
        self._line(
            (xpos, ypos - TARGET_QUBIT_RADIUS),
            (xpos, ypos + TARGET_QUBIT_RADIUS),
            zorder=PORDER_TEXT,
        )
        # -
        self._line(
            (xpos - TARGET_QUBIT_RADIUS, ypos),
            (xpos + TARGET_QUBIT_RADIUS, ypos),
            zorder=PORDER_TEXT,
        )

        self._control_bits(gate["control_bit"], (xpos, ypos))

    def _control_bits(
        self, control_bits: List[int], xy_from: Tuple[float, float]
    ) -> None:
        for control_bit in control_bits:
            to_ypos = control_bit * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
            to_xpos = xy_from[0]

            self._line(
                xy_from,
                (to_xpos, to_ypos),
            )
            ctl = patches.Circle(
                xy=(to_xpos, to_ypos),
                radius=0.2,
                fc="k",
                ec="w",
                linewidth=0,
                zorder=PORDER_GATE,
            )
            self._ax.add_patch(ctl)

    def _swap(self, gate: GateData, col: int, row: int) -> None:
        TARGET_QUBIT_MARK_SIZE: Final[float] = 0.1
        ypos, xpos = col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT), row * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )

        for target_bit in gate["target_bit"]:
            to_ypos = target_bit * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
            self._line(
                (xpos, ypos),
                (xpos, to_ypos),
            )
            # draw target qubit's "x" mark
            # \
            self._line(
                (xpos - TARGET_QUBIT_MARK_SIZE, to_ypos - TARGET_QUBIT_MARK_SIZE),
                (xpos + TARGET_QUBIT_MARK_SIZE, to_ypos + TARGET_QUBIT_MARK_SIZE),
            )
            # /
            self._line(
                (xpos + TARGET_QUBIT_MARK_SIZE, to_ypos - TARGET_QUBIT_MARK_SIZE),
                (xpos - TARGET_QUBIT_MARK_SIZE, to_ypos + TARGET_QUBIT_MARK_SIZE),
            )


def parse_circuit(circuit: QuantumCircuit) -> CircuitData:
    arr: CircuitData = [
        [
            {
                "text": r"$I$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "I",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "text": r"$X$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "X",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "text": r"$Y$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Y",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "text": r"$Z$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Z",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "text": r"$H$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "H",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "text": r"$S$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "S",
                "target_bit": [0],
                "control_bit": [],
            },
        ],
        [
            {
                "text": r"$S^\dagger$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Sdag",
                "target_bit": [1],
                "control_bit": [],
            },
            {
                "text": r"$T$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "T",
                "target_bit": [1],
                "control_bit": [],
            },
            {
                "text": r"$T^\dagger$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Tdag",
                "target_bit": [1],
                "control_bit": [],
            },
        ],
        [
            {
                "text": r"$CNOT$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "CNOT",
                "target_bit": [2],
                "control_bit": [3, 4],
            },
            {
                "text": r"$ghost$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "ghost",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "text": r"$SWAP$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "SWAP",
                "target_bit": [2, 3],
                "control_bit": [],
            },
            {
                "text": r"$DeM$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "DenseMatrix",
                "target_bit": [2, 3, 4],
                "control_bit": [],
            },
            {
                "text": r"$DeM$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "DenseMatrix",
                "target_bit": [2, 4],
                "control_bit": [],
            },
        ],
        [
            {
                "text": r"$ghost$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "ghost",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "text": r"$CNOT$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "CNOT",
                "target_bit": [],
                "control_bit": [2, 4],
            },
            {
                "text": r"$ghost$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "ghost",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [],
    ]
    return arr
