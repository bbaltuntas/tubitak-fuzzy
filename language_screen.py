from PyQt5.QtWidgets import *
from design.language_python import Ui_Dialog as LanguageWindow
import googletrans
import textblob
import json


class LanguageScreen(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.lan_ui = LanguageWindow()
        self.lanWindow = QDialog()

        self.lan_ui.setupUi(self.lanWindow)
        self.lanWindow.setWindowTitle("Languages")
        self.languages = googletrans.LANGUAGES
        self.language_list = list(self.languages.values())

        self.lan_ui.lang_list_widget.addItems(self.language_list)
        self.lan_ui.lang_list_widget.currentTextChanged.connect(self.choose_language)
        self.lan_ui.set_lan_button.clicked.connect(self.set_language)
        self.lanWindow.exec()

    def choose_language(self, language):
        self.lan_ui.selected_lan_text.setText(language)

    def set_language(self):
        language = self.lan_ui.lang_list_widget.selectedItems()[0].text()

        with open('config.json', 'r') as f:
            config = json.load(f)

        # edit the data

        config['lan'] = language

        # write it back to the file
        with open('config.json', 'w') as f:
            json.dump(config, f)
        self.parent.config = config
        QApplication.quit()
