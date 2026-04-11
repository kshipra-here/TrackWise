def create_task(conn, userID, title, description, priority, dueDate=""):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todo_tasks (userID, title, description, priority, status, dueDate) VALUES (?, ?, ?, ?, ?, ?)",
        (userID, title, description, priority, "pending", dueDate)
    )
    conn.commit()


def get_tasks(conn, userID):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_tasks WHERE userID=?", (userID,))
    return cursor.fetchall()


def get_task_by_id(conn, taskID):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_tasks WHERE todoTaskID=?", (taskID,))
    return cursor.fetchone()


def mark_completed(conn, taskID):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todo_tasks SET status=? WHERE todoTaskID=?",
        ("completed", taskID)
    )
    conn.commit()


def delete_task(conn, taskID):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo_tasks WHERE todoTaskID=?", (taskID,))
    conn.commit()


def update_task(conn, taskID, title=None, description=None, priority=None, status=None, dueDate=None):
    cursor = conn.cursor()

    query = "UPDATE todo_tasks SET "
    params = []

    if title is not None:
        query += "title=?, "
        params.append(title)
    if description is not None:
        query += "description=?, "
        params.append(description)
    if priority is not None:
        query += "priority=?, "
        params.append(priority)
    if status is not None:
        query += "status=?, "
        params.append(status.lower())
    if dueDate is not None:
        query += "dueDate=?, "
        params.append(dueDate)

    if params:
        query = query.rstrip(", ")
        query += " WHERE todoTaskID=?"
        params.append(taskID)

        cursor.execute(query, params)
        conn.commit()