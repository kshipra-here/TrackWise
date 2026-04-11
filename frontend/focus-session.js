// Check if user is logged in
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

let seconds = 0;
let timerInterval = null;
let quoteInterval = null;
let sessionStartTime = null;

const timerDisplay = document.getElementById("timer");
const quoteDisplay = document.getElementById("quote");

const backBtn = document.getElementById("backBtn");

// SMART BACK BUTTON + TASK DISPLAY
const params = new URLSearchParams(window.location.search);
const from = params.get("from");
const taskId = params.get("taskId");

if (from === "tasks") {
    backBtn.onclick = function () {
        window.location.href = "my-tasks.html";
    };
} else {
    backBtn.onclick = function () {
        window.location.href = "dashboard.html";
    };
}

// Show task info if opened from tasks
async function loadSelectedTask() {
    if (from !== "tasks" || !taskId) return;

    try {
        const res = await fetch(`${API_URL}/task/${taskId}`);
        if (!res.ok) throw new Error("Failed to load selected task");

        const selectedTask = await res.json();

        if (selectedTask) {
            document.getElementById("taskInfo").style.display = "block";
            document.getElementById("taskTitleDisplay").textContent =
                "Working on: " + selectedTask.title;
        }
    } catch (err) {
        console.error("Failed to load selected task:", err);
    }
}

// Timer logic
const quotes = [
    "Discipline equals freedom.",
    "Stay consistent, not perfect.",
    "Your future self is watching.",
    "Focus now. Celebrate later.",
    "You’re stronger than distractions.",
    "Deep work creates deep results.",
    "One focused hour beats three distracted ones.",
    "Success is built in focused moments.",
    "Eliminate distractions. Elevate results.",
    "Focus is the bridge between dreams and achievement."
];

function updateDisplay() {
    let hrs = Math.floor(seconds / 3600);
    let mins = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;

    hrs = hrs < 10 ? "0" + hrs : hrs;
    mins = mins < 10 ? "0" + mins : mins;
    secs = secs < 10 ? "0" + secs : secs;

    timerDisplay.textContent = `${hrs}:${mins}:${secs}`;
}

function startTimer() {
    if (timerInterval) return;

    sessionStartTime = new Date().toISOString();

    timerInterval = setInterval(() => {
        seconds++;
        updateDisplay();
    }, 1000);

    startQuoteRotation();
}

function pauseTimer() {
    if (!timerInterval) return;

    clearInterval(timerInterval);
    timerInterval = null;

    clearInterval(quoteInterval);
    quoteInterval = null;

    // Save session
    saveStopwatchSession(sessionStartTime, new Date().toISOString(), seconds);
}

function resetTimer() {
    clearInterval(timerInterval);
    clearInterval(quoteInterval);

    timerInterval = null;
    quoteInterval = null;

    seconds = 0;
    updateDisplay();
}

function startQuoteRotation() {
    if (quoteInterval) return;

    changeQuote();

    quoteInterval = setInterval(() => {
        changeQuote();
    }, 60000);
}

function changeQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    quoteDisplay.textContent = quotes[randomIndex];
}

const rainSound = document.getElementById("rainSound");
const forestSound = document.getElementById("forestSound");

function changeSound(value) {
    rainSound.pause();
    forestSound.pause();
    rainSound.currentTime = 0;
    forestSound.currentTime = 0;

    if (value === "rain") {
        rainSound.play();
    } else if (value === "forest") {
        forestSound.play();
    }
}

updateDisplay();
loadSelectedTask();

// Save stopwatch session
async function saveStopwatchSession(startTime, endTime, totalDuration) {
  try {
    const res = await fetch(`${API_URL}/start-stopwatch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        userID,
        startTime,
        endTime,
        totalDuration
      })
    });

    if (!res.ok) {
      throw new Error("Failed to save stopwatch session");
    }

    console.log("Stopwatch session saved");

  } catch (err) {
    console.error('Failed to save stopwatch session', err);
  }
}