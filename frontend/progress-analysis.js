// Check authentication
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

function formatTime(seconds) {
  seconds = seconds || 0;

  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  return `${hrs}h ${mins}m ${secs}s`;
}

// Load analytics data
async function loadAnalytics() {
  try {
    const summaryRes = await fetch(`${API_URL}/analytics/summary/${userID}`);
    const summary = await summaryRes.json();

    const tasksCompleted = summary.tasksCompleted || 0;
    const pendingTasks = summary.pendingTasks || 0;
    const totalTasks = tasksCompleted + pendingTasks;

    let productivityScore = totalTasks > 0
      ? Math.round((tasksCompleted / totalTasks) * 100)
      : 0;

    let scoreLabel = "No data available";
    if (totalTasks > 0) {
      if (productivityScore >= 80) scoreLabel = "Excellent Performance";
      else if (productivityScore >= 60) scoreLabel = "Above Average Performance";
      else if (productivityScore >= 40) scoreLabel = "Average Performance";
      else scoreLabel = "Needs Improvement";
    }

    document.getElementById('productivityScore').textContent = productivityScore + ' / 100';
    document.getElementById('scoreLabel').textContent = scoreLabel;

    document.getElementById('completedTasks').textContent = tasksCompleted;
    document.getElementById('pendingTasks').textContent = pendingTasks;
    document.getElementById('goalsAchieved').textContent = summary.goalsCompleted || 0;
    document.getElementById('totalFocusTime').textContent = formatTime(summary.totalFocusTime || 0);

    // Daily
    const dailyRes = await fetch(`${API_URL}/analytics/daily/${userID}`);
    const daily = await dailyRes.json();
    createDailyChart(daily);

    // Weekly
    const weeklyRes = await fetch(`${API_URL}/analytics/weekly/${userID}`);
    const weekly = await weeklyRes.json();
    createWeeklyChart(weekly);

    // Goal progress
    await loadGoalProgress();

    // Insights
    await loadInsights(summary);

  } catch (err) {
    console.error('Failed to load analytics:', err);
  }
}

// Daily chart
function createDailyChart(data) {
  const ctx = document.getElementById("dailyChart");
  if (!ctx || !Array.isArray(data)) return;

  const labels = data.map(d => d.date || "");
  const tasks = data.map(d => d.tasks_completed || 0);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Tasks Completed',
        data: tasks,
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.1,
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: { y: { beginAtZero: true } }
    }
  });
}

// Weekly chart
function createWeeklyChart(data) {
  const ctx = document.getElementById("weeklyChart");
  if (!ctx || !Array.isArray(data)) return;

  const labels = data.map(d => `Week ${d.week || ""}`);
  const focusTime = data.map(d => Number(((d.total_focus_time || 0) / 3600).toFixed(2)));

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Focus Time (hours)',
        data: focusTime,
        backgroundColor: '#10B981',
        borderColor: '#059669',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: { y: { beginAtZero: true } }
    }
  });
}

// Task status chart
async function createTaskStatusChart() {
  const ctx = document.getElementById("taskStatusChart");
  if (!ctx) return;

  try {
    const summaryRes = await fetch(`${API_URL}/analytics/summary/${userID}`);
    const summary = await summaryRes.json();

    const completed = summary.tasksCompleted || 0;
    const pending = summary.pendingTasks || 0;

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'Pending'],
        datasets: [{
          data: [completed, pending],
          backgroundColor: ['#10B981', '#3B82F6'],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: true } }
      }
    });
  } catch (err) {
    console.error('Failed to load task status chart:', err);
  }
}

// Session chart
async function createSessionChart() {
  const ctx = document.getElementById("sessionChart");
  if (!ctx) return;

  try {
    const sessionsRes = await fetch(`${API_URL}/sessions/${userID}`);
    const sessions = await sessionsRes.json();

    let pomodoroCount = 0;
    let focusCount = 0;

    if (Array.isArray(sessions)) {
      sessions.forEach(session => {
        if (session.type === 'pomodoro') pomodoroCount++;
        else if (session.type === 'stopwatch') focusCount++;
      });
    }

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Pomodoro', 'Focus Sessions'],
        datasets: [{
          data: [pomodoroCount, focusCount],
          backgroundColor: ['#F59E0B', '#8B5CF6'],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: true } }
      }
    });
  } catch (err) {
    console.error('Failed to load session chart:', err);
  }
}

