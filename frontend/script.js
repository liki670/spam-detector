const user = localStorage.getItem("user");
document.getElementById("user").innerText = user;

// Navigation
function showCompose() {
    toggle("composeSection");
}

function showInbox() {
    toggle("inboxSection");
    loadEmails();
}

function showSpam() {
    toggle("spamSection");
    loadEmails();
}

function showHistory() {
    toggle("historySection");
    loadHistory();
}

// Toggle sections
function toggle(sectionId) {
    document.getElementById("composeSection").classList.add("hidden");
    document.getElementById("inboxSection").classList.add("hidden");
    document.getElementById("spamSection").classList.add("hidden");
    document.getElementById("historySection").classList.add("hidden");

    document.getElementById(sectionId).classList.remove("hidden");
}

// Send email to backend
async function sendEmail() {
    let text = document.getElementById("text").value;

    let res = await fetch("https://spam-backend-x32p.onrender.com", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    let data = await res.json();

    let emails = JSON.parse(localStorage.getItem("emails")) || [];
    emails.push({ text: text, result: data.result });

    localStorage.setItem("emails", JSON.stringify(emails));

    alert("Result: " + data.result);
}

// Load inbox + spam
function loadEmails() {
    let emails = JSON.parse(localStorage.getItem("emails")) || [];

    let inbox = document.getElementById("inboxList");
    let spam = document.getElementById("spamList");

    inbox.innerHTML = "";
    spam.innerHTML = "";

    emails.forEach(e => {
        let div = document.createElement("div");
        div.className = "email-card";

        div.innerText = e.text + " (" + e.result + ")";

        if (e.result === "Spam") {
            div.classList.add("spam");
            spam.appendChild(div);
        } else {
            div.classList.add("not-spam");
            inbox.appendChild(div);
        }
    });
}

// Load history
function loadHistory() {
    let emails = JSON.parse(localStorage.getItem("emails")) || [];
    let history = document.getElementById("historyList");

    history.innerHTML = "";

    emails.forEach(e => {
        let div = document.createElement("div");
        div.className = "email-card";

        if (e.result === "Spam") {
            div.classList.add("spam");
        } else {
            div.classList.add("not-spam");
        }

        div.innerText = e.text + " (" + e.result + ")";
        history.appendChild(div);
    });
}