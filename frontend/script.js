// ================================
// ELEMENT REFERENCES (MUST MATCH HTML IDS)
// ================================
const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const themeToggle = document.getElementById("themeToggle");
const body = document.body;

// ================================
// THEME TOGGLE (DARK / LIGHT)
// ================================
themeToggle.addEventListener("click", () => {
    body.classList.toggle("dark");

    if (body.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        themeToggle.textContent = "☀️";
    } else {
        localStorage.setItem("theme", "light");
        themeToggle.textContent = "🌙";
    }
});

// Load saved theme on refresh
window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        body.classList.add("dark");
        themeToggle.textContent = "☀️";
    } else {
        themeToggle.textContent = "🌙";
    }
});

// ================================
// TYPING EFFECT (AI ONLY)
// ================================
function typeText(element, text, speed = 25) {
    let index = 0;
    element.innerHTML = "";

    function type() {
        if (index < text.length) {
            element.innerHTML += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    }
    type();
}

// ================================
// ADD MESSAGE TO CHAT
// ================================
function addMessage(text, sender = "ai") {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;

    if (sender === "ai") {
        typeText(msg, text);
    } else {
        msg.innerHTML = text;
    }

    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ================================
// SANSKRIT DETECTION
// ================================
function isSanskritLine(text) {
    return /[\u0900-\u097F]/.test(text);
}

// ================================
// SMART FORMATTER (STEP 6B.6 + 6B.7)
// ================================
function formatAIResponse(text) {
    const container = document.createElement("div");
    container.className = "message ai ai-message";

    const lines = text.split("\n").map(l => l.trim()).filter(Boolean);

    let currentSection = null;
    let buffer = [];

    function flushSection() {
        if (!currentSection || buffer.length === 0) return;

        const section = document.createElement("div");
        section.className = "ai-section";

        const title = document.createElement("div");
        title.className = "ai-section-title";
        title.textContent = currentSection;

        section.appendChild(title);

        if (
            currentSection.toLowerCase().includes("verse") ||
            currentSection.toLowerCase().includes("shloka")
        ) {
            buffer.forEach(v => {
                const verse = document.createElement("div");
                verse.className = "verse-card";

                if (isSanskritLine(v)) {
                    verse.classList.add("sanskrit");
                }

                verse.textContent = v;
                section.appendChild(verse);
            });
        } else {
            buffer.forEach(p => {
                const para = document.createElement("p");
                para.textContent = p;
                section.appendChild(para);
            });
        }

        container.appendChild(section);
        buffer = [];
    }

    lines.forEach(line => {
        const lower = line.toLowerCase();

        if (
            lower.startsWith("summary") ||
            lower.startsWith("explanation") ||
            lower.startsWith("verse") ||
            lower.startsWith("verses") ||
            lower.startsWith("shloka") ||
            lower.startsWith("sources")
        ) {
            flushSection();
            currentSection = line.replace(":", "");
        } else {
            buffer.push(line);
        }
    });

    flushSection();
    return container;
}

// ================================
// CONVERT STRUCTURED DATA TO TEXT
// ================================
function dharmicDataToText(data) {
    let text = "";

    if (data.summary) {
        text += `Summary:\n${data.summary}\n\n`;
    }

    if (data.explanation && data.explanation.length) {
        text += "Explanation:\n";
        data.explanation.forEach(p => {
            text += `- ${p}\n`;
        });
        text += "\n";
    }

    if (data.verses && data.verses.length) {
        text += "Verses:\n";
        data.verses.forEach(v => {
            if (v.sanskrit) {
                text += `${v.sanskrit}\n`;
            }
            if (v.meaning) {
                text += `Meaning: ${v.meaning}\n`;
            }
            if (v.ref) {
                text += `— ${v.ref}\n`;
            }
            text += "\n";
        });
    }

    if (data.sources && data.sources.length) {
        text += `Sources:\n${data.sources.join(", ")}\n\n`;
    }

    if (data.disclaimer) {
        text += data.disclaimer;
    }

    return text;
}


// ================================
// SEND MESSAGE TO BACKEND
// ================================
async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    addMessage(question, "user");
    userInput.value = "";

    const thinkingMsg = document.createElement("div");
    thinkingMsg.className = "message ai";
    thinkingMsg.innerHTML = "⏳ Thinking...";
    chatContainer.appendChild(thinkingMsg);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        const response = await fetch("http://127.0.0.1:5000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        chatContainer.removeChild(thinkingMsg);

        if (data.type === "greeting" || data.type === "unclear") {
            addMessage(data.message, "ai");
        }
        else if (data.type === "dharmic_answer") {
            const text = dharmicDataToText(data);
            const formatted = formatAIResponse(text);
            chatContainer.appendChild(formatted);
        }
        else {
            addMessage("⚠️ I could not understand the question.", "ai");
        }

        chatContainer.scrollTop = chatContainer.scrollHeight;

    } catch (error) {
        chatContainer.removeChild(thinkingMsg);
        addMessage("❌ Unable to connect to server.", "ai");
    }
}

// ================================
// EVENTS
// ================================
sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});
