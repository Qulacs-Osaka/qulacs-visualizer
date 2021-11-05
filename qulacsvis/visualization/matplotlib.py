from typing import List, Tuple

from matplotlib import patches
from matplotlib import pyplot as plt
from qulacs import QuantumCircuit
from typing_extensions import Final
from .circuit_parser import (
    CircuitParser,
    CircuitData,
    GateData,
    GATE_DEFAULT_HEIGHT,
)

GATE_MARGIN_RIGHT = 0.5
GATE_MARGIN_BOTTOM = 0.5
GATE_MARGIN_TOP = 0.5

PORDER_GATE: Final[int] = 5
PORDER_LINE: Final[int] = 3
PORDER_REGLINE: Final[int] = 2
PORDER_GRAY: Final[int] = 3
PORDER_TEXT: Final[int] = 6


class MPLCircuitlDrawer:
    def __init__(self, circuit: QuantumCircuit, *, dpi: int = 72, scale: float = 0.7):
        self._figure = plt.figure(dpi=dpi)
        self._ax = self._figure.add_subplot(111)
        self._ax.set_aspect("equal")
        self._ax.axis("off")

        self._circuit = circuit
        self._parser = CircuitParser(circuit)
        # self._circuit_data = parse_circuit(self._circuit)
        self._circuit_data: CircuitData = self._parser.gate_info
        # 図の描画サイズの倍率
        self._fig_scale_factor = scale

    def draw(self, *, debug: bool = True):  # type: ignore
        if debug:
            self._ax.axis("on")
            self._ax.grid()

        circuit_layer_count = len(self._circuit_data[0])

        circuit_width = (
            sum(self._parser.layer_width) + circuit_layer_count * GATE_MARGIN_RIGHT
        )
        circuit_height = (
            self._parser.qubit_count * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
            - GATE_MARGIN_BOTTOM
        )

        QUBIT_LABEL_AREA = 3
        self._ax.set_xlim(-QUBIT_LABEL_AREA, circuit_width)
        self._ax.set_ylim(
            circuit_height, -GATE_DEFAULT_HEIGHT / 2 - GATE_MARGIN_TOP
        )  # (max, min)にすると吊り下げになる

        fig_width = abs(self._ax.get_xlim()[1] - self._ax.get_xlim()[0])
        fig_heigth = abs(self._ax.get_ylim()[1] - self._ax.get_ylim()[0])
        self._figure.set_size_inches(
            fig_width * self._fig_scale_factor, fig_heigth * self._fig_scale_factor
        )

        for qubit in range(self._parser.qubit_count):
            line_ypos = qubit * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
            self._text(
                -2,
                line_ypos,
                "$q_{" + str(qubit) + "}$",
                fontsize=20,
            )

            self._line(
                (-1, line_ypos),
                (
                    circuit_width - GATE_MARGIN_RIGHT,
                    line_ypos,
                ),
            )

        layer_xpos = 0.0

        for layer in range(circuit_layer_count):
            for qubit in range(self._parser.qubit_count):
                qubit_ypos = qubit * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
                gate = self._circuit_data[qubit][layer]
                if gate["raw_text"] == "ghost":
                    continue
                elif gate["raw_text"] == "wire":
                    continue
                elif gate["raw_text"] == "CNOT":
                    self._cnot(gate, (layer_xpos, qubit_ypos))
                elif gate["raw_text"] == "SWAP":
                    self._swap(gate, (layer_xpos, qubit_ypos))
                elif len(gate["target_bit"]) > 1:
                    self._multi_gate(gate, (layer_xpos, qubit_ypos))
                else:
                    self._gate(gate, (layer_xpos, qubit_ypos))

            layer_xpos += self._parser.layer_width[layer] + GATE_MARGIN_RIGHT

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

    def _gate(self, gate: GateData, xy: Tuple[float, float]) -> None:
        xpos, ypos = xy
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
        self, gate: GateData, xy: Tuple[float, float], multi_gate_size: int
    ) -> None:
        xpos, ypos = xy
        # sizeを持つゲートのy座標の中点を求める
        ypos = (
            ypos
            + (
                ypos
                + (multi_gate_size - 1) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
            )
        ) * 0.5
        multi_gate_height = (
            GATE_DEFAULT_HEIGHT * multi_gate_size
            + GATE_MARGIN_RIGHT * (multi_gate_size - 1)
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

    def _multi_gate(self, gate: GateData, xy: Tuple[float, float]) -> None:
        xpos, ypos = xy

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
        group_x = xpos
        group_y = connected_bit_list[0] * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
        self._gate_with_size(
            multi_gate_data,
            (group_x, group_y),
            len(connected_bit_list),
        )
        # 名前無しで表示
        multi_gate_data["text"] = ""
        for connected_bit_list in connected_group[1:]:
            group_y = connected_bit_list[0] * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
            self._gate_with_size(
                multi_gate_data, (group_x, group_y), len(connected_bit_list)
            )

        ypos = min(gate["target_bit"]) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
        to_ypos = max(gate["target_bit"]) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_BOTTOM)
        self._line((xpos, ypos), (xpos, to_ypos), lw=10, lc="gray")

        self._control_bits(gate["control_bit"], (xpos, ypos))

    def _cnot(self, gate: GateData, xy: Tuple[float, float]) -> None:
        xpos, ypos = xy
        TARGET_QUBIT_RADIUS: Final[float] = 0.4

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

    def _swap(self, gate: GateData, xy: Tuple[float, float]) -> None:
        xpos, ypos = xy
        TARGET_QUBIT_MARK_SIZE: Final[float] = 0.1

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
