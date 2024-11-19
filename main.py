import sqlite3
import sys
import os
from pathlib import Path
from winshell import desktop
from win32com.client import Dispatch
from PIL import Image
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTableView, QComboBox, QWizard, QLineEdit
from PyQt6.QtWidgets import QTextBrowser, QWizardPage, QAbstractItemView, QPlainTextEdit, QMessageBox, QFileDialog
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


# основной класс програмы

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data_base = sqlite3.connect('Military_equipment_RF.sqlite')

    # создание UI основного окна

    def initUI(self):
        font = QFont()
        font.setFamily("Comic Sans MS")

        # создание первой страницы

        self.setGeometry(0, 0, 1500, 750)
        self.setFixedSize(1500, 750)
        self.setWindowTitle('Справочник Лётчика РФ')
        self.setStyleSheet('background-color: {}'.format('#e8e6e6'))
        self.firstButton = QPushButton('на главную', self)
        self.firstButton.setFont(font)
        self.firstButton.setStyleSheet('font-size: {}'.format('20pt'))
        self.firstButton.resize(285, 50)
        self.firstButton.hide()
        self.firstButton.clicked.connect(self.first_page)
        self.aviationButton = QPushButton('Авиация', self)
        self.fleetButton = QPushButton(self)
        self.fleetButton.resize(500, 100)
        self.fleetButton.move(500, 250)
        self.fleetButton.setStyleSheet("background-color: {}".format('#fff'))
        self.aviationButton.setStyleSheet("background-color: {}".format('#1d0be3'))
        self.aviationButton.resize(500, 100)
        self.aviationButton.move(500, 400)
        self.aviationButton.setStyleSheet('''font-size: 20pt;
        background-color: blue;''')
        self.armyButton = QPushButton(self)
        self.armyButton.setStyleSheet("background-color: {}".format('#e30b0b'))
        self.armyButton.move(500, 550)
        self.armyButton.resize(500, 100)
        self.aviationButton.clicked.connect(self.aviation)
        self.armyButton.setFont(font)
        self.fleetButton.setFont(font)
        self.aviationButton.setFont(font)
        self.nameProject = QLabel('Справочник Лётчика РФ', self)
        self.nameProject.resize(1500, 100)
        self.nameProject.move(0, 20)
        self.nameProject.setStyleSheet('font-size: {}'.format('80pt'))
        self.nameProject.setFont(font)
        self.nameProject.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # создание второй страницы

        self.first_tabel = QTableView(self)
        self.first_tabel.move(1150, 0)
        self.first_tabel.resize(350, 750)
        self.first_tabel.setStyleSheet('background-color: {}'.format('#fff'))
        self.first_tabel.hide()
        self.first_tabel.setFont(font)
        self.first_tabel.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.queryButton = QPushButton('поиск', self)
        self.queryButton.hide()
        self.parameterSelection = QComboBox(self)
        self.parameterSelection.hide()
        self.parameterSelection.resize(285, 60)
        self.parameterSelection.move(0, 60)
        self.parameterSelection.activated.connect(self.filter_aviation)
        self.parameterSelection.setFont(font)
        self.parameterSelection.setStyleSheet('font-size: {}'.format('20pt'))
        self.typeSelection = QComboBox(self)
        # Зададим тип базы данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        self.db.setDatabaseName('Military_equipment_RF.sqlite')
        # И откроем подключение
        self.db.open()
        self.widget = QWizard(self)
        self.page = Widget()
        self.widget.addPage(self.page)
        self.widget.resize(1500, 520)
        self.search = QLineEdit(self)
        self.search.setFont(font)
        self.search.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search.hide()
        self.search.resize(580, 60)
        self.search.move(300, 60)
        self.search.setStyleSheet('font-size: {}'.format('20pt'))
        self.searchButton = QPushButton('Поиск', self)
        self.searchButton.resize(250, 60)
        self.searchButton.move(890, 60)
        self.searchButton.setStyleSheet('font-size: {}'.format('20pt'))
        self.searchButton.setFont(font)
        self.searchButton.hide()
        self.searchLabel = QLabel('Поиск информации', self)
        self.searchLabel.setStyleSheet('font-size: {}'.format('40pt'))
        self.searchLabel.resize(800, 60)
        self.searchLabel.move(330, 0)
        self.addLabel = QLabel('Добавление в таблицу', self)
        self.addLabel.setStyleSheet('font-size: {}'.format('40pt'))
        self.addLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addLabel.setFont(font)
        self.searchLabel.setFont(font)
        self.addLabel.resize(1150, 60)
        self.addLabel.move(0, 150)
        self.addLabel.hide()
        self.searchLabel.hide()
        self.typeSelection.hide()
        self.typeSelection.resize(285, 60)
        self.typeSelection.move(0, 250)
        self.typeSelection.setFont(font)
        self.typeSelection.setStyleSheet('font-size: {}'.format('20pt'))
        self.titleEnter = QLineEdit(self)
        self.titleEnter.setPlaceholderText('Введите название техники')
        self.titleEnter.resize(420, 60)
        self.titleEnter.move(290, 250)
        self.titleEnter.setFont(font)
        self.titleEnter.setStyleSheet('font-size: {}'.format('20pt'))
        self.titleEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.yearEnter = QLineEdit(self)
        self.yearEnter.setPlaceholderText('Введите год создания техники')
        self.yearEnter.resize(420, 60)
        self.yearEnter.move(720, 250)
        self.yearEnter.setFont(font)
        self.yearEnter.setStyleSheet('font-size: {}'.format('20pt'))
        self.yearEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.infoEnter = QPlainTextEdit(self)
        self.infoEnter.setPlaceholderText('Введите краткую информацию о технике')
        self.infoEnter.setFont(font)
        self.infoEnter.setStyleSheet('font-size: {}'.format('20pt'))
        self.infoEnter.resize(1000, 250)
        self.infoEnter.move(50, 350)
        self.titleEnter.hide()
        self.yearEnter.hide()
        self.infoEnter.hide()
        self.addButton = QPushButton('Добавить в таблицу/редактировать таблицу', self)
        self.addButton.resize(1000, 100)
        self.addButton.move(50, 630)
        self.addButton.setFont(font)
        self.addButton.hide()
        self.addButton.setStyleSheet('font-size: {}'.format('20pt'))
        self.search.setPlaceholderText('Введите id техники')
        self.error = QMessageBox(self)
        self.widget.setFixedSize(1500, 750)

        # для первого запуская программы

        file = open('FirstEnter.txt', mode='r', encoding='UTF-8')
        self.dButton = QPushButton('добавить ярлык на рабочий стол', self)
        self.dButton.resize(200, 200)
        self.dButton.move(0, 350)
        self.dButton.clicked.connect(self.first_enter_f)
        self.dButton.hide()
        if file.read() == '0':
            self.dButton.show()
        
        # для фторой формы

        self.infoButton = QPushButton('информация о приложении', self)
        self.infoButton.resize(500, 50)
        self.infoButton.move(500, 680)
        self.infoButton.clicked.connect(self.showWidget)
        self.ww = InfoWidget()

    # Функция для первого запуская программы

    def first_enter_f(self):
        self.firstEnter = QWizard()
        page2 = FirstEnter()
        page2.yesButton.clicked.connect(self.desktop)
        page2.noButton.clicked.connect(self.hides)
        self.firstEnter.addPage(page2)
        self.firstEnter.resize(750, 520)
        self.firstEnter.setFixedSize(750, 520)
        self.firstEnter.show()

    # Функция, перенаправляющая на начальную страницу

    def first_page(self):
        self.hide_f()
        self.aviationButton.show()
        self.fleetButton.show()
        self.armyButton.show()
        self.nameProject.show()

    # Функция для кнопки noButton

    def hides(self):
        file = open('FirstEnter.txt', mode='w', encoding='UTF-8')
        t = '1'
        file.write(t)
        file.close()
        self.firstEnter.hide()
        self.dButton.hide()

    # Функция, создающаяя ярлык на рабочем столе

    def desktop(self):
        t = os.path.abspath('__Main__')[:-8]
        target = rf"{t}PilotsHandbook.exe"
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(Path(desktop()) / "PilotsHandbook.lnk"))
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = str(Path(target).parent)
        shortcut.IconLocation = target
        shortcut.save()
        self.hides()

    # Функция для скрытия объектов

    def hide_f(self):
        self.dButton.hide()
        self.aviationButton.hide()
        self.fleetButton.hide()
        self.armyButton.hide()
        self.nameProject.hide()
        self.first_tabel.hide()
        self.parameterSelection.hide()
        self.queryButton.hide()
        self.firstButton.hide()
        self.typeSelection.hide()
        self.search.hide()
        self.searchLabel.hide()
        self.searchButton.hide()
        self.addLabel.hide()
        self.addButton.hide()
        self.titleEnter.hide()
        self.yearEnter.hide()
        self.infoEnter.hide()

    def showWidget(self):
        self.ww.show()

    # функия для корректирования базы данных

    def change_aviation(self):
        db = sqlite3.connect("Military_equipment_RF.sqlite")
        cur = db.cursor()
        if self.typeSelection.currentText() == 'многоцелевой':
            types = cur.execute(f"""SELECT id from type
                        where title == 'многоцелевой'""").fetchone()[0]
        elif self.typeSelection.currentText() == 'транспортный':
            types = cur.execute(f"""SELECT id from type
                        where title == 'транспортный'""").fetchone()[0]
        elif self.typeSelection.currentText() == 'учебно-боевой':
            types = cur.execute(f"""SELECT id from type
                        where title == 'учебно-боевой'""").fetchone()[0]
        elif self.typeSelection.currentText() == 'бомбардировщик':
            types = cur.execute(f"""SELECT id from type
                        where title == 'Бомбардировщик'""").fetchone()[0]
        elif self.typeSelection.currentText() == 'атакующие':
            types = cur.execute(f"""SELECT id from type
                        where title == 'Атакующие'""").fetchone()[0]
        elif self.typeSelection.currentText() == 'разведывательные':
            types = cur.execute(f"""SELECT id from type
                        where title == 'Разведовательные'""").fetchone()[0]
        elif self.typeSelection.currentText() == 'истребитель':
            types = cur.execute(f"""SELECT id from type
                        where title == 'Истребитель'""").fetchone()[0]
        if self.titleEnter.text():
            pass
            titeles1 = cur.execute("""SELECT title from aviation""").fetchall()
            titels = [x[0] for x in titeles1]
            if self.titleEnter.text() in titels:
                if self.yearEnter.text():
                    if self.yearEnter.text().isdigit():
                        if int(self.yearEnter.text()) != cur.execute(f"""SELECT year from aviation
                                                        where title == '{self.titleEnter.text()}'""").fetchone()[0]:
                            db.execute(f"""UPDATE aviation
                                SET year = '{self.yearEnter.text()}'
                                WHERE title == '{self.titleEnter.text()}';""")
                            db.commit()
                            self.filter_aviation()
                        if self.infoEnter.toPlainText():
                            print('да')
                            text = open(f'texts/{self.titleEnter.text()}.txt', mode='r', encoding='UTF-8').read()
                            if self.infoEnter.toPlainText() != text:
                                text = open(f'texts/{self.titleEnter.text()}.txt', mode='w', encoding='UTF-8')
                                text.write(self.infoEnter.toPlainText())
                                text.close()
                    else:
                        self.error.setText('Неправильный формат ввода в поле "год"')
                        self.error.show()
                else:
                    if self.infoEnter.toPlainText():
                        print('да')
                        text = open(f'texts/{self.titleEnter.text()}.txt', mode='r', encoding='UTF-8').read()
                        if self.infoEnter.toPlainText() != text:
                            text = open(f'texts/{self.titleEnter.text()}.txt', mode='w', encoding='UTF-8')
                            text.write(self.infoEnter.toPlainText())
                            text.close()
            else:
                if not self.yearEnter.text():
                    self.error.setText('Введите год производства техники')
                    self.error.show()
                else:
                    if not self.yearEnter.text().isdigit():
                        self.error.setText('Неправельный формат ввода в поле "год"')
                        self.error.show()
                    else:
                        if not self.infoEnter.toPlainText():
                            self.error.setText('Введите краткую информацию')
                            self.error.show()
                        else:
                            try:
                                fname = QFileDialog.getOpenFileName(
                                    self, 'Выбрать картинку', '',
                                    'Картинка (*.png);;Все файлы (*)')[0]
                                image = Image.open(fname)
                                t = cur.execute("""SELECT title from aviation""").fetchall()
                                t = [x[0] for x in t][-1]
                                ids = int(cur.execute(f"""SELECT id from aviation
                                where title == '{t}'""").fetchone()[0]) + 1
                                year = self.yearEnter.text()
                                title = self.titleEnter.text()
                                image.save(f'images/{title}.png')
                                db.execute(
                                    f"""INSERT INTO aviation(title, year, type) VALUES('{title}', '{year}', '{types}')""")
                                db.commit()
                                self.filter_aviation()
                                text = open(f'texts/{title}.txt', mode='w', encoding='UTF-8')
                                text.write(self.infoEnter.toPlainText())
                                text.close()
                            except Exception:
                                self.error.setText('Ошибка, попробуйте снова')
                                self.error.show()
        else:
            self.error.setText('Введите название техники')
            self.error.show()

    # Функция для кнопки aviationButton

    def aviation(self):
        self.new_page()
        self.addButton.clicked.connect(self.change_aviation)
        self.searchButton.clicked.connect(self.search_aviation)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('aviation')
        self.model.removeColumn(3)
        self.model.select()
        self.first_tabel.setModel(self.model)
        self.parameterSelection.insertItem(0, 'все')
        self.parameterSelection.insertItem(1, 'многоцелевой')
        self.parameterSelection.insertItem(2, 'транспортный')
        self.parameterSelection.insertItem(3, 'учебно-боевой')
        self.parameterSelection.insertItem(4, 'бомбардировщик')
        self.parameterSelection.insertItem(5, 'атакующие')
        self.parameterSelection.insertItem(6, 'разведывательные')
        self.parameterSelection.insertItem(7, 'истребитель')
        self.typeSelection.insertItem(0, 'многоцелевой')
        self.typeSelection.insertItem(1, 'транспортный')
        self.typeSelection.insertItem(2, 'учебно-боевой')
        self.typeSelection.insertItem(3, 'бомбардировщик')
        self.typeSelection.insertItem(4, 'атакующие')
        self.typeSelection.insertItem(5, 'разведывательные')
        self.typeSelection.insertItem(6, 'истребитель')

    # функция, осуществляющая фильтрацию таблицы по указанному типу авиации

    def filter_aviation(self):
        cur = sqlite3.connect("Military_equipment_RF.sqlite").cursor()
        if str(self.parameterSelection.currentText()) == 'все':
            self.model.setFilter(None)
            self.model.select()
        else:
            if str(self.parameterSelection.currentText()) == 'истребитель':
                ids = cur.execute("""SELECT id from type
                            where title == 'Истребитель';""").fetchone()[0]
            elif str(self.parameterSelection.currentText()) == 'многоцелевой':
                ids = cur.execute("""SELECT id from type
                            where title == 'многоцелевой';""").fetchone()[0]
            elif str(self.parameterSelection.currentText()) == 'транспортный':
                ids = cur.execute("""SELECT id from type
                            where title == 'транспортный';""").fetchone()[0]
            elif str(self.parameterSelection.currentText()) == 'учебно-боевой':
                ids = cur.execute("""SELECT id from type
                            where title == 'учебно-боевой';""").fetchone()[0]
            elif str(self.parameterSelection.currentText()) == 'бомбардировщик':
                ids = cur.execute("""SELECT id from type
                            where title == 'Бомбардировщик';""").fetchone()[0]
            elif str(self.parameterSelection.currentText()) == 'атакующие':
                ids = cur.execute("""SELECT id from type
                            where title == 'Атакующие';""").fetchone()[0]
            elif str(self.parameterSelection.currentText()) == 'разведывательные':
                ids = cur.execute("""SELECT id from type
                            where title == 'Разведывательные';""").fetchone()[0]
            self.model.setFilter(f"type = '{ids}'")
            self.model.select()

    # Функция осуществляющая поиск и вывод информации по id

    def search_aviation(self):
        if self.search.text().isdigit():
            cur = sqlite3.connect("Military_equipment_RF.sqlite").cursor()
            ids = [x[0] for x in cur.execute("""SELECT id from aviation""").fetchall()]
            if int(self.search.text()) in ids:
                name = cur.execute(f"""SELECT title from aviation
                            where id == '{int(self.search.text())}'""").fetchone()[0]
                self.page.set_text_and_image(name)
                self.widget.show()
            else:
                self.error.setText('id не найден')
                self.error.show()
        else:
            self.error.setText('некорректный ввод')
            self.error.show()

    # Функция перехода на новую страницу

    def new_page(self):
        self.hide_f()
        self.first_tabel.show()
        self.parameterSelection.show()
        self.setStyleSheet('background-color: {}'.format('#e8e6e6'))
        self.search.show()
        self.searchButton.show()
        self.searchLabel.show()
        self.addLabel.show()
        self.typeSelection.show()
        self.titleEnter.show()
        self.yearEnter.show()
        self.infoEnter.show()
        self.addButton.show()
        self.firstButton.show()


