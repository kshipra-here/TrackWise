from database import get_connection

# DAILY ANALYTICS

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
    task_rows = cursor.fetchall()

    cursor.execute("""
        SELECT sessionDate, COALESCE(SUM(totalDuration), 0) as total_focus_time
        FROM stopwatch_sessions
        WHERE userID=?
        GROUP BY sessionDate
        ORDER BY sessionDate
    """, (userID,))
    focus_rows = cursor.fetchall()

    focus_map = {}
    for row in focus_rows:
        focus_map[row[0]] = row[1]

    daily_data = []
    for row in task_rows:
        daily_data.append({
            "date": row[0],
            "tasks_completed": row[1],
            "total_focus_time": focus_map.get(row[0], 0)
        })

    conn.close()
    return daily_data


# WEEKLY ANALYTICS

def get_weekly_analytics(userID):
    conn = get_connection()
    cursor = conn.cursor()

    weekly_totals = {}

    cursor.execute("""
        SELECT 
            strftime('%Y-%W', sessionDate) as week,
            COALESCE(SUM(workDuration), 0) as total_focus_time
        FROM pomodoro_sessions
        WHERE userID=?
        GROUP BY week
        ORDER BY week
    """, (userID,))
    for row in cursor.fetchall():
        week = row[0]
        total = row[1] or 0
        weekly_totals[week] = weekly_totals.get(week, 0) + total

    cursor.execute("""
        SELECT 
            strftime('%Y-%W', sessionDate) as week,
            COALESCE(SUM(totalDuration), 0) as total_focus_time
        FROM stopwatch_sessions
        WHERE userID=?
        GROUP BY week
        ORDER BY week
    """, (userID,))
    for row in cursor.fetchall():
        week = row[0]
        total = row[1] or 0
        weekly_totals[week] = weekly_totals.get(week, 0) + total

    weekly_data = []
    for week in sorted(weekly_totals.keys()):
        weekly_data.append({
            "week": week,
            "total_focus_time": weekly_totals[week]
        })

    conn.close()
    return weekly_data


# MONTHLY ANALYTICS

def get_monthly_analytics(userID):
    conn = get_connection()
    cursor = conn.cursor()

    monthly_totals = {}

    cursor.execute("""
        SELECT 
            strftime('%Y-%m', sessionDate) as month,
            COALESCE(SUM(workDuration), 0) as total_focus_time
        FROM pomodoro_sessions
        WHERE userID=?
        GROUP BY month
        ORDER BY month
    """, (userID,))
    for row in cursor.fetchall():
        month = row[0]
        total = row[1] or 0
        monthly_totals[month] = monthly_totals.get(month, 0) + total

    cursor.execute("""
        SELECT 
            strftime('%Y-%m', sessionDate) as month,
            COALESCE(SUM(totalDuration), 0) as total_focus_time
        FROM stopwatch_sessions
        WHERE userID=?
        GROUP BY month
        ORDER BY month
    """, (userID,))
    for row in cursor.fetchall():
        month = row[0]
        total = row[1] or 0
        monthly_totals[month] = monthly_totals.get(month, 0) + total

    monthly_data = []
    for month in sorted(monthly_totals.keys()):
        monthly_data.append({
            "month": month,
            "total_focus_time": monthly_totals[month]
        })

    conn.close()
    return monthly_data


# SUMMARY ANALYTICS

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

    # Get break time
    cursor.execute("""
        SELECT COALESCE(SUM(breakDuration), 0)
        FROM pomodoro_sessions
        WHERE userID=?
    """, (userID,))
    break_time = cursor.fetchone()[0] or 0

    total_focus_time = pomodoro_time + stopwatch_time
    total_allocation_time = stopwatch_time + pomodoro_time + break_time

    if total_allocation_time > 0:
        deep_work_percent = round((stopwatch_time / total_allocation_time) * 100)
        study_percent = round((pomodoro_time / total_allocation_time) * 100)
        break_percent = round((break_time / total_allocation_time) * 100)
    else:
        deep_work_percent = 0
        study_percent = 0
        break_percent = 0

    conn.close()

    return {
        "tasksCompleted": tasks_completed,
        "pendingTasks": pending_tasks,
        "goalsCompleted": goals_completed,
        "totalFocusTime": total_focus_time,
        "deepWorkPercent": deep_work_percent,
        "studyPercent": study_percent,
        "breakPercent": break_percent
    }