const form = document.querySelector("form");
const statusEl = document.querySelector("#account-status");

const preferencesModal = document.getElementById("preferences-modal");
const preferencesForm = document.getElementById("preferences-form");
const closePreferencesButton = document.getElementById("close-preferences");
const cancelPreferencesButton = document.getElementById("cancel-preferences");
const savePreferencesButton = document.getElementById("save-preferences");

const HOME_URL = "/";

// Maps each modal field name to which AccessibilityProfile category it belongs to,
// matching the Pydantic models in app/models/models.py.
const PROFILE_SCHEMA = {
  mobility: {
    bools: [
      "wheelchair_accessible",
      "short_walking_distances",
      "long_walking_distances",
      "remote_controlled_doors",
      "remote_controlled_curtains",
      "remote_controlled_lights",
      "ramp_access",
      "elevator_access",
      "accessible_bathroom",
      "wide_hallways",
    ],
    arrays: [],
  },
  dietary: {
    bools: [
      "non_vegetarian",
      "pescatarian",
      "vegetarian",
      "vegan",
      "gluten_free",
      "halal",
      "kosher",
    ],
    arrays: ["allergy_accommodations"],
  },
  speech: {
    bools: [
      "hearing_impaired_support",
      "speech_impaired_support",
      "sign_language",
      "captions",
    ],
    arrays: ["languages"],
  },
  sensory: {
    bools: [
      "dimly_lit_spaces",
      "quiet_rooms",
      "sensory_rooms",
      "noise_cancelling_support",
      "weighted_blankets",
      "fidget_tools",
      "aromatherapy_free_rooms",
    ],
    arrays: [],
  },
  cognitive: {
    bools: [
      "ibcces_certification",
      "clear_wayfinding",
      "staff_disability_awareness_training",
    ],
    arrays: [],
  },
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

// Build the AccessibilityProfile payload that matches the Pydantic model the
// PUT /api/users/{user_id}/profile endpoint expects.
function buildAccessibilityProfile() {
  const formData = new FormData(preferencesForm);
  const profile = {};

  for (const [category, fields] of Object.entries(PROFILE_SCHEMA)) {
    profile[category] = {};

    fields.bools.forEach((name) => {
      profile[category][name] = formData.has(name);
    });

    fields.arrays.forEach((name) => {
      const raw = (formData.get(name) || "").trim();
      profile[category][name] = raw
        ? raw.split(",").map((s) => s.trim()).filter(Boolean)
        : [];
    });
  }

  return profile;
}

async function savePreferencesToBackend() {
  if (!createdUserId) return;
  const profile = buildAccessibilityProfile();
  const response = await fetch(`/api/users/${createdUserId}/profile`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  if (!response.ok) {
    throw new Error("Could not save preferences.");
  }
}

function markSignedIn(userId) {
  localStorage.setItem("inclusitripSignedIn", "true");
  if (userId) {
    localStorage.setItem("inclusitripUserId", userId);
  }
}

function goHome() {
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
    markSignedIn(createdUserId);
    showStatus(`Account created for ${data.name}! Set your accessibility preferences.`);
    openPreferences();
  } catch (error) {
    showStatus("Something went wrong. Please try again.", true);
  }
});

savePreferencesButton.addEventListener("click", async () => {
  savePreferencesButton.disabled = true;
  const originalLabel = savePreferencesButton.textContent;
  savePreferencesButton.textContent = "Saving...";

  try {
    await savePreferencesToBackend();
    closePreferences();
    goHome();
  } catch (error) {
    savePreferencesButton.disabled = false;
    savePreferencesButton.textContent = originalLabel;
    showStatus("Could not save preferences. Please try again.", true);
  }
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
