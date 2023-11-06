import sqlite3


def update_result():
    con = sqlite3.connect('sc_db')
    cur = con.cursor()

    result = cur.execute(f"""SELECT * FROM items
            WHERE name = 'Глаз'""").fetchall()
    print(result)

update_result()
