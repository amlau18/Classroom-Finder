import sqlite3

# Create a connection to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('example.db')  # 'example.db' is the name of the database file

# Convert the DataFrame to an SQL table
df.to_sql('people', conn, if_exists='replace', index=False)

# Close the connection
conn.close()