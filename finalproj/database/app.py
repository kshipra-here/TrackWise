from flask import Flask, request, jsonify
from database import get_connection
from todo import create_task, get_tasks, mark_completed

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

@app.route("/ping")
def ping():
    return "pong"



app.run(debug=True)
