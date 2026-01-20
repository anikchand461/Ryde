// auth.js

const API_BASE = ""; // relative → works with FastAPI root

// Helper for all API calls
async function apiCall(endpoint, method = "POST", body = null) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json" };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config = { method, headers };
  if (body) config.body = JSON.stringify(body);

  try {
    const res = await fetch(API_BASE + endpoint, config);

    if (!res.ok) {
      let errorData;
      try {
        errorData = await res.json();
      } catch {
        errorData = { detail: "Network or server error" };
      }
      throw new Error(errorData.detail || `HTTP ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}

// Login
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const data = await apiCall("/login", "POST", {
      username: email,
      password,
    });
    localStorage.setItem("token", data.access_token);
    window.location.href = "/dashboard";
  } catch (err) {
    alert("Login failed: " + err.message);
  }
});

// Register
document
  .getElementById("registerForm")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      full_name: document.getElementById("fullName").value.trim(),
      email: document.getElementById("regEmail").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      password: document.getElementById("regPassword").value,
      role: document.getElementById("role").value,
    };

    if (payload.role === "OWNER") {
      payload.owner_profile = {
        vehicle_type: document.getElementById("vehicleType")?.value,
        vehicle_name: document.getElementById("vehicleName")?.value.trim(),
        vehicle_model: document.getElementById("vehicleModel")?.value.trim(),
        vehicle_registration: document
          .getElementById("vehicleRegistration")
          ?.value.trim(),
      };
    }
    // → Add repair_profile / towing_profile later when needed

    try {
      await apiCall("/users/", "POST", payload);
      alert("Account created! Please login.");
      window.location.href = "/";
    } catch (err) {
      alert("Registration failed:\n" + err.message);
    }
  });

// Logout
window.logout = function () {
  localStorage.removeItem("token");
  window.location.href = "/";
};

// Simple dashboard protection (client-side)
if (
  window.location.pathname === "/dashboard" &&
  !localStorage.getItem("token")
) {
  window.location.href = "/";
}
