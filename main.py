import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTableView, QComboBox, QWizard, QTextEdit
from PyQt6.QtWidgets import QTextBrowser, QWizardPage
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data_base = sqlite3.connect('Military_equipment_RF.sqlite')

    def initUI(self):
        self.setGeometry(0, 0, 1500, 750)
        self.setWindowTitle('Справочник Военного РФ')
        self.setStyleSheet('background-color: {}'.format('#4f4646'))
        self.aviationButton = QPushButton('Авиация', self)
        self.fleetButton = QPushButton('Флот', self)
        self.aviationButton.resize(500, 100)
        self.aviationButton.move(500, 250)
        self.aviationButton.setStyleSheet("background-color: {}".format('#fff'))
        self.fleetButton.setStyleSheet("background-color: {}".format('#1d0be3'))
        self.fleetButton.resize(500, 100)
        self.fleetButton.move(500, 400)
        self.armyButton = QPushButton('Назменая техника', self)
        self.armyButton.setStyleSheet("background-color: {}".format('#e30b0b'))
        self.armyButton.move(500, 550)
        self.armyButton.resize(500, 100)
        self.aviationButton.clicked.connect(self.aviation)
        self.fleetButton.clicked.connect(self.fleet)
        self.armyButton.clicked.connect(self.army)
        self.nameProject = QLabel('Военная Техника РФ', self)
        self.nameProject.resize(1500, 100)
        self.nameProject.move(300, 20)
        self.nameProject.setStyleSheet('font-size: {}'.format('80pt'))
        self.first_tabel = QTableView(self)
        self.first_tabel.move(750, 0)
        self.first_tabel.resize(750, 750)
        self.first_tabel.setStyleSheet('background-color: {}'.format('#fff'))
        self.first_tabel.hide()
        self.queryButton = QPushButton('поиск', self)
        self.queryButton.hide()
        self.parameterSelection = QComboBox(self)
        self.parameterSelection.hide()
        self.parameterSelection.resize(200, 30)
        self.parameterSelection.activated.connect(self.filter_aviation)
        # Зададим тип базы данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        self.db.setDatabaseName('Military_equipment_RF.sqlite')
        # И откроем подключение
        self.db.open()
        self.widget = QWizard(self)
        t = Widget()
        self.widget.addPage(t)
        self.widget.resize(750, 500)
        self.widget.show()

    def hide(self):
        self.aviationButton.hide()
        self.fleetButton.hide()
        self.armyButton.hide()
        self.nameProject.hide()

    def aviation(self):
        self.new_page()
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

    def new_page(self):
        self.first_tabel.show()
        self.hide()
        self.parameterSelection.show()
        self.setStyleSheet('background-color: {}'.format('#fff'))

    def fleet(self):
        self.new_page()
        model = QSqlTableModel(self, self.db)
        model.setTable('fleet')
        model.removeColumn(3)
        model.select()
        self.first_tabel.setModel(model)

    def army(self):
        self.new_page()
        model = QSqlTableModel(self, self.db)
        model.setTable('army')
        model.removeColumn(3)
        model.select()
        self.first_tabel.setModel(model)


class Widget(QWizardPage):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.text = QTextBrowser(self)
        self.text.move(0, 0)
        self.text.resize(325, 350)
        self.text.setText('''Негры работают в полях////////////////////////////////////////////////////////////''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Main()
    n.show()
    sys.exit(app.exec())