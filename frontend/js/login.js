const loginForm = document.querySelector("#login-form");
const loginStatus = document.querySelector("#login-status");

function showStatus(message, isError = false) {
  loginStatus.textContent = message;
  loginStatus.hidden = false;
  loginStatus.classList.toggle("error", isError);
}

function showLoginHelp(message) {
  loginStatus.textContent = message;
  loginStatus.hidden = false;
  loginStatus.classList.add("error");
  loginStatus.append(" ");

  const createAccountLink = document.createElement("a");
  createAccountLink.href = "/create-account";
  createAccountLink.textContent = "Create an account";

  const guestLink = document.createElement("a");
  guestLink.href = "/";
  guestLink.textContent = "Use as a guest";

  loginStatus.append(createAccountLink, " or ", guestLink, ".");
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(loginForm);
  const email = formData.get("email");
  const password = formData.get("password");

  showStatus("Checking your login...");

  try {
    const loginResponse = await fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const loginData = await loginResponse.json();

    if (!loginResponse.ok) {
      showLoginHelp(loginData.detail);
      return;
    }

    const profileResponse = await fetch(loginData.profile_url);
    const profile = await profileResponse.json();

    if (!profileResponse.ok) {
      showStatus(profile.detail, true);
      return;
    }

    showStatus(`Welcome back, ${profile.name}. Your profile loaded successfully.`);
  } catch (error) {
    showStatus("Something went wrong while logging in. Please try again.", true);
  }
});
