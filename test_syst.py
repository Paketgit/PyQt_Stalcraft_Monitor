import json
import sqlite3


def update_result():
    con = sqlite3.connect('sc_db')
    cur = con.cursor()
    with open('./ru/listing.json', 'r', encoding='UTF-8') as all_list:
        records = json.load(all_list)

    for i in records:
        try:
            #print(f"""INSERT INTO items(name, game_code) VALUES('{i['name']['lines']['ru']}', '{i['data']}')""")
            with open('./ru/'+i['data'], 'r', encoding='UTF-8') as f:
                info = json.load(f)

            try:
                print(info['infoBlocks'][-1]['text']['lines']['ru'])
                print(
                    f"""UPDATE items SET game_info = '{info['infoBlocks'][-1]['text']['lines']['ru']}' 
                    WHERE name = '{i['data'][-9:-5]}'""")
                cur.execute(
                    f"""UPDATE items SET game_info = '{info['infoBlocks'][-1]['text']['lines']['ru']}' 
                    WHERE name = '{i['data'][-9:-5]}'""")
                con.commit()
            except:
                pass
                f.close()
        except sqlite3.IntegrityError:
            print('NO')
            pass
        con.close()


update_result()
