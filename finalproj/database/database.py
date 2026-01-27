import sqlite3

def get_connection():
    return sqlite3.connect("productivity.db")

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            createdAt TEXT
        );
    """)
    conn.commit()
    conn.close()

def create_todo_tasks_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todo_tasks (
            todoTaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            title TEXT,
            description TEXT,
            priority TEXT,
            status TEXT,
            dueDate TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        );
    """)
    conn.commit()
    conn.close()
