import sqlite3

# Create connection to database.
connection = sqlite3.connect('hangman.db')

# Set up the database itself.
with open('schema.sql', 'r') as f:
    connection.executescript(f.read())

# Create a cursor and prepare an insert query.
cur = connection.cursor()
query = "INSERT INTO Words VALUES (NULL,?,7)"

# Read local text document, check if current line is valid, if so then execute query with current line data.
with open("words.txt", "r") as words:
    for data in words:
        line = data.split()
        print(line)
        if len(line) > 0:
            cur.execute(query, line)

# Commit changes and close connection.
connection.commit()
connection.close()
