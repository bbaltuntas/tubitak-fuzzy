from design.rule_sugeno_python import Ui_MainWindow as InputWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
import numpy as np
from skfuzzy import control as ctrl
from error_message import ErrorMessage


class Rule:
    def __init__(self, mf_rules, constant, content, operator, function_type):
        self.mf_rules = mf_rules
        # [["var1", "dusuk", 0], ["var2", "orta",2],["var2", "None"]] old
        # "var1": ["dusuk",2] ,"var2":["None",0] new
        # self.parameters = parameters
        self.constant = constant
        self.content = content
        self.operator = operator
        self.function_type = function_type


class RuleSugeno(object):
    def __init__(self, input_variables, rules):
        super().__init__()
        self.rules: list = rules
        self.input_variables = input_variables
        self.operator = "and"
        self.function_type = "linear"
        self.sug_rul_ui = InputWindow()
        self.sugenoRuleWin = QMainWindow()

        self.sug_rul_ui.setupUi(self.sugenoRuleWin)
        self.sugenoRuleWin.show()
        self.sugenoRuleWin.setWindowTitle("Sugeno Rules")
        self.sug_rul_ui.operator_box.addItem("and")
        self.sug_rul_ui.operator_box.addItem("or")
        for rule in self.rules:
            self.sug_rul_ui.rule_list.addItem(QListWidgetItem(rule.content))

        mf_functions_to_page(self.input_variables, self.sug_rul_ui.input_mf_frame_layout)

        self.sug_rul_ui.add_rule_button.clicked.connect(self.add_rule)
        self.sug_rul_ui.delete_button.clicked.connect(self.delete_rule)
        self.sug_rul_ui.update_button.clicked.connect(self.update_rule)
        self.sug_rul_ui.rule_list.doubleClicked.connect(self.change_current_index)
        self.sug_rul_ui.operator_box.currentTextChanged.connect(self.set_operator)
        self.sug_rul_ui.function_type.currentTextChanged.connect(self.set_function_type)

    def create_rule(self):
        term_list = dict()

        input_mf_values = []
        for layout in self.sug_rul_ui.input_mf_frame_layout.children():
            mf = layout.itemAt(1).widget().selectedItems()[0].text()
            input_mf_values.append(mf)
            # input_mf_values.append(layout.itemAt(1).widget().selectedItems()[0].text())

        content = "IF "
        for index, var in enumerate(self.input_variables):
            term = input_mf_values[index]
            #   term_list.append([var.name, term])
            term_list[var.name] = [term]
            if term != "None":
                if index == 0:
                    content += "{0} is {1} ".format(var.name, term_list[var.name][0])
                elif len(content) != 3:
                    content += "{0} {1} is {2} ".format(self.operator, var.name, term_list[var.name][0])
                else:
                    content += "{0} is {1} ".format(var.name, term_list[var.name][0])

        content += "THEN Output is "
        try:
            param_text = self.sug_rul_ui.param_line.text()
            parameters = param_text.strip(" ").split(" ")
            parameters = list(filter("".__ne__, parameters))
            if self.function_type == "linear":
                if len(parameters) != len(self.input_variables) + 1:
                    ErrorMessage("Parameter Error", "Enter {0} parameters".format(len(self.input_variables) + 1)).show()
                else:
                    function = ""
                    for index, (key, value) in enumerate(term_list.items()):
                        value.append(parameters[index])
                        if parameters[index] != "0":
                            function += "{0}({1}) + ".format(parameters[index], key)
                            index += 1

                    # for index, var in enumerate(self.input_variables):
                    #     if parameters[index] != "0":
                    #         function += "{0}({1}) + ".format(parameters[index], var.name)
                    #         index += 1
                    const = parameters[len(parameters) - 1]
                    function += "{0}".format(const)
                    rule_content = "{0} {1}".format(content, function)
                    return Rule(term_list, const, rule_content, self.operator, self.function_type)
            elif self.function_type == "constant":
                if len(parameters) != 1:
                    ErrorMessage("Parameter Error", "Enter a constant value.").show()
                else:
                    for val in term_list.values():
                        val.append(0)
                    const = parameters[0]
                    function = "{0}".format(const)
                    rule_content = "{0} {1}".format(content, function)
                    return Rule(term_list, const, rule_content, self.operator, self.function_type)

        except IndexError as index_err:
            ErrorMessage("Index Error",
                         "You should enter valid number of parameters!").show()

    def add_rule(self):
        new_rule = self.create_rule()
        if new_rule is not None:
            self.rules.append(new_rule)
            item = QListWidgetItem(new_rule.content)
            self.sug_rul_ui.rule_list.addItem(item)
            self.sug_rul_ui.param_line.setText("")

    def delete_rule(self):
        selected_index = self.sug_rul_ui.rule_list.currentRow().__index__()
        self.rules.pop(selected_index)
        self.sug_rul_ui.rule_list.takeItem(selected_index)

    def update_rule(self):
        selected_index = self.sug_rul_ui.rule_list.currentRow().__index__()
        rule = self.create_rule()

        self.rules[selected_index] = rule
        self.sug_rul_ui.rule_list.item(selected_index).setText(rule.content)

    def change_current_index(self, index: QModelIndex):
        rule_index = int(index.row())
        current_rule: Rule = self.rules[rule_index]

        for k in range(self.sug_rul_ui.input_mf_frame_layout.count()):
            list_widget: QListWidget = self.sug_rul_ui.input_mf_frame_layout.itemAt(k).itemAt(1).widget()
            list_widget.setCurrentRow(0)
            for index, var_name in enumerate(current_rule.mf_rules):
                if list_widget.objectName() == var_name:
                    for j in range(list_widget.count()):
                        if list_widget.item(j).text() == current_rule.mf_rules[var_name][0]:
                            list_widget.setCurrentRow(j)
        params = ""
        if current_rule.function_type == "linear":
            params = ' '.join([str(elem[1]) for elem in current_rule.mf_rules.values()])
            params += " " + current_rule.constant
        elif current_rule.function_type == "constant":
            params = str(current_rule.constant)
        self.sug_rul_ui.param_line.setText(params)
        self.sug_rul_ui.operator_box.setCurrentText(current_rule.operator)
        self.sug_rul_ui.function_type.setCurrentText(current_rule.function_type)

    def set_operator(self, text):
        self.operator = text

    def set_function_type(self, text):
        self.function_type = text


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
