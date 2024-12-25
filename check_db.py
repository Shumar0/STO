import sqlite3

# Connect to the database
conn = sqlite3.connect('sto.db')
cursor = conn.cursor()

# Query to get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the tables
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection
conn.close()
