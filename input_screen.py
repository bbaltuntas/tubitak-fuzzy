import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from design.input_python import Ui_MainWindow as InputWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
from threading import Thread
from error_message import ErrorMessage


class InputScreen(QMainWindow):
    def __init__(self, ui, var, inp_variables, button):
        super().__init__()
        self.var = var
        self.ui = ui
        self.button = button

        self.inp_variables = inp_variables
        self.inp_ui = InputWindow()
        self.inputWindow = QMainWindow()

        self.inp_ui.setupUi(self.inputWindow)
        self.inputWindow.show()
        self.inputWindow.setWindowTitle(var.name)
        self.only_num = QDoubleValidator(-sys.maxsize - 1, sys.maxsize, 0)

        self.graph = InputGraph(self.var.fig)
        self.inp_ui.graph_layout.addWidget(self.graph)

        if self.var.function_type == "triangular":
            self.set_mf_values(3, type="triangular")
            self.inp_ui.triangular_mf.setChecked(True)
        elif self.var.function_type == "gaussian":
            self.set_mf_values(2, type="gaussian")
            self.inp_ui.gaussian_mf.setChecked(True)
        elif self.var.function_type == "trapezoidal":
            self.set_mf_values(4, type="trapezoidal")
            self.inp_ui.trapezoidal_mf.setChecked(True)

        self.inp_ui.var_name.setText(var.name)
        self.inp_ui.domain_min.setText(str(self.var.start) if self.var.start is not None else None)
        self.inp_ui.domain_max.setText(str(self.var.end - 1) if self.var.start is not None else None)

        self.set_actions()
        self.set_validator()
        self.update_mf_list()

    def set_actions(self):

        self.inp_ui.triangular_mf.clicked.connect(lambda: self.set_mf_values(3, "triangular"))
        self.inp_ui.gaussian_mf.clicked.connect(lambda: self.set_mf_values(2, "gaussian"))
        self.inp_ui.trapezoidal_mf.clicked.connect(lambda: self.set_mf_values(4, "trapezoidal"))
        self.inp_ui.mf_add_button.clicked.connect(self.add_mf)
        self.inp_ui.remove_mf_button.clicked.connect(self.remove_mf)
        self.inp_ui.var_name.editingFinished.connect(self.update_var_name)
        self.inp_ui.set_domain.clicked.connect(self.set_domain_range)
        self.inp_ui.mf_function_list.itemDoubleClicked.connect(self.bring_mf_infos)

    def set_validator(self):
        self.inp_ui.domain_min.setValidator(self.only_num)
        self.inp_ui.domain_max.setValidator(self.only_num)

    def update_var_name(self):
        self.var.name = self.inp_ui.var_name.text()
        self.button.setText(self.var.name)

    def set_domain_range(self):
        try:
            if len(self.var.mf_function_value.keys()) == 0:
                start = int(self.inp_ui.domain_min.text())
                end = int(self.inp_ui.domain_max.text())
                self.var.init_range(start, end + 1)
            else:
                ErrorMessage("Domain Error",
                             "Before setting domain, make sure there is no membership function exist.").show()
        except ValueError:
            ErrorMessage("Domain Error", "Enter proper domain value.").show()

    def set_mf_values(self, count, type):
        if type == "triangular":
            self.var.function_type = "triangular"

        elif type == "gaussian":
            self.var.function_type = "gaussian"

        elif type == "trapezoidal":
            self.var.function_type = "trapezoidal"

        for i in reversed(range(self.inp_ui.mf_values_layout.count())):
            self.inp_ui.mf_values_layout.itemAt(i).widget().setParent(None)
        self.mf_line_edit = []
        for i in range(count):
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            line_edit = QLineEdit()
            line_edit.setFixedWidth(50)
            line_edit.setSizePolicy(sizePolicy)
            line_edit.setValidator(self.only_num)
            self.inp_ui.mf_values_layout.addWidget(line_edit)
            self.mf_line_edit.append(line_edit)

    def add_mf(self):
        if self.var.start is None or self.var.end is None:
            ErrorMessage("Domain Error", "Before adding membership function, set domain values.").show()
        else:
            if self.inp_ui.triangular_mf.isChecked():
                self.mf_general_func("trimmf")
            elif self.inp_ui.gaussian_mf.isChecked():
                self.mf_general_func("gaussmf")
            elif self.inp_ui.trapezoidal_mf.isChecked():
                self.mf_general_func("trapmf")

    def mf_general_func(self, function):
        is_exist = False
        label = self.inp_ui.mf_label.text()
        for key in self.var.mf_function_value.keys():
            if key == label:
                is_exist = True
                sleep_thread = Thread(target=lambda: self.show_info_label("This Label Taken"))
                sleep_thread.start()

        if not is_exist:
            try:
                mf_values = []
                for i in self.mf_line_edit:
                    mf_values.append(int(i.text()))

                if function == "trimmf":
                    self.var.add_trimf_membership_function(label, mf_values)
                elif function == "gaussmf":
                    self.var.add_gaussmf_membership_function(label, mf_values[0], mf_values[1])
                elif function == "trapmf":
                    self.var.add_trapmf_membership_function(label, mf_values)

                self.var.mf_function_value[label] = mf_values
                self.update_graph()

                self.inp_ui.mf_function_list.addItem(QListWidgetItem(label))
                self.inp_ui.mf_label.setText("")
                for i in self.mf_line_edit:
                    i.setText(None)
            except ValueError:
                ErrorMessage("Membership Function Value Error",
                             "Enter proper value for membership function.").show()
            except AssertionError:
                if function == "trimmf":
                    ErrorMessage("Membership Function Value Error",
                                 "The elements requires pattern like a <= b <= c").show()
                elif function == "trapmf":
                    ErrorMessage("Membership Function Value Error",
                                 "The elements requires pattern like a <= b <= c <= d").show()

    def remove_mf(self):
        try:
            selected_mf = self.inp_ui.mf_function_list.selectedItems()[0].text()

            for i in self.var.graph.get_lines():
                if i.get_label() == selected_mf:
                    self.var.graph.lines.remove(i)

            del self.var.membership_functions[selected_mf]
            del self.var.mf_function_value[selected_mf]

            self.update_graph()
            self.update_mf_list()
        except IndexError:
            ErrorMessage("Remove Error", "Select an element before removing.").show()

    def update_mf(self, old_label):
        label = self.inp_ui.mf_label.text()
        mf_values = []
        for i in self.mf_line_edit:
            mf_values.append(int(i.text()))

        del self.var.mf_function_value[old_label]
        self.var.mf_function_value[label] = mf_values

        for i in self.var.graph.get_lines():
            if i.get_label() == old_label:
                self.var.graph.lines.remove(i)

        del self.var.membership_functions[old_label]
        self.var.add_trimf_membership_function(label, mf_values)

        self.update_graph()

        self.inp_ui.mf_label.setText("")
        for i in self.mf_line_edit:
            i.setText(None)

        self.update_mf_list()

    def bring_mf_infos(self, item):
        label = item.text()
        self.inp_ui.mf_label.setText(label)
        mf_value = self.var.mf_function_value[label]

        for index, widget in enumerate(self.mf_line_edit):
            widget.setText(str(mf_value[index]))

        try:
            self.inp_ui.update_mf_button.clicked.disconnect()
        except TypeError:
            "There is no connections"
        self.inp_ui.update_mf_button.clicked.connect(lambda: self.update_mf(label))

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
        for item in self.var.mf_function_value.keys():
            self.inp_ui.mf_function_list.addItem(QListWidgetItem(item))

    def show_info_label(self, content):
        self.inp_ui.info_label.setText(content)
        time.sleep(4)
        self.inp_ui.info_label.setText("")


class InputGraph(FigureCanvas):

    def __init__(self, fig, parent=None):
        self.fig = fig
        super().__init__(self.fig)
