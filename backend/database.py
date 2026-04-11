import sqlite3
import os

# FIXED DATABASE PATH (important)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "productivity.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    return conn


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


def create_goals_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            goalID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            goalTitle TEXT,
            description TEXT,
            startDate TEXT,
            endDate TEXT,
            status TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        );
    """)
    conn.commit()
    conn.close()


def create_goal_tasks_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goal_tasks (
            goalTaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            goalID INTEGER,
            taskName TEXT,
            status TEXT,
            completionDate TEXT,
            FOREIGN KEY(goalID) REFERENCES goals(goalID)
        );
    """)
    conn.commit()
    conn.close()


# ----------------------------
# POMODORO SESSIONS
# ----------------------------
def create_pomodoro_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            pomodoroID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            startTime TEXT,
            endTime TEXT,
            workDuration INTEGER,
            breakDuration INTEGER,
            sessionDate TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        );
    """)

    conn.commit()
    conn.close()


# ----------------------------
# STOPWATCH SESSIONS
# ----------------------------
def create_stopwatch_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stopwatch_sessions (
            stopwatchID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            startTime TEXT,
            endTime TEXT,
            totalDuration INTEGER,
            sessionDate TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        );
    """)

    conn.commit()
    conn.close()