import json
import sqlite3


def update_result():
    con = sqlite3.connect('sc_db')
    cur = con.cursor()
    with open('./ru/listing.json', 'r', encoding='UTF-8') as all_list:
        records = json.load(all_list)

    for i in records:
        try:
            print(f"""INSERT INTO items(name, game_code) VALUES('{i['name']['lines']['ru']}', '{i['data'][-9:-5]}')""")
            cur.execute(f"""INSERT INTO items(name, game_code) VALUES('{i['name']['lines']['ru']}', '{i['data'][-9:-5]}')""")
            con.commit()
            print('OK')
        except sqlite3.IntegrityError:
            print('NO')
            pass

update_result()
