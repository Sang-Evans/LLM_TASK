const API_URL = "http://127.0.0.1:8000/api"; 

export async function checkHealth() {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) throw new Error("Backend not healthy");
  return res.json();
}

export async function askGemini(question) {
  const res = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error("Failed to fetch response");
  return res.json();
}
