import http.client
import json
import sys
import datetime
import sqlite3

import matplotlib.pyplot as plt
from matplotlib import rcParams
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from os import remove

import Auth

rcParams.update({'font.size': 10})
conn = http.client.HTTPSConnection("eapi.stalcraft.net")


class Sc_helper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt_sc.ui', self)  # Загружаем дизайн
        self.pixmap = QPixmap('Graph.png')
        self.Graph_time.setPixmap(self.pixmap)
        self.actionReset_graph.triggered.connect(self.__get_grpah)
        self.actionDelete_graph.triggered.connect(self.remove_graph)
        self.actionSaveData.triggered.connect(self.save_data)
        self.actionDeleteDataHistoryLot.triggered.connect(self.delete_saved_data)
        self.actionDelete_ALL_SavedData.triggered.connect(self.delete_all_saved_data)
        self.actionGetSavedLot.triggered.connect(self.upload_saved_data_lot)

    def __get_lot(self):
        lots = self.Input_item.toPlainText()
        try:
            inputlots = lots.lower()
            inputlots = inputlots[0].upper() + inputlots[1:]
        except Exception:
            self.__sint_err()
            return 0
        return inputlots

    def upload_saved_data_lot(self):
        inputlots = self.__get_lot()
        con = sqlite3.connect('sc_db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM items
                                WHERE name = '{inputlots}'""").fetchall()
        info, id_product = result[0][2], result[0][3]
        result = result[0][3]
        print('dfdsfsdffsdf')
        result = cur.execute(f"""SELECT * FROM auction
                                        WHERE id_product = {result}""").fetchall()
        print(result)
        if not result:
            self.__sint_err()
            return 0
        x, y = [], []
        for i in range(len(result)):
            x, y = result[i][2], result[i][1]
        self.build_data(x, y, info, id_product)

    def delete_all_saved_data(self):
        con = sqlite3.connect('sc_db')
        cur = con.cursor()
        try:
            cur.execute(f"""DELETE FROM auction""")
        except Exception:
            self.__sint_err()
        con.commit()

    def delete_saved_data(self):
        inputlots = self.__get_lot()
        con = sqlite3.connect('sc_db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM items
                        WHERE name = '{inputlots}'""").fetchall()
        result = result[0][3]
        try:
            cur.execute(f"""DELETE FROM auction
                                WHERE id_product = {result}""")
        except Exception:
            self.__sint_err()
        con.commit()

    def save_data(self):
        date, money, id_product = self.__get_grpah()
        if money == 0:
            return 0
        con = sqlite3.connect('sc_db')
        cur = con.cursor()
        for i in range(len(money)):
            try:
                print(f"""INSERT INTO auction(id_product, money, date) 
                            VALUES({id_product}, {money[i]}, '{date[i]}')""")
                cur.execute(
                    f"""INSERT INTO auction(id_product, money, date) 
                            VALUES({id_product}, {money[i]}, '{date[i]}')""")
                print('Ok')
            except Exception:
                print('error')
                pass
        con.commit()
        cur.close()

    def remove_graph(self):
        try:
            remove('Graph.png')
            self.Graph_time.setText('(╯°□°）╯')
        except Exception:
            self.__graph_err()

    def build_data(self, x, y, info, id_product):
        if x == "Error":
            return 0, 0, 0
        self.aucList.setColumnCount(2)
        title = QTableWidgetItem()
        title.setText('Цена выкупа')
        self.aucList.setHorizontalHeaderItem(0, title)
        title = QTableWidgetItem()
        title.setText('Дата окончания лота')
        self.aucList.setHorizontalHeaderItem(1, title)
        print('1')
        try:
            self.aucList.setRowCount(len(y))
            for i in range(len(y)):
                self.aucList.setItem(i - 1, 2, QTableWidgetItem(str(y[i])))
                self.aucList.setItem(i, 1, QTableWidgetItem(str(datetime.datetime.strptime(x[i], '%Y-%m-%dT%H:%M:%SZ'))))
                print(x[i], y[i])
        except Exception:
            print('ОШИБКА')
        try:
            self.Info.setText(info)
        except Exception:
            print('Ошибка')
        print('-------------------------')
        print(x, y)
        plt.plot(x, y)
        rcParams.update({'font.size': 5})
        plt.xlabel('Дата', fontsize=10)
        plt.ylabel(r'Цены', fontsize=10)
        plt.semilogy()
        plt.savefig('Graph')
        img = Image.open('Graph.png')
        # изменяем размер
        new_image = img.resize((1000, 800))
        # сохранение картинки
        new_image.save('./Graph.png')
        self.pixmap = QPixmap('Graph.png')
        self.Graph_time.setPixmap(self.pixmap)
        self.show()
        return x, y, id_product

    def __get_grpah(self):
        lots = self.Input_item.toPlainText()
        x, y, info, id_product = self.get_data(lots)
        if x == "Error":
            return 0, 0, 0
        self.build_data(x, y, info, id_product)
        return x, y, id_product

    def __sortkey(self, dataset): #Это PEP8, знаю, но если сделать т.к. он просит, то всё сломается
        return dataset['buyoutPrice']

    def __sint_err(self):
        QMessageBox.question(self, 'Error',
        'Проверьте интернет соединение или написание лота ¯\_(ツ)_/¯', QMessageBox.Ok)

    def __graph_err(self):
        QMessageBox.question(self, 'Error',
        'Графика либо нету, либо системная ошибка ¯\_(ツ)_/¯', QMessageBox.Ok)

    def get_data(self, lots):
        print('Я в stalc_handler')
        try:
            inputlots = lots.lower()
            inputlots = inputlots[0].upper() + inputlots[1:]
        except Exception:
            self.__sint_err()
            return 'Error', 0, 0

        con = sqlite3.connect('sc_db')
        cur = con.cursor()

        result = cur.execute(f"""SELECT * FROM items
                WHERE name = '{inputlots}'""").fetchall()
        cur.close()
        print(result, inputlots)
        if not result:
            self.__sint_err()
            return 'Error', 0, 0, 0
        inputlots_find = result[0][1]
        conn.request("GET", f"/RU/auction/{inputlots_find}/lots?limit=200&additional=true", headers=Auth.headers)
        print('conn ok')
        rowdata = conn.getresponse().read().decode('utf-8')
        data = json.loads(rowdata)
        data = data['lots']
        print("Я прошёл конн и получение данныых")
        data = sorted(data, key=self.__sortkey)
        print(data)
        money_lots = []
        date_lots = []
        for i in data:
            date_lots.append(i['endTime'])
            money_lots.append(i['buyoutPrice'])
        print(money_lots, date_lots, sep='\n')
        print('Я вышел')

        print('saddasdasdasd', result)
        return date_lots, money_lots, result[0][2], result[0][3]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sc_helper()
    ex.show()
    sys.exit(app.exec_())
