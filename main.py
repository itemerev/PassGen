#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
from random import choice
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class App(QWidget):
    def __init__(self):
        self.num = 8
        self.symbols_to_generate = '0123456789'
        self.password = ''
        super().__init__()
        self.passgen = uic.loadUi('PassGen_Des01.ui')
        self.start()
        self.set()

    def start(self):
        self.passgen.show()

    def set(self):
        self.passgen.btn_gen.clicked.connect(lambda: self.click())

    def click(self):
        self.password = ''
        for i in range(self.num):
            self.password += choice(self.symbols_to_generate)
        self.passgen.label.setText(self.password)


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()

if __name__ == '__main__':
    main()
