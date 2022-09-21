from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import variable
from design.design_python import Ui_MainWindow as MainWindow
from flow_layout import FlowLayout
from skfuzzy import control as ctrl
from input_screen import InputScreen
from rule_screen import RuleScreen
import sys
import traceback


class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_variables = []
        self.output_variables = []
        self.rules = {}
        self.ui = MainWindow()
        self.ui.setupUi(self)

        # self.ui.gridLayout = FlowLayout(self.ui.gridFrame)
        # self.ui.gridFrame.setLayout(self.ui.gridLayout)
        self.add_input_variable()
        self.add_output_variable()

        self.input_w = None
        self.rule_w = None

        self.set_actions()

    def set_actions(self):
        self.ui.actionInput.triggered.connect(self.add_input_variable)
        self.ui.actionOutput.triggered.connect(self.add_output_variable)

        self.ui.variable_name_line.editingFinished.connect(self.update_variable)
        self.ui.var_value.editingFinished.connect(self.set_input_value)

        self.ui.rule_button.clicked.connect(self.open_rule_page)
        self.ui.startButton.clicked.connect(self.calc_result)

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

                     
                    elif var.type == "output":
                        self.output_variables.remove(var)
                        self.ui.output_layout.removeWidget(obj)
                        self.ui.output_layout.update()
                        obj.deleteLater()

        return QObject.event(obj, event)

    def add_input_variable(self):
        length = len(self.input_variables)
        var = variable.Variable("input", ("input" + str(length + 1)))
        self.input_variables.append(var)
        length += 1
        # print(length)
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
        self.ui.gridLayout.addWidget(
            button,
            int((length / 3)) + 1 if length % 3 != 0 else int(length / 3),
            length % 3 if length % 3 != 0 else 3,
        )
        self.ui.gridLayout.update()
        # self.ui.gridLayout.update()

    def add_output_variable(self):
        length = len(self.output_variables)
        var = variable.Variable("output", ("output" + str(length + 1)), )
        self.output_variables.append(var)
        length += 1
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
        button.doubleClicked.connect(lambda: self.input_button_action(var, button))
        button.installEventFilter(self)
        self.ui.output_layout.addWidget(button)
        self.ui.output_layout.update()

    def update_variable_line(self, var, button):
        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().setStyleSheet(
                "#inputButton:focus {border : 3px solid green;}  #inputButton{border: 1px solid grey; border-radius:5px}")

        for o in reversed(range(self.ui.output_layout.count())):
            self.ui.output_layout.itemAt(o).widget().setStyleSheet(
                "#outputButton:focus {border : 3px solid green;} #outputButton{border: 1px solid grey;border-radius:5px}")

        self.ui.variable_name_line.setText(var.name)
        self.ui.variable_type_line.setText(var.type)
        self.ui.var_value.setText(str(var.input) if var.input is not None else "")

        if var.type == "input":
            self.ui.var_value.setDisabled(False)
            button.setStyleSheet(
                "#inputButton:focus {border : 3px solid green;} #inputButton{border:3px solid green;border-radius:5px}")
        else:
            self.ui.var_value.setDisabled(True)
            button.setStyleSheet(
                "#outputButton:focus {border : 3px solid green;} #outputButton{border:3px solid green;border-radius:5px}")

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

            for output_var in self.output_variables:
                if var_name == output_var.name:
                    output_var.name = self.ui.variable_name_line.text()

    def set_input_value(self):
        value = self.ui.var_value.text()
        focus_widget = self.ui.frame.focusWidget()
        var_name = focus_widget.text()

        try:
            for input_var in self.input_variables:
                if var_name == input_var.name:
                    input_var.input = int(value)
        except ValueError:
            print("Hata")

    def input_button_action(self, var, button):
        self.input_w = InputScreen(self.ui, var, self.input_variables, button)

    def open_rule_page(self):

        self.rule_w = RuleScreen(self.input_variables, self.output_variables, self.rules)

    def calc_result(self):
        # brake0 = np.zeros_like(self.output_variables[0].variable)
        #
        # out_brake = np.fmax(self.rule_w.rules["dusuk"], self.rule_w.rules["orta"], self.rule_w.rules['yuksek'])
        # defuzzified = fuzz.defuzz(self.output_variables[0].variable, out_brake, "centroid")
        #
        # result = fuzz.interp_membership(self.output_variables[0].variable, out_brake, defuzzified)
        #
        # print(defuzzified)

        tipping_ctrl = ctrl.ControlSystem(self.rules.keys())
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

        for index in range(len(self.input_variables)):
            tipping.input[self.input_variables[index].name] = self.input_variables[index].input

        # Crunch the numbers
        tipping.compute()

        for index in range(len(self.output_variables)):
            print(tipping.output[self.output_variables[index].name])


class InputGraph(FigureCanvas):

    def __init__(self, fig, parent=None):
        self.fig = fig
        super().__init__(self.fig)


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


