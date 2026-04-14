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

    all_sessions = []

    # Pomodoro sessions
    cursor.execute("""
        SELECT pomodoroID, userID, startTime, endTime, workDuration, breakDuration, sessionDate
        FROM pomodoro_sessions
        WHERE userID = ?
    """, (userID,))
    pomodoro_rows = cursor.fetchall()

    for row in pomodoro_rows:
        all_sessions.append({
            "type": "pomodoro",
            "sessionID": row[0],
            "userID": row[1],
            "startTime": row[2],
            "endTime": row[3],
            "duration": row[4],
            "breakDuration": row[5],
            "sessionDate": str(row[6])
        })

    # Stopwatch sessions
    cursor.execute("""
        SELECT stopwatchID, userID, startTime, endTime, totalDuration, sessionDate
        FROM stopwatch_sessions
        WHERE userID = ?
    """, (userID,))
    stopwatch_rows = cursor.fetchall()

    for row in stopwatch_rows:
        all_sessions.append({
            "type": "stopwatch",
            "sessionID": row[0],
            "userID": row[1],
            "startTime": row[2],
            "endTime": row[3],
            "duration": row[4],
            "sessionDate": str(row[5])
        })

    conn.close()

    all_sessions.sort(key=lambda session: session["sessionDate"])
    return all_sessions