const signupForm = document.querySelector(".signup");
const loginForm = document.querySelector(".login");

console.log("auth.js is loaded");

function showLogin() {
  signupForm.classList.remove("active");
  loginForm.classList.add("active");
}

function showSignup() {
  loginForm.classList.remove("active");
  signupForm.classList.add("active");
}

function goHome() {
  window.location.href = "homepage.html";
}

// Email validation function
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// SIGNUP
document.querySelector(".signup button").onclick = async (e) => {
  e.preventDefault();

  const data = {
    name: document.getElementById("signupName").value.trim(),
    email: document.getElementById("signupEmail").value.trim(),
    password: document.getElementById("signupPassword").value.trim()
  };

  if (!data.name || !data.email || !data.password) {
    alert("Please fill all fields");
    return;
  }

  //  Email format check
  if (!isValidEmail(data.email)) {
    alert("Please enter a valid email address");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    
    if (res.status === 201) {
      // Auto-login after signup
      const loginRes = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: data.email,
          password: data.password
        })
      });
      
      const loginResult = await loginRes.json();
      
      if (loginRes.status === 200) {
        localStorage.setItem("userID", loginResult.userID);
        localStorage.setItem("name", loginResult.name);
        window.location.href = "dashboard.html";
      } else {
        alert("Account created! Please log in.");
        showLogin();
      }
    } else {
      alert(result.error || "Signup failed");
    }

  } catch (err) {
    alert("Signup failed: " + err.message);
    console.error(err);
  }
};

// LOGIN
document.querySelector(".login button").onclick = async (e) => {
  e.preventDefault();

  const data = {
    email: document.getElementById("loginEmail").value.trim(),
    password: document.getElementById("loginPassword").value.trim()
  };

  if (!data.email || !data.password) {
    alert("Please fill all fields");
    return;
  }

  //  Email format check for login too
  if (!isValidEmail(data.email)) {
    alert("Please enter a valid email address");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.status === 200) {
      localStorage.setItem("userID", result.userID);
      localStorage.setItem("name", result.name);
      window.location.href = "dashboard.html";
    } else {
      alert(result.error);
    }

  } catch (err) {
    alert("Login failed");
    console.error(err);
  }
};