def fuzzy_ctrl():
    model = ctrl.Antecedent(np.arange(2002, 2013, 1), 'model')
    km = ctrl.Antecedent(np.arange(0, 101, 1), 'km')
    fiyat = ctrl.Consequent(np.arange(0, 41, 1), 'fiyat')

    # Auto-membership function population is possible with .automf(3, 5, or 7)

    model.automf(3)
    km.automf(3)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    fiyat['poor'] = fuzz.trimf(fiyat.universe, [0, 0, 20])
    fiyat['average'] = fuzz.trimf(fiyat.universe, [0, 20, 40])
    fiyat['good'] = fuzz.trimf(fiyat.universe, [20, 40, 40])

    rule1 = ctrl.Rule(model['poor'] & km['good'], fiyat['poor'])
    rule2 = ctrl.Rule(model['average'] & km['average'], fiyat['average'])
    rule3 = ctrl.Rule(model['good'] & km['poor'], fiyat['good'])

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    tipping.input['model'] = 2005
    tipping.input['km'] = 100

    # Crunch the numbers
    tipping.compute()

    print(tipping.output['fiyat'])


def fuzzy():
    model = np.arange(2002, 2013, 1)
    km = np.arange(0, 101, 1)

    fiyat = np.arange(0, 41, 1)

    model_dusuk = mf.trimf(model, [2002, 2002, 2007])
    model_orta = mf.trimf(model, [2002, 2007, 2012])
    model_yuksek = mf.trimf(model, [2007, 2012, 2012])

    km_dusuk = mf.trimf(km, [0, 0, 50])
    km_orta = mf.trimf(km, [0, 50, 100])
    km_yuksek = mf.trimf(km, [50, 100, 100])

    fiyat_dusuk = mf.trimf(fiyat, [0, 0, 20])
    fiyat_orta = mf.trimf(fiyat, [0, 20, 40])
    fiyat_yuksek = mf.trimf(fiyat, [20, 40, 40])

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(6, 10))

    ax0.plot(model, model_dusuk, "r", linewidth=2, label="Düşük")
    ax0.plot(model, model_orta, "g", linewidth=2, label="Orta")
    ax0.plot(model, model_yuksek, "b", linewidth=2, label="Yüksek")
    ax0.set_title("Pedal Basıncı")
    ax0.legend()

    ax1.plot(km, km_dusuk, "r", linewidth=2, label="Düşük")
    ax1.plot(km, km_orta, "g", linewidth=2, label="Orta")
    ax1.plot(km, km_yuksek, "b", linewidth=2, label="Yüksek")
    ax1.set_title("Araç Hızı")
    ax1.legend()

    ax2.plot(fiyat, fiyat_dusuk, "r", linewidth=2, label="Zayıf")
    ax2.plot(fiyat, fiyat_orta, "g", linewidth=2, label="Orta")
    ax2.plot(fiyat, fiyat_yuksek, "b", linewidth=2, label="Yuksek")

    ax2.set_title("Fren")
    ax2.legend()

    plt.show()

    input_model = 2005
    input_km = 100

    # Üyelik derecelerinin hesaplanması

    model_fit_dusuk = fuzz.interp_membership(model, model_dusuk, input_model)
    model_fit_orta = fuzz.interp_membership(model, model_orta, input_model)
    model_fit_yuksek = fuzz.interp_membership(model, model_yuksek, input_model)

    km_fit_dusuk = fuzz.interp_membership(km, km_dusuk, input_km)
    km_fit_orta = fuzz.interp_membership(km, km_orta, input_km)
    km_fit_yuksek = fuzz.interp_membership(km, km_yuksek, input_km)

    # Kuralların oluşturulması

    rule1 = np.fmin(np.fmin(model_fit_dusuk, km_fit_yuksek), fiyat_dusuk)
    rule2 = np.fmin(np.fmin(model_fit_orta, km_fit_orta), fiyat_orta)
    rule3 = np.fmin(np.fmin(model_fit_yuksek, km_fit_dusuk), fiyat_yuksek)

    # Birleşim kümelerinin oluşturulması

    out_strong = rule3
    out_med = rule2
    out_poor = rule1

    # Veri görselleştirme

    brake0 = np.zeros_like(fiyat)

    fig, ax0 = plt.subplots(figsize=(7, 4))
    ax0.fill_between(fiyat, brake0, out_poor, facecolor="r", alpha=0.7)
    ax0.plot(fiyat, fiyat_dusuk, "r", linestyle="--")
    ax0.fill_between(fiyat, brake0, out_strong, facecolor="g", alpha=0.7)
    ax0.plot(fiyat, fiyat_orta, "g", linestyle="--")
    ax0.set_title("Fren Çıkışı")

    plt.show()

    # Durulaştırma

    out_brake = np.fmax(out_poor, out_med, out_strong)

    defuzzified = fuzz.defuzz(fiyat, out_brake, "centroid")

    result = fuzz.interp_membership(fiyat, out_brake, defuzzified)

    # Sonuç

    print("(Fren)Çıkış Değeri:", defuzzified)

    # Veri görselleştirme

    fig, ax0 = plt.subplots(figsize=(7, 4))

    ax0.plot(fiyat, fiyat_dusuk, "b", linewidth=0.5, linestyle="--")
    ax0.plot(fiyat, fiyat_orta, "g", linewidth=0.5, linestyle="--")
    ax0.fill_between(fiyat, brake0, out_brake, facecolor="Orange", alpha=0.7)
    ax0.plot([defuzzified, defuzzified], [0, result], "k", linewidth=1.5, alpha=0.9)
    ax0.set_title("Ağırlık Merkezi ile Durulaştırma")

    plt.show()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


# fuzzy_ctrl()

sys.excepthook = excepthook
app = QApplication([])
window = MainScreen()
window.show()
ret = app.exec_()
sys.exit(ret)
