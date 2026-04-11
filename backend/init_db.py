from database import get_connection

# Create all tables in a single connection to avoid locking issues
conn = get_connection()
cursor = conn.cursor()

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        createdAt TEXT
    )
""")

# Create todo_tasks table
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
    )
""")

# Create goals table
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
    )
""")

# Create goal_tasks table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS goal_tasks (
        goalTaskID INTEGER PRIMARY KEY AUTOINCREMENT,
        goalID INTEGER,
        taskName TEXT,
        status TEXT,
        completionDate TEXT,
        FOREIGN KEY(goalID) REFERENCES goals(goalID)
    )
""")

# Create pomodoro_sessions table
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
    )
""")

# Create stopwatch_sessions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stopwatch_sessions (
        stopwatchID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        startTime TEXT,
        endTime TEXT,
        totalDuration INTEGER,
        sessionDate TEXT,
        FOREIGN KEY(userID) REFERENCES users(userID)
    )
""")

conn.c
print("Database initialized successfully")

