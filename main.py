#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
from random import choice
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.passgen = uic.loadUi('PassGen_Des01.ui')
        self.start()

    def start(self):
        self.passgen.show()


class Btn_action(QWidget):
    def __init__(self):
        self.num = 1
        self.password = ''
        self.symbols_for_generate = ''
        self.digits = '0123456789'
        super().__init__()
        self.passgen = uic.loadUi('PassGen_Des01.ui')
        self.set()
        
    def set(self):
        self.passgen.btn_ent.clicked.connect(lambda: self.generate())

    def generate(self):
        for i in range(self.num):
            self.password += choice(self.symbols_for_generate)
        self.passgen.label.setText(self.password)


def main():
    app = QApplication(sys.argv)
    ex = App()
    btn_act = Btn_action()
    app.exec_()


if __name__ == '__main__':
    main()
