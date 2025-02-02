import sqlite3

# Create a connection to SQLite (Creates 'my_database.db' if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# Commit and close the connection
conn.commit()
conn.close()