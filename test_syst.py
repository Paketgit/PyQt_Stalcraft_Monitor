import json
import sqlite3


def stalc_handler(lots=''):
    inputlots_find = lots
    inputlots = lots.lower().title()
    with open('./ru/listing.json', 'r', encoding='UTF-8') as all_list:
        records = json.load(all_list)
    for i in records:

        return (i['data'][-9:-5], i['name']['lines']['ru'])

def update_result():
    con = sqlite3.connect('sc_db')
    cur = con.cursor()
    with open('./ru/listing.json', 'r', encoding='UTF-8') as all_list:
        records = json.load(all_list)

    for i in records:
        print(f"""INSERT INTO items(name, game_code) VALUES('{i['name']['lines']['ru']}', '{i['data'][-9:-5]}')""")
        cur.execute(f"""INSERT INTO items(name, game_code) VALUES('{i['name']['lines']['ru']}', '{i['data'][-9:-5]}')""")

update_result()