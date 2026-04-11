from database import get_connection
from datetime import datetime


# ----------------------------
# START POMODORO SESSION
# ----------------------------
def start_pomodoro(userID, startTime, endTime, workDuration, breakDuration):
    conn = get_connection()
    cursor = conn.cursor()

    sessionDate = datetime.now().date()

    cursor.execute("""
        INSERT INTO pomodoro_sessions 
        (userID, startTime, endTime, workDuration, breakDuration, sessionDate)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (userID, startTime, endTime, workDuration, breakDuration, sessionDate))

    conn.commit()
    conn.close()


# ----------------------------
# START STOPWATCH SESSION
# ----------------------------
def start_stopwatch(userID, startTime, endTime, totalDuration):
    conn = get_connection()
    cursor = conn.cursor()

    sessionDate = datetime.now().date()

    cursor.execute("""
        INSERT INTO stopwatch_sessions
        (userID, startTime, endTime, totalDuration, sessionDate)
        VALUES (?, ?, ?, ?, ?)
    """, (userID, startTime, endTime, totalDuration, sessionDate))

    conn.commit()
    conn.close()


# ----------------------------
# GET ALL SESSIONS FOR USER
# ----------------------------
def get_sessions(userID):
    conn = get_connection()
    cursor = conn.cursor()

    # Pomodoro
    cursor.execute("""
        SELECT * FROM pomodoro_sessions WHERE userID = ?
    """, (userID,))
    pomodoro_rows = cursor.fetchall()

    # Stopwatch
    cursor.execute("""
        SELECT * FROM stopwatch_sessions WHERE userID = ?
    """, (userID,))
    stopwatch_rows = cursor.fetchall()

    conn.close()

    pomodoro_sessions = []
    for row in pomodoro_rows:
        pomodoro_sessions.append({
            "pomodoroID": row[0],
            "userID": row[1],
            "startTime": row[2],
            "endTime": row[3],
            "workDuration": row[4],
            "breakDuration": row[5],
            "sessionDate": row[6]
        })

    stopwatch_sessions = []
    for row in stopwatch_rows:
        stopwatch_sessions.append({
            "stopwatchID": row[0],
            "userID": row[1],
            "startTime": row[2],
            "endTime": row[3],
            "totalDuration": row[4],
            "sessionDate": row[5]
        })

    return {
        "pomodoro": pomodoro_sessions,
        "stopwatch": stopwatch_sessions
    }
