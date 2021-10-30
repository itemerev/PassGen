#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
from random import choice
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.digits = '0123456789'
        self.alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.symbols = '~!@#$%^&*(()<>{}[]№?'
        self.special = 'IlO01'
        self.num = 8
        self.passgen = uic.loadUi('PassGen_Des01.ui')
        self.start()
        self.click()

    def start(self):
        self.passgen.show()

    def click(self):
        self.passgen.btn_gen.clicked.connect(lambda: self.generate())

    def generate(self):
        symbols_to_generate = ''
        password = ''
        if self.passgen.btn_123.isChecked():
            symbols_to_generate += self.digits
        if self.passgen.btn_ABC.isChecked():
            symbols_to_generate += self.alpha_upper
        if self.passgen.btn_abc.isChecked():
            symbols_to_generate += self.alpha_lower
        if self.passgen.btn_symbols.isChecked():
            symbols_to_generate += self.symbols
        if not self.passgen.btn_special.isChecked():
            temp_sym_to_gen = ''
            for c in symbols_to_generate:
                if c not in self.special:
                    temp_sym_to_gen += c
            symbols_to_generate = temp_sym_to_gen
        if symbols_to_generate:
            for i in range(self.num):
                password += choice(symbols_to_generate)
            self.passgen.label.setText(password)
        else:
            self.passgen.label.setText('ВЫБЕРИТЕ СИМВОЛЫ!')


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


if __name__ == '__main__':
    main()
