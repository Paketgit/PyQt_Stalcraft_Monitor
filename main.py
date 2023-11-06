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

    def __get_grpah(self):
        lots = self.Input_item.toPlainText()
        print(lots)
        x, y = self.stalc_handler(lots)
        if x == "Error":
            return 0
        self.aucList.setColumnCount(2)
        print('1')
        try:
            self.aucList.setRowCount(len(y))
            for i in range(len(y)):
                self.aucList.setItem(i - 1, 2, QTableWidgetItem(str(y[i])))
                self.aucList.setItem(i, 1, QTableWidgetItem(x[i]))
                print(x[i], y[i])
        except Exception:
            print('ОШИБКА')

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

    def __sortkey(self, dataset):
        return dataset['buyoutPrice']

    def err(self):
        QMessageBox.question(self, 'Error',
                             'Проверьте интернет соединение или написание лота', QMessageBox.Ok)

    def stalc_handler(self, lots):
        print('Я в stalc_handler')
        inputlots_find = ''
        inputlots = lots.lower().title()

        con = sqlite3.connect('sc_db')
        cur = con.cursor()

        result = cur.execute(f"""SELECT * FROM items
                WHERE name = '{inputlots}'""").fetchall()
        cur.close()
        print(result)
        inputlots_find = result[0][1]
        if not inputlots_find:
            self.err()
            return 'Error', 0
        print('Я прошёл файл')
        conn.request("GET", f"/RU/auction/{inputlots_find}/lots?limit=200&additional=true", headers=Auth.headers)
        print('conn ok')
        rowdata = conn.getresponse().read().decode('utf-8')
        print('rowdata ok')
        data = json.loads(rowdata)
        print('data ok')
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
        con = sqlite3.connect('sc_db')
        cur = con.cursor()
        for i in range(len(money_lots)):
            try:
                print(f"""INSERT INTO auction(id_product, money, date) VALUES({result[0][3]}, {money_lots[i]}, '{date_lots[i]}')""")
                cur.execute(
                    f"""INSERT INTO auction(id_product, money, date) VALUES({result[0][3]}, {money_lots[i]}, '{date_lots[i]}')""")
                con.commit()
                print('Ok')
            except Exception:
                print('error')
                pass
        cur.close()
        print('saddasdasdasd')
        return date_lots, money_lots


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sc_helper()
    ex.show()
    sys.exit(app.exec_())
