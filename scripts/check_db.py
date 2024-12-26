import os
import sqlite3

# Path to the database
db_path = 'order_service.db'

# Drop the existing database
if os.path.exists(db_path):
    os.remove(db_path)
    print("Database dropped successfully.")

# Create a new database
conn = sqlite3.connect(db_path)
conn.close()
print("New database created successfully.")
