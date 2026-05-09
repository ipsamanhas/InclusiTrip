const form = document.querySelector("form");
const statusEl = document.querySelector("#account-status");

function showStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.hidden = false;
  statusEl.className = isError ? "status error" : "status success";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const name = formData.get("name").trim();
  const email = formData.get("email").trim();
  const password = formData.get("password");

  if (password.length < 8) {
    showStatus("Password must be at least 8 characters.", true);
    return;
  }

  showStatus("Creating your account...");

  try {
    const response = await fetch("/api/create-account", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      const message = typeof data.detail === "string"
        ? data.detail
        : "Something went wrong. Please try again.";
      showStatus(message, true);
      return;
    }

    showStatus(`Account created for ${data.name}! Redirecting to login...`);
    setTimeout(() => {
      window.location.href = "/login";
    }, 1500);
  } catch (error) {
    showStatus("Something went wrong. Please try again.", true);
  }
});
