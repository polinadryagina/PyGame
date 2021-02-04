import sys
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('records_db.sqlite')
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('record')
        model.select()
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)
        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Пример работы с QtSql')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(app)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
