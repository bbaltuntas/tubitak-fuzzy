from design.rule_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
import numpy as np
from skfuzzy import control as ctrl


class RuleScreen(object):
    def __init__(self, input_variables, output_variables, rules):
        super().__init__()
        self.inputVariables = input_variables
        self.outputVariables = output_variables
        self.operator = "and"
        self.rules = rules
        self.rule_ui = InputWindow()
        self.inputWindow = QMainWindow()

        self.rule_ui.setupUi(self.inputWindow)
        self.inputWindow.show()

        # self.rule_ui.rule_list.clear()
        for rule in self.rules.values():
            self.rule_ui.rule_list.addItem(QListWidgetItem(rule))

        mf_functions_to_page(self.inputVariables, self.rule_ui.input_mf_frame_layout)
        mf_functions_to_page(self.outputVariables, self.rule_ui.output_mf_frame_layout)
        self.rule_ui.add_rule_button.clicked.connect(self.add_rule)
        self.rule_ui.operator_box.currentTextChanged.connect(self.set_operator)

        self.rule_ui.operator_box.addItem("and")
        self.rule_ui.operator_box.addItem("or")

    def set_operator(self, text):
        self.operator = text

    def add_rule(self):
        input_mf_values = []
        for layout in self.rule_ui.input_mf_frame_layout.children():
            input_mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        output_mf_values = []
        for layout in self.rule_ui.output_mf_frame_layout.children():
            output_mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        ########
        inp_rule = self.inputVariables[0].variable_ctrl[input_mf_values[0]]

        for index, element in enumerate(input_mf_values[1:]):
            inp_rule = inp_rule & self.inputVariables[index + 1].variable_ctrl[element]

        output_rule = self.outputVariables[0].variable_ctrl[output_mf_values[0]]
        for index, element in enumerate(output_mf_values[1:]):
            output_rule = output_rule & self.outputVariables[index + 1].variable_ctrl[element]

        rule = ctrl.Rule(
            inp_rule,
            output_rule)

        rule_content = "If " + self.inputVariables[0].name + " is " + input_mf_values[0]

        for index, mf in enumerate(input_mf_values[1:]):
            rule_content = rule_content + " and " + self.inputVariables[index + 1].name + " is " + input_mf_values[
                index + 1]

        rule_content = rule_content + " then "

        for index, mf in enumerate(output_mf_values):
            rule_content = rule_content + "(" + self.outputVariables[index].name + " is " + output_mf_values[
                index] + ")"

        self.rules[rule] = rule_content
        # self.rules[rule] = [rule_content , [...]]

        #########

        # rule = np.fmin(
        #     np.fmin(self.inputVariables[0].var_fit[mf_values[0]], self.inputVariables[1].var_fit[mf_values[1]]),
        #     self.outputVariables[0].membership_functions[mf_values[2]])
        #
        # self.rules[mf_values[2]] = rule

        # print(mf_values)

        item = QListWidgetItem(rule_content)
        self.rule_ui.rule_list.addItem(item)


def mf_functions_to_page(variable_list, layout):
    for inp in variable_list:
        list_w = QListWidget()
        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        list_w.setSizePolicy(size_policy)
        for key in inp.membership_functions:
            widget_item = QListWidgetItem(key)
            list_w.addItem(widget_item)
        v_layout = QVBoxLayout()
        layout.addLayout(v_layout)
        v_layout.addWidget(QLabel(inp.name))
        v_layout.addWidget(list_w)
