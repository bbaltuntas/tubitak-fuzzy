from design.rule_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
import numpy as np
from skfuzzy import control as ctrl


class RuleScreen(object):
    def __init__(self, input_variables, output_variables, rules):
        self.inputVariables = input_variables
        self.outputVariables = output_variables

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

    def add_rule(self):
        mf_values = []
        for layout in self.rule_ui.input_mf_frame_layout.children():
            mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        for layout in self.rule_ui.output_mf_frame_layout.children():
            mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        ########
        rule = ctrl.Rule(
            self.inputVariables[0].variable_ctrl[mf_values[0]] & self.inputVariables[1].variable_ctrl[mf_values[1]],
            self.outputVariables[0].variable_ctrl[mf_values[2]])

        rule_content = "If " + self.inputVariables[0].name + " is " + mf_values[0] + " and " + self.inputVariables[
            1].name + " is " + mf_values[1] + " then " + self.outputVariables[0].name + " is " + mf_values[2]

        self.rules[rule] = rule_content

        # self.rules.append(rule)

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
