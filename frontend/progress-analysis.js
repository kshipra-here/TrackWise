// Check authentication
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

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
    document.getElementById('totalFocusTime').textContent =
      Math.floor((summary.totalFocusTime || 0) / 60) + ' hours';

    // Daily
    const dailyRes = await fetch(`${API_URL}/analytics/daily/${userID}`);
    const daily = await dailyRes.json();
    createDailyChart(daily);

    // Weekly
    const weeklyRes = await fetch(`${API_URL}/analytics/weekly/${userID}`);
    const weekly = await weeklyRes.json();
    createWeeklyChart(weekly);

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
        tension: 0.1
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
  const focusTime = data.map(d => Math.floor((d.total_focus_time || 0) / 60));

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
    const data = weekly.map(w => {
      const completed = w.tasks_completed || 0;
      const total = (w.tasks_completed || 0) + (w.pending_tasks || 0);
      return total > 0 ? Math.round((completed / total) * 100) : 0;
    });

    new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Weekly Progress %',
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
        scales: { y: { beginAtZero: true, max: 100 } }
      }
    });
  } catch (err) {
    console.error('Failed to load monthly chart:', err);
  }
}

// Init
document.addEventListener("DOMContentLoaded", function() {
  loadAnalytics();
  createTaskStatusChart();
  createSessionChart();
  createMonthlyChart();
});