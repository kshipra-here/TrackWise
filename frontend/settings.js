// Check authentication
if (!localStorage.getItem('userID')) {
  window.location.href = 'auth.html';
}

const userID = parseInt(localStorage.getItem('userID'));
const API_URL = 'http://127.0.0.1:5000';

// Show/hide sections
function showSection(sectionId) {
  document.querySelectorAll('.section').forEach(sec => {
    sec.classList.remove('active-section');
  });

  const selectedSection = document.getElementById(sectionId);
  if (selectedSection) {
    selectedSection.classList.add('active-section');
  }

  document.querySelectorAll('.sidebar button').forEach(btn => {
    btn.classList.remove('active');
  });

  const clickedButton = Array.from(document.querySelectorAll('.sidebar button'))
    .find(btn => btn.getAttribute('onclick')?.includes(sectionId));

  if (clickedButton) {
    clickedButton.classList.add('active');
  }
}

// Load profile data
async function loadProfile() {
  try {
    const nameInput = document.getElementById('profileName');
    const emailInput = document.getElementById('profileEmail');

    if (nameInput) {
      nameInput.value = localStorage.getItem('name') || '';
    }

    if (emailInput) {
      emailInput.value = localStorage.getItem('email') || '';
    }
  } catch (err) {
    console.error('Failed to load profile:', err);
  }
}

// Save profile changes
async function saveProfile() {
  const nameInput = document.getElementById('profileName');
  const emailInput = document.getElementById('profileEmail');

  const name = nameInput.value.trim();
  const email = emailInput.value.trim();

  if (!name || !email) {
    alert('Please fill all profile fields');
    return;
  }

  try {
    const res = await fetch(`${API_URL}/update-profile/${userID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name,
        email
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to update profile');
    }

    localStorage.setItem('name', name);
    localStorage.setItem('email', email);

    alert('Profile updated successfully!');
  } catch (err) {
    console.error('Failed to update profile:', err);
    alert(err.message || 'Failed to update profile');
  }
}

// Save notifications
async function saveNotifications() {
  const reminderInput = document.getElementById('reminderTime');
  const reminderTime = reminderInput.value;

  try {
    const res = await fetch(`${API_URL}/update-notifications/${userID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        reminderTime
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to update notifications');
    }

    alert('Notification settings updated successfully!');
  } catch (err) {
    console.error('Failed to update notifications:', err);
    alert(err.message || 'Failed to update notifications');
  }
}

// Update password
async function updatePassword() {
  const currentPasswordInput = document.getElementById('currentPassword');
  const newPasswordInput = document.getElementById('newPassword');
  const confirmPasswordInput = document.getElementById('confirmPassword');

  const currentPassword = currentPasswordInput.value.trim();
  const newPassword = newPasswordInput.value.trim();
  const confirmPassword = confirmPasswordInput.value.trim();

  if (!currentPassword || !newPassword || !confirmPassword) {
    alert('Please fill all password fields');
    return;
  }

  if (newPassword.length < 6) {
    alert('New password must be at least 6 characters long');
    return;
  }

  if (newPassword !== confirmPassword) {
    alert('New password and confirm password do not match');
    return;
  }

  try {
    const res = await fetch(`${API_URL}/update-password/${userID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        currentPassword,
        newPassword
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to update password');
    }

    alert('Password updated successfully!');

    currentPasswordInput.value = '';
    newPasswordInput.value = '';
    confirmPasswordInput.value = '';
  } catch (err) {
    console.error('Failed to update password:', err);
    alert(err.message || 'Failed to update password');
  }
}

// Logout
function logoutUser() {
  localStorage.clear();
  window.location.href = 'auth.html';
}

// Delete account
async function deleteAccount() {
  const confirmDelete = confirm('Are you sure you want to delete your account? This cannot be undone.');

  if (!confirmDelete) return;

  try {
    const res = await fetch(`${API_URL}/delete-account/${userID}`, {
      method: 'DELETE'
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to delete account');
    }

    alert('Account deleted successfully');

    localStorage.clear();
    window.location.href = 'auth.html';
  } catch (err) {
    console.error('Failed to delete account:', err);
    alert(err.message || 'Failed to delete account');
  }
}

// Export data
async function exportData() {
  try {
    const res = await fetch(`${API_URL}/export-data/${userID}`);
    if (!res.ok) throw new Error('Failed to export data');

    const data = await res.json();

    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'trackwise-data.json';
    link.click();

    URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Failed to export data:', err);
    alert('Failed to export data');
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', function () {
  loadProfile();

  const profileSaveBtn = document.getElementById('saveProfileBtn');
  const notificationSaveBtn = document.getElementById('saveNotificationBtn');
  const passwordSaveBtn = document.getElementById('updatePasswordBtn');
  const logoutBtn = document.getElementById('logoutBtn');
  const deleteBtn = document.getElementById('deleteAccountBtn');
  const exportBtn = document.getElementById('exportDataBtn');

  if (profileSaveBtn) {
    profileSaveBtn.addEventListener('click', saveProfile);
  }

  if (notificationSaveBtn) {
    notificationSaveBtn.addEventListener('click', saveNotifications);
  }

  if (passwordSaveBtn) {
    passwordSaveBtn.addEventListener('click', updatePassword);
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', logoutUser);
  }

  if (deleteBtn) {
    deleteBtn.addEventListener('click', deleteAccount);
  }

  if (exportBtn) {
    exportBtn.addEventListener('click', exportData);
  }
});