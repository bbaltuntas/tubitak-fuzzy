from design.rule_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
import numpy as np
from skfuzzy import control as ctrl
from error_message import ErrorMessage


def create_rule_content(rule):
    list_to_str = ' '.join([str(elem) for elem in rule.consequent])
    rule_content = "If " + str(rule.antecedent) + " then " + list_to_str

    return rule_content


class RuleScreen(object):
    def __init__(self, input_variables, output_variables, rules, parent):
        super().__init__()
        self.inputVariables = input_variables
        self.outputVariables = output_variables
        self.parent = parent
        self.operator = "and"
        self.rules: list = rules
        self.rule_ui = InputWindow()
        self.inputWindow = QMainWindow()

        self.rule_ui.setupUi(self.inputWindow)
        self.inputWindow.show()
        self.inputWindow.setWindowTitle("Mamdani Rules")
        # self.rule_ui.rule_list.clear()
        for rule in self.rules:
            self.rule_ui.rule_list.addItem(QListWidgetItem(create_rule_content(rule)))

        mf_functions_to_page(self.inputVariables, self.rule_ui.input_mf_frame_layout)
        mf_functions_to_page(self.outputVariables, self.rule_ui.output_mf_frame_layout)

        self.rule_ui.add_rule_button.clicked.connect(self.add_rule)
        self.rule_ui.operator_box.currentTextChanged.connect(self.set_operator)
        self.rule_ui.rule_list.doubleClicked.connect(self.change_current_index)
        self.rule_ui.delete_button.clicked.connect(self.delete_rule)
        self.rule_ui.update_button.clicked.connect(self.update_rule)

        self.rule_ui.operator_box.addItem("and")
        self.rule_ui.operator_box.addItem("or")

    def change_current_index(self, index: QModelIndex):
        rule_index = int(index.row())
        current_rule: ctrl.Rule = self.rules[rule_index]

        for k in range(self.rule_ui.input_mf_frame_layout.count()):
            list_widget: QListWidget = self.rule_ui.input_mf_frame_layout.itemAt(k).itemAt(1).widget()
            list_widget.setCurrentRow(0)
            for i, rule in enumerate(current_rule.antecedent_terms):
                var_name = str(rule).split("[")[0]
                term = str(rule).split("[")[1].split("]")[0]
                if list_widget.objectName() == var_name:
                    for j in range(list_widget.count()):
                        if list_widget.item(j).text() == term:
                            list_widget.setCurrentRow(j)

        for i, rule in enumerate(current_rule.consequent):
            term = str(rule).split("[")[1].split("]")[0]
            list_widget: QListWidget = self.rule_ui.output_mf_frame_layout.itemAt(i).itemAt(1).widget()
            for j in range(list_widget.count()):
                if list_widget.item(j).text() == term:
                    list_widget.setCurrentRow(j)

    def set_operator(self, text):
        self.operator = text

    def create_control_rule(self):
        input_mf_values = []
        for layout in self.rule_ui.input_mf_frame_layout.children():
            input_mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        output_mf_values = []
        for layout in self.rule_ui.output_mf_frame_layout.children():
            output_mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        ########
        if input_mf_values[0] == "None":
            inp_rule = None
        else:
            inp_rule = self.inputVariables[0].variable_ctrl[input_mf_values[0]]

        for index, element in enumerate(input_mf_values[1:]):
            if element == "None":
                pass
            else:
                if inp_rule is None:
                    inp_rule = self.inputVariables[index + 1].variable_ctrl[element]
                else:
                    if self.operator == "and":
                        inp_rule = inp_rule & self.inputVariables[index + 1].variable_ctrl[element]
                    elif self.operator == "or":
                        inp_rule = inp_rule | self.inputVariables[index + 1].variable_ctrl[element]

        if output_mf_values[0] == "None":
            output_rule = None
        else:
            output_rule = self.outputVariables[0].variable_ctrl[output_mf_values[0]]

        for index, element in enumerate(output_mf_values[1:]):
            if element == "None":
                pass
            else:
                if output_rule is None:
                    output_rule = self.outputVariables[index + 1].variable_ctrl[element]
                else:
                    output_rule = output_rule, self.outputVariables[index + 1].variable_ctrl[element]

        rule = ctrl.Rule(
            inp_rule,
            output_rule)

        return rule

    def add_rule(self):
        rule = self.create_control_rule()

        self.rules.append(rule)

        rule_content = create_rule_content(rule)

        item = QListWidgetItem(rule_content)
        self.rule_ui.rule_list.addItem(item)

    def delete_rule(self):
        selected_index = self.rule_ui.rule_list.currentRow().__index__()
        self.rules.pop(selected_index)
        self.rule_ui.rule_list.takeItem(selected_index)

    def update_rule(self):
        selected_index = self.rule_ui.rule_list.currentRow().__index__()
        rule = self.create_control_rule()

        self.rules[selected_index] = rule
        self.rule_ui.rule_list.item(selected_index).setText(create_rule_content(rule))


def mf_functions_to_page(variable_list, layout):
    for inp in variable_list:
        list_w = QListWidget()
        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        list_w.setSizePolicy(size_policy)
        list_w.addItem(QListWidgetItem("None"))
        list_w.setObjectName(inp.name)
        for key in inp.mf_function_value:
            widget_item = QListWidgetItem(key)
            list_w.addItem(widget_item)
        v_layout = QVBoxLayout()
        layout.addLayout(v_layout)
        v_layout.addWidget(QLabel(inp.name))
        v_layout.addWidget(list_w)
