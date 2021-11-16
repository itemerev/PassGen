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
        
        # Переменные, содержащие символы для генерации пароля
        self.digits = '0123456789'
        self.alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.symbols = '~!@#$%^&*(()+-<>{}[]№?'
        self.special = 'IlO01'
        
        self.data = ''  # Переменная, определяющая будет ли создаваться список ответов при поиске сохраненного значения
        self.answer_list = []  # Список ответов, найденных при поиске сохраненного значения
        
        # Переменные, необходимые для генерации пароля:
        self.num = 3  # Длина пароля в символах
        self.password = ''  # Сгенерированный пароль (по-умолчанию пустая строка)
        self.login = ''  # Сохраненный логин (по-умолчанию пустая строка)
        self.login_password = {}  # Сохраненный словарь - связка логин: пароль (по-умолчанию пустой словарь)
        self.name_login_password = {}  # Сохраненный словарь - связка имя: логин: пароль (по-умолчанию пустой словарь)
        
        self.pass_gen = uic.loadUi('PassGen_Des01.ui')  # Импорт графического интерфейса
        
        self.start()
        self.click()

    def start(self):
        # Запускает (показывает) окно приложения
        self.pass_gen.show()

    def click(self):
        # Вызывает действие при клике на кнопку
        self.pass_gen.btn_gen.clicked.connect(lambda: self.generate())
        self.pass_gen.btn_enter.clicked.connect(lambda: self.set_num())
        self.pass_gen.btn_login.clicked.connect(lambda: self.set_login())
        self.pass_gen.btn_save.clicked.connect(lambda: self.save_password())
        self.pass_gen.btn_find.clicked.connect(lambda: self.find_data())

    def find_data(self):
        # Метод, позволяющий выполнить поиск введенного значения (имя, логин или пароль) в сохраненных данных
        
        request = self.pass_gen.lineEdit.text()  # Сохранение введенного запроса в переменную
        
        # Если поиск запрашиваемого значения выполняется в первый раз, то есть переменная self.data не ссылается на текущий запрос, то все найденные результаты сохраняются в список ответов.
        if self.data != request:
            with open('results.txt', 'r', encoding='utf-8') as read_file:
                name_password = ''
                for row in read_file:
                    if row == '':
                        continue
                    elif '    ' not in row:
                        name_password = row[:-2]
                        if request in row:
                            self.answer_list.append(f'Значение "{request}" найдено, как имя для записи: {read_file.readline().strip()}')
                    else:
                        if request in row[12:13 + len(request)]:
                            self.answer_list.append(f'Значение "{request}" найдено, как логин для записи {name_password}: {row[4:]}')
                        elif request in row[22 + len(request):]:
                            self.answer_list.append(f'Значение "{request}" найдено, как пароль для записи {name_password}: {row[4:]}')
            self.data = self.pass_gen.lineEdit.text()
        
        # Если список ответов имеет хотя бы одну запись, то в строку подсказок выводиться последняя, с удалением ее из списка (при повторном клике будет выведена следующая по-порядку с конца запись, если она имеется в списке)
        if len(self.answer_list) > 0:
            self.pass_gen.label.setText(self.answer_list.pop())
        
        # Если записей в списке ответов больше нет (или не было), то в строку подсказок выводиться информация, что запрос не найден, а поиск запрашиваемого значения обнуляется, то есть можно повторно сформировать список ответов
        else:
            self.pass_gen.label.setText(f'Значение "{request}" не найдено в сохранённых паролях!')
            self.data = ''

    def save_password(self):
        # Метод, сохраняющий под указанным имененем сгенерированный пароль вместе с логином в файл
        
        # Введенное имя сохраняется в переменную name, а также в словарь self.name_login_password в качестве ключа к связке "логин: пароль"
        name = self.pass_gen.lineEdit.text()
        self.name_login_password = {name: self.login_password}
        
        # Сохранение словаря "имя: логин: пароль" в файл 
        with open('results.txt', 'a', encoding='utf-8') as save_file:
            print(f'{name}:', file=save_file)
            print(f'    Логин - {self.login}: Пароль - {self.name_login_password.get(name).get(self.login)}', file=save_file)
            print('', file=save_file)
            
        self.pass_gen.label.setText('Пароль сохранен в файл')

    def set_login(self):
        # Метод, сохраняющий введеный логин в переменную self.login и в словарь self.login_password "логин: пароль" в качестве ключа к паролю
        self.login = self.pass_gen.lineEdit.text()
        self.login_password = {self.login: self.password}
        self.pass_gen.label.setText('Чтобы сохранить пароль, введите его имя и нажмите SAVE')

    def set_num(self):
        # Метод, задающий длину пароля от 3-х до 18-ти символов
        if self.pass_gen.lineEdit.text().isdigit():  # Проверка, что введенный текст является числом
            self.num = int(self.pass_gen.lineEdit.text())
            if self.num > 18:
                self.num = 18
            if self.num < 3:
                self.num = 3
            if self.num == 3 or self.num == 4:
                self.pass_gen.label.setText(f'Длина пароля {self.num} символа')
            else:
                self.pass_gen.label.setText(f'Длина пароля {self.num} символов')
        else:
            self.pass_gen.label.setText('Введите число от 3-х до 18-ти!')

    def generate(self):
        # Метод, генерирующий пароль учитывая включенные кнопки
        symbols_to_generate = ''  # переменная, которые содержит все символы из которых будет генерироваться пароль (по умолчанию пустая строка)

        # Проверка включенных кнопок для выбора символов из которых будет генерироваться пароль
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

        # Если переменная, содержащая символы для генерации пароля не пустая, то пароль генерируется
        if symbols_to_generate:
            self.password = ''
            for i in range(self.num):  # Генерируется пароль из заданного количества символов
                self.password += choice(symbols_to_generate)

            # Проверка включенных кнопок для обязательных символов (+), а также наличие обязательных символов в сгенерированном пароле
            if self.pass_gen.btn_add_123.isChecked():  # Для кнопки "123"
                temp = False
                for c in self.password:
                    if c in self.digits:
                        temp = True
                        break
                if not temp:  # Если обязательных символов в пароле нет, то он (обязательный символ) добавляется в конец сгенерированного пароля, удаляя первый символ.
                    self.password = self.password[1:] + str(randrange(2, 9))
                    
            if self.pass_gen.btn_add_ABC.isChecked():  # Для кнопки "ABC"
                temp = False
                for c in self.password:
                    if c in self.alpha_upper:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('ABCDEFGHJKLMNPRSTUVWXYZ')
                    
            if self.pass_gen.btn_add_abc.isChecked():  # Для кнопки "abc"
                temp = False
                for c in self.password:
                    if c in self.alpha_lower:
                        temp = True
                        break
                if not temp:
                    self.password = self.password[1:] + choice('abcdefghijkmnopqrstuvwxyz')
                    
            if self.pass_gen.btn_add_symbols.isChecked():  # Для кнопки "symbols"
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
            self.pass_gen.label.setText('ВЫБЕРИТЕ СИМВОЛЫ!')  #  Если нет нажатых кнопок для выбора символов для генерации пароля, то это выводиться в подсказку


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


if __name__ == '__main__':
    main()
