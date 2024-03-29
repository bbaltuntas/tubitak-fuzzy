import sys
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from skfuzzy import control as ctrl
from skfuzzy.control.visualization import FuzzyVariableVisualizer
from design.result_python import Ui_MainWindow as InputWindow
from error_message import ErrorMessage
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time

class Worker(QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        # long running task
        print("Başladı")
        ver_lay = QVBoxLayout()
        output_ctrl = ctrl.ControlSystem(self.parent.rules)
        output = ctrl.ControlSystemSimulation(output_ctrl)
        # TODO try catch ekle
        for index in range(len(self.parent.input_variables)):
            output.input[self.parent.input_variables[index].variable_ctrl.label] = self.parent.input_variables[
                index].input

        # Crunch the numbers
        output.compute()
        print("Bitti")
        for i in reversed(range(self.parent.res_lay.count())):
            self.parent.res_lay.itemAt(i).widget().setParent(None)
        self.parent.fig, self.parent.ax = None, None
        content = ""
        for index in range(len(self.parent.output_variables)):
            content = content + "The Result for {0} is {1:.2f} \n".format(self.parent.output_variables[index].name,
                                                                          output.output[
                                                                              self.parent.output_variables[
                                                                                  index].name])
            self.parent.res_ui.result_label.setText(content)
            out_ctrl: ctrl.Consequent = self.parent.output_variables[index].variable_ctrl
            self.parent.fig, self.parent.ax = FuzzyVariableVisualizer(out_ctrl).view(sim=output)

            self.parent.fig.tight_layout(pad=3, w_pad=3, h_pad=3)
            graph = InputGraph(self.parent.fig)
            ver_lay.addWidget(graph)
        widget = QWidget()
        widget.setLayout(ver_lay)
        self.parent.res_ui.graph_list.setWidget(widget)
        # self.res_ui.graph_layout.addWidget(graph)
        self.parent.res_lay.update()


class ResultScreen(QMainWindow):
    def __init__(self, rules, input_variables, output_variables):
        super().__init__()
        self.res_ui = InputWindow()
        self.resWindow = QMainWindow()

        self.res_ui.setupUi(self.resWindow)
        self.resWindow.show()
        self.setWindowTitle("Result")

        self.rules = rules
        self.input_variables = input_variables
        self.output_variables = output_variables
        self.only_num = QDoubleValidator(-sys.maxsize - 1, sys.maxsize, 0)
        self.fig, self.ax = None, None
        self.res_lay = QVBoxLayout()
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
        self.res_ui.inputList.setWidget(widgetV)

        # self.line1.returnPressed.connect(self.setLine1)
        # self.line2.returnPressed.connect(self.setLine2)
        self.res_ui.fuzzy_button.clicked.connect(self.calc_fuzzy)
        # self.res_ui.input_list_widget.currentRowChanged.connect(self.show_var_value)
        # self.res_ui.var_value.returnPressed.connect(self.set_var_value)

    def calc_fuzzy(self):
        try:
            # long running task
            print("Başladı")
            ver_lay = QVBoxLayout()
            start = time.time()
            output_ctrl = ctrl.ControlSystem(self.rules[0:50])
            end = time.time()
            print(end - start)
            print("Rule bitti")
            output = ctrl.ControlSystemSimulation(output_ctrl)
            print("outputctrl")
            # TODO try catch ekle
            for index in range(len(self.input_variables)):
                output.input[self.input_variables[index].variable_ctrl.label] = self.input_variables[
                    index].input
            print("for bitti")
            # Crunch the numbers
            output.compute()
            print("Bitti")
            for i in reversed(range(self.res_lay.count())):
                self.res_lay.itemAt(i).widget().setParent(None)
            self.fig, self.ax = None, None
            content = ""
            for index in range(len(self.output_variables)):
                content = content + "The Result for {0} is {1:.2f} \n".format(self.output_variables[index].name,
                                                                              output.output[
                                                                                  self.output_variables[
                                                                                      index].name])
                self.res_ui.result_label.setText(content)
                out_ctrl: ctrl.Consequent = self.output_variables[index].variable_ctrl
                self.fig, self.ax = FuzzyVariableVisualizer(out_ctrl).view(sim=output)

                self.fig.tight_layout(pad=3, w_pad=3, h_pad=3)
                graph = InputGraph(self.fig)
                ver_lay.addWidget(graph)
            widget = QWidget()
            widget.setLayout(ver_lay)
            self.res_ui.graph_list.setWidget(widget)
            # self.res_ui.graph_layout.addWidget(graph)
            self.res_lay.update()


        except Exception as err:
            ErrorMessage("Value Error", err.__str__()).show()

    def set_var_value(self):
        for index, var in enumerate(self.input_variables):
            line_edit = self.res_ui.inputList.widget().layout().itemAt(index).widget().layout().itemAt(2).widget()
            value = line_edit.text()
            print(value)
            try:
                if value != "":
                    var.input = int(value)
                else:
                    var.input = None
            except ValueError as err:
                print(err)

    def show_var_value(self, index):
        var = self.input_variables[index]
        self.res_ui.var_value.setText(str(var.input) if var.input is not None else "")


class InputGraph(FigureCanvas):

    def __init__(self, fig, parent=None):
        self.fig = fig
        super().__init__(self.fig)
