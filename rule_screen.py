from design.rule_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
import numpy as np
from skfuzzy import control as ctrl


def create_rule_content(rule):
    list_to_str = ' '.join([str(elem) for elem in rule.consequent])
    rule_content = "If " + str(rule.antecedent) + " then " + list_to_str

    return rule_content


class RuleScreen(object):
    def __init__(self, input_variables, output_variables, rules):
        super().__init__()
        self.inputVariables = input_variables
        self.outputVariables = output_variables
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

        # TODO index seçerken input sırası ile isimler uyuşmuyor
        # list widgetlarin object name ini var name yapabilirsin onun üzerinden işlem yapılabilir.
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
        if input_mf_values[0] == "None" \
                                 "":
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
                    if self.operator == "and":
                        output_rule = output_rule & self.outputVariables[index + 1].variable_ctrl[element]
                    elif self.operator == "or":
                        output_rule = output_rule | self.outputVariables[index + 1].variable_ctrl[element]
        # TODO multiple output sıkıntılı
        rule = ctrl.Rule(
            inp_rule,
            output_rule)

        return rule

    def add_rule(self):
        try:
            rule = self.create_control_rule()
            # rule_content = "If " + self.inputVariables[0].name + " is " + input_mf_values[0]
            #
            # for index, mf in enumerate(input_mf_values[1:]):
            #     rule_content = rule_content + " and " + self.inputVariables[index + 1].name + " is " + input_mf_values[
            #         index + 1]
            #
            # rule_content = rule_content + " then "
            #
            # for index, mf in enumerate(output_mf_values):
            #     rule_content = rule_content + "(" + self.outputVariables[index].name + " is " + output_mf_values[
            #         index] + ")"
            print(rule)
            self.rules.append(rule),

            # self.rules[rule] = [rule_content , [...]]
            rule_content = create_rule_content(rule)
            #########

            # rule = np.fmin(
            #     np.fmin(self.inputVariables[0].var_fit[mf_values[0]], self.inputVariables[1].var_fit[mf_values[1]]),
            #     self.outputVariables[0].membership_functions[mf_values[2]])
            #
            # self.rules[mf_values[2]] = rule

            # print(mf_values)

            item = QListWidgetItem(rule_content)
            self.rule_ui.rule_list.addItem(item)
        except ValueError:
            pass

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
        for key in inp.membership_functions:
            widget_item = QListWidgetItem(key)
            list_w.addItem(widget_item)
        v_layout = QVBoxLayout()
        layout.addLayout(v_layout)
        v_layout.addWidget(QLabel(inp.name))
        v_layout.addWidget(list_w)
