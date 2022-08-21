import sqlite3

connection = sqlite3.connect('hangman.db')

# First, set up the database itself.
with open('schema.sql', 'r') as f:
    connection.executescript(f.read())

# Create a cursor and prepare an insert query.
cur = connection.cursor()
query = "INSERT INTO Words VALUES (NULL,?,7)"

with open("words.txt", "r") as words:
    for data in words:
        line = data.split()
        print(line)
        if len(line) > 0:
            cur.execute(query, line)

connection.commit()
connection.close()
