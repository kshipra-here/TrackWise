from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection
from todo import create_task, get_tasks, mark_completed, delete_task, get_task_by_id, update_task
from goals import (
    create_goal,
    add_goal_task,
    complete_goal_task,
    calculate_goal_progress,
    get_goals,
    get_goal_tasks,
    delete_goal
)



app = Flask(__name__)
CORS(app)

# Initialize database tables on startup
def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            createdAt TEXT
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS todo_tasks (
            todoTaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            title TEXT,
            description TEXT,
            priority TEXT,
            status TEXT,
            dueDate TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS goals (
            goalID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            goalTitle TEXT,
            description TEXT,
            startDate TEXT,
            endDate TEXT,
            status TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS goal_tasks (
            goalTaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            goalID INTEGER,
            taskName TEXT,
            status TEXT,
            completionDate TEXT,
            FOREIGN KEY(goalID) REFERENCES goals(goalID)
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            pomodoroID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            startTime TEXT,
            endTime TEXT,
            workDuration INTEGER,
            breakDuration INTEGER,
            sessionDate TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS stopwatch_sessions (
            stopwatchID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            startTime TEXT,
            endTime TEXT,
            totalDuration INTEGER,
            sessionDate TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS user_settings (
            settingID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER UNIQUE,
            reminderTime TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID)
        )""")
        
        conn.close()
    except Exception as e:
        print(f"Database init error: {e}")

# Initialize database on app start
init_db()

@app.route("/add-task", methods=["POST"])
def add_task():
    try:
        data = request.json

        if not data or "userID" not in data:
            return {"error": "Invalid data"}, 400

        conn = get_connection()
        create_task(conn, data["userID"], data["title"], data.get("description", ""), data.get("priority", "Medium"), data.get("dueDate", ""))
        conn.close()
        return {"message": "Task added successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/tasks/<int:userID>")
def tasks(userID):
    try:
        conn = get_connection()
        tasks_list = get_tasks(conn, userID)
        conn.close()
        
        tasks_data = []
        for task in tasks_list:
            tasks_data.append({
                "todoTaskID": task[0],
                "userID": task[1],
                "title": task[2],
                "description": task[3],
                "priority": task[4],
                "status": task[5],
                "dueDate": task[6]
            })
        
        return jsonify(tasks_data)
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/task/<int:taskID>")
def get_task(taskID):
    try:
        conn = get_connection()
        task = get_task_by_id(conn, taskID)
        conn.close()
        
        if task:
            return jsonify({
                "todoTaskID": task[0],
                "userID": task[1],
                "title": task[2],
                "description": task[3],
                "priority": task[4],
                "status": task[5],
                "dueDate": task[6]
            })
        else:
            return {"error": "Task not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/complete-task/<int:taskID>", methods=["PUT"])
def complete_task(taskID):
    try:
        conn = get_connection()
        mark_completed(conn, taskID)
        conn.close()
        return {"message": "Task marked as completed"}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/delete-task/<int:taskID>", methods=["DELETE"])
def delete_task_api(taskID):
    try:
        conn = get_connection()
        delete_task(conn, taskID)
        conn.close()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/update-task/<int:taskID>", methods=["PUT"])
def update_task_api(taskID):
    try:
        data = request.json
        conn = get_connection()
        update_task(conn, taskID, data.get("title"), data.get("description"), data.get("priority"), data.get("status"), data.get("dueDate"))
        conn.close()
        return {"message": "Task updated successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


from auth import create_user, login_user

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        create_user(data["name"], data["email"], data["password"])
        return {"message": "User created successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        user = login_user(data["email"], data["password"])

        if user:
            return {
                "message": "Login successful",
                "userID": user[0],
                "name": user[1],
                "email": data["email"]
            }, 200
        else:
            return {"error": "Invalid credentials"}, 401
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/create-goal", methods=["POST"])
def create_goal_api():
    try:
        data = request.json
        create_goal(data["userID"], data["title"], data.get("description", ""), data.get("startDate", ""), data.get("endDate", ""))
        return {"message": "Goal created successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/goals/<int:userID>")
def goals_api(userID):
    try:
        goals_list = get_goals(userID)
        goals_data = []
        for goal in goals_list:
            goals_data.append({
                "goalID": goal[0],
                "userID": goal[1],
                "title": goal[2],
                "description": goal[3],
                "startDate": goal[4],
                "endDate": goal[5],
                "status": goal[6]
            })
        return jsonify(goals_data)
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/goal-tasks/<int:goalID>")
def goal_tasks_api(goalID):
    try:
        tasks_list = get_goal_tasks(goalID)
        tasks_data = []
        for task in tasks_list:
            tasks_data.append({
                "goalTaskID": task[0],
                "goalID": task[1],
                "taskName": task[2],
                "status": task[3],
                "completionDate": task[4]
            })
        return jsonify(tasks_data)
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/add-goal-task", methods=["POST"])
def add_goal_task_api():
    try:
        data = request.json
        add_goal_task(data["goalID"], data["taskName"])
        return {"message": "Goal task added"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/complete-goal-task/<int:goalTaskID>", methods=["PUT"])
def complete_goal_task_api(goalTaskID):
    try:
        complete_goal_task(goalTaskID)
        return {"message": "Goal task completed"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/complete-goal/<int:goalID>", methods=["PUT"])
def complete_goal_api(goalID):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE goals SET status = ? WHERE goalID = ?",
            ("completed", goalID)
        )

        conn.commit()
        conn.close()

        return {"message": "Goal marked as completed"}

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/goal-progress/<int:goalID>")
def goal_progress(goalID):
    try:
        progress = calculate_goal_progress(goalID)
        return {"goalID": goalID, "progress": progress}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/delete-goal/<int:goalID>", methods=["DELETE"])
def delete_goal_api(goalID):
    try:
        delete_goal(goalID)
        return {"message": "Goal deleted successfully"}
    except Exception as e:
        return {"error": str(e)}, 500




from sessions import start_pomodoro, start_stopwatch, get_sessions

@app.route("/start-pomodoro", methods=["POST"])
def start_pomodoro_api():
    try:
        data = request.json
        start_pomodoro(
            data["userID"],
            data["startTime"],
            data["endTime"],
            data["workDuration"],
            data["breakDuration"]
        )
        return {"message": "Pomodoro session saved"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/start-stopwatch", methods=["POST"])
def start_stopwatch_api():
    try:
        data = request.json
        start_stopwatch(
            data["userID"],
            data["startTime"],
            data["endTime"],
            data["totalDuration"]
        )
        return {"message": "Stopwatch session saved"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/sessions/<int:userID>")
def sessions_api(userID):
    try:
        data = get_sessions(userID)
        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500




from analytics import get_daily_analytics, get_weekly_analytics, get_summary

@app.route("/analytics/daily/<int:userID>")
def daily_analytics(userID):
    try:
        data = get_daily_analytics(userID)
        return jsonify(data) if isinstance(data, list) else data
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/analytics/weekly/<int:userID>")
def weekly_analytics(userID):
    try:
        data = get_weekly_analytics(userID)
        return jsonify(data) if isinstance(data, list) else data
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/analytics/summary/<int:userID>")
def summary_analytics(userID):
    try:
        data = get_summary(userID)
        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route("/update-profile/<int:userID>", methods=["PUT"])
def update_profile(userID):
    try:
        data = request.json
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()

        if not name or not email:
            return {"error": "Name and email are required"}, 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE userID = ?",
            (name, email, userID)
        )

        conn.commit()
        conn.close()

        return {"message": "Profile updated successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/update-password/<int:userID>", methods=["PUT"])
def update_password(userID):
    try:
        data = request.json
        current_password = data.get("currentPassword", "").strip()
        new_password = data.get("newPassword", "").strip()

        if not current_password or not new_password:
            return {"error": "Current password and new password are required"}, 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE userID = ?",
            (userID,)
        )
        user = cursor.fetchone()

        if not user:
            conn.close()
            return {"error": "User not found"}, 404

        if user[0] != current_password:
            conn.close()
            return {"error": "Current password is incorrect"}, 400

        cursor.execute(
            "UPDATE users SET password = ? WHERE userID = ?",
            (new_password, userID)
        )

        conn.commit()
        conn.close()

        return {"message": "Password updated successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/update-notifications/<int:userID>", methods=["PUT"])
def update_notifications(userID):
    try:
        data = request.json
        reminder_time = data.get("reminderTime", "").strip()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT settingID FROM user_settings WHERE userID = ?",
            (userID,)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE user_settings SET reminderTime = ? WHERE userID = ?",
                (reminder_time, userID)
            )
        else:
            cursor.execute(
                "INSERT INTO user_settings (userID, reminderTime) VALUES (?, ?)",
                (userID, reminder_time)
            )

        conn.commit()
        conn.close()

        return {"message": "Notification settings updated successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get-notifications/<int:userID>", methods=["GET"])
def get_notifications(userID):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT reminderTime FROM user_settings WHERE userID = ?",
            (userID,)
        )
        row = cursor.fetchone()

        conn.close()

        return {
            "reminderTime": row[0] if row else ""
        }
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/delete-account/<int:userID>", methods=["DELETE"])
def delete_account(userID):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM user_settings WHERE userID = ?", (userID,))
        cursor.execute("DELETE FROM todo_tasks WHERE userID = ?", (userID,))
        cursor.execute("DELETE FROM goals WHERE userID = ?", (userID,))
        cursor.execute("DELETE FROM pomodoro_sessions WHERE userID = ?", (userID,))
        cursor.execute("DELETE FROM stopwatch_sessions WHERE userID = ?", (userID,))
        cursor.execute("DELETE FROM users WHERE userID = ?", (userID,))

        conn.commit()
        conn.close()

        return {"message": "Account deleted successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/export-data/<int:userID>", methods=["GET"])
def export_data(userID):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT userID, name, email, createdAt FROM users WHERE userID = ?",
            (userID,)
        )
        user = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM todo_tasks WHERE userID = ?",
            (userID,)
        )
        tasks = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM goals WHERE userID = ?",
            (userID,)
        )
        goals = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM pomodoro_sessions WHERE userID = ?",
            (userID,)
        )
        pomodoro_sessions = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM stopwatch_sessions WHERE userID = ?",
            (userID,)
        )
        stopwatch_sessions = cursor.fetchall()

        cursor.execute(
            "SELECT reminderTime FROM user_settings WHERE userID = ?",
            (userID,)
        )
        settings = cursor.fetchone()

        conn.close()

        return jsonify({
            "user": {
                "userID": user[0],
                "name": user[1],
                "email": user[2],
                "createdAt": user[3]
            } if user else None,
            "tasks": tasks,
            "goals": goals,
            "pomodoroSessions": pomodoro_sessions,
            "stopwatchSessions": stopwatch_sessions,
            "settings": {
                "reminderTime": settings[0]
            } if settings else {}
        })
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
