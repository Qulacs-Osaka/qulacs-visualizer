import dataclasses
from collections import deque
from collections.abc import Sequence
from itertools import chain
from typing import Deque, List, Optional, Tuple

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class ControlQubitInfo:
    index: int
    control_value: int


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class GateData:
    name: str
    target_bits: List[int] = dataclasses.field(default_factory=list)
    control_bit_infos: List[ControlQubitInfo] = dataclasses.field(default_factory=list)

    @property
    def indices(self) -> Tuple[int, ...]:
        return tuple(chain(self.target_bits, (c.index for c in self.control_bit_infos)))

    @property
    def max_index(self) -> int:
        return max(self.indices)

    @property
    def min_index(self) -> int:
        return min(self.indices)


GateDataSeq = Sequence[Sequence[GateData]]


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class CircuitData:
    qubit_count: int
    layer_count: int
    gates: GateDataSeq

    @staticmethod
    def from_gate_sequence(
        gates: Sequence[GateData], qubit_count: Optional[int] = None
    ) -> "CircuitData":
        if qubit_count is None:
            qubit_count = max(g.max_index for g in gates)
        temp_lines: List[Deque[GateData]] = [deque() for _ in range(qubit_count)]
        for gate in gates:
            _align_layers(temp_lines, gate.min_index, gate.max_index)
            for index in range(gate.min_index, gate.max_index + 1):
                line = temp_lines[index]
                if index == gate.target_bits[0]:
                    line.append(gate)
                elif index in gate.target_bits:
                    line.append(GateData("ghost"))
                else:
                    line.append(GateData("wire"))

        _align_layers(temp_lines, 0, qubit_count)
        layer_count = len(temp_lines[0])
        return CircuitData(
            qubit_count=qubit_count,
            layer_count=layer_count,
            gates=[list(queue) for queue in temp_lines],
        )


def _align_layers(
    lines: Sequence[Deque[GateData]], min_line_index: int, max_line_index: int
) -> None:
    """
    Align layer sizes for a specified range of rows.

    Parameters
    ----------
    min_line_index : int
        Minimum row index to be aligned.
    max_line_index : int
        Maximum row index to be aligned.
    """
    if min_line_index > max_line_index:
        min_line_index, max_line_index = max_line_index, min_line_index
    lines = lines[min_line_index : max_line_index + 1]
    layer_counts = [len(queue) for queue in lines]
    max_layer_count = max(layer_counts)

    for queue, layer_count in zip(lines, layer_counts):
        for _ in range(max_layer_count - layer_count):
            queue.append(GateData("wire"))