// Monthly chart
async function createMonthlyChart() {
  const ctx = document.getElementById("monthlyChart");
  if (!ctx) return;

  try {
    const weeklyRes = await fetch(`${API_URL}/analytics/weekly/${userID}`);
    const weekly = await weeklyRes.json();

    if (!Array.isArray(weekly) || weekly.length === 0) return;

    const labels = weekly.map(w => `Week ${w.week || ''}`);
    const data = weekly.map(w => Number(((w.total_focus_time || 0) / 3600).toFixed(2)));

    new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Monthly Focus Trend (hours)',
          data,
          borderColor: '#06B6D4',
          backgroundColor: 'rgba(6, 182, 212, 0.1)',
          tension: 0.1,
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: true } },
        scales: { y: { beginAtZero: true } }
      }
    });
  } catch (err) {
    console.error('Failed to load monthly chart:', err);
  }
}

// Goal progress section
async function loadGoalProgress() {
  try {
    const res = await fetch(`${API_URL}/goals/${userID}`);
    if (!res.ok) throw new Error("Failed to load goals");

    const goals = await res.json();

    const totalGoals = goals.length;
    const completedGoals = goals.filter(goal =>
      goal.status && goal.status.trim().toLowerCase() === "completed"
    ).length;

    const percent = totalGoals > 0
      ? Math.round((completedGoals / totalGoals) * 100)
      : 0;

    const goalProgressBar = document.getElementById("goalProgressBar");
    const consistencyText = document.getElementById("consistencyText");

    if (goalProgressBar) {
      goalProgressBar.style.width = `${percent}%`;
    }

    if (consistencyText) {
      if (totalGoals === 0) {
        consistencyText.textContent = "No goals added yet.";
      } else {
        consistencyText.textContent = `${completedGoals} of ${totalGoals} goals completed (${percent}%)`;
      }
    }
  } catch (err) {
    console.error("Failed to load goal progress:", err);
  }
}

// Insights section
async function loadInsights(summary) {
  try {
    const insightsText = document.getElementById("insightsText");
    if (!insightsText) return;

    const tasksCompleted = summary.tasksCompleted || 0;
    const pendingTasks = summary.pendingTasks || 0;
    const goalsCompleted = summary.goalsCompleted || 0;
    const totalFocusTime = summary.totalFocusTime || 0;

    let message = "";

    if (tasksCompleted === 0 && totalFocusTime === 0) {
      message = "No activity recorded yet. Start a focus session or complete a task to see performance insights.";
    } else if (tasksCompleted >= 5 && totalFocusTime >= 3600) {
      message = "Excellent consistency. You completed multiple tasks and spent strong focused time on your work.";
    } else if (tasksCompleted > pendingTasks) {
      message = "Good momentum. You are completing more tasks than you are leaving pending.";
    } else if (pendingTasks > tasksCompleted) {
      message = "You have more pending tasks than completed ones right now. Try finishing a few small tasks first to build momentum.";
    } else if (goalsCompleted > 0) {
      message = "Nice progress on your goals. Keep the same pace to improve your overall productivity score.";
    } else if (totalFocusTime > 0) {
      message = "You are spending time focusing well. Now convert that focus into more completed tasks for stronger progress.";
    } else {
      message = "Keep going. A little daily progress will make your analytics stronger over time.";
    }

    insightsText.textContent = message;
  } catch (err) {
    console.error("Failed to load insights:", err);
  }
}

// Init
document.addEventListener("DOMContentLoaded", function() {
  loadAnalytics();
  createTaskStatusChart();
  createSessionChart();
  createMonthlyChart();
});