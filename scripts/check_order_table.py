import sqlite3

# Connect to the database
conn = sqlite3.connect('data/shared_service.db')
cursor = conn.cursor()

# Query the schema of the 'order' table
cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
tables = cursor.fetchall()

# Print the tables
print("Tables in the database:")
for table in tables:
    print(table)

# Close the connection
conn.close()
