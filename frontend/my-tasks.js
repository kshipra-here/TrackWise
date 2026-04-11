// Check authentication
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

const modal = document.getElementById("taskModal");
let tasks = [];

// Open modal
document.querySelector(".add-task-btn").addEventListener("click", function () {
  modal.style.display = "flex";
});

// Close modal
function closeModal() {
  modal.style.display = "none";
}

window.addEventListener("click", (e) => {
  if (e.target === modal) {
    closeModal();
  }
});

// Load tasks from backend
async function loadTasks() {
  try {
    const res = await fetch(`${API_URL}/tasks/${userID}`);
    if (!res.ok) throw new Error("Failed to load tasks");

    tasks = await res.json();
    renderTasks();
  } catch (err) {
    console.error("Failed to load tasks:", err);
    alert("Failed to load tasks");
  }
}

// Save task to backend
async function saveTask() {
  const title = document.getElementById("taskTitle").value.trim();
  const desc = document.getElementById("taskDesc").value.trim();
  const priority = document.getElementById("taskPriority").value;
  const date = document.getElementById("taskDate").value;

  if (!title) {
    alert("Task title is required");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/add-task`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        userID,
        title,
        description: desc,
        priority,
        dueDate: date
      })
    });

    if (!res.ok) throw new Error("Failed to save task");

    // Clear form
    document.getElementById("taskTitle").value = "";
    document.getElementById("taskDesc").value = "";
    document.getElementById("taskDate").value = "";

    closeModal();
    loadTasks();
  } catch (err) {
    console.error("Failed to save task:", err);
    alert("Failed to save task");
  }
}

// Toggle task completion
async function toggleTask(taskID) {
  try {
    const res = await fetch(`${API_URL}/complete-task/${taskID}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) throw new Error("Failed to update task");

    await loadTasks();
  } catch (err) {
    console.error("Failed to toggle task:", err);
    alert("Failed to update task");
  }
}

// Delete task
async function deleteTask(taskID) {
  if (confirm("Are you sure you want to delete this task?")) {
    try {
      const res = await fetch(`${API_URL}/delete-task/${taskID}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json"
        }
      });

      if (!res.ok) throw new Error("Failed to delete task");

      await loadTasks();
    } catch (err) {
      console.error("Failed to delete task:", err);
      alert("Failed to delete task");
    }
  }
}

// Render tasks
function renderTasks() {
  const taskList = document.querySelector(".task-list");
  taskList.innerHTML = "";

  let total = tasks.length;
  let completed = 0;
  let pending = 0;
  let overdue = 0;

  const today = new Date().toISOString().split("T")[0];

  tasks.forEach(task => {
    const status = (task.status || "").toLowerCase();

    if (status === "completed") {
      completed++;
    } else {
      pending++;
    }

    if (status !== "completed" && task.dueDate && task.dueDate < today) {
      overdue++;
    }

    const taskCard = document.createElement("div");
    taskCard.classList.add("task-card");

    if (status === "completed") {
      taskCard.classList.add("completed");
    }

    if (status !== "completed" && task.dueDate && task.dueDate < today) {
      taskCard.classList.add("overdue");
    }

    taskCard.innerHTML = `
      <div class="task-info">
        <h4>${task.title}</h4>
        <span class="priority ${task.priority.toLowerCase()}">
          ${task.priority}
        </span>
      </div>

      <div class="task-meta">
        <span>Due: ${task.dueDate || "No date"}</span>
      </div>

      <div class="task-actions">
        <a href="pomodoro.html?from=tasks&taskId=${task.todoTaskID}">
          <button class="session-btn">Start Pomodoro</button>
        </a>

        <a href="focus-session.html?from=tasks&taskId=${task.todoTaskID}">
          <button class="session-btn">Start Focus Session</button>
        </a>

        <button class="complete-btn" onclick="toggleTask(${task.todoTaskID})">
          ${status === "completed" ? "Completed ✓" : "Mark as Completed"}
        </button>

        <button class="delete-btn" onclick="deleteTask(${task.todoTaskID})">Delete</button>
      </div>
    `;

    taskList.appendChild(taskCard);
  });

  // Update Summary
  document.getElementById("totalCount").textContent = total;
  document.getElementById("completedCount").textContent = completed;
  document.getElementById("pendingCount").textContent = pending;
  document.getElementById("overdueCount").textContent = overdue;
}

// Initialize
document.addEventListener("DOMContentLoaded", loadTasks);

// Close modal button
document.querySelector(".cancel").addEventListener("click", closeModal);
document.querySelector(".save").addEventListener("click", saveTask);