import http.client
import json
import sys
import datetime

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import Auth

conn = http.client.HTTPSConnection("eapi.stalcraft.net")
#берём отсюда цены
#data = stalc_handler(text)
#for i in data:
#    print(i['buyoutPrice'])


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
        x, y = stalc_handler(lots)
        self.aucList.setRowCount(1)
        self.aucList.setColumnCount(1000)
        print('1')
        try:
            for i in range(len(x)):
                self.aucList.setItem(i, 1, x[i])
        except Exception:
            print('DOLBAEB')
        print(x, y)
        print(x)
        plt.plot(x, y)
        plt.savefig('Graph')
        img = Image.open('Graph.png')
        # изменяем размер
        new_image = img.resize((1000, 800))
        # сохранение картинки
        new_image.save('./Graph.png')
        self.pixmap = QPixmap('Graph.png')
        self.Graph_time.setPixmap(self.pixmap)
        self.show()


def sortkey(dataset):
    return dataset['buyoutPrice']


def stalc_handler(lots):
    print('Я в stalc_handler')
    inputlots_find = lots
    inputlots = lots.lower().title()
    money, time = 0, ''
    with open('./ru/listing.json', 'r', encoding='UTF-8') as all_list:
        # комнуздим из файла как записан тот или иной итем
        records = json.load(all_list)
    for i in records:  # Это чудо инжинерной мысли не трогать
        try:
            if inputlots == i['name']['lines']['ru']:
                inputlots_find = i['data'][-9:-5]
                print(i['data'][-9:-5])
            if inputlots == 'all':
                print(i['name']['lines']['ru'], i['data'][-9:-5])
        except KeyError:
            print('eblan')
            pass
    print('Я прошёл файл')
    conn.request("GET", f"/RU/auction/{inputlots_find}/lots?limit=200&additional=true", headers=Auth.headers)
    print('conn ok')
    rowdata = conn.getresponse().read().decode('utf-8')
    print('rowdata ok')
    data = json.loads(rowdata)
    print('data ok')
    data = data['lots']
    print("Я прошёл конн и получение данныых")
    data = sorted(data, key=sortkey)
    print(data)
    money_lots = []
    date_lots = []
    for i in data:
        date_lots.append(i['endTime'])
        money_lots.append(i['buyoutPrice'])
    print(money_lots, date_lots, sep='\n')
    print('Я вышел')
    return date_lots, money_lots


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sc_helper()
    ex.show()
    sys.exit(app.exec_())