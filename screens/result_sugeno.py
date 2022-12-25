import sys

from PyQt5.QtGui import QDoubleValidator

from design.result_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from skfuzzy import control as ctrl
from skfuzzy.control.visualization import FuzzyVariableVisualizer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from error_message import ErrorMessage


class ResultSugeno(object):
    def __init__(self, rules, input_variables):
        super().__init__()
        self.res_sug_ui = InputWindow()
        self.resWindow = QMainWindow()

        self.res_sug_ui.setupUi(self.resWindow)
        self.resWindow.show()
        self.rules = rules
        self.input_variables = input_variables
        self.only_num = QDoubleValidator(-sys.maxsize - 1, sys.maxsize, 0)
        self.res_lay = QVBoxLayout()
        # self.res_sug_ui.graph_layout.addLayout(self.res_lay)
        lines = []
        vlayout = QVBoxLayout()
        widgetV = QWidget()
        for index, var in enumerate(input_variables):
            widget = QWidget()
            layout = QHBoxLayout()
            lineEdit = QLineEdit()
            lines.append(lineEdit)
            lineEdit.setText(str(var.input) if var.input is not None else None)
            lineEdit.setValidator(self.only_num)
            lineEdit.returnPressed.connect(self.set_var_value)
            label = QLabel(var.name)
            layout.addWidget(label)
            layout.addStretch()
            layout.addWidget(lineEdit)

            widget.setLayout(layout)
            vlayout.addWidget(widget)

        widgetV.setLayout(vlayout)
        self.res_sug_ui.inputList.setWidget(widgetV)

        self.res_sug_ui.fuzzy_button.clicked.connect(self.calc_sugeno)

    def calc_sugeno(self):
        isValid = True
        for var in self.input_variables:
            if var.input is None:
                isValid = False
                ErrorMessage("Input Hatası", "Değişken değerleri giriniz!").show()
                break
        if isValid:
            for i in reversed(range(self.res_lay.count())):
                layout = self.res_lay.itemAt(i).layout()
                for j in reversed(range(layout.count())):
                    layout.itemAt(j).widget().setParent(None)
            self.fig, self.ax = None, None
            try:
                total_val = 0
                min_weight_list = []
                for rule in self.rules:
                    ver_lay = QHBoxLayout()

                    rule_val = 0
                    weight_list = []
                    for index, term in enumerate(rule.mf_rules.values()):
                        if term[0] != "None":
                            values = self.input_variables[index].mf_function_value[term[0]]
                            weight = None
                            var_ctrl = self.input_variables[index].variable_ctrl[term[0]]
                            self.fig, self.ax = FuzzyVariableVisualizer(var_ctrl).view()
                            self.ax.get_legend().remove()
                            self.fig.set_figwidth(2)
                            self.fig.set_figheight(2)
                            input = self.input_variables[index].input
                            self.ax.add_artist(lines.Line2D([input, input], [0, 1], color="red"))
                            self.ax.set_xticklabels([])
                            self.ax.yaxis.set_label_text("")
                            # self.ax.xaxis.set_label_text("")
                            self.fig.patch.set_alpha(0.0)
                            self.fig.tight_layout(pad=2, w_pad=2, h_pad=2)
                            graph = InputGraph(self.fig)
                            ver_lay.addWidget(graph)

                            if self.input_variables[index].function_type == "triangular":
                                weight = self.trifunc(values[0], values[1], values[2],
                                                      self.input_variables[index].input)

                            elif self.input_variables[index].function_type == "trapezoidal":
                                weight = self.trapfunc(values[0], values[1], values[2], values[3],
                                                       self.input_variables[index].input)
                            print("weight ", weight)
                            weight_list.append(weight)
                            rule_val += float(term[1]) * self.input_variables[index].input
                            print("rule val ", rule_val)
                    #  rule_val += rule.
                    min_weight = min(weight_list)
                    print("min weight", min_weight)
                    min_weight_list.append(min_weight)
                    total_val += min_weight * rule_val
                    print("total val ", total_val)

                    ver_lay.addWidget(self.bar(min_weight))
                    self.res_lay.addLayout(ver_lay)
                    self.res_lay.update()
                res = total_val / sum(min_weight_list)
                result_content = "The result is {0:.2f}".format(res)
                self.res_sug_ui.result_label.setText(result_content)
                lwidget = QWidget()
                lwidget.setLayout(self.res_lay)
                self.res_sug_ui.graph_list.setWidget(lwidget)
            except ZeroDivisionError as zeroErr:
                self.res_sug_ui.result_label.setText("The result is 0")

    def set_var_value(self):
        for index, var in enumerate(self.input_variables):
            line_edit = self.res_sug_ui.inputList.widget().layout().itemAt(index).widget().layout().itemAt(2).widget()
            value = line_edit.text()
            print(value)
            try:
                if value != "":
                    var.input = int(value)
                else:
                    var.input = None
            except ValueError as err:
                print(err)

    def trifunc(self, a, b, c, x):
        try:
            x1 = (x - a) / (b - a)
        except:
            x1 = sys.maxsize
        try:
            x2 = (c - x) / (c - b)
        except:
            x2 = sys.maxsize

        result = max(min(x1, x2), 0)
        return result

        # if x <= a:
        #     return 0
        # elif a <= x <= b:
        #     res = (x - a) / (b - a)
        #     return res
        # elif b <= x <= c:
        #     res = (c - x) / (c - b)
        #     return res
        # elif c <= x:
        #     return 0

    def trapfunc(self, a, b, c, d, x):
        if x <= a:
            return 0
        elif a <= x <= b:
            res = (x - a) / (b - a)
            return res
        elif b <= x <= c:
            return 1
        elif c <= x <= d:
            res = (d - x) / (d - c)
            return res
        elif d <= x:
            return 0
        # try:
        #     x1 = (x - a) / (b - a)
        # except:
        #     x1 = sys.maxsize
        # try:
        #     x2 = (d - x) / (d - c)
        # except:
        #     x2 = sys.maxsize
        #
        # res = max(min(x1, x2, 1), 0)
        # return res

    def show_var_value(self, index):
        var = self.input_variables[index]
        self.res_sug_ui.var_value.setText(str(var.input) if var.input is not None else "")

    def bar(self, value):

        # creating progress bar
        bar = QProgressBar(self.resWindow)
        bar.setObjectName("bar")
        bar.setStyleSheet(
            "#bar{ min-width: 12px; max-width: 12px;color:transparent} #bar::chunk{background-color: red}")
        # setting geometry to progress bar
        bar.setGeometry(200, 150, 40, 200)

        # set value to progress bar
        bar.setValue(value * 100)
        # changing the orientation
        bar.setOrientation(Qt.Vertical)
        return bar

    def find_var(self, var_name):
        for var in self.input_variables:
            if var.name == var_name:
                return var


class InputGraph(FigureCanvas):

    def __init__(self, fig, parent=None):
        self.fig = fig
        super().__init__(self.fig)
