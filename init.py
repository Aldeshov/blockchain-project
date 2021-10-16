import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql ') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Inserting user profile and statistics
cur.execute("INSERT INTO statistics (month_purchase, year_purchase) VALUES (?, ?)",
            (1380, 10665))

cur.execute("INSERT INTO profile (name, credits, statistics_id) VALUES (?, ?, ?)",
            ('KBTU Student', 4765, 1))


connection.commit()
connection.close()

print("Initialized successfully")
