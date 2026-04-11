from database import get_connection

def create_goal(userID, title, description="", startDate="", endDate=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO goals (userID, goalTitle, description, startDate, endDate, status) VALUES (?, ?, ?, ?, ?, ?)",
        (userID, title, description, startDate, endDate, "In Progress")
    )
    conn.commit()
    conn.close()


def get_goals(userID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals WHERE userID=?", (userID,))
    goals = cursor.fetchall()
    conn.close()
    return goals


def delete_goal(goalID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE goalID=?", (goalID,))
    cursor.execute("DELETE FROM goal_tasks WHERE goalID=?", (goalID,))
    conn.commit()
    conn.close()


def add_goal_task(goalID, taskName):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO goal_tasks (goalID, taskName, status) VALUES (?, ?, ?)",
        (goalID, taskName, "Pending")
    )
    conn.commit()
    conn.close()


def get_goal_tasks(goalID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goal_tasks WHERE goalID=?", (goalID,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def complete_goal_task(goalTaskID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE goal_tasks SET status='Completed', completionDate=datetime('now') WHERE goalTaskID=?",
        (goalTaskID,)
    )
    conn.commit()
    conn.close()


def calculate_goal_progress(goalID):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM goal_tasks WHERE goalID=?",
        (goalID,)
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM goal_tasks WHERE goalID=? AND status='Completed'",
        (goalID,)
    )
    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return (completed / total) * 100


