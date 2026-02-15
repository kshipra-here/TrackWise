from flask import Flask, request, jsonify
from database import get_connection
from todo import create_task, get_tasks, mark_completed
from goals import (
    create_goal,
    add_goal_task,
    complete_goal_task,
    calculate_goal_progress
)



app = Flask(__name__)

@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json

    if not data or "userID" not in data:
        return {"error": "Invalid data"}, 400

    conn = get_connection()
    create_task(conn, data["userID"], data["title"], data["description"], data["priority"])
    return {"message": "Task added successfully"}


@app.route("/tasks/<int:userID>")
def tasks(userID):
    conn = get_connection()
    tasks = get_tasks(conn, userID)
    return jsonify(tasks)

#app.run(debug=True)


@app.route("/complete-task/<int:taskID>", methods=["PUT"])
def complete_task(taskID):
    conn = get_connection()
    mark_completed(conn, taskID)
    return {"message": "Task marked as completed"}

#for testing the connections
#@app.route("/ping")
#def ping():
#    return "pong"


from auth import create_user

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    create_user(data["name"], data["email"], data["password"])
    return {"message": "User created successfully"}


from auth import login_user

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = login_user(data["email"], data["password"])

    if user:
        return {
            "message": "Login successful",
            "userID": user[0],
            "name": user[1]
        }
    else:
        return {"error": "Invalid credentials"}, 401

@app.route("/create-goal", methods=["POST"])
def create_goal_api():
    data = request.json
    create_goal(data["userID"],data["title"],data["description"],data["startDate"],data["endDate"])
    return {"message": "Goal created successfully"}

@app.route("/add-goal-task", methods=["POST"])
def add_goal_task_api():
    data = request.json
    add_goal_task(data["goalID"], data["taskName"])
    return {"message": "Goal task added"}

@app.route("/complete-goal-task/<int:goalTaskID>", methods=["PUT"])
def complete_goal_task_api(goalTaskID):
    complete_goal_task(goalTaskID)
    return {"message": "Goal task completed"}

@app.route("/goal-progress/<int:goalID>")
def goal_progress(goalID):
    progress = calculate_goal_progress(goalID)
    return {"goalID": goalID, "progress": progress}





app.run(debug=True)
