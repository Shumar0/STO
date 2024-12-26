import sqlite3

# Connect to the database
conn = sqlite3.connect('sto.db')
cursor = conn.cursor()

# Query the tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the tables
print("Tables in the database:")
for table in tables:
    print(table[0])

# Query and print the schema for each table
for table in tables:
    table_name = table[0]
    print(f"\nColumns in the '{table_name}' table:")
    try:
        cursor.execute(f'PRAGMA table_info("{table_name}");')
        columns = cursor.fetchall()
        if columns:
            for column in columns:
                print(column[1])  # Print only the column names
        else:
            print("No columns found.")
    except Exception as e:
        print(f"Error retrieving columns for table '{table_name}': {e}")

# Close the connection
conn.close()
