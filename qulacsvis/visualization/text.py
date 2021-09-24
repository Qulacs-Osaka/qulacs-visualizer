# mypy: ignore-errors
import shutil

import numpy as np

CON_DOT_STYLE = {
    "large": "●",
    "small": "･",
}


def _set_con_dot(dot: str) -> str:
    """
    Set a character to mean control qubit.

    Parameters
    ----------
    dot: str
        dot style "large" or "small"

    Returns
    -------
    str
        dot character
    """
    if dot in CON_DOT_STYLE:
        return CON_DOT_STYLE[dot]
    else:
        return CON_DOT_STYLE["large"]


class _Gate_AA_Generator:
    """qulacsの量子ゲート(QuantumGateBase)を描画するためのクラス"""

    def __init__(self, *, dot: str = "large"):
        # qulacsの対応バージョン:0.2.0
        # 想定のゲートの出力の文字の幅が３文字分なので3文字用のゲートの名前を定義
        self.gate_dict = {
            "I": " I ",
            "X": " X ",
            "Y": " Y ",
            "Z": " Z ",
            "H": " H ",
            "S": " S ",
            "Sdag": "Sdg",
            "T": " T ",
            "Tdag": "Tdg",
            "sqrtX": "sqX",
            "sqrtXdag": "sXd",
            "sqrtY": "sqY",
            "sqrtYdag": "sYd",
            "Projection-0": "P0 ",
            "Projection-1": "P1 ",
            "U1": "U1 ",
            "U2": "U2 ",
            "U3": "U3 ",
            "X-rotation": "RX ",
            "Y-rotation": "RY ",
            "Z-rotation": "RZ ",
            "Pauli": "Pau",
            "Pauli-rotation": "PR ",
            "CZ": "CZ ",
            "CNOT": "CX ",
            "SWAP": "SWP",
            "Reflection": "Ref",
            "ReversibleBoolean": "ReB",
            "DenseMatrix": "DeM",
            "DinagonalMatrix": "DiM",
            "SparseMatrix": "SpM",
            "Generic gate": "GeG",
            "ParametricRX": "pRX",
            "ParametricRY": "pRY",
            "ParametricRZ": "pRZ",
            "ParametricPauliRotation": "pPR",
        }

        # このgate_stringにゲートの上の部分から文字列を作成して追加していきゲートの形を作成
        self.gate_string = []

        # 制御qubitの記号
        self.CON_DOT = _set_con_dot(dot)

    def generate(self, gate, index="   ", verbose=False):
        """引数のゲートを文字列表示で返してくれる関数
        Argeuments:
            gate:    Qulacsのゲート(QuantumGateBase)
            index:   circuitに追加された順番を示す値, 1000以上の場合は表示が崩れる
            verbose: Trueだと詳細出力, 表示されるゲートにcircuitで追加された順番(引数のindex)を表示
        Return:
            gate_string: 1次元のリスト(リストのリスト)
                         1次元目が行の指定, 2次元目が文字の指定

        ゲートの表示法とパーツの説明(CNOTを例に)
        ・大きさは縦8×横7
          0123456       パーツ名                 説明
        0            <= control_q_head       : 制御qubitのときの空白文字
        1            <= control_q_name       : 上に同じ
        2 ---･---    <= control_q_body       : このqubitが制御qubitであることを示す"･"
        3    |       <= vertical_wire        : 制御qubitと接続する縦向きのワイヤー
        4   _|_      <= gate_head            : ゲートの天井
        5  |CX |     <= gate_name            : どのゲートかを表示するゲートの名前と左右の壁
        6 -|   |-    <= gate_body_with_wire  : ゲートの左右の壁, ワイヤーのないものはgate_body
        7  |___|     <= gate_botom           : ゲートの下底

        """
        # ゲートの文字列表現を初期化
        self.gate_string.clear()

        # verboseに応じて回路への追加番号を表示させるかさせないか文字列を作成
        if verbose:
            index = str(index).zfill(3)
        else:
            index = "   "

        # 実際にゲートが適用されるターゲットqubitのリストと, コントロール用の制御qubitのリストを取得
        t_list = gate.get_target_index_list()
        c_list = gate.get_control_index_list()
        # ゲート作成時の引数の順番や, add_control_qubitメソッドなどで
        # 制御qubitを追加したときなどでリストが昇順になっていないことがあるのでソートしておく
        t_list.sort()
        c_list.sort()

        # 制御qubitが実ゲート(ターゲットqubitにかかるゲート)より上に存在するかチェック
        if len(c_list) != 0 and min(t_list) > min(c_list):
            # 制御qubitが実ゲートより上に存在した
            upper = True
            # ターゲットqubitにかかるゲートより上側に存在する制御qubitの部分の文字列表現を作成
            self.gen_upper_control_part(t_list, c_list)
        else:
            # 制御qubitが実ゲートより上に存在しない
            upper = False

        # ターゲットqubitにかかる部分のゲートの文字列表現を作成
        self.gen_target_part(gate, t_list, index, upper)

        # 制御qubitが実ゲートの間に存在するときの制御qubitを描画
        self.gen_inner_control_part(t_list, c_list)

        # 制御qubitが実ゲート(ターゲットqubitにかかるゲート)より下に存在するかチェック
        if len(c_list) != 0 and max(t_list) < max(c_list):
            # ターゲットqubitにかかるゲートより上側に存在する制御qubitの部分の文字列表現を作成
            self.gen_lower_control_part(t_list, c_list)

        return self.gate_string

    def gen_upper_control_part(self, t_list, c_list):
        """ターゲットqubitにかかるゲートより上側に存在する制御qubitを描くメソッド"""
        # 以下制御qubit用のパーツ作り
        # 制御qubit用の部分の形(空)
        control_q_head = "       "
        # 制御qubit用の部分の形(空)
        control_q_name = "       "
        # 制御qubit用の部分の接続の部分の形
        control_q_body = "   {}   ".format(self.CON_DOT)
        # 制御信号用のワイヤーの形
        vertical_wire = "   |   "

        # ターゲットqubitにかかるゲートよりも上側に存在している制御qubitのリスト
        upper_c_list = [i for i in c_list if i < min(t_list)]

        # 制御qubitの回路図を構成していく
        self.gate_string.append(control_q_head)
        self.gate_string.append(control_q_name)
        self.gate_string.append(control_q_body)
        # 制御qubitと実ゲートのqubitでもっとも離れているqubit(実ゲートのqubitは一番上のqubit)を選び
        # 距離を計算. このqubitから下へと縦のワイヤーを引く
        diff = min(t_list) - min(upper_c_list)
        for _ in range(diff * 4 - 3):
            self.gate_string.append(vertical_wire)

        # 制御信号をどのワイヤーからとっているか表す"･"を描き込む
        # 最初の制御qubitは描き込み済みなので２つ目以降の制御qubitから
        for i in upper_c_list[1:]:
            # 制御qubitと実ゲートのかかるqubitで最も近いものとがいくつ離れているか計算
            diff = min(t_list) - i
            # 仕様に合わせて位置を調整
            p = diff * 4 - 2
            # 配列に"･"を描き込み(上書き)
            self.gate_string[-p] = control_q_body

    def gen_target_part(self, gate, t_list, index, upper):
        """ターゲットqubitにかかる部分のゲートの文字列表現を描くメソッド"""
        # ターゲットqubitにかかる部分のゲートの大きさを取得
        # ゲートのかかるqubit同士が離れている場合はその間のqubitも使用すると考えて回路図を描くので,
        # 正確にはゲートのかかるqubitのうち一番上のqubitから一番下のqubitまでの大きさ
        gate_size = max(t_list) - min(t_list) + 1

        # ゲートの上部分の形
        # もしコントロールqubitが実ゲートよりも上にあるとき, つまり上から制御用のワイヤーが入るとき
        # ゲートの上の形は制御の線を接続した形になる
        if upper:
            gate_head = "  _|_  "
        else:
            gate_head = "  ___  "
        # ゲートの名前が表示される部分の形
        try:
            # ゲートの横幅を３文字分で作成しているので,文字をgate_dictから決定
            gate_name = " |{}| ".format(self.gate_dict[gate.get_name()])
        except KeyError:
            # もし新たに追加されたゲートなどで見つからなかったときは"UnDeFined"
            gate_name = " |UDF| "
        # ワイヤー付き, またはついていない部分のゲートの形
        # パラメータ付き回路やDenseMatrixの場合はこの部分にパラメータを入れて表示させたい
        gate_body_with_wire = "-|   |-"
        gate_body = " |   | "
        # ゲートの下部分の形
        gate_bottom = " |___| "

        # 作成を始める
        if gate_name == " |SWP| ":
            # SWAPの時だけ別に描く, どこがスワップするのか少し見にくかったので. 下のelse以下の表示法でも可.
            self.create_SWAP_gate_string(gate_size, t_list, index)
        else:
            # SWAP以外の全てのゲートは以下
            self.gate_string.append(gate_head)  # ゲートの一番頭部分
            self.gate_string.append(gate_name)  # ゲートの種類表示の部分
            self.gate_string.append("-|{}|-".format(index))  # ゲートの追加番号or空白の部分
            for i in range(1, gate_size * 4 - 3):  # 左右の壁の部分を描くループ
                # ((i+2)//4)+(描き始めのqubitのインデックス)は現在いるqubitのインデックス描いているqubitのインデックス
                q_index = (i + 2) // 4 + min(t_list)
                if q_index in t_list:
                    # 現在描いている壁がターゲットqubitのリストの中にあるとき,
                    # つまり, 今描いている壁の部分は実際にゲートが適用されるqubitであるとき
                    # i%4の値でゲートのどの部分を描いているかが分かる(1つのゲートの高さが4なため)
                    if i % 4 == 0:
                        # 余りが0のときは横向きのワイヤーが接続する部分なのでwith_wireを繋ぐ
                        self.gate_string.append(gate_body_with_wire)
                    elif i % 4 == 1:
                        # 余りが1のときはゲートの底部分, または離れたqubitにかかるゲートを描いているときの
                        # 横幅が狭い(1文字分)の壁の部分. どちらかによって描き方が変わる.
                        if q_index + 1 in t_list:
                            # 今描いているqubitのインデックス+1のqubitもゲートがかかるとき,
                            # つまり, 次のqubitもゲートがかかるとき
                            self.gate_string.append(gate_body)  # 3文字分のゲート幅の壁を追加
                        else:
                            # 今描いているqubitのインデックス+1のqubitにはゲートがかからないとき,
                            # つまり, 今描いているのqubitの隣のqubitにはゲートがかからず,
                            # 離れたqubitにゲートがかかるとき(ゲートのかかるqubitが隣接していないとき)
                            self.gate_string.append(
                                " |_ _| "
                            )  # 次のqubitにはかからないことを示すため狭める
                    elif i % 4 == 2:
                        # 余りが2のときはゲートの頭部分, または連続したqubitにかかる多qubitゲートを
                        # 描いているときの3文字分のゲートの壁の部分. どちらかによって描き方が変わる.
                        if q_index - 1 in t_list:
                            # 今描いているqubitの1つ前のqubitにもゲートがかかっていたとき,
                            # つまり, 前のqubitのゲートと連続して今描いているqubitにもゲートがかかるとき
                            self.gate_string.append(gate_body)  # 3文字分のゲート幅の壁を追加
                        else:
                            # 今描いているqubitの1つ前のqubitにはゲートがかかっていなかったとき,
                            # つまり, 前のqubitはゲートのかからないqubitで今描いているqubitが実は
                            # 離れた位置に存在したゲートのかかるqubitのとき
                            self.gate_string.append(
                                " _| |_ "
                            )  # このqubitからゲートがかかることを示すため広げる
                    else:
                        # 余りが3のときはgate_nameにあたる部分だが, 多qubitゲートの場合は描くものがない
                        self.gate_string.append(gate_body)  # 3文字分のゲートの壁を追加

                else:
                    # 現在描いている壁がターゲットqubitのリストの中にないとき,
                    # つまり, 今描いている壁の部分は実際にゲートが適用されないqubitで
                    # もっと下の(離れた位置にある)qubitにかかるゲートを描くための間の部分のqubitのときである.
                    # このときは, 今のqubitにはかかっていないことを見やすくするためにゲートの幅を1文字分に変更したものを表示する
                    if i % 4 == 0:
                        # この位置は横向きのワイヤーを描く部分
                        self.gate_string.append("--| |--")
                    else:
                        # ゲート幅が1文字分になるようのゲートの左右の壁を描く
                        self.gate_string.append("  | |  ")
            self.gate_string.append(gate_bottom)  # ゲートの最も底部分

    def create_SWAP_gate_string(self, gate_size, t_list, index):
        """SWAPゲートをきれいに描くためのメソッド"""
        # ゲートの上部分の形, SWAPは空
        gate_head = "       "
        # ゲートの名前が表示される部分の形, verbose=Trueのときは追加された順番でそれ以外は空
        gate_name = "  {}  ".format(index)
        # SWAPする位置を表す部分. この部分が他のゲートの場合と異なり, "×"が着くのは
        # SWAPする2点のqubitのみでその間のqubitのワイヤーは接続の縦線ワイヤーで描きたい
        swap_body_with_wire = "---x---"
        gate_body_with_wire = "---|---"
        # 右壁と左壁の部分, SWAPの場合はSWAPするqubit同士を繋ぐ縦線のワイヤー
        gate_body = "   |   "
        # ゲートの下部分の形, SWAPは空
        gate_bottom = "       "

        # 作成し始める
        self.gate_string.append(gate_head)  # 頭部分
        self.gate_string.append(gate_name)  # ゲートの種類表示の部分
        self.gate_string.append(swap_body_with_wire)  # SWAPする1つ目のqubitの"×"部分
        for i in range(1, gate_size * 4 - 4):  # 左右の壁の部分
            if i % 4 == 0:
                self.gate_string.append(gate_body_with_wire)
            else:
                self.gate_string.append(gate_body)
        self.gate_string.append(swap_body_with_wire)  # SWAPする2つ目のqubitの"×"部分
        self.gate_string.append(gate_bottom)  # 底部分

    def gen_inner_control_part(self, t_list, c_list):
        """実ゲートが離れたqubitにかかる場合で, 制御qubitがその間にあるときに描くメソッド"""
        # 実ゲートの間に存在している制御qubitのリストを作成
        inner_c_list = [i for i in c_list if i > min(t_list) and i < max(t_list)]

        # 上で作成したリストを基に, 既に作成済みである実ゲートを上書きする(空リストの時はなにもしない)
        for index in inner_c_list:
            # (取得した制御qubitのインデックス)-(実ゲートの一番上のqubit)で描き始めのqubitから
            # 何個下のqubitに描き込めばよいか分かる. この値をゲートの高さ分修正(*4-2)して中央をドットに書き換える
            row = (index + 1 - min(t_list)) * 4 - 2
            self.gate_string[row] = (
                self.gate_string[row][:3] + self.CON_DOT + self.gate_string[row][4:]
            )

    def gen_lower_control_part(self, t_list, c_list):
        """ターゲットqubitにかかるゲートより下側に存在する制御qubitを描くメソッド"""
        # 以下制御qubit用のパーツ作り
        # 制御qubit用の部分の接続の部分の形
        control_q_body = "   {}   ".format(self.CON_DOT)
        # 制御信号用のワイヤーの形
        vertical_wire = "   |   "

        # ターゲットqubitにかかるゲートよりの下側に存在している制御qubitのリスト
        below_c_list = [i for i in c_list if i > max(t_list)]

        # 制御qubitと実ゲートのqubitでもっとも離れているqubit(実ゲートのqubitは一番下のqubit)を選び
        # 距離を計算. このqubitから下へと縦向きのワイヤーを引く
        diff = max(below_c_list) - max(t_list)
        loop = diff * 4 - 1
        for _ in range(loop):
            self.gate_string.append(vertical_wire)

        # 制御信号をどのワイヤーからとっているか表す"･"を描き込む
        for i in below_c_list:
            # 制御qubitとゲートとの距離を計算
            diff = i - max(t_list)
            # 仕様に合わせて位置を調整
            p = diff * 4 - loop - 2
            # 配列に"･"を描き込み(上書き)
            self.gate_string[p] = control_q_body


