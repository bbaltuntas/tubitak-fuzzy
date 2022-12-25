import sys
import traceback
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, StringVar, Button
import tkinter as tk
import copy
from kod2 import tutarlilikhesapla, agirlikhesapla
import math
import numpy as np
import customtkinter
from PIL import Image, ImageTk
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget
from screens.main_mamdani import MainScreen
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from screens.home import HomeScreen

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
agirlikresmi = None


class Kisi:
    def __init__(self):
        pass


class AltKriter:
    def __init__(self, kritersayisi, kisisayisi):
        self.kritersayisi = kritersayisi
        self.kisisayisi = kisisayisi
        self.altkriteradlari = []  # 2d
        self.cevaplar = [None for _ in range(kisisayisi)]  # 2d
        self.finalmatrisi_m = []  # 2d
        self.finalmatrisi_lu = []  # 2d
        self.tutarlilik = None

    def yazdir(self):
        print("kriter sayisi=", self.kritersayisi)
        print("kriter adlari=", self.altkriteradlari)
        print("kisi sayisi", self.kisisayisi)
        print("cevaplar", self.cevaplar)

    def verigirisi(self, kullanici, kriter):  # kriter indisi geldi
        self.girdiler = []
        df = pd.read_csv(dosyaadi + "-" + str(kullanici) + str(kriter) + ".csv", encoding='latin-1')
        pencere = customtkinter.CTkToplevel(app)
        pencere.geometry(str((self.kisisayisi + 1) * 240) + "x" + str((self.kritersayisi + 2)) * 50)
        pencere.title("KV " + str(kullanici + 1) + " - Kriter " + str(kriter + 1))
        # pencere.geometry("900x600")
        for i in range(1, self.kritersayisi):
            customtkinter.CTkLabel(pencere, text=altkriteradlari[kriter][i]).grid(row=0, column=i, padx=5, pady=5)
        for i in range(self.kritersayisi - 1):
            customtkinter.CTkLabel(pencere, text=altkriteradlari[kriter][i]).grid(row=i + 1, column=0, padx=5, pady=5)
        for i in range(self.kritersayisi - 1):
            for j in range(i + 1, self.kritersayisi):
                self.girdiler.append(ttk.Combobox(pencere, values=secenekler))
                self.girdiler[-1].set(df.iloc[i, j])
                self.girdiler[-1].grid(row=i + 1, column=j, padx=5, pady=5)
        global agirlikresmi
        agirlikresmi = customtkinter.CTkImage(Image.open("icon/fuzzyagirliklar.jpg"), size=(400, 300))
        customtkinter.CTkLabel(master=pencere, image=agirlikresmi, text="").grid(row=0, column=self.kritersayisi + 1,
                                                                                 padx=5, pady=5, rowspan=6)
        customtkinter.CTkButton(pencere, text="Kaydet",
                                command=lambda kullanici=kullanici, kriter=kriter, pencere=pencere: self.verioku(
                                    kullanici, kriter, pencere), fg_color="#5bc0de").grid(row=self.kritersayisi + 3,
                                                                                          column=0, padx=5, pady=5)

    def verioku(self, kullanici, kriter, pencere):
        df = pd.read_csv(dosyaadi + "-" + str(kullanici) + str(kriter) + ".csv", encoding='latin-1')
        x = 0
        satir = copy.deepcopy([])
        for i in range(self.kritersayisi):
            sutun = copy.deepcopy([])
            for j in range(self.kritersayisi):
                if i >= j:
                    sutun.append([1, 1, 1])
                    if i == j:
                        df.iloc[i, j] = "EÖ"
                else:
                    sutun.append(sayisallastir(self.girdiler[x].get()))
                    df.iloc[i, j] = self.girdiler[x].get()
                    x += 1
            satir.append(sutun)
        print("satir", satir)
        for i in range(self.kritersayisi):
            for j in range(self.kritersayisi):
                if i > j:
                    satir[i][j] = tersi(satir[j][i])
                    df.iloc[i, j] = tersisozel(df.iloc[j, i])
        df.to_csv(dosyaadi + "-" + str(kullanici) + str(kriter) + ".csv", index=False, encoding='latin-1')
        print("satir", satir)
        self.cevaplar[kullanici] = satir
        # self.cevaplar.append(satir)
        tutarlilik_m = np.asarray(satir)
        tutarlilik_m = tutarlilik_m[:, :, 1]
        tutarlilik_m = tutarlilikhesapla(tutarlilik_m)

        tutarlilik_lu = np.asarray(satir)
        tutarlilik_lu = tutarlilik_lu[:, :, 0] * tutarlilik_lu[:, :, 2]
        tutarlilik_lu = np.sqrt(tutarlilik_lu)
        tutarlilik_lu = tutarlilikhesapla(tutarlilik_lu, "lu")
        """
        buyukdeger = max(tutarlilik_m, tutarlilik_lu)
        if np.isnan(buyukdeger):
            buyukdeger = 0.0
        if buyukdeger<=0.1:
            customtkinter.CTkButton(tutarliliksekmesi, text=str(buyukdeger)[:5], text_font=("Calibri", 12), fg_color="#5bc0de").grid(row=6+kisisayisi+kriter, column=kullanici+1, padx=5, pady=5)
        else:
            customtkinter.CTkButton(tutarliliksekmesi, text=str(buyukdeger)[:5], text_font=("Calibri", 12), fg_color="#d9534f").grid(row=6+kisisayisi+kriter, column=kullanici+1, padx=5, pady=5)
        """
        if len(self.cevaplar) == self.kisisayisi or True:
            try:
                # matris olusturma
                carpilmismatris = [[[1, 1, 1] for i in range(self.kritersayisi)] for j in range(self.kritersayisi)]

                for i in range(self.kritersayisi):
                    for j in range(self.kritersayisi):
                        for k in range(self.kisisayisi):
                            carpilmismatris[i][j][0] *= self.cevaplar[k][i][j][0]
                            carpilmismatris[i][j][1] *= self.cevaplar[k][i][j][1]
                            carpilmismatris[i][j][2] *= self.cevaplar[k][i][j][2]
                        carpilmismatris[i][j][0] = carpilmismatris[i][j][0] ** (1.0 / self.kisisayisi)
                        carpilmismatris[i][j][1] = carpilmismatris[i][j][1] ** (1.0 / self.kisisayisi)
                        carpilmismatris[i][j][2] = carpilmismatris[i][j][2] ** (1.0 / self.kisisayisi)
                print("carpilmis matris", carpilmismatris)
                print("agirlikhesapla", agirlikhesapla(carpilmismatris, self.kritersayisi))
                for i in range(len(agirlikhesapla(carpilmismatris, self.kritersayisi))):
                    customtkinter.CTkButton(agirliksekmesiyerel,
                                            text=str(agirlikhesapla(carpilmismatris, self.kritersayisi)[i])[:5],
                                            fg_color="#5bc0de").grid(row=3 + kriter * 2, column=1 + i, padx=5, pady=5)
                    altagirliklar[kriter][i] = agirlikhesapla(carpilmismatris, self.kritersayisi)[i]
                    customtkinter.CTkButton(agirliksekmesiglobal,
                                            text=str(altagirliklar[kriter][i] * anaagirliklar[kriter])[:5],
                                            fg_color="#5bc0de").grid(row=3 + kriter * 2, column=1 + i, padx=5, pady=5)
                self.finalmatrisi_m = copy.deepcopy(carpilmismatris)
                self.finalmatrisi_lu = copy.deepcopy(carpilmismatris)
                for i in range(self.kritersayisi):
                    for j in range(self.kritersayisi):
                        self.finalmatrisi_m[i][j] = carpilmismatris[i][j][1]
                        self.finalmatrisi_lu[i][j] = math.sqrt(carpilmismatris[i][j][0] * carpilmismatris[i][j][2])
                print("carpilmis matris", carpilmismatris)
                self.tutarlilik_m = tutarlilikhesapla(self.finalmatrisi_m)
                self.tutarlilik_lu = tutarlilikhesapla(self.finalmatrisi_lu, "lu")
                print("tutarlilik_m", self.tutarlilik_m)
                print("tutarlilik_lu", self.tutarlilik_lu)
                # customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_m)[:5]).grid(row=2+kriter, column=1, padx=5, pady=5)
                # customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_lu)[:5]).grid(row=2+kriter, column=2, padx=5, pady=5)
                if self.tutarlilik_m <= 0.1:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_m)[:5], fg_color="#5bc0de").grid(
                        row=2 + kriter, column=1, padx=5, pady=5)
                else:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_m)[:5], fg_color="#d9534f").grid(
                        row=2 + kriter, column=1, padx=5, pady=5)
                if self.tutarlilik_lu <= 0.1:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_lu)[:5],
                                           fg_color="#5bc0de").grid(row=2 + kriter, column=2, padx=5, pady=5)
                else:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_lu)[:5],
                                           fg_color="#d9534f").grid(row=2 + kriter, column=2, padx=5, pady=5)
                buyukdeger = max(self.tutarlilik_m, self.tutarlilik_lu)
                if np.isnan(buyukdeger):
                    buyukdeger = 0.0
                if buyukdeger <= 0.1:
                    customtkinter.CTkButton(tutarliliksekmesi, text=str(buyukdeger)[:5], fg_color="#5bc0de").grid(
                        row=2 + kriter, column=3, padx=5, pady=5)
                else:
                    customtkinter.CTkButton(tutarliliksekmesi, text=str(buyukdeger)[:5], fg_color="#d9534f").grid(
                        row=2 + kriter, column=3, padx=5, pady=5)
            except:
                print("hata")
        pencere.destroy()


