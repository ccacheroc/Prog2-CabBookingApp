import sqlite3
with sqlite3.connect('Users.data') as db:
    c=db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user(username TEXT not null, password TEXT not null)')
    db.commit()