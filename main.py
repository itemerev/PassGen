#!/urs/bin/python3
# -*- coding: utf-8 -*-

import sys
import win32clipboard
from random import choice, randrange
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.digits = '0123456789'
        self.alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.symbols = '~!@#$%^&*(()+-<>{}[]№?'
        self.special = 'IlO01'
        self.num = 3
        self.password = ''  # сгенерированный пароль (по-умолчанию пустая строка)
        self.login = ''
        self.login_password = {}
        self.name_login_password = {}
        self.pass_gen = uic.loadUi('PassGen_Des01.ui')
        self.start()
        self.click()

    def start(self):
        self.pass_gen.show()

    def click(self):
        self.pass_gen.btn_gen.clicked.connect(lambda: self.generate())
        self.pass_gen.btn_enter.clicked.connect(lambda: self.set_num())
        self.pass_gen.btn_login.clicked.connect(lambda: self.set_login())
        self.pass_gen.btn_save.clicked.connect(lambda: self.save_password())

    def save_password(self):
        name = self.pass_gen.lineEdit.text()
        self.name_login_password = {name: self.login_password}
        with open('results.txt', 'a', encoding='utf-8') as save_file:
            print(f'{name}:', file=save_file)
            print(f'    Логин - {self.login}: Пароль - {self.name_login_password.get(name).get(self.login)}', file=save_file)
            print('', file=save_file)

    def set_login(self):
        self.login = self.pass_gen.lineEdit.text()
        self.login_password = {self.login: self.password}
        self.pass_gen.label.setText('Чтобы сохранить пароль, введите его имя и нажмите SAVE')

    def set_num(self):
        self.num = int(self.pass_gen.lineEdit.text())
        if self.num > 18:
            self.num = 18
        if self.num < 3:
            self.num = 3
        if self.num == 3 or self.num == 4:
            self.pass_gen.label.setText(f'Длина пароля {self.num} символа')
        else:
            self.pass_gen.label.setText(f'Длина пароля {self.num} символов')

    def generate(self):
        symbols_to_generate = ''  # строка, содержащая все символы из которых будет генерироваться пароль
        symbols_list = []

        # Проверка включенных кнопок для выбора символов пароля
        if self.pass_gen.btn_123.isChecked():
            symbols_to_generate += self.digits
            symbols_list.append('digits')
        if self.pass_gen.btn_ABC.isChecked():
            symbols_to_generate += self.alpha_upper
            symbols_list.append('ABC')
        if self.pass_gen.btn_abc.isChecked():
            symbols_to_generate += self.alpha_lower
            symbols_list.append('abc')
        if self.pass_gen.btn_symbols.isChecked():
            symbols_to_generate += self.symbols
            symbols_list.append('symbols')
        if not self.pass_gen.btn_special.isChecked():
            temp_sym_to_gen = ''
            for c in symbols_to_generate:
                if c not in self.special:
                    temp_sym_to_gen += c
            symbols_to_generate = temp_sym_to_gen

        # Если выбраны символы для генерации пароля, то пароль генерируется
        if symbols_to_generate:
            self.password = ''
            for i in range(self.num):  # Генерируется пароль из заданного количества символов
                self.password += choice(symbols_to_generate)

            # Проверка включенных кнопок для обязательных символов (+)
            if self.pass_gen.btn_add_123.isChecked():
                temp = False
                for c in self.password:
                    if c in self.digits:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + str(randrange(2, 9))
            if self.pass_gen.btn_add_ABC.isChecked():
                temp = False
                for c in self.password:
                    if c in self.alpha_upper:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('ABCDEFGHJKLMNPRSTUVWXYZ')
            if self.pass_gen.btn_add_abc.isChecked():
                temp = False
                for c in self.password:
                    if c in self.alpha_lower:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('abcdefghijkmnopqrstuvwxyz')
            if self.pass_gen.btn_add_symbols.isChecked():
                temp = False
                for c in self.password:
                    if c in self.symbols:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('~!@#$%^&*(()+-<>{}[]№?')

            self.pass_gen.lineEdit.setText(self.password)  # Показать пароль в окне lineEdit
            self.pass_gen.label.setText(f'Чтобы задать логин для {self.password}, введите логин и нажмите LOGIN')

            # Копирование сгенерированного пароля в буфер обмена
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(self.password)
            win32clipboard.CloseClipboard()

        else:
            self.pass_gen.label.setText('ВЫБЕРИТЕ СИМВОЛЫ!')


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


if __name__ == '__main__':
    main()
