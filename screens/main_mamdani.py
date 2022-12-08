from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import googletrans
import textblob

from skfuzzy import control as ctrl
import json
import pickle

from design.design_python import Ui_MainWindow as MainWindow

import variable
from screens.input_screen import InputScreen
from screens.result_screen import ResultScreen
from screens.rule_screen import RuleScreen
from screens.language_screen import LanguageScreen
from error_message import ErrorMessage
from screens.main_sugeno import MainSugeno


class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_variables = []
        self.output_variables = []
        self.rules = []
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Mamdani Fuzzy Inference System")
        self.add_input_variable()
        self.add_output_variable()
        self.and_method = "min"
        self.or_method = "max"
        self.system = "Mamdani"
        self.input_w = None
        self.rule_w = None
        self.res_w = None
        self.lang_w = None
        self.sugeno_w = None
        self.set_actions()
        self.to_language_key = None
        try:
            with open('../config.json', 'r') as f:
                self.config = json.load(f)
        except Exception:
            config = {'lan': 'turkish'}
            with open('../config.json', 'w') as f:
                json.dump(config, f)

        try:
            for key, value in googletrans.LANGUAGES.items():
                if value == self.config['lan']:
                    self.to_language_key = key

            words = textblob.TextBlob(self.ui.startButton.text())
            words = words.translate(from_lang="en", to=self.to_language_key)
            self.ui.startButton.setText(str(words))

        except Exception as ex:
            print(str(ex))

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(
    #         self, "Message",
    #         "Are you sure you want to quit? Any unsaved work will be lost.",
    #         QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
    #         QMessageBox.Save)
    #
    #     if reply == QMessageBox.Close:
    #         event.accept()
    #         # app.quit()
    #     elif reply == QMessageBox.Save:
    #         self.save_data()
    #     else:
    #         event.ignore()

    def set_actions(self):
        self.ui.actionInput.triggered.connect(self.add_input_variable)
        self.ui.actionLanguage.triggered.connect(self.set_language)
        self.ui.actionOutput.triggered.connect(self.add_output_variable)
        self.ui.actionImport_Data.triggered.connect(self.import_data)
        self.ui.actionSave_Data.triggered.connect(self.save_data)
        self.ui.actionSugeno.triggered.connect(self.openSugeno)
        self.ui.actionMamdani.triggered.connect(self.openMamdani)

        self.ui.variable_name_line.editingFinished.connect(self.update_variable)

        self.ui.rule_button.clicked.connect(self.open_rule_page)
        self.ui.startButton.clicked.connect(self.calc_result)
        self.ui.and_method_box.currentTextChanged.connect(self.set_and_method)
        self.ui.or_method_box.currentTextChanged.connect(self.set_or_method)

        self.ui.and_method_box.addItem("min")
        self.ui.or_method_box.addItem("max")
        self.ui.defuz_box.addItems(["centroid", "bisector", "mom", "som", "lom"])

    def openSugeno(self):
        self.close()
        self.sugeno_w = MainSugeno(self)

    def openMamdani(self):
        self.close()
        window = MainScreen()
        window.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                menu = QMenu()
                del_action = menu.addAction("Delete Variable")
                action = menu.exec_(obj.mapToGlobal(event.pos()))
                var = obj.var
                if action == del_action:
                    if var.type == "input":
                        self.input_variables.remove(var)
                        self.ui.gridLayout.removeWidget(obj)
                        self.ui.gridLayout.update()
                        obj.deleteLater()
                        # print(self.ui.gridLayout.itemAtPosition(1, 2).widget().text())
                        count = 0
                        while True:
                            if count == len(self.rules):
                                break
                            if var.name in str(self.rules[count]):
                                self.rules.pop(count)
                            else:
                                count += 1

                    elif var.type == "output":
                        self.output_variables.remove(var)
                        self.ui.output_layout.removeWidget(obj)
                        self.ui.output_layout.update()
                        obj.deleteLater()

                        count = 0
                        while True:
                            if count == len(self.rules):
                                break
                            if var.name in str(self.rules[count]):
                                self.rules.pop(count)
                            else:
                                count += 1

        return QObject.event(obj, event)

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
            "#inputButton:focus {border : 2px solid #1990EA;background-color:#D5E7F5;}  #inputButton{border: 1px solid grey; border-radius:5px;background-color:#D5E7F5;}")

        button.clicked.connect(lambda: self.update_variable_line(var, button))
        button.doubleClicked.connect(lambda: self.input_button_action(var, button))
        button.installEventFilter(self)

        # self.ui.gridLayout.addWidget(button)
        self.ui.gridLayout.addWidget(
            button,
            int((length / 3)) + 1 if length % 3 != 0 else int(length / 3),
            length % 3 if length % 3 != 0 else 3,
        )
        self.ui.gridLayout.update()

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
            "#outputButton:focus {border : 2px solid #1990EA;background-color:#FDFDBD;}  #outputButton{border: 1px solid grey; border-radius:5px;background-color:#FDFDBD;}")

        button.clicked.connect(lambda: self.update_variable_line(var, button))
        button.doubleClicked.connect(lambda: self.input_button_action(var, button))
        button.installEventFilter(self)
        self.ui.output_layout.addWidget(button)
        self.ui.output_layout.update()

    def update_variable_line(self, var, button):
        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().setStyleSheet(
                "#inputButton:focus {border : 3px solid #1990EA;background-color:#D5E7F5;}  #inputButton{border: 1px solid grey; border-radius:5px;background-color:#D5E7F5;}")

        for o in reversed(range(self.ui.output_layout.count())):
            self.ui.output_layout.itemAt(o).widget().setStyleSheet(
                "#outputButton:focus {border : 3px solid #1990EA;background-color:#FDFDBD;} #outputButton{border: 1px solid grey;border-radius:5px;background-color:#FDFDBD;}")

        self.ui.variable_name_line.setText(var.name)
        self.ui.variable_type_line.setText(var.type)
        self.ui.range_label.setText(
            "[{0} , {1}]".format(var.start if var.start is not None else "0",
                                 var.end if var.end is not None else "1"))
        if var.type == "input":

            button.setStyleSheet(
                "#inputButton:focus {border : 3px solid #1990EA;background-color:#D5E7F5;} #inputButton{border:3px solid #1990EA;border-radius:5px;background-color:#D5E7F5;}")
        else:

            button.setStyleSheet(
                "#outputButton:focus {border : 3px solid #1990EA; background-color:#FDFDBD;} #outputButton{border:3px solid green;border-radius:5px;background-color:#FDFDBD;}")

    def update_variable(self):

        new_variable_name = self.ui.variable_name_line.text()
        focus_widget = self.ui.frame.focusWidget()
        var_name = focus_widget.text()
        contains = False
        for i in self.input_variables:
            if i.name == new_variable_name:
                contains = True
        for o in self.output_variables:
            if o.name == new_variable_name:
                contains = True

        if not contains:
            focus_widget.setText(self.ui.variable_name_line.text())

            for input_var in self.input_variables:
                if var_name == input_var.name:
                    input_var.name = self.ui.variable_name_line.text()
                    if input_var.variable_ctrl is not None:
                        input_var.variable_ctrl.label = self.ui.variable_name_line.text()
                    self.update_rule(var_name)

            for output_var in self.output_variables:
                if var_name == output_var.name:
                    output_var.name = self.ui.variable_name_line.text()
                    if output_var.variable_ctrl is not None:
                        output_var.variable_ctrl.label = self.ui.variable_name_line.text()
                    self.update_rule(var_name)

    def input_button_action(self, var, button):
        self.input_w = InputScreen(self.ui, var, button, self, self.input_variables, self.output_variables)

    def open_rule_page(self):
        self.rule_w = RuleScreen(self.input_variables, self.output_variables, self.rules, self)

    def set_language(self):
        self.lang_w = LanguageScreen(self)

    def set_and_method(self, method):
        self.and_method = method

    def set_or_method(self, method):
        self.or_method = method

    def load_all(self, filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def import_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "Fuzzy Files (*.fis)")
        if filename:
            try:
                items = list(self.load_all(filename))
                self.input_variables = items[0]
                self.output_variables = items[1]
                self.rules = items[2]
                for i in range(len(self.rules)):
                    self.rule_converter(i)

                for i in reversed(range(self.ui.gridLayout.count())):
                    self.ui.gridLayout.itemAt(i).widget().setParent(None)
                for index, var_inp in enumerate(self.input_variables):
                    self.load_input_button(var_inp, index + 1)

                for i in reversed(range(self.ui.output_layout.count())):
                    self.ui.output_layout.itemAt(i).widget().setParent(None)
                for var_out in self.output_variables:
                    self.load_output_buttons(var_out)
            except Exception as ex:
                ErrorMessage("Import Error", "Error occurred during importing (Possibly unsupported file").show()
                # print("Error during unpickling object (Possibly unsupported):", ex)

    def save_data(self):
        dirname, _ = QFileDialog.getSaveFileName(self, "Choose Directory", "data", "Python Files (*.fis)")
        if dirname:
            try:
                with open(dirname, "wb") as f:
                    pickle.dump(self.input_variables, f, protocol=pickle.HIGHEST_PROTOCOL)
                    pickle.dump(self.output_variables, f, protocol=pickle.HIGHEST_PROTOCOL)
                    pickle.dump(self.rules, f, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as ex:
                ErrorMessage("File Error", ex).show()

    def update_rule(self, oldname):
        for index, rule in enumerate(self.rules):
            input_mf_labels = []
            output_mf_labels = []
            if str(rule.antecedent).__contains__("AND"):
                operator = "and"
            else:
                operator = "or"

            if str(rule.antecedent).__contains__(oldname) or str(rule.consequent).__contains__(oldname):

                for var_inp in rule.antecedent_terms:
                    term_inp = str(var_inp).split("[")[1].split("]")[0]
                    input_mf_labels.append(term_inp)

                for rule_out in rule.consequent:
                    term_out = str(rule_out).split("[")[1].split("]")[0]
                    output_mf_labels.append(term_out)

                if input_mf_labels[0] == "None":
                    inp_rule = None
                else:
                    inp_rule = self.input_variables[0].variable_ctrl[input_mf_labels[0]]

                for index, element in enumerate(input_mf_labels[1:]):
                    if element == "None":
                        pass
                    else:
                        if inp_rule is None:
                            inp_rule = self.input_variables[index + 1].variable_ctrl[element]
                        else:
                            if operator == "and":
                                inp_rule = inp_rule & self.input_variables[index + 1].variable_ctrl[element]
                            elif operator == "or":
                                inp_rule = inp_rule | self.input_variables[index + 1].variable_ctrl[element]

                if output_mf_labels[0] == "None":
                    output_rule = None
                else:
                    output_rule = self.output_variables[0].variable_ctrl[output_mf_labels[0]]

                for index, element in enumerate(output_mf_labels[1:]):
                    if element == "None":
                        pass
                    else:
                        if output_rule is None:
                            output_rule = self.output_variables[index + 1].variable_ctrl[element]
                        else:
                            output_rule = output_rule, self.output_variables[index + 1].variable_ctrl[element]

                rule = ctrl.Rule(
                    inp_rule,
                    output_rule)
                self.rules[index] = rule

    def rule_converter(self, index):
        rule = self.rules[index]
        input_mf_labels = []
        output_mf_labels = []
        if str(rule.antecedent).__contains__("AND"):
            operator = "and"
        else:
            operator = "or"

        for var_inp in rule.antecedent_terms:
            term_inp = str(var_inp).split("[")[1].split("]")[0]
            input_mf_labels.append(term_inp)

        for rule_out in rule.consequent:
            term_out = str(rule_out).split("[")[1].split("]")[0]
            output_mf_labels.append(term_out)

        if input_mf_labels[0] == "None":
            inp_rule = None
        else:
            inp_rule = self.input_variables[0].variable_ctrl[input_mf_labels[0]]

        for index_inp, element in enumerate(input_mf_labels[1:]):
            if element == "None":
                pass
            else:
                if inp_rule is None:
                    inp_rule = self.input_variables[index_inp + 1].variable_ctrl[element]
                else:
                    if operator == "and":
                        inp_rule = inp_rule & self.input_variables[index_inp + 1].variable_ctrl[element]
                    elif operator == "or":
                        inp_rule = inp_rule | self.input_variables[index_inp + 1].variable_ctrl[element]

        if output_mf_labels[0] == "None":
            output_rule = None
        else:
            output_rule = self.output_variables[0].variable_ctrl[output_mf_labels[0]]

        for index_out, element in enumerate(output_mf_labels[1:]):
            if element == "None":
                pass
            else:
                if output_rule is None:
                    output_rule = self.output_variables[index_out + 1].variable_ctrl[element]
                else:
                    output_rule = output_rule, self.output_variables[index_out + 1].variable_ctrl[element]

        rule = ctrl.Rule(
            inp_rule,
            output_rule)

        self.rules[index] = rule

    def calc_result(self):
        # brake0 = np.zeros_like(self.output_variables[0].variable)
        #
        # out_brake = np.fmax(self.rule_w.rules["dusuk"], self.rule_w.rules["orta"], self.rule_w.rules['yuksek'])
        # defuzzified = fuzz.defuzz(self.output_variables[0].variable, out_brake, "centroid")
        #
        # result = fuzz.interp_membership(self.output_variables[0].variable, out_brake, defuzzified)
        #
        # print(defuzzified)

        self.res_w = ResultScreen(self.rules, self.input_variables, self.output_variables)


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
