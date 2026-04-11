from database import get_connection


# ----------------------------
# DAILY ANALYTICS
# ----------------------------
def get_daily_analytics(userID):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dueDate as date, COUNT(*) as tasks_completed
        FROM todo_tasks
        WHERE userID=? AND LOWER(status)='completed' AND dueDate IS NOT NULL AND dueDate != ''
        GROUP BY dueDate
        ORDER BY dueDate
    """, (userID,))

    daily_data = []
    for row in cursor.fetchall():
        daily_data.append({
            "date": row[0],
            "tasks_completed": row[1],
            "total_focus_time": 0
        })

    conn.close()
    return daily_data


# ----------------------------
# WEEKLY ANALYTICS
# ----------------------------
def get_weekly_analytics(userID):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            strftime('%Y-%W', sessionDate) as week,
            COALESCE(SUM(workDuration), 0) as total_focus_time
        FROM pomodoro_sessions
        WHERE userID=?
        GROUP BY week
        ORDER BY week
    """, (userID,))

    weekly_data = []
    for row in cursor.fetchall():
        weekly_data.append({
            "week": row[0],
            "total_focus_time": row[1] or 0
        })

    conn.close()
    return weekly_data


# ----------------------------
# SUMMARY ANALYTICS
# ----------------------------
def get_summary(userID):
    conn = get_connection()
    cursor = conn.cursor()

    # Total tasks completed
    cursor.execute("""
        SELECT COUNT(*) 
        FROM todo_tasks
        WHERE userID=? AND LOWER(status)='completed'
    """, (userID,))
    tasks_completed = cursor.fetchone()[0] or 0

    # Pending tasks
    cursor.execute("""
        SELECT COUNT(*) 
        FROM todo_tasks
        WHERE userID=? AND LOWER(status)='pending'
    """, (userID,))
    pending_tasks = cursor.fetchone()[0] or 0

    # Completed goals
    cursor.execute("""
        SELECT COUNT(*) 
        FROM goals
        WHERE userID=? AND LOWER(status)='completed'
    """, (userID,))
    goals_completed = cursor.fetchone()[0] or 0

    # Total pomodoro focus time
    cursor.execute("""
        SELECT COALESCE(SUM(workDuration), 0)
        FROM pomodoro_sessions
        WHERE userID=?
    """, (userID,))
    pomodoro_time = cursor.fetchone()[0] or 0

    # Total stopwatch focus time
    cursor.execute("""
        SELECT COALESCE(SUM(totalDuration), 0)
        FROM stopwatch_sessions
        WHERE userID=?
    """, (userID,))
    stopwatch_time = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "tasksCompleted": tasks_completed,
        "pendingTasks": pending_tasks,
        "goalsCompleted": goals_completed,
        "totalFocusTime": pomodoro_time + stopwatch_time
    }