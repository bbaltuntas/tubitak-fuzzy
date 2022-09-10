from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from design.input_python import Ui_MainWindow as InputWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class InputScreen(object):
    def __init__(self, ui, var, inp_variables, button):
        self.var = var
        self.ui = ui
        self.button = button

        self.inp_variables = inp_variables
        self.inp_ui = InputWindow()
        self.inputWindow = QMainWindow()

        self.inp_ui.setupUi(self.inputWindow)
        self.inputWindow.show()

        self.only_num = QDoubleValidator(-100, 100, 0)

        self.graph = InputGraph(self.var.fig)
        self.inp_ui.graph_layout.addWidget(self.graph)
        self.var.graph.legend()

        self.inp_ui.var_name.setText(var.name)
        self.inp_ui.domain_min.setText(str(self.var.start) if self.var.start is not None else "")
        self.inp_ui.domain_max.setText(str(self.var.end - 1) if self.var.start is not None else "")

        self.set_actions()
        self.set_validator()
        self.update_mf_list()

    def set_actions(self):
        self.inp_ui.triangular_mf.clicked.connect(lambda: self.set_mf_values(3))
        self.inp_ui.gaussian_mf.clicked.connect(lambda: self.set_mf_values(2))
        self.inp_ui.trapezoidal_mf.clicked.connect(lambda: self.set_mf_values(4))
        self.inp_ui.mf_add_button.clicked.connect(self.add_mf)

        self.inp_ui.remove_mf_button.clicked.connect(self.remove_mf)
        self.inp_ui.var_name.editingFinished.connect(self.update_var_name)
        self.inp_ui.set_domain.clicked.connect(self.set_domain_range)

    def set_validator(self):
        self.inp_ui.domain_min.setValidator(self.only_num)
        self.inp_ui.domain_max.setValidator(self.only_num)

    def update_var_name(self):
        self.var.name = self.inp_ui.var_name.text()
        self.button.setText(self.var.name)

    def set_domain_range(self):
        start = int(self.inp_ui.domain_min.text())
        end = int(self.inp_ui.domain_max.text())
        self.var.init_range(start, end + 1)

    def set_mf_values(self, count):
        for i in reversed(range(self.inp_ui.mf_values_layout.count())):
            self.inp_ui.mf_values_layout.itemAt(i).widget().setParent(None)
        self.mf_line_edit = []
        for i in range(count):
            line_edit = QLineEdit()
            line_edit.setValidator(self.only_num)
            self.inp_ui.mf_values_layout.addWidget(line_edit)
            self.mf_line_edit.append(line_edit)

    def add_mf(self):
        if self.inp_ui.triangular_mf.isChecked():
            mf_values = []
            for i in self.mf_line_edit:
                mf_values.append(int(i.text()))
            self.var.add_trimf_membership_function(self.inp_ui.mf_label.text(), mf_values)

            self.update_graph()

            self.inp_ui.mf_function_list.addItem(QListWidgetItem(self.inp_ui.mf_label.text()))
            self.inp_ui.mf_label.setText("")
            for i in self.mf_line_edit:
                i.setText("")

    def remove_mf(self):
        selected_mf = self.inp_ui.mf_function_list.selectedItems()[0].text()

        for i in self.var.graph.get_lines():
            if i.get_label() == selected_mf:
                self.var.graph.lines.remove(i)

        del self.var.membership_functions[selected_mf]

        print(type(self.var.variable_ctrl))
        self.update_graph()
        self.update_mf_list()

    def set_input(self):
        value = int(self.inp_ui.var_input_line.text())
        self.var.set_input(value)

    def update_graph(self):
        self.inp_ui.graph_layout.removeWidget(self.graph)
        self.graph = InputGraph(self.var.fig)

        self.inp_ui.graph_layout.addWidget(self.graph)
        self.var.graph.legend()
        self.inp_ui.graph_layout.update()

    def update_mf_list(self):
        self.inp_ui.mf_function_list.clear()
        for item in self.var.membership_functions.keys():
            self.inp_ui.mf_function_list.addItem(QListWidgetItem(item))


class InputGraph(FigureCanvas):

    def __init__(self, fig, parent=None):
        self.fig = fig
        super().__init__(self.fig)
