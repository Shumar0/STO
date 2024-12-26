import sqlite3

def check_users():
    conn = sqlite3.connect('account_service.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()

    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}")

    conn.close()

if __name__ == "__main__":
    check_users()
