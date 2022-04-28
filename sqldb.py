import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(" INSERT INTO posts (title, content, telefone) VALUES (?, ?, ?)",
            ('First post', 'content for the first post', 123)
            )

# cur.execute("INSERT INTO user (username, email, pwd) VALUES (?, ?, ?)",
#             ('Username', 'email@mail.com', 123456789)
#             )

connection.commit()
connection.close()
