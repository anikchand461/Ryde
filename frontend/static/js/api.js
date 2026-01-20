// frontend/js/api.js
const API_BASE = "http://localhost:8000";

async function apiCall(endpoint, method = "GET", body = null) {
  const token = localStorage.getItem("token");
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
  const config = { method, headers };
  if (body) config.body = JSON.stringify(body);
  const response = await fetch(`${API_BASE}${endpoint}`, config);
  return await response.json();
}
