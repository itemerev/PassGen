#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
import win32clipboard
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
        self.num = 3
        self.pass_gen = uic.loadUi('PassGen_Des01.ui')
        self.start()
        self.click()

    def start(self):
        self.pass_gen.show()

    def click(self):
        self.pass_gen.btn_gen.clicked.connect(lambda: self.generate())
        self.pass_gen.btn_enter.clicked.connect(lambda: self.set_num())

    def set_num(self):
        self.num += 1
        if self.num > 18:
            self.num = 3
        if self.num == 3 or self.num == 4:
            self.pass_gen.label.setText(f'Длина {self.num} символа')
        else:
            self.pass_gen.label.setText(f'Длина {self.num} символов')

    def generate(self):
        symbols_to_generate = ''
        password = ''
        if self.pass_gen.btn_123.isChecked():
            symbols_to_generate += self.digits
        if self.pass_gen.btn_ABC.isChecked():
            symbols_to_generate += self.alpha_upper
        if self.pass_gen.btn_abc.isChecked():
            symbols_to_generate += self.alpha_lower
        if self.pass_gen.btn_symbols.isChecked():
            symbols_to_generate += self.symbols
        if not self.pass_gen.btn_special.isChecked():
            temp_sym_to_gen = ''
            for c in symbols_to_generate:
                if c not in self.special:
                    temp_sym_to_gen += c
            symbols_to_generate = temp_sym_to_gen
        if symbols_to_generate:
            for i in range(self.num):
                password += choice(symbols_to_generate)
            self.pass_gen.label.setText(password)
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(password)
            win32clipboard.CloseClipboard()
        else:
            self.pass_gen.label.setText('ВЫБЕРИТЕ СИМВОЛЫ!')


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


if __name__ == '__main__':
    main()
