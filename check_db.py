import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('sto.db')
cursor = conn.cursor()

# Запит для отримання списку таблиць
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Вивести таблиці
print("Таблиці в базі даних:")
for table in tables:
    print(table[0])

# Закрити з'єднання
conn.close()
