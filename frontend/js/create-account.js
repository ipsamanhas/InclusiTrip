const form = document.querySelector("form");
const statusEl = document.querySelector("#account-status");

const preferencesModal = document.getElementById("preferences-modal");
const preferencesForm = document.getElementById("preferences-form");
const closePreferencesButton = document.getElementById("close-preferences");
const cancelPreferencesButton = document.getElementById("cancel-preferences");
const savePreferencesButton = document.getElementById("save-preferences");

const HOME_URL = "/";

const categoryLabels = {
  "Mobility": "mobility",
  "Food/Diet": "foodDiet",
  "Language/Speech Accommodations": "languageSpeech",
  "Sensory Needs": "sensory",
  "Cognitive Needs": "cognitive",
};

let createdUserId = null;

function showStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.hidden = false;
  statusEl.className = isError ? "status error" : "status success";
}

function openPreferences() {
  preferencesModal.hidden = false;
  preferencesModal.classList.add("is-open");
  document.body.style.overflow = "hidden";
  closePreferencesButton.focus();
}

function closePreferences() {
  preferencesModal.classList.remove("is-open");
  preferencesModal.hidden = true;
  document.body.style.overflow = "";
}

// Save preferences in the SAME shape welcome.html expects, so when the user
// lands on the home page right after, the data is already there.
function savePreferenceSelections() {
  const savedProfile = {};

  preferencesForm.querySelectorAll(".preference-group").forEach((group) => {
    const categoryName = group.querySelector("legend").textContent.trim();
    const categoryKey = categoryLabels[categoryName];
    const selections = [];

    group.querySelectorAll(".checkbox-label").forEach((label) => {
      const checkbox = label.querySelector("input[type='checkbox']");
      if (checkbox.checked) {
        selections.push(label.textContent.trim());
      }
    });

    group.querySelectorAll(".text-field input").forEach((input) => {
      if (input.value.trim()) {
        const fieldLabel = group.querySelector(`label[for="${input.id}"]`).textContent.trim();
        selections.push(`${fieldLabel}: ${input.value.trim()}`);
      }
    });

    savedProfile[categoryKey] = {
      label: categoryName,
      selections,
    };
  });

  localStorage.setItem("inclusitripPreferences", JSON.stringify(savedProfile));
}

function goHome() {
  // Mark the user as signed in so welcome.html shows "My Profile" / "Log Out".
  localStorage.setItem("inclusitripSignedIn", "true");
  window.location.href = HOME_URL;
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

    createdUserId = data.id;
    showStatus(`Account created for ${data.name}! Set your accessibility preferences.`);
    openPreferences();
  } catch (error) {
    showStatus("Something went wrong. Please try again.", true);
  }
});

savePreferencesButton.addEventListener("click", () => {
  savePreferenceSelections();
  closePreferences();
  goHome();
});

cancelPreferencesButton.addEventListener("click", () => {
  closePreferences();
  goHome();
});

closePreferencesButton.addEventListener("click", () => {
  closePreferences();
  goHome();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !preferencesModal.hidden) {
    closePreferences();
    goHome();
  }
});

preferencesModal.addEventListener("click", (event) => {
  if (event.target === preferencesModal) {
    closePreferences();
    goHome();
  }
});
