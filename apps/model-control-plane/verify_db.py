import sqlite3

def verify_tables():
    conn = sqlite3.connect('aegis.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in Database:")
    for table in tables:
        print(f"- {table[0]}")
    conn.close()

if __name__ == "__main__":
    verify_tables()
