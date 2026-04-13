// Check authentication
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

const modal = document.getElementById("goalModal");
const goalContainer = document.getElementById("goalContainer");
const stepsContainer = document.getElementById("stepsContainer");
let currentGoals = [];

// Open modal
document.querySelector(".add-btn").addEventListener("click", function() {
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

// Add step input
function addStep(value = "") {
  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Enter step...";
  input.value = value;
  input.classList.add("step-input");
  stepsContainer.appendChild(input);
}

// Load goals from backend
async function loadGoals() {
  try {
    const res = await fetch(`${API_URL}/goals/${userID}`);
    if (!res.ok) throw new Error('Failed to load goals');

    currentGoals = await res.json();
    renderGoals();
  } catch (err) {
    console.error('Failed to load goals:', err);
    alert('Failed to load goals');
  }
}

// Load goal steps from backend
async function loadGoalSteps(goalID, container) {
  try {
    const res = await fetch(`${API_URL}/goal-tasks/${goalID}`);
    if (!res.ok) throw new Error('Failed to load goal steps');

    const steps = await res.json();
    container.innerHTML = "";

    if (!steps.length) {
      container.innerHTML = `<p class="no-steps">No steps added</p>`;
      return;
    }

    steps.forEach(step => {
      const stepItem = document.createElement("div");
      stepItem.className = "goal-step-item";
      stepItem.innerHTML = `
        <span>• ${step.taskName}</span>
        <span class="step-status">${step.status}</span>
      `;
      container.appendChild(stepItem);
    });
  } catch (err) {
    console.error(`Failed to load steps for goal ${goalID}:`, err);
    container.innerHTML = `<p class="no-steps">Failed to load steps</p>`;
  }
}

// Save goal
async function saveGoal() {
  const title = document.getElementById("goalTitle").value.trim();
  const type = document.getElementById("goalType").value;
  const deadline = document.getElementById("goalDeadline").value;

  if (!title) {
    alert("Please enter goal title");
    return;
  }

  try {
    // 1. Create goal
    const res = await fetch(`${API_URL}/create-goal`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        userID,
        title,
        description: type,
        startDate: new Date().toISOString().split('T')[0],
        endDate: deadline
      })
    });

    if (!res.ok) throw new Error('Failed to save goal');

    // 2. Reload goals to get latest created goal
    const goalsRes = await fetch(`${API_URL}/goals/${userID}`);
    if (!goalsRes.ok) throw new Error('Failed to reload goals');

    const goalsList = await goalsRes.json();
    if (!goalsList.length) throw new Error('Goal created but not found');

    const latestGoal = goalsList[goalsList.length - 1];
    const goalId = latestGoal.goalID;

    // 3. Save steps
    const stepInputs = document.querySelectorAll(".step-input");
    for (const input of stepInputs) {
      const stepValue = input.value.trim();
      if (stepValue !== "") {
        const stepRes = await fetch(`${API_URL}/add-goal-task`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            goalID: goalId,
            taskName: stepValue
          })
        });

        if (!stepRes.ok) {
          throw new Error(`Failed to save step: ${stepValue}`);
        }
      }
    }

    // 4. Clear form
    document.getElementById("goalTitle").value = "";
    document.getElementById("goalDeadline").value = "";
    stepsContainer.innerHTML = "";

    closeModal();
    loadGoals();
  } catch (err) {
    console.error('Failed to save goal:', err);
    alert('Failed to save goal');
  }
}

// Delete goal
async function deleteGoal(goalID) {
  if (confirm("Are you sure you want to delete this goal?")) {
    try {
      const res = await fetch(`${API_URL}/delete-goal/${goalID}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json"
        }
      });

      if (!res.ok) throw new Error('Failed to delete goal');

      loadGoals();
    } catch (err) {
      console.error('Failed to delete goal:', err);
      alert('Failed to delete goal');
    }
  }
}

// Toggle goal completion
async function toggleComplete(goalID) {
  try {
    const res = await fetch(`${API_URL}/complete-goal/${goalID}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) {
      throw new Error('Failed to update goal');
    }

    loadGoals();
  } catch (err) {
    console.error('Failed to toggle goal:', err);
    alert('Failed to update goal');
  }
}

// Render goals
function renderGoals() {
  goalContainer.innerHTML = "";

  currentGoals.forEach(goal => {
    const card = document.createElement("div");
    card.className = "task-card";
    if (goal.status === "completed") card.classList.add("completed");

    const deadline = goal.endDate
      ? new Date(goal.endDate).toLocaleDateString("en-GB", {
          day: "numeric",
          month: "short",
          year: "numeric"
        })
      : "No deadline set";

    card.innerHTML = `
      <button class="delete-btn" onclick="deleteGoal(${goal.goalID})">×</button>

      <h3>${goal.title}</h3>

      <p class="deadline">
        Deadline: ${deadline}
      </p>

      <span class="priority">${goal.description} Goal</span>

      <div id="steps-${goal.goalID}" class="goal-steps"></div>

      <button class="complete-btn" onclick="toggleComplete(${goal.goalID})">
        ${goal.status === "completed" ? "completed ✓" : "Mark as completed"}
      </button>
    `;

    goalContainer.appendChild(card);

    const stepContainer = document.getElementById(`steps-${goal.goalID}`);
    loadGoalSteps(goal.goalID, stepContainer);
  });
}

// Initialize
document.addEventListener("DOMContentLoaded", loadGoals);

// Modal buttons
document.querySelector(".cancel").addEventListener("click", closeModal);
document.querySelector(".save").addEventListener("click", saveGoal);
document.querySelector(".add-step-btn").addEventListener("click", function() {
  addStep();
});