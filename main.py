from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import numpy as np
import graphics as gp
import skfuzzy as fuzz
import skfuzzy.membership as mf
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from design_python import Ui_MainWindow as MainWindow
from input_python import Ui_MainWindow as InputWindow


class loadUi_example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.inputButton.clicked.connect(self.input_button_action)

        self.inp_ui = InputWindow()
        self.inputWindow = QMainWindow()

        """      
        self.graph = InputGraph()
        """

    def input_button_action(self):
        self.inp_ui.setupUi(self.inputWindow)
        self.inputWindow.show()

        self.inp_ui.graph_layout.addWidget(self.graph)


"""
class InputGraph(FigureCanvas):

    def __init__(self, parent=None):
        self.fig, self.plot = gp.draw_graph()
        super().__init__(self.fig)

        self.plot.plot()
      
        self.fig, self.ax = plt.subplots(1, dpi=150, figsize=(5, 5), facecolor='white')
       super().__init__(self.fig)
        self.fig.suptitle("Graph", size=9)
        np.random.seed(50)
        y = np.random.randn(5).cumsum()
        self.ax = plt.axes()
        plt.plot(y, color='magenta')
      



"""

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

ax0.plot(model, model_dusuk, 'r', linewidth=2, label='Düşük')
ax0.plot(model, model_orta, 'g', linewidth=2, label='Orta')
ax0.plot(model, model_yuksek, 'b', linewidth=2, label='Yüksek')
ax0.set_title('Pedal Basıncı')
ax0.legend()

ax1.plot(km, km_dusuk, 'r', linewidth=2, label='Düşük')
ax1.plot(km, km_orta, 'g', linewidth=2, label='Orta')
ax1.plot(km, km_yuksek, 'b', linewidth=2, label='Yüksek')
ax1.set_title('Araç Hızı')
ax1.legend()

ax2.plot(fiyat, fiyat_dusuk, 'r', linewidth=2, label='Zayıf')
ax2.plot(fiyat, fiyat_orta, 'g', linewidth=2, label='Orta')
ax2.plot(fiyat, fiyat_yuksek, 'b', linewidth=2, label='Yuksek')

ax2.set_title('Fren')
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
ax0.fill_between(fiyat, brake0, out_poor, facecolor='r', alpha=0.7)
ax0.plot(fiyat, fiyat_dusuk, 'r', linestyle='--')
ax0.fill_between(fiyat, brake0, out_strong, facecolor='g', alpha=0.7)
ax0.plot(fiyat, fiyat_orta, 'g', linestyle='--')
ax0.set_title('Fren Çıkışı')

plt.show()

# Durulaştırma

out_brake = np.fmax(out_poor, out_med, out_strong)

defuzzified = fuzz.defuzz(fiyat, out_brake, 'centroid')

result = fuzz.interp_membership(fiyat, out_brake, defuzzified)

# Sonuç

print("(Fren)Çıkış Değeri:", defuzzified)

# Veri görselleştirme

fig, ax0 = plt.subplots(figsize=(7, 4))

ax0.plot(fiyat, fiyat_dusuk, 'b', linewidth=0.5, linestyle='--')
ax0.plot(fiyat, fiyat_orta, 'g', linewidth=0.5, linestyle='--')
ax0.fill_between(fiyat, brake0, out_brake, facecolor='Orange', alpha=0.7)
ax0.plot([defuzzified, defuzzified], [0, result], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Ağırlık Merkezi ile Durulaştırma')

plt.show()

app = QApplication([])
window = loadUi_example()
window.show()
app.exec_()
