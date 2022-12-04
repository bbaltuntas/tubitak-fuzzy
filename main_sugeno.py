import pickle
import os
import variable
from design.design_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from error_message import ErrorMessage
from input_screen import InputScreen

from rule_sugeno import RuleSugeno
from result_sugeno import ResultSugeno


# TODO rule kısmında yanlış girilmeyi önle
class MainSugeno(QMainWindow):
    def __init__(self, mamdani):
        super().__init__()
        self.sugeno_ui = InputWindow()
        self.sugenoWindow = QMainWindow()
        self.mamdani = mamdani
        self.sugeno_ui.setupUi(self.sugenoWindow)
        self.sugenoWindow.show()

        self.sugenoWindow.setWindowTitle("Sugeno")
        self.input_variables = []
        self.output_variables = []
        self.add_input_variable()
        self.add_output_variable()
        self.sugeno_ui.rule_button.setText("Sugeno")

        self.rules = []
        self.set_actions()
        self.system = "Sugeno"
        self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        self.rw = None

    def set_actions(self):
        self.sugeno_ui.actionInput.triggered.connect(self.add_input_variable)
        self.sugeno_ui.actionSave_Data.triggered.connect(self.save_data)
        self.sugeno_ui.actionImport_Data.triggered.connect(self.import_data)
        self.sugeno_ui.actionMamdani.triggered.connect(self.open_mamdani)
        self.sugeno_ui.actionSugeno.triggered.connect(self.open_sugeno)

        self.sugeno_ui.variable_name_line.editingFinished.connect(self.update_variable)
        self.sugeno_ui.rule_button.clicked.connect(self.open_rule_page)
        self.sugeno_ui.startButton.clicked.connect(self.calc_result)

    def open_mamdani(self):
        self.sugenoWindow.close()
        window = self.mamdani.show()

    def open_sugeno(self):
        self.sugenoWindow.close()
        window = MainSugeno(self.mamdani)

    def open_rule_page(self):
        self.rw = RuleSugeno(self.input_variables, self.rules)

    def calc_result(self):
        self.resw = ResultSugeno(self.rules, self.input_variables)

    def input_button_action(self, var, button):
        self.input_w = InputScreen(self.sugeno_ui, var, button, self, self.input_variables, self.output_variables)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                menu = QMenu()
                del_action = menu.addAction("Delete Variable")
                action = menu.exec_(obj.mapToGlobal(event.pos()))
                var = obj.var
                if action == del_action:
                    self.delete_variable(var, obj)
        return QObject.event(obj, event)

    def delete_variable(self, var, obj):
        if var.type == "input":
            self.input_variables.remove(var)
            self.sugeno_ui.gridLayout.removeWidget(obj)
            self.sugeno_ui.gridLayout.update()
            obj.deleteLater()
            # print(self.ui.gridLayout.itemAtPosition(1, 2).widget().text())
            print(len(self.rules))
            print(var.name)
            count = 0
            while True:
                if count == len(self.rules):
                    break
                if var.name in self.rules[count].content:
                    self.rules.pop(count)
                else:
                    # TODO var silinince rulelardaki term silinsin
                    count += 1

            for rule in self.rules:
                del rule.mf_rules[var.name]

            # for rule in self.rules:
            #     if var.name in rule.content:
            #         self.rules.remove(rule)

    def add_input_variable(self):
        length = len(self.input_variables)
        var = variable.Variable("input", ("input" + str(length + 1)))
        self.input_variables.append(var)
        length += 1
        self.load_input_button(var, length)

    def load_input_button(self, var, length):
        button = QDoublePushButton(var)
        button.setObjectName("inputButton")
        size_policy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(size_policy)
        button.setStyleSheet(
            "#inputButton:focus {border : 2px solid green;}  #inputButton{border: 1px solid grey; border-radius:5px}")

        button.clicked.connect(lambda: self.update_variable_line(var, button))
        button.doubleClicked.connect(lambda: self.input_button_action(var, button))
        button.installEventFilter(self)

        # self.ui.gridLayout.addWidget(button)
        self.sugeno_ui.gridLayout.addWidget(
            button
        )
        self.sugeno_ui.gridLayout.update()

    def add_output_variable(self):
        length = len(self.output_variables)
        var = variable.Variable("output", ("output" + str(length + 1)), )
        self.output_variables.append(var)
        length += 1
        self.load_output_buttons(var)

    def load_output_buttons(self, var):
        button = QDoublePushButton(var)
        button.setObjectName("outputButton")
        size_policy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(size_policy)
        button.setStyleSheet(
            "#outputButton:focus {border : 2px solid green;}  #outputButton{border: 1px solid grey; border-radius:5px}")

        button.clicked.connect(lambda: self.update_variable_line(var, button))
        self.sugeno_ui.output_layout.addWidget(button)
        self.sugeno_ui.output_layout.update()

    def update_variable_line(self, var, button):
        for i in reversed(range(self.sugeno_ui.gridLayout.count())):
            self.sugeno_ui.gridLayout.itemAt(i).widget().setStyleSheet(
                "#inputButton:focus {border : 3px solid green;}  #inputButton{border: 1px solid grey; border-radius:5px}")

        for o in reversed(range(self.sugeno_ui.output_layout.count())):
            self.sugeno_ui.output_layout.itemAt(o).widget().setStyleSheet(
                "#outputButton:focus {border : 3px solid green;} #outputButton{border: 1px solid grey;border-radius:5px}")

        self.sugeno_ui.variable_name_line.setText(var.name)
        self.sugeno_ui.variable_type_line.setText(var.type)
        self.sugeno_ui.range_label.setText(
            "[{0} , {1}]".format(var.start if var.start is not None else "0",
                                 var.end if var.end is not None else "1"))
        if var.type == "input":

            button.setStyleSheet(
                "#inputButton:focus {border : 3px solid green;} #inputButton{border:3px solid green;border-radius:5px}")
        else:

            button.setStyleSheet(
                "#outputButton:focus {border : 3px solid green;} #outputButton{border:3px solid green;border-radius:5px}")

    def update_variable(self):
        new_variable_name = self.sugeno_ui.variable_name_line.text()
        focus_widget = self.sugeno_ui.frame.focusWidget()
        var_name = focus_widget.text()
        contains = False
        for i in self.input_variables:
            if i.name == new_variable_name:
                contains = True
        for o in self.output_variables:
            if o.name == new_variable_name:
                contains = True

        if not contains:
            focus_widget.setText(self.sugeno_ui.variable_name_line.text())

            for index, input_var in enumerate(self.input_variables):
                if var_name == input_var.name:
                    input_var.name = self.sugeno_ui.variable_name_line.text()
                    if input_var.variable_ctrl is not None:
                        input_var.variable_ctrl.label = self.sugeno_ui.variable_name_line.text()
                    self.update_rule(var_name, new_variable_name)

    def update_rule(self, old_name, new_name):
        for rule in self.rules:
            if old_name in rule.content:
                rule.mf_rules[new_name] = rule.mf_rules.pop(old_name)
                rule.content = rule.content.replace(old_name, new_name)

                # new_rule = self.rw.create_rule(rule.mf_rules, rule.parameters)
                # rule.content = new_rule.content

    def save_data(self):
        dirname, _ = QFileDialog.getSaveFileName(self.sugenoWindow, "Choose Directory", self.desktop, "data",
                                                 "Python Files (*.fis)")
        if dirname:
            try:
                with open(dirname, "wb") as f:
                    pickle.dump(self.input_variables, f, protocol=pickle.HIGHEST_PROTOCOL)
                    pickle.dump(self.rules, f, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as ex:
                ErrorMessage("File Error", ex)

    def load_all(self, filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def import_data(self):
        filename, _ = QFileDialog.getOpenFileName(self.sugenoWindow, "Choose File", self.desktop, "Fuzzy Files (*.fis)")
        if filename:
            try:
                items = list(self.load_all(filename))
                self.input_variables = items[0]
                self.rules = items[1]

                for i in reversed(range(self.sugeno_ui.gridLayout.count())):
                    self.sugeno_ui.gridLayout.itemAt(i).widget().setParent(None)
                for index, var_inp in enumerate(self.input_variables):
                    self.load_input_button(var_inp, index + 1)

            except Exception as ex:
                print("Error during unpickling object (Possibly unsupported):", ex)


class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, var, *args, **kwargs):

        QPushButton.__init__(self, *args, **kwargs)
        self.var = var
        self.setText(var.name)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)
