#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
from random import choice
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class App(QWidget):
    def __init__(self):
        self.digits = '0123456789'
        self.alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.symbols = '~!@#$%^&*(()<>{}[]№?'
        self.special = 'IlO01'
        self.num = 8
        super().__init__()
        self.passgen = uic.loadUi('PassGen_Des01.ui')
        self.start()
        self.set()

    def start(self):
        self.passgen.show()

    def set(self):
        self.passgen.btn_gen.clicked.connect(lambda: self.click())

    def click(self):
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
        for i in range(self.num):
            password += choice(symbols_to_generate)
        self.passgen.label.setText(password)


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


if __name__ == '__main__':
    main()
