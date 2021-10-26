#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.passgen = uic.loadUi('PassGen_Des01.ui')
        self.start()
        self.set()

    def start(self):
        self.passgen.show()

    def set(self):
        self.passgen.btn_123.clicked.connect(lambda: self.click())

    def click(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
