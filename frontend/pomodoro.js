// Check if user is logged in
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

let time = 25 * 60;
let timerInterval = null;
let isRunning = false;
let sessions = 0;
let focusMinutes = 0;
let sessionStartTime = null;

const timerDisplay = document.getElementById("timer");
const modeText = document.getElementById("mode");

// SMART BACK BUTTON + TASK DATA
const params = new URLSearchParams(window.location.search);
const from = params.get("from");
const taskId = params.get("taskId");

const backBtn = document.getElementById("backBtn");

if (from === "tasks") {
  backBtn.href = "my-tasks.html";
} else {
  backBtn.href = "dashboard.html";
}

// Show task info
if (from === "tasks" && taskId) {
  fetch(`${API_URL}/task/${taskId}`)
    .then(res => res.json())
    .then(task => {
      document.getElementById("taskInfo").style.display = "block";
      document.getElementById("taskTitleDisplay").textContent =
        "Working on: " + task.title;
    })
    .catch(err => console.error('Failed to load task:', err));
}

// Timer display
function updateDisplay() {
  const minutes = Math.floor(time / 60);
  const seconds = time % 60;
  timerDisplay.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
}

function startTimer() {
  if (isRunning) return;

  isRunning = true;

  if (!sessionStartTime && modeText.textContent === "Focus") {
    sessionStartTime = new Date().toISOString();
  }

  timerInterval = setInterval(async () => {
    if (time > 0) {
      time--;
      updateDisplay();
    } else {
      clearInterval(timerInterval);
      timerInterval = null;
      isRunning = false;

      if (modeText.textContent === "Focus") {
        sessions++;
        focusMinutes += 25;

        document.getElementById("sessionsDone").textContent = sessions;
        document.getElementById("focusTime").textContent = focusMinutes + " min";

        await savePomodoroSession(
          sessionStartTime,
          new Date().toISOString(),
          25 * 60,
          5 * 60
        );

        sessionStartTime = null;
      }

      alert("Session completed! 🎉");
    }
  }, 1000);
}

function pauseTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  isRunning = false;
}

function resetTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  isRunning = false;
  time = 25 * 60;
  modeText.textContent = "Focus";
  sessionStartTime = null;
  updateDisplay();

  document.querySelectorAll(".mode-selector button")
    .forEach(btn => btn.classList.remove("active"));

  document.querySelector(".mode-selector button")
    .classList.add("active");
}

function setMode(minutes, mode, event) {
  clearInterval(timerInterval);
  timerInterval = null;
  isRunning = false;

  time = minutes * 60;
  modeText.textContent = mode;

  if (mode !== "Focus") {
    sessionStartTime = null;
  }

  updateDisplay();

  document.querySelectorAll(".mode-selector button")
    .forEach(btn => btn.classList.remove("active"));

  event.target.classList.add("active");
}

updateDisplay();

// Save pomodoro session
async function savePomodoroSession(startTime, endTime, workDuration, breakDuration) {
  try {
    const res = await fetch(`${API_URL}/start-pomodoro`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        userID,
        startTime,
        endTime,
        workDuration,
        breakDuration
      })
    });

    if (!res.ok) {
      throw new Error("Failed to save pomodoro session");
    }

    console.log("Pomodoro session saved");
  } catch (err) {
    console.error('Failed to save pomodoro session', err);
  }
}