class AnaKriter:
    def __init__(self, kritersayisi, kisisayisi):
        self.kritersayisi = kritersayisi
        self.kisisayisi = kisisayisi
        self.anakriteradlari = []
        self.cevaplar = [None for _ in range(kisisayisi)]
        self.finalmatrisi_m = []
        self.finalmatrisi_lu = []
        self.tutarlilik = None
        self.altkriter = []

    def yazdir(self):
        print("kriter sayisi=", self.kritersayisi)
        print("kriter adlari=", self.anakriteradlari)
        print("alt kriterler=", self.altkriter)
        for ak in self.altkriter:
            ak.yazdir()
            print("---")

    def verigirisi(self, kullanici):
        df = pd.read_csv(dosyaadi + "-" + str(kullanici) + "A.csv", encoding='latin-1')
        self.girdiler = []
        pencere = customtkinter.CTkToplevel(app)
        pencere.geometry(str((self.kisisayisi + 1) * 240) + "x" + str((self.kritersayisi + 2)) * 50)
        pencere.title("KV " + str(kullanici + 1) + " - Ana Kriter")
        for i in range(1, self.kritersayisi):
            customtkinter.CTkLabel(pencere, text=kriteradlari[i]).grid(row=0, column=i, padx=5, pady=5)
        for i in range(self.kritersayisi - 1):
            customtkinter.CTkLabel(pencere, text=kriteradlari[i]).grid(row=i + 1, column=0, padx=5, pady=5)
        for i in range(self.kritersayisi - 1):
            for j in range(i + 1, self.kritersayisi):
                self.girdiler.append(ttk.Combobox(pencere, values=secenekler))
                self.girdiler[-1].set(df.iloc[i, j])
                self.girdiler[-1].grid(row=i + 1, column=j, padx=5, pady=5)
        global agirlikresmi
        agirlikresmi = customtkinter.CTkImage(Image.open("icon/fuzzyagirliklar.jpg"), size=(400, 300))
        customtkinter.CTkLabel(master=pencere, image=agirlikresmi, text="").grid(row=0, column=self.kritersayisi + 1,
                                                                                 padx=5, pady=5, rowspan=6)
        customtkinter.CTkButton(pencere, text="Kaydet",
                                command=lambda kullanici=kullanici, pencere=pencere: self.verioku(kullanici, pencere),
                                fg_color="#5bc0de").grid(row=self.kritersayisi + 3, column=0, padx=5, pady=5)
        customtkinter

    def verioku(self, kullanici, pencere):
        df = pd.read_csv(dosyaadi + "-" + str(kullanici) + "A.csv", encoding='latin-1')
        x = 0
        satir = copy.deepcopy([])
        for i in range(self.kritersayisi):
            sutun = copy.deepcopy([])
            for j in range(self.kritersayisi):
                if i >= j:
                    sutun.append([1, 1, 1])
                    if i == j:
                        df.iloc[i, j] = "EÖ"
                else:
                    sutun.append(sayisallastir(self.girdiler[x].get()))
                    df.iloc[i, j] = self.girdiler[x].get()
                    x += 1
            satir.append(sutun)
        print("satir", satir)
        for i in range(self.kritersayisi):
            for j in range(self.kritersayisi):
                if i > j:
                    satir[i][j] = tersi(satir[j][i])
                    df.iloc[i, j] = tersisozel(df.iloc[j, i])
        df.to_csv(dosyaadi + "-" + str(kullanici) + "A.csv", index=False, encoding='latin-1')
        print("satir", satir)
        self.cevaplar[kullanici] = satir
        # self.cevaplar.append(satir)
        tutarlilik_m = np.asarray(satir)
        print("tutarlilik_m_test", tutarlilik_m)
        tutarlilik_m = tutarlilik_m[:, :, 1]
        tutarlilik_m = tutarlilikhesapla(tutarlilik_m)

        tutarlilik_lu = np.asarray(satir)
        print("tutarlilik_lu_test", tutarlilik_lu)
        tutarlilik_lu = np.sqrt(tutarlilik_lu[:, :, 0] * tutarlilik_lu[:, :, 2])
        print("tutarlilik_lu", tutarlilik_lu)
        # tutarlilik_lu = np.sqrt(tutarlilik_lu)
        tutarlilik_lu = tutarlilikhesapla(tutarlilik_lu, "lu")
        """
        buyukdeger = max(tutarlilik_m, tutarlilik_lu)
        if np.isnan(buyukdeger):
            buyukdeger = 0.0
        if buyukdeger<=0.1:
            customtkinter.CTkLabel(tutarliliksekmesi, text=str(buyukdeger)[:5], text_font=("Calibri", 12), fg_color="#5bc0de").grid(row=5+kisisayisi, column=kullanici+1, padx=5, pady=5)
        else:
            customtkinter.CTkLabel(tutarliliksekmesi, text=str(buyukdeger)[:5], text_font=("Calibri", 12), fg_color="#d9534f").grid(row=5+kisisayisi, column=kullanici+1, padx=5, pady=5)
        """
        if len(self.cevaplar) == self.kisisayisi or True:
            try:
                # matris olusturma
                carpilmismatris = [[[1, 1, 1] for i in range(self.kritersayisi)] for j in range(self.kritersayisi)]

                for i in range(self.kritersayisi):
                    for j in range(self.kritersayisi):
                        for k in range(self.kisisayisi):
                            carpilmismatris[i][j][0] *= self.cevaplar[k][i][j][0]
                            carpilmismatris[i][j][1] *= self.cevaplar[k][i][j][1]
                            carpilmismatris[i][j][2] *= self.cevaplar[k][i][j][2]
                        carpilmismatris[i][j][0] = carpilmismatris[i][j][0] ** (1.0 / self.kisisayisi)
                        carpilmismatris[i][j][1] = carpilmismatris[i][j][1] ** (1.0 / self.kisisayisi)
                        carpilmismatris[i][j][2] = carpilmismatris[i][j][2] ** (1.0 / self.kisisayisi)
                print("carpilmis matris", carpilmismatris)
                print("agirlikhesapla", agirlikhesapla(carpilmismatris, kritersayisi))
                for i in range(len(agirlikhesapla(carpilmismatris, kritersayisi))):
                    customtkinter.CTkButton(agirliksekmesi,
                                            text=str(agirlikhesapla(carpilmismatris, kritersayisi)[i])[:5],
                                            fg_color="#5bc0de").grid(row=1, column=1 + i, padx=5, pady=5)
                    anaagirliklar[i] = agirlikhesapla(carpilmismatris, kritersayisi)[i]
                    print("ana agirliklar", anaagirliklar)
                self.finalmatrisi_m = copy.deepcopy(carpilmismatris)
                self.finalmatrisi_lu = copy.deepcopy(carpilmismatris)
                for i in range(self.kritersayisi):
                    for j in range(self.kritersayisi):
                        self.finalmatrisi_m[i][j] = carpilmismatris[i][j][1]
                        self.finalmatrisi_lu[i][j] = math.sqrt(carpilmismatris[i][j][0] * carpilmismatris[i][j][2])
                print("carpilmis matris", carpilmismatris)
                self.tutarlilik_m = tutarlilikhesapla(self.finalmatrisi_m)
                self.tutarlilik_lu = tutarlilikhesapla(self.finalmatrisi_lu, "lu")
                print("tutarlilik_m", self.tutarlilik_m)
                print("tutarlilik_lu", self.tutarlilik_lu)
                # customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_m)[:5]).grid(row=1, column=1, padx=5, pady=5)
                # customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_lu)[:5]).grid(row=1, column=2, padx=5, pady=5)
                if self.tutarlilik_m <= 0.1:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_m)[:5], fg_color="#5bc0de").grid(
                        row=1, column=1, padx=5, pady=5)
                else:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_m)[:5], fg_color="#d9534f").grid(
                        row=1, column=1, padx=5, pady=5)
                if self.tutarlilik_lu <= 0.1:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_lu)[:5],
                                           fg_color="#5bc0de").grid(row=1, column=2, padx=5, pady=5)
                else:
                    customtkinter.CTkLabel(tutarliliksekmesi, text=str(self.tutarlilik_lu)[:5],
                                           fg_color="#d9534f").grid(row=1, column=2, padx=5, pady=5)
                buyukdeger = max(self.tutarlilik_m, self.tutarlilik_lu)
                if np.isnan(buyukdeger):
                    buyukdeger = 0.0
                if buyukdeger <= 0.1:
                    customtkinter.CTkButton(tutarliliksekmesi, text=str(buyukdeger)[:5], fg_color="#5bc0de").grid(row=1,
                                                                                                                  column=3,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
                else:
                    customtkinter.CTkButton(tutarliliksekmesi, text=str(buyukdeger)[:5], fg_color="#d9534f").grid(row=1,
                                                                                                                  column=3,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
            except:
                pass
        pencere.destroy()


# style = Style(theme="litera")
# print(style.theme_names())
# master = customtkinter.CTk() #style.master
app = customtkinter.CTk()
# master.title("Ana ekran")
# master.geometry("900x600")
# master.configure(bg="red")
# master["bg"]="blue"

"""
window1 = style.master
window1.title("")
window1.geometry('1200x600')
"""
anasekme = None
sekmeler = None
yansekmeler = []
anakriter = None

kararverici = 0
kritersayisi = 0
kriteradlarialani = []
kriteradlari = []
karsilastirmaalani = []
altkritersayilarialani = []
altkritersayilari = []
altkriteradlarialani = []
altkriteradlari = []

secenekler = ["TÖZ", "ÇKÖZ", "KÖZ", "DÖZ", "EÖ", "DÖ", "KÖ", "ÇKÖ", "TÖ"]


def tersi(a):
    tersa = []
    for i in range(len(a)):
        tersa.append(1 / a[len(a) - 1 - i])
    return tersa


def tersisozel(a):
    if a == "TÖ":
        return "TÖZ"
    elif a == "ÇKÖ":
        return "ÇKÖZ"
    elif a == "KÖ":
        return "KÖZ"
    elif a == "DÖ":
        return "DÖZ"
    elif a == "TÖZ":
        return "TÖ"
    elif a == "ÇKÖZ":
        return "ÇKÖ"
    elif a == "KÖZ":
        return "KÖ"
    elif a == "DÖZ":
        return "DÖ"
    else:
        return "EÖ"


def sayisallastir(metin):
    # print(metin)
    if metin == "TÖZ":
        return [1.0 / 9, 1.0 / 9, 1.0 / 7]
    elif metin == "ÇKÖZ":
        return [1.0 / 9, 1.0 / 7, 1.0 / 5]
    elif metin == "KÖZ":
        return [1.0 / 7, 1.0 / 5, 1.0 / 3]
    elif metin == "DÖZ":
        return [1.0 / 5, 1.0 / 3, 1.0]
    elif metin == "EÖ":
        return [1.0, 1.0, 1.0]
    elif metin == "DÖ":
        return [1.0, 3.0, 5.0]
    elif metin == "KÖ":
        return [3.0, 5.0, 7.0]
    elif metin == "ÇKÖ":
        return [5.0, 7.0, 9.0]
    elif metin == "TÖ":
        return [7.0, 9.0, 9.0]


def karsilastirmalarioku():
    for i in range(len(karsilastirmaalani)):
        print("karsilastirmaalani.i.get", karsilastirmaalani[i].get())
    kritermatrisi = [[[[1, 1, 1] for i in range(kritersayisi)] for j in range(kritersayisi)] for k in
                     range(kararverici)]
    altkritermatrisilistesi = []
    for i in range(kritersayisi):
        eklenecek = [[[1, 1, 1] for i in range(altkritersayilari[i])] for j in range(altkritersayilari[i])]
        altkritermatrisilistesi.append(eklenecek)
    altkritermatrisilistesi = [copy.deepcopy(altkritermatrisilistesi) for i in range(kararverici)]
    # print(kritermatrisi)
    # print(altkritermatrisilistesi)
    x = 0
    for i in range(kararverici):
        for j in range(kritersayisi):
            for k in range(j + 1, kritersayisi):
                kritermatrisi[i][j][k] = karsilastirmaalani[x].get()
                kritermatrisi[i][j][k] = sayisallastir(kritermatrisi[i][j][k].get())
                kritermatrisi[i][k][j] = tersi(kritermatrisi[i][j][k].get())
                x += 1
    for i in range(kararverici):
        for j in range(len(altkritersayilari)):
            for k in range(len(altkritermatrisilistesi[i][j])):
                for l in range(k + 1, len(altkritermatrisilistesi[i][j])):
                    altkritermatrisilistesi[i][j][k][l] = karsilastirmaalani[x].get()
                    altkritermatrisilistesi[i][j][k][l] = sayisallastir(altkritermatrisilistesi[i][j][k][l])
                    altkritermatrisilistesi[i][j][l][k] = tersi(altkritermatrisilistesi[i][j][k][l])
                    x += 1
    print("kriter matrisi", kritermatrisi)
    print("alt kriter matris listesi", altkritermatrisilistesi)

    tutarlilik = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(tutarlilik, text="Tutarlilik")
    sekmeler.pack(expand=True, fill="both")

    customtkinter.CTkLabel(tutarlilik, text="Genel tutarlılık").grid(row=0, column=0, padx=5, pady=5)
    for i in range(len(kriteradlari)):
        customtkinter.CTkLabel(tutarlilik, text=kriteradlari[i]).grid(row=1 + i, column=0, padx=5, pady=5)

    carpilmismatris = [[[1, 1, 1] for i in range(kritersayisi)] for j in range(kritersayisi)]
    for i in range(kritersayisi):
        for j in range(kritersayisi):
            for k in range(kararverici):
                carpilmismatris[i][j][0] *= kritermatrisi[k][i][j][0]
                carpilmismatris[i][j][1] *= kritermatrisi[k][i][j][1]
                carpilmismatris[i][j][2] *= kritermatrisi[k][i][j][2]
            carpilmismatris[i][j][0] = carpilmismatris[i][j][0] ** (1 / kararverici)
            carpilmismatris[i][j][1] = carpilmismatris[i][j][1] ** (1 / kararverici)
            carpilmismatris[i][j][2] = carpilmismatris[i][j][2] ** (1 / kararverici)
    print("carpilmis matris", carpilmismatris)
    for i in range(kritersayisi):
        for j in range(kritersayisi):
            carpilmismatris[i][j] = (carpilmismatris[i][j][0] + 2 * carpilmismatris[i][j][1] + carpilmismatris[i][j][
                2]) / 4
    print("carpilmis matris", carpilmismatris)
    customtkinter.CTkLabel(tutarlilik, text=str(tutarlilikhesapla(carpilmismatris))[:5]).grid(row=0, column=1, padx=5,
                                                                                              pady=5)


def altkriteradlandir():
    for i in range(len(altkriteradlarialani)):
        altkriteradlari.append(altkriteradlarialani[i].get())
    print("alt kriter adlari", altkriteradlari)
    x = 0
    for i in range(len(anakriter.anakriteradlari)):
        for j in range(anakriter.altkriter[i].kritersayisi):
            anakriter.altkriter[i].altkriteradlari.append(altkriteradlari[x])
            x += 1


def adlandir():
    global anakriter, kritersayisi, kararverici, sekmeler, anasekme
    anakriter = AnaKriter(kritersayisi=kritersayisi, kisisayisi=kararverici)
    for i in range(len(kriteradlarialani)):
        kriteradlari.append(kriteradlarialani[i].get())
        anakriter.anakriteradlari.append(kriteradlarialani[i].get())
        print(kriteradlari[i], end=", ")
        altkritersayilari.append(int(altkritersayilarialani[i].get()))
        anakriter.altkriter.append(AltKriter(kritersayisi=int(altkritersayilarialani[i].get()), kisisayisi=kararverici))
        print(altkritersayilari[i], end=", ")
    # for i in range()
    for i in range(kritersayisi):
        customtkinter.CTkLabel(anasekme, text=kriteradlari[i]).grid(row=7 + i, column=0, padx=5, pady=5)
        for j in range(altkritersayilari[i]):
            altkriteradlarialani.append(customtkinter.CTkEntry(anasekme))
            altkriteradlarialani[-1].grid(row=7 + i, column=j + 1, padx=5, pady=5)
        adlandirmabutonu = customtkinter.CTkButton(anasekme, text="Adlandir", command=altkriteradlandir)
        adlandirmabutonu.grid(row=8 + kritersayisi, column=0, padx=5, pady=5)

    for i in range(kararverici):
        # customtkinter.CTkLabel(window1, text="Kriter adlari").grid(row=6+i, column=0, padx=5, pady=5)
        yansekmeler.append(customtkinter.CTkFrame(sekmeler))
        yansekmeler[-1].pack(fill='both', expand=True)
        sekmeler.add(yansekmeler[-1], text=str(i + 1))
        for j in range(kritersayisi - 1):
            for k in range(j + 1, kritersayisi):
                karsilastirmaalani.append(
                    ttk.Combobox(yansekmeler[i], values=secenekler, width=5))  # customtkinter.CTkEntry(yansekmeler[i]))
                karsilastirmaalani[-1].grid(row=1 + j, column=k, padx=5, pady=5)
    for i in range(kararverici):
        for j in range(kritersayisi - 1):
            customtkinter.CTkLabel(yansekmeler[i], text=kriteradlari[j]).grid(row=1 + j, column=0, padx=5, pady=5)
            customtkinter.CTkLabel(yansekmeler[i], text=kriteradlari[j + 1]).grid(row=0, column=1 + j, padx=5, pady=5)
    kumulatif = 0
    for i in range(kararverici):
        for j in range(kritersayisi):
            altkritersayisi = altkritersayilari[j]
            kumulatif += altkritersayisi
            for k in range(altkritersayisi - 1):
                for l in range(k + 1, altkritersayisi):
                    karsilastirmaalani.append(ttk.Combobox(yansekmeler[i], values=secenekler,
                                                           width=5))  # customtkinter.CTkEntry(yansekmeler[i]))
                    karsilastirmaalani[-1].grid(row=5 + kritersayisi + k + kumulatif, column=l, padx=5, pady=5)
    customtkinter.CTkButton(yansekmeler[-1], text="Hesapla", command=karsilastirmalarioku).grid(
        row=8 + kritersayisi + kumulatif, column=0, padx=5, pady=5)


def altkriterverigirisi(kisi, kriter):
    anakriter.altkriter[kriter].verigirisi(kisi, kriter)
    butonlistesi[kisisayisi + kisi * kritersayisi + kriter].configure(fg_color="#d9534f")


def anakriterverigirisi(kisi):
    global butonlistesi
    anakriter.verigirisi(kisi)
    anakriter.yazdir()
    butonlistesi[kisi].configure(fg_color="#d9534f")


anaagirliklar = []
altagirliklar = []


def verigirisibutonlariolustur():
    global anaagirliklar, altagirliklar
    anaagirliklar = []
    altagirliklar = []
    for i in range(kritersayisi):
        anaagirliklar.append(1)
    for i in range(kritersayisi):
        dummy = []
        for j in range(altkritersayilari[i]):
            dummy.append(1)
        altagirliklar.append(dummy)
    print("ana agirliklar", anaagirliklar)
    print("alt agirliklar", altagirliklar)
    global butonlistesi
    butonlistesi = []
    for i in range(kisisayisi):
        customtkinter.CTkButton(verisekmesi, text="KV " + str(i + 1), fg_color="#428bca").grid(row=0, column=i + 1,
                                                                                               padx=5, pady=5)
    customtkinter.CTkButton(verisekmesi, text="Ana kriter", fg_color="#428bca").grid(row=1, column=0, padx=5, pady=5)
    x = 2
    for ka in kriteradlari:
        customtkinter.CTkButton(verisekmesi, text=ka, fg_color="#428bca").grid(row=x, column=0, padx=5, pady=5)
        x += 1
    for i in range(kisisayisi):
        butonlistesi.append(
            customtkinter.CTkButton(verisekmesi, text="Veri girişi", command=lambda i=i: anakriterverigirisi(i),
                                    fg_color="#5bc0de"))
        butonlistesi[-1].grid(row=1, column=1 + i, padx=5, pady=5)
    for i in range(kisisayisi):
        for j in range(kritersayisi):
            if altkritersayilari[j] > 1:
                butonlistesi.append(customtkinter.CTkButton(verisekmesi, text="Veri girişi",
                                                            command=lambda i=i, j=j: altkriterverigirisi(i, j),
                                                            fg_color="#5bc0de"))
            else:
                butonlistesi.append(customtkinter.CTkLabel(verisekmesi, text=""))
            butonlistesi[-1].grid(row=2 + j, column=1 + i, padx=5, pady=5)
    # print(i, j)


def altkriteradlarikaydet(pencere):
    global altkriteradlari, anakriter

    if pencere != None:
        for i in range(kritersayisi):
            for j in range(len(altkriteradlari[i])):
                altkriteradlari[i][j] = altkriteradlari[i][j].get()
        print("altkriteradlari", altkriteradlari)
        anakriter = AnaKriter(kritersayisi=kritersayisi, kisisayisi=kisisayisi)
        for i in range(kritersayisi):
            anakriter.altkriter.append(AltKriter(kritersayisi=len(altkriteradlari[i]), kisisayisi=kisisayisi))
        customtkinter.CTkButton(tutarliliksekmesi, text="Ana kriter").grid(row=1, column=0, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık CR m").grid(row=0, column=1, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık CR g").grid(row=0, column=2, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık CR genel").grid(row=0, column=3, padx=5, pady=5)
        # customtkinter.CTkLabel(tutarliliksekmesi, text="Tutarlılık lu").grid(row=0, column=2, padx=5, pady=5)
        customtkinter.CTkButton(agirliksekmesi, text="Ana kriter", ).grid(row=1, column=0, padx=5, pady=5)
        for i in range(kritersayisi):
            customtkinter.CTkButton(tutarliliksekmesi, text=kriteradlari[i]).grid(row=2 + i, column=0, padx=5, pady=5)
            customtkinter.CTkButton(agirliksekmesi, text=kriteradlari[i], ).grid(row=0, column=1 + i, padx=5, pady=5)
            for j in range(len(altkriteradlari[i])):
                customtkinter.CTkButton(agirliksekmesiyerel, text=altkriteradlari[i][j], ).grid(row=2 + 2 * i,
                                                                                                column=1 + j, padx=5,
                                                                                                pady=5)
                customtkinter.CTkButton(agirliksekmesiglobal, text=altkriteradlari[i][j], ).grid(row=2 + 2 * i,
                                                                                                 column=1 + j, padx=5,
                                                                                                 pady=5)
            customtkinter.CTkButton(agirliksekmesiyerel, text=kriteradlari[i], ).grid(row=3 + 2 * i, column=0, padx=5,
                                                                                      pady=5)
            customtkinter.CTkButton(agirliksekmesiglobal, text=kriteradlari[i], ).grid(row=3 + 2 * i, column=0, padx=5,
                                                                                       pady=5)
        for i in range(kisisayisi):
            customtkinter.CTkButton(tutarliliksekmesi, text="KV " + str(i + 1)).grid(row=2 + kritersayisi, column=i + 1,
                                                                                     padx=5, pady=5)
            customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık").grid(row=3 + kritersayisi, column=i + 1,
                                                                               padx=5, pady=5)
        # customtkinter.CTkLabel(tutarliliksekmesi, text="Tutarlılık lu").grid(row=3+kritersayisi, column=2*i+2, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Ana kriter").grid(row=4 + kritersayisi, column=0, padx=5,
                                                                           pady=5)
        for i in range(kritersayisi):
            customtkinter.CTkButton(tutarliliksekmesi, text=kriteradlari[i]).grid(row=5 + i + kritersayisi, column=0,
                                                                                  padx=5, pady=5)

        verigirisibutonlariolustur()
    # pencere.destroy()
    else:
        anakriter = AnaKriter(kritersayisi=kritersayisi, kisisayisi=kisisayisi)
        for i in range(kritersayisi):
            anakriter.altkriter.append(AltKriter(kritersayisi=len(altkriteradlari[i]), kisisayisi=kisisayisi))
        customtkinter.CTkButton(tutarliliksekmesi, text="Ana kriter").grid(row=1, column=0, padx=5, pady=5)
        # customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık").grid(row=0, column=1, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık CR m").grid(row=0, column=1, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık CR g").grid(row=0, column=2, padx=5, pady=5)
        customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık CR genel").grid(row=0, column=3, padx=5, pady=5)
        # customtkinter.CTkLabel(tutarliliksekmesi, text="Tutarlılık lu").grid(row=0, column=2, padx=5, pady=5)
        customtkinter.CTkButton(agirliksekmesi, text="Ana kriter", ).grid(row=1, column=0, padx=5, pady=5)
        for i in range(kritersayisi):
            customtkinter.CTkButton(tutarliliksekmesi, text=kriteradlari[i]).grid(row=2 + i, column=0, padx=5, pady=5)
            customtkinter.CTkButton(agirliksekmesi, text=kriteradlari[i], ).grid(row=0, column=1 + i, padx=5, pady=5)
            for j in range(len(altkriteradlari[i])):
                customtkinter.CTkButton(agirliksekmesiyerel, text=altkriteradlari[i][j], ).grid(row=2 + 2 * i,
                                                                                                column=1 + j, padx=5,
                                                                                                pady=5)
                customtkinter.CTkButton(agirliksekmesiglobal, text=altkriteradlari[i][j], ).grid(row=2 + 2 * i,
                                                                                                 column=1 + j, padx=5,
                                                                                                 pady=5)
            customtkinter.CTkButton(agirliksekmesiyerel, text=kriteradlari[i], ).grid(row=3 + 2 * i, column=0, padx=5,
                                                                                      pady=5)
            customtkinter.CTkButton(agirliksekmesiglobal, text=kriteradlari[i], ).grid(row=3 + 2 * i, column=0, padx=5,
                                                                                       pady=5)
        for i in range(kisisayisi):
            pass
        # customtkinter.CTkButton(tutarliliksekmesi, text="KV "+str(i+1)).grid(row=2+kritersayisi, column=i+1, padx=5, pady=5)
        # customtkinter.CTkButton(tutarliliksekmesi, text="Tutarlılık").grid(row=3+kritersayisi, column=i+1, padx=5, pady=5)
        # customtkinter.CTkLabel(tutarliliksekmesi, text="Tutarlılık lu").grid(row=3+kritersayisi, column=2*i+2, padx=5, pady=5)
        # customtkinter.CTkButton(tutarliliksekmesi, text="Ana kriter").grid(row=4+kritersayisi, column=0, padx=5, pady=5)
        for i in range(kritersayisi):
            pass
        # customtkinter.CTkButton(tutarliliksekmesi, text=kriteradlari[i]).grid(row=5+i+kritersayisi, column=0, padx=5, pady=5)

        verigirisibutonlariolustur()


def altkriteradlaripenceresi():
    pencere = customtkinter.CTkFrame(anasekme)
    pencere.grid(row=5, column=2, padx=5, pady=5)
    # pencere.title("Alt kriter adları")
    # pencere.geometry("700x700")
    global altkritersayilari
    for i in range(kritersayisi):
        dummy = []
        for j in range(altkritersayilari[i]):
            dummy.append(customtkinter.CTkEntry(pencere, height=20, ))
            dummy[-1].grid(row=i, column=j + 1, padx=1, pady=1)
        altkriteradlari.append(dummy)
        customtkinter.CTkLabel(pencere, text=kriteradlari[i], height=20, ).grid(row=i, column=0, padx=1, pady=1)
    customtkinter.CTkButton(anasekme, text="Kaydet", command=lambda pencere=pencere: altkriteradlarikaydet(pencere),
                            fg_color="#5bc0de").grid(row=5, column=3, padx=5, pady=5)


def altkritersayilarikaydet():
    global altkritersayilari
    for i in range(kritersayisi):
        altkritersayilari[i] = int(altkritersayilari[i].get())
        if altkritersayilari[i] == 0:
            altkritersayilari[i] = 1
    print("altkritersayilari", altkritersayilari)
    altkriteradlaripenceresi()


# pencere.destroy()

def altkritersayisipenceresi():
    pencere = customtkinter.CTkFrame(anasekme)
    pencere.grid(row=4, column=2, padx=5, pady=5)
    # pencere.title("Alt kriter sayıları")
    # pencere.geometry("700x700")
    global altkritersayilari
    for i in range(kritersayisi):
        altkritersayilari.append(customtkinter.CTkEntry(pencere, height=20, ))
        altkritersayilari[-1].grid(row=i, column=1, padx=1, pady=1)
        customtkinter.CTkLabel(pencere, text=kriteradlari[i], height=20, ).grid(row=i, column=0, padx=1, pady=1)
    customtkinter.CTkButton(anasekme, text="Kaydet", command=altkritersayilarikaydet, fg_color="#5bc0de").grid(row=4,
                                                                                                               column=3,
                                                                                                               padx=5,
                                                                                                               pady=5)


def kriteradlarikaydet():
    global kriteradlari
    for i in range(kritersayisi):
        kriteradlari[i] = kriteradlari[i].get()
    print("kriteradlari", kriteradlari)
    altkritersayisipenceresi()


# pencere.destroy()

def kriteradlaripenceresi():
    pencere = customtkinter.CTkFrame(anasekme)
    pencere.grid(row=3, column=2, padx=5, pady=5)
    # pencere.title("Kriter adları")
    # pencere.geometry("700x700")
    global kriteradlari
    for i in range(kritersayisi):
        kriteradlari.append(customtkinter.CTkEntry(pencere, height=20, ))
        kriteradlari[-1].grid(row=i, column=0, padx=1, pady=1)
    customtkinter.CTkButton(anasekme, text="Kaydet", command=kriteradlarikaydet, fg_color="#5bc0de").grid(row=3,
                                                                                                          column=3,
                                                                                                          padx=5,
                                                                                                          pady=5)


def kritersayisikaydet():
    global kritersayisi
    kritersayisi = int(kritersayisi.get())
    print("kritersayisi", kritersayisi)
    kriteradlaripenceresi()


# pencere.destroy()

def kritersayisipenceresi():
    # pencere = customtkinter.CTkToplevel(app)
    # pencere.title("Kriter sayısı")
    # pencere.geometry("700x700")
    global kritersayisi
    kritersayisi = customtkinter.CTkEntry(anasekme)
    kritersayisi.grid(row=2, column=2, padx=5, pady=5)
    customtkinter.CTkButton(anasekme, text="Kaydet", command=kritersayisikaydet, fg_color="#5bc0de").grid(row=2,
                                                                                                          column=3,
                                                                                                          padx=5,
                                                                                                          pady=5)


def kisisayisikaydet():
    global kisisayisi
    kisisayisi = int(kisisayisi.get())
    print("kisisayisi", kisisayisi)
    kritersayisipenceresi()


# pencere.destroy()

def kisisayisipenceresi():
    # pencere = customtkinter.CTkToplevel(app)
    # pencere.title("Karar verici sayısı")
    # pencere.geometry("700x700")
    global kisisayisi
    kisisayisi = customtkinter.CTkEntry(anasekme)
    kisisayisi.grid(row=1, column=2, padx=5, pady=5)
    customtkinter.CTkButton(anasekme, text="Kaydet", command=kisisayisikaydet, fg_color="#5bc0de").grid(row=1, column=3,
                                                                                                        padx=5, pady=5)


dosyaadi = "yok"


def kaydet():
    global dosyaadi
    from tkinter.filedialog import asksaveasfile
    f = asksaveasfile(mode="w")
    # f = open(filename, "w")
    f.write(str(kisisayisi) + "\n")
    f.write(str(kritersayisi) + "\n")
    for i in range(len(kriteradlari)):
        f.write(str(kriteradlari[i]) + "\n")
    for i in altkritersayilari:
        f.write(str(i) + "\n")
    for i in altkriteradlari:
        for j in i:
            f.write(j + "\n")
    from pathlib import Path
    dosyaadi = Path(f.name).stem
    f.close()
    for i in range(kisisayisi):
        # ana kriter
        dosya = [["EÖ" for j in range(kritersayisi)] for k in range(kritersayisi)]
        df = pd.DataFrame(dosya, columns=kriteradlari)
        print(df)
        df.to_csv(dosyaadi + "-" + str(i) + "A.csv", index=False, encoding='latin-1')
        # alt kriterler

        for j in range(kritersayisi):
            dosya = [["EÖ" for j in range(altkritersayilari[j])] for k in range(altkritersayilari[j])]
            df = pd.DataFrame(dosya, columns=altkriteradlari[j])
            print(df)
            df.to_csv(dosyaadi + "-" + str(i) + str(j) + ".csv", index=False, encoding='latin-1')
    anasekme.destroy()


def problemyukle():
    global kisisayisi, kritersayisi, kriteradlari, altkritersayilari, altkriteradlari, dosyaadi
    from tkinter.filedialog import askopenfile
    f = askopenfile(mode="r")
    icerik = [line.strip() for line in f.readlines()]  # f.readlines()
    print(icerik)
    kisisayisi = int(icerik[0])
    kritersayisi = int(icerik[1])
    for i in range(kritersayisi):
        kriteradlari.append(icerik[i + 2])
    for i in range(kritersayisi):
        altkritersayilari.append(int(icerik[2 + kritersayisi + i]))
    x = 2 + kritersayisi * 2
    for i in range(kritersayisi):
        dummy = []
        for j in range(altkritersayilari[i]):
            dummy.append(icerik[x])
            x += 1
        altkriteradlari.append(dummy)
    print("yüklendi")
    print(kisisayisi, kritersayisi, kriteradlari, altkritersayilari, altkriteradlari)
    # verigirisibutonlariolustur()
    altkriteradlarikaydet(None)
    from pathlib import Path
    dosyaadi = Path(f.name).stem
    f.close()


def anasekmeac():
    global anasekme, sekmeler, verisekmesi, tutarliliksekmesi, agirliksekmesi, agirliksekmesiyerel, agirliksekmesiglobal
    anasekme = customtkinter.CTkToplevel(app)  # customtkinter.CTkFrame(sekmeler)
    anasekme.title("Problem oluştur")

    kisisayisipenceresi()
    customtkinter.CTkButton(anasekme, text="Karar verici sayısı", compound="top", image=kisiresmi, command=None,
                            fg_color="#5bc0de").grid(row=1, column=1, padx=5,
                                                     pady=5)  # pack(side="top",expand=True,fill="both", padx=10, pady=10)#
    customtkinter.CTkButton(anasekme, text="Ana Kriter sayısı", compound="top", image=numararesmi, command=None,
                            fg_color="#5bc0de").grid(row=2, column=1, padx=5,
                                                     pady=5)  # pack(expand=True,fill="both", padx=10, pady=10)#
    customtkinter.CTkButton(anasekme, text="Ana Kriter adları", compound="top", image=listeresmi, command=None,
                            fg_color="#5bc0de").grid(row=3, column=1, padx=5,
                                                     pady=5)  # pack(expand=True,fill="both", padx=10, pady=10)#
    customtkinter.CTkButton(anasekme, text="Alt kriter sayısı", compound="top", image=numararesmi, command=None,
                            fg_color="#5bc0de").grid(row=4, column=1, padx=5,
                                                     pady=5)  # .pack(expand=True,fill="both", padx=10, pady=10)#
    customtkinter.CTkButton(anasekme, text="Alt kriter adları", compound="top", image=listeresmi, command=None,
                            fg_color="#5bc0de").grid(row=5, column=1, padx=5,
                                                     pady=5)  # .pack(expand=True,fill="both", padx=10, pady=10)#
    customtkinter.CTkButton(anasekme, text="Kaydet", compound="top", image=kaydetresmi, command=kaydet,
                            fg_color="#5bc0de").grid(row=6, column=1, padx=5,
                                                     pady=5)  # .pack(expand=True,fill="both", padx=10, pady=10)#


"""
verisekmesi = Toplevel()#customtkinter.CTkFrame(sekmeler)
verisekmesi.withdraw()
tutarliliksekmesi = Toplevel()#customtkinter.CTkFrame(sekmeler)
tutarliliksekmesi.withdraw()
agirliksekmesi = Toplevel()#customtkinter.CTkFrame(sekmeler)
agirliksekmesi.withdraw()
"""

kisiresmi = customtkinter.CTkImage(Image.open("icon/people.png"), size=(20, 20))

listeresmi = customtkinter.CTkImage(Image.open("icon/list.png"), size=(20, 20))
numararesmi = customtkinter.CTkImage(Image.open("icon/sayi.png"), size=(20, 20))
kaydetresmi = customtkinter.CTkImage(Image.open("icon/kaydet.png"), size=(20, 20))
"""
def verigirispenceresi():
	verisekmesi.deiconify()

def tutarlilikpenceresi():
	tutarliliksekmesi.deiconify()

def agirlikpenceresi():
	agirliksekmesi.deiconify()
"""


def anaekran():
    global anasekme, sekmeler, verisekmesi, tutarliliksekmesi, agirliksekmesi, agirliksekmesiyerel, agirliksekmesiglobal
    modul11 = customtkinter.CTkToplevel()
    # modul11.geometry("800x500")
    # modul11.attributes('-fullscreen',True)
    width = modul11.winfo_screenwidth()
    height = modul11.winfo_screenheight()
    modul11.geometry("%dx%d" % (width - 100, height - 100))
    modul11.title("Modul 1.1: KPI'ların Ağırlıklandırılması (FAHP)")
    sekmeler = ttk.Notebook(modul11)

    girissekmesi = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(girissekmesi, text="Giriş")
    girisaciklamasi = """
	Yeni: Yeni bir problem oluşturur.
	Aç: Önceden oluşturulan problemi açar.
	Veri girişi: Kriterlerin karşılaştırılmasını sağlar.
	Tutarlılık hesabı: Tutarlılık hesabını gösterir.
	Ağırlık değerleri: Ağırlık değerlerini gösterir.
	"""
    aciklama = customtkinter.CTkLabel(girissekmesi, text=girisaciklamasi, )
    aciklama.pack(side="right", expand=False, fill="none")

    # open =  ImageTk.PhotoImage(Image.open(PATH + r"/icon/open.png").resize((50, 50)))#PhotoImage(file = r"icon\open.png")
    open = customtkinter.CTkImage(Image.open("icon/open.png"), size=(20, 20))

    new = customtkinter.CTkImage(Image.open("icon/addfile.png"), size=(20, 20))

    veriresmi = PhotoImage(file=r"icon\addfile50.png")
    tutarlilikresmi = PhotoImage(file=r"icon\addfile50.png")
    agirlikresmi = PhotoImage(file=r"icon\addfile50.png")
    yukari = customtkinter.CTkFrame(girissekmesi)
    yukari.pack(side="left", expand=True, fill="both")
    customtkinter.CTkButton(yukari, text="Aç", compound="top", image=open, command=problemyukle,
                            fg_color="#5bc0de").pack(side="right", expand=True, fill="none", padx=10, pady=10)
    customtkinter.CTkButton(yukari, text="Yeni", compound="top", image=new, command=anasekmeac,
                            fg_color="#5bc0de").pack(side="left", expand=True, fill="none", padx=10, pady=10)

    # asagi=customtkinter.CTkFrame(girissekmesi)
    # asagi.pack(side="bottom", expand=True, fill="both")
    # customtkinter.CTkButton(asagi, text="Veri girişi", image=veriresmi, compound= "top", command=verigirispenceresi).pack(side="top", expand=True, fill="none", padx=10, pady=10)
    # customtkinter.CTkButton(asagi, text="Ağırlık değerleri", image=agirlikresmi, compound= "top", command=agirlikpenceresi).pack(side="bottom", expand=True, fill="none", padx=10, pady=10)
    # customtkinter.CTkButton(asagi, text="Tutarlılık hesabı", image=tutarlilikresmi, compound= "top", command=tutarlilikpenceresi).pack(side="bottom", expand=True, fill="none", padx=10, pady=10)

    # sekmeler.add(anasekme, text="Ana ekran")
    sekmeler.pack(expand=True, fill="both")

    verisekmesi = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(verisekmesi, text="Veri girişi")

    tutarliliksekmesi = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(tutarliliksekmesi, text="Tutarlılık")

    agirliksekmesi = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(agirliksekmesi, text="Ana kriter ağırlıkları")

    agirliksekmesiyerel = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(agirliksekmesiyerel, text="Yerel ağırlıklar")

    agirliksekmesiglobal = customtkinter.CTkFrame(sekmeler)
    sekmeler.add(agirliksekmesiglobal, text="Global ağırlıklar")


# master.mainloop()
# girisekraniresmi = PhotoImage(Image.open(PATH +r"\\resim.png"))
# print(type(girisekraniresmi))
def modul1ekrani():
    modul1 = customtkinter.CTkToplevel()
    modul1.geometry("500x500")
    modul1.title("Modul 1: Makine Kritiklik Oranının Belirlenmesi")
    customtkinter.CTkLabel(master=modul1, text="Modul 1: Makine Kritiklik Oranının Belirlenmesi", ).pack(padx=10,
                                                                                                         pady=20)
    customtkinter.CTkButton(master=modul1,
                            text="Modül 1.1: \nKPI'ların ağırlıklandırılması (FAHP)",
                            command=anaekran,
                            fg_color="#5bc0de",
                            ).pack(padx=10, pady=10, fill="both")
    customtkinter.CTkButton(master=modul1,
                            text="Modül 1.2: \nMakine kritiklik oranlarının belirlenmesi (FIS)",
                            command=openFIS,
                            fg_color="#5bc0de",
                            ).pack(padx=10, pady=10, fill="both")


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QApplication.quit()


def openFIS():
    sys.excepthook = excepthook
    app = QApplication([])
    app.setWindowIcon(QIcon(":/icons/icons/settings.png"))
    # window = MainScreen()
    window = HomeScreen()
    window.show()
    ret = app.exec_()


def girisekrani():
    """
    global anasekme, sekmeler, verisekmesi, tutarliliksekmesi, agirliksekmesi
    giris=Notebook(master)
    customtkinter.CTkButton(giris, text="A").grid(row=0, column=0, padx=5, pady=5)
    master.mainloop()
    """

    # giris = ttk.Notebook(master)

    app.geometry("800x600")

    app.title("Akıllı Bakım Karar Destek Sistemi")
    app.configure(bg="#f9f9f9")
    frame1 = customtkinter.CTkFrame(master=app,
                                    width=600,
                                    height=500,
                                    corner_radius=10)
    frame1.pack(padx=10, pady=10, side="left", fill="both")
    frame2 = customtkinter.CTkFrame(master=app,
                                    width=300,
                                    height=500,
                                    corner_radius=10)
    frame2.pack(padx=10, pady=10, side="right", fill="both")

    customtkinter.CTkLabel(master=frame2, text="Modüller", ).pack(padx=10, pady=20)
    customtkinter.CTkButton(master=frame2,
                            text="Modül 1:\nMakine kritiklik\noranının belirlenmesi",
                            command=modul1ekrani,
                            fg_color="#5bc0de",
                            ).pack(padx=10, pady=10, fill="both")
    customtkinter.CTkButton(master=frame2,
                            text="Modül 2:\nKritik makinelere yönelik\ndetaylı analiz",
                            command=None,
                            fg_color="#5bc0de",
                            ).pack(padx=10, pady=10, fill="both")
    customtkinter.CTkButton(master=frame2,
                            text="Modül 3:\nKestirimci bakım\nuygulaması",
                            command=None,
                            fg_color="#5bc0de",
                            ).pack(padx=10, pady=10, fill="both")
    # customtkinter.CTkButton(frame1, image=kisiresmi).pack(expand=True,fill="both", padx=10, pady=10)
    girisekraniresmi = customtkinter.CTkImage(Image.open("resim.png"), size=(400, 400))
    customtkinter.CTkLabel(master=frame1, text="", image=girisekraniresmi).pack(padx=10, pady=10, expand=False,
                                                                                fill="none")
    # label1.image = resim
    customtkinter.CTkLabel(master=frame1, text="AKILLI BAKIM KARAR\nDESTEK SİSTEMİ", ).pack(padx=100, pady=10)
    customtkinter.CTkLabel(master=frame1, text="Erciyes Üniversitesi Endüstri Mühendisliği Bölümü", ).pack(padx=10,
                                                                                                           pady=10,
                                                                                                           side=BOTTOM,
                                                                                                           fill="both")
    app.mainloop()
    pass


girisekrani()
# girisekrani()
