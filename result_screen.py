import sys
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from skfuzzy import control as ctrl
from skfuzzy.control.visualization import FuzzyVariableVisualizer
from design.result_python import Ui_MainWindow as InputWindow
from error_message import ErrorMessage


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
        self.res_ui.var_value.setValidator(self.only_num)
        self.fig, self.ax = None, None
        self.graph = None
        for i in input_variables:
            self.res_ui.input_list_widget.addItem(QListWidgetItem(i.name))

        self.res_ui.fuzzy_button.clicked.connect(self.calc_fuzzy)
        self.res_ui.input_list_widget.currentRowChanged.connect(self.show_var_value)
        self.res_ui.var_value.returnPressed.connect(self.set_var_value)

    def calc_fuzzy(self):
        try:
            output_ctrl = ctrl.ControlSystem(self.rules)
            output = ctrl.ControlSystemSimulation(output_ctrl)

            for index in range(len(self.input_variables)):
                output.input[self.input_variables[index].name] = self.input_variables[index].input

            # Crunch the numbers
            output.compute()
            # TODO birden çok output için fig kısmını düzelt

            for index in range(len(self.output_variables)):
                self.res_ui.result_label.setText(
                    "The Result for {0} is {1:.2f}".format(self.output_variables[index].name,
                                                           output.output[
                                                               self.output_variables[
                                                                   index].name]))
                out_ctrl: ctrl.Consequent = self.output_variables[index].variable_ctrl
                self.fig, self.ax = FuzzyVariableVisualizer(out_ctrl).view(sim=output)

            self.res_ui.graph_layout.removeWidget(self.graph)
            self.fig.tight_layout(pad=2)
            self.graph = InputGraph(self.fig)
            self.res_ui.graph_layout.addWidget(self.graph)
            self.res_ui.graph_layout.update()
        except ValueError as err:
            ErrorMessage("Value Error", err.__str__()).show()

    def set_var_value(self):
        value = self.res_ui.var_value.text()
        index = self.res_ui.input_list_widget.currentRow()
        var = self.input_variables[index]

        try:
            var.input = int(value)
        except ValueError:
            print("hata")

    def show_var_value(self, index):
        var = self.input_variables[index]
        self.res_ui.var_value.setText(str(var.input) if var.input is not None else "")


class InputGraph(FigureCanvas):

    def __init__(self, fig, parent=None):
        self.fig = fig
        super().__init__(self.fig)