class TextCircuitDrawer:
    """qulacsの量子回路(QuantumCircuit)を描画するためのクラス"""

    def __init__(self, circuit, *, dot: str = "large"):
        # 制御qubitの記号
        self.CON_DOT = _set_con_dot(dot)
        # 出力したい量子回路
        self.circ = circuit
        # 出力したい量子回路の深さ
        self.depth = circuit.calculate_depth()
        # 出力したい量子回路のqubit数
        self.qubit_num = circuit.get_qubit_count()

        # 量子回路図をできるだけ左詰め(回路が浅くなるよう)に配置するための参照する配列
        # 2次元配列であり要素数は(qubit数)*(回路の深さ) <= 場合により深くなっていく
        # 各qubitのそれぞれの深さにおいてゲートをセットできる場合はTrueを, できない場合はFalseを表示する
        # 例) gate_map = [[False, False, True],  ← 1qubit目
        #                 [False, True,  True],  ← 2qubit目
        #                 [True,  True,  True]]  ← 3qubit目
        #                   ↑      ↑      ↑
        #                  深さ1   深さ2   深さ3
        # 上のgate_mapは
        # ・1qubit目は深さ1と深さ2ですでにゲートが存在している, 次にゲートを適用できるのは深さ3の場所
        # ・2qubit目は深さ1の場所にすでにゲートが存在している, 次にゲートを適用できるのは深さ2の場所
        # ・3qubit目はまだゲートが存在していない, 次にゲートを適用できるのは深さ1の場所
        # を表す
        self.gate_map = np.full((self.qubit_num, self.depth), True)

        # 量子回路の文字列表示を保持させる変数(2次元配列)
        # 要素に文字1文字を割り当て、回路図として表現する方針
        # 大きさは縦が(qubit数×4). 4は1つのゲートの縦幅.
        #       横が(深さ×7)+(深さ-1)+2. 7は1つのゲートの横幅. (深さ-1)は各深さに存在するゲート同士を
        #                              "-"で繋ぐため,その数. +2は回路の左端と右端を"-"1文字で描画するため.
        # 以下イメージ
        #              深さが1と2のゲートの
        #  左端        間のワイヤーの位置       右端
        #   ↓               ↓               ↓
        #   0 1 2 3 4 5 6 7 8 9 A B C D E F 10 (<=16進数表示) ←横サイズ
        # 0       _ _ _
        # 1     |   X   |
        # 2 - - |       | - - - - - ･ - - - -
        # 3     | _ _ _ |           |
        # 4                       _ | _
        # 5                     | D e M |
        # 6 - - - - - - - - - - |       | - -
        # 7                     | _ _ _ |
        # ↑縦サイズ                <=====> ゲートの幅は3文字分, これに前後の壁である"-|", "|-"を
        #                                合わせると１つのゲートの幅は7文字分.

        self.vertical_size = self.qubit_num * 4  # 縦サイズ
        self.horizontal_size = self.depth * 7 + self.depth - 1 + 2  # 横サイズ
        self.circuit_picture = np.full(
            (self.vertical_size, self.horizontal_size), " "
        )  # 配列作成,空白1文字で初期化
        # 量子回路の左端と右端のワイヤーを"-"で描いておく
        for i in range(self.qubit_num):
            # 横向きのワイヤーがある場所は配列番号で2,6,10,14,...番目
            row = (i + 1) * 4 - 2
            self.circuit_picture[row][0] = "-"
            self.circuit_picture[row][-1] = "-"

        # 単体のゲートの文字列表現を作成するクラスを呼び出す
        self.AA_Generator = _Gate_AA_Generator(dot=dot)

    def draw(self, verbose):
        """実際に回路を描き始め出力までするメソッド"""
        # 出力したい量子回路の持つゲート数を取得
        gate_num = self.circ.get_gate_count()
        # ゲートを１つずつ取り出し回路図に描き込んでいく
        for i in range(gate_num):
            gate = self.circ.get_gate(i)
            # 確率的に作用するゲートなどでtarget_qubitのインデックスが無いものはスキップする
            if len(gate.get_target_index_list()) == 0:
                print(
                    f"CAUTION: The {i}-th Gate you added is skipped."
                    + 'This gate does not have "target_qubit_list"'
                )
            else:
                self._draw_gate(gate, index=i, verbose=verbose)

        # ゲートを描き終えたら, ゲート同士や接続が切れているワイヤーを繋ぐ
        self._connect_wire()

        # 描き込まれたゲートを実際に出力する
        # ただし、回路の長さに応じて表示方法を変える
        terminal_size = shutil.get_terminal_size().columns - 1  # プロンプトの1行に表示できる文字数-1
        # プロンプトに収まる場合は普通に表示
        if self.horizontal_size <= terminal_size:
            for line in self.circuit_picture:
                print("".join(line))
        # 回路が長いときは途中で折り返して表示する
        else:
            # 折り返して表示するときの、表示を繰り返す回数
            col = self.horizontal_size // terminal_size
            # 折り返して表示する際の区切り文字。"#"で区切る
            delimiter = "\n" + "#" * terminal_size
            # 回路図のどこまでを表示したか思えておく変数
            plot_range = 0
            # プロンプトの横幅までの表示を繰り返す
            print(delimiter)
            for i in range(col):
                # 今何回目の表示かを出力
                print(">>", i)
                # 回路図の出力
                for line in self.circuit_picture:
                    print("".join(line[plot_range : plot_range + terminal_size]))
                # 表示済みの回路図を記憶
                plot_range += terminal_size
                # 区切りの出力
                print(delimiter)
            # 回路の最後の部分の表示
            print(">>", col)
            for line in self.circuit_picture:
                print("".join(line[plot_range:]))
            print(delimiter)

    def _draw_gate(self, gate, index, verbose):
        """引数にgateをとり, 「ゲートの文字化」, 「適切な位置に描き込み」 の順で実際に描き込むメソッド"""
        # 単一のゲートの文字列表示を作成
        gate_string = self.AA_Generator.generate(gate, index, verbose)

        # 実際にゲートが適用されるターゲットqubitと, コントロール用の制御qubitのリストを取得
        target_qubit_list = gate.get_target_index_list()
        control_qubit_list = gate.get_control_index_list()
        # 続いて, 制御qubitとターゲットqubitの両方を合わせた, 実際にゲートがかかるqubitのリストを取得.
        tc_list = target_qubit_list + control_qubit_list
        # これは例えばCNOT(0,2), X(1)のような回路を描こうとしたとき, 回路の深さは1だがそのまま深さ1で描こうとすると
        # ゲートの追加順に応じて CNOTの制御用ワイヤー上にXゲートが乗ってしまう or Xゲートで縦向きの制御信号の上書き
        # が起こってしまった. よって, 本プログラムでは回路の深さを増やして表示が重ならないようにして対応しようと考えた.
        # 方針として制御qubitとターゲットqubitが離れている場合を想定し, 間にまたがるqubit全てを確保することで実装する.

        # circuit_pictureに描き込むに必要な左上隅のインデックスを取得
        # 引数は使用するqubitのリストの最小値と最大値
        upper_left_corner = self._place_check(min(tc_list), max(tc_list))
        # 作成した文字列表示をircuit_pictureに描き込む
        self._write_gate_on_picture(gate_string, upper_left_corner)

    def _place_check(self, min_v, max_v):
        """適切なゲートの描き込み位置を計算するメソッド"""
        # 回路の浅い所から探索
        for i in range(self.depth):
            # 使用したいqubitすべてが利用できるかチェック
            if all(self.gate_map[min_v : max_v + 1, i]):
                # 現在使うqubitの位置をFalseに変更する
                # このときTrueの場所(ゲートのかかる場所)より左側も全部Falseにする
                # そうしておかないと, 左詰めで適用する実装になっているので
                # 後から適用する1qubitゲートがその前にかかってしまったりする
                self.gate_map[min_v : max_v + 1, : i + 1] = False
                # 最終的に作成する２次元配列で考えた場合のqubitの位置・深さを計算するため
                # gate_mapの場合の計算結果を変数に保持させて終了する
                col = i
                break

            # 一番深いとこまで探索したのに, 描き込める場所が見つからなかったとき
            elif i + 1 == self.depth:
                # gate_mapとcircuit_pictureを拡張する
                self._expand_map_and_picture()
                # 追加した場所にゲートを割り当てていく
                self.gate_map[min_v : max_v + 1, : i + 2] = False
                col = i + 1

        # 仕様(２次元配列)に合わせて位置を調整
        row = min_v * 4
        col = col * 8 + 1

        return row, col

    def _expand_map_and_picture(self):
        """回路図が重なって表示されないように深さを増やすメソッド"""
        # self.gate_mapの拡張
        additional_gate_map = np.full(self.qubit_num, True).reshape(self.qubit_num, 1)
        self.gate_map = np.concatenate([self.gate_map, additional_gate_map], axis=1)

        # self.circuit_pictureを拡張
        additional_circuit_pic = np.full((self.vertical_size, 8), " ")
        self.circuit_picture = np.concatenate(
            [self.circuit_picture, additional_circuit_pic], axis=1
        )
        # 右端を"-"でセット
        for i in range(self.qubit_num):
            # 横向きのワイヤーがある場所は配列番号で2,6,10,14,...番目
            row = (i + 1) * 4 - 2
            self.circuit_picture[row][-1] = "-"

        # 深さを+1
        self.depth += 1
        # 深さが+1になったのでcircuit_pictureの横サイズも増やす
        self.horizontal_size += 8

    def _write_gate_on_picture(self, gate_string, ulc):
        """作成したゲート文字列を実際に描き込むメソッド"""
        row, col = ulc
        width = 7
        for line in gate_string:
            self.circuit_picture[row][col : col + width] = list(line)
            row += 1

    def _connect_wire(self):
        """量子回路の横向きのワイヤーの接続を補うメソッド"""
        # 回路のqubit数回ループ
        for i in range(self.qubit_num):
            # 横向きのワイヤーがある場所は配列番号で2,6,10,14,...番目
            row = (i + 1) * 4 - 2
            # 先頭から１文字ずつ調査していくための変数
            p = 0
            # 各行の先頭から見ていく
            while True:
                # 先頭の文字を読む
                char_now = self.circuit_picture[row][p]
                if char_now == "{}".format(self.CON_DOT):
                    # 読んだのが"･"のときは次の文字が必ず空白になっているはずなので"-"に書き換える
                    self.circuit_picture[row][p + 1] = "-"
                elif char_now == "-":
                    # 読んだのが"-"のときは次の１文字を読む
                    if self.circuit_picture[row][p + 1] == " ":
                        # "-"の次が" "(空白)なので"-"に書き換えワイヤーを繋げる
                        self.circuit_picture[row][p + 1] = "-"
                    elif self.circuit_picture[row][p + 1] == "|":
                        # 読んだ文字が"|"のときはゲートの左壁にぶつかったorコントロールユニタリの制御信号(縦線)のどちらか
                        # 最初に, 3文字分(通常のゲートの横幅分)を空けて次の文字を読んでみる
                        # つまりp+1 + 3 + 1文字分先を読む
                        if self.circuit_picture[row][p + 5] == "|":
                            # ぶつかったのは通常のゲートの幅の左壁だったので, ゲートの右側まで抜ける
                            # 現在位置pは(左壁の位置-1)で+5すれば現在地は右壁の"|"になる
                            # そして最後のインクリメントで右壁の次にいく
                            p += 5
                        elif self.circuit_picture[row][p + 3] == "|":
                            # ぶつかったのは離れたqubitにかかるゲート用の壁(幅の狭いゲート)の左壁だった
                            # +3すれば現在地は右壁の"|"になるので, 最後のインクリメントで右壁の次にいく
                            p += 3
                        else:
                            # 読んでみるとゲートの右の壁でない => 読んだのはコントロールユニタリの縦線だった
                            # なので次の空白を"-"とする
                            # "|"を"+"に書き換えワイヤーがクロスする表示も試したが,
                            # どこが制御qubitかわかりにくかったのでやめた.
                            self.circuit_picture[row][p + 2] = "-"
                            # 次に読む文字を今変更した"-"にするために調整
                            p += 1
                # インクリメントして次の文字の位置をセット
                p += 1
                # もしインクリメントしたときに配列のサイズを超えたら終了
                if p + 1 == self.horizontal_size:
                    break


def draw_circuit(circuit, verbose: bool = False, dot: str = "large") -> None:  # type: ignore
    """
    量子回路図をテキストで出力するための関数

    Parameters
    ----------
    circuit: qulacs.QuantumCircuit
        出力したい量子回路(qulacs.QuantumCircuit)
    verbose: bool
        詳細出力(default=False). Trueのときはgateにcircuitに追加された順番が出力される
    dot: str
        制御qubitを表すドットのスタイル(default="large")
    """

    Drawer = TextCircuitDrawer(circuit, dot=dot)
    Drawer.draw(verbose=verbose)
