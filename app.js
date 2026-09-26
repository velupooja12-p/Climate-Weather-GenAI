const state = { age: "3-5", weather: "sunny", style: "cartoon" };

const $ = (sel) => document.querySelector(sel);
const result = $("#result");
const img = $("#resultImg");
const loader = $("#loader");
const errorBox = $("#error");
const synth = window.speechSynthesis;

function bindGroup(containerSel, itemSel, key, dataAttr) {
  $(containerSel).addEventListener("click", (e) => {
    const btn = e.target.closest(itemSel);
    if (!btn) return;
    document.querySelectorAll(`${containerSel} ${itemSel}`).forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-checked", "false");
    });
    btn.classList.add("active");
    btn.setAttribute("aria-checked", "true");
    state[key] = btn.dataset[dataAttr];
  });
}

bindGroup("#ageChips", ".chip", "age", "age");
bindGroup("#weatherGrid", ".weather-btn", "weather", "weather");
bindGroup("#styleChips", ".chip", "style", "style");

function stopAudio() {
  if (synth) synth.cancel();
}

function speak(text) {
  if (!synth) return;
  stopAudio();
  const u = new SpeechSynthesisUtterance(text);
  // Younger kids get slower, higher-pitched speech
  u.rate = state.age === "3-5" ? 0.8 : state.age === "6-8" ? 0.9 : 1;
  u.pitch = state.age === "3-5" ? 1.3 : 1.1;
  u.lang = "en-US";
  synth.speak(u);
}

async function generate() {
  stopAudio();
  errorBox.hidden = true;
  result.hidden = false;
  img.hidden = true;
  loader.hidden = false;
  $("#resultTitle").textContent = "";
  $("#resultText").textContent = "";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");

    $("#resultTitle").textContent = data.title;
    $("#resultText").textContent = data.text;
    img.alt = `${state.weather} weather in ${state.style} style`;
    img.onload = () => { loader.hidden = true; img.hidden = false; };
    img.onerror = () => {
      loader.hidden = true;
      errorBox.textContent = "The picture could not load. Tap the button to try again.";
      errorBox.hidden = false;
    };
    img.src = data.image_url;
    speak(data.text);
  } catch (err) {
    loader.hidden = true;
    errorBox.textContent = err.message;
    errorBox.hidden = false;
  }
  result.scrollIntoView({ behavior: "smooth", block: "start" });
}

$("#generateBtn").addEventListener("click", generate);
$("#playBtn").addEventListener("click", () => speak($("#resultText").textContent));
$("#stopBtn").addEventListener("click", stopAudio);
