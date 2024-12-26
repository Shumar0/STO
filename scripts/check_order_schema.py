import sqlite3

# Connect to the database
conn = sqlite3.connect('data/shared_service.db')
cursor = conn.cursor()

# Query the schema of the 'order' table
cursor.execute('PRAGMA table_info("order");')
columns = cursor.fetchall()

# Print the columns
if columns:
    for column in columns:
        print(column[1])  # Print only the column names
else:
    print("No columns found in the 'order' table.")

# Close the connection
conn.close()