# создание страниы диалога с информацией и изображением


class Widget(QWizardPage):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.text = QTextBrowser(self)
        self.text.move(0, 130)
        self.text.resize(325, 750)
        self.image = QLabel(self)
        self.image.resize(1150, 750)
        self.image.move(325, 30)
        self.label = QLabel(self)
        self.label.resize(1500, 30)
        self.label.move(0, 0)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('font-size: {}'.format('20pt'))

    def set_text_and_image(self, name):
        self.text.setText(open(f'texts/{name}.txt', mode='r', encoding='UTF-8').read())
        self.image.setPixmap(QPixmap(f'images/{name}.png'))
        self.label.setText(name)


# создание страниы диалога


class FirstEnter(QWizardPage):
    def __init__(self):
        super().__init__()
        self.InitUI()

    # создания UI страницы диалога

    def InitUI(self):
        self.label = QLabel('Приветствуем вас в нашем приложении!', self)
        self.yesButton = QPushButton('Да', self)
        self.noButton = QPushButton('Нет', self)
        self.label.resize(750, 30)
        self.label.move(0, 0)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('font-size: {}'.format('20pt'))
        self.label2 = QLabel('Хотите ли вы создать ярлык на рабочем столе?', self)
        self.label2.resize(750, 30)
        self.label2.move(0, 30)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setStyleSheet('font-size: {}'.format('20pt'))
        font = QFont()
        font.setFamily('Comic Sans MS')
        self.label.setFont(font)
        self.label2.setFont(font)
        self.yesButton.move(0, 120)
        self.yesButton.resize(315, 50)
        self.noButton.move(335, 120)
        self.noButton.resize(315, 50)
        self.yesButton.setFont(font)
        self.noButton.setFont(font)
        self.yesButton.setStyleSheet("""font-size: 20pt;
        background-color: green""")
        self.noButton.setStyleSheet("""font-size: 20pt;
        background-color: red""")


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle('Информация о программе')
        self.setGeometry(0, 0, 500, 500)
        self.label = QLabel('Информация о программе', self)
        self.label.resize(500, 100)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('font-size: {}'.format('20pt'))
        self.text = QTextBrowser(self)
        self.text.resize(500, 400)
        self.text.move(0, 100)
        file = open('README.md', mode='r', encoding='UTF-8')
        self.text.setText(file.read())
        self.text.setStyleSheet('font-size: {}'.format('20pt'))
        self.setFixedSize(500, 500)


# запуск программы


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Main()
    n.show()
    sys.exit(app.exec())
