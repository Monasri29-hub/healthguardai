// ---------------- SIGNUP ----------------
async function signup() {
    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        phone: document.getElementById("phone").value
    };

    const res = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.msg);

    window.location = "login.html";
}

// ---------------- LOGIN ----------------
async function login() {
    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (result.status === "ok") {
        localStorage.setItem("email", data.email);
        window.location = "dashboard.html";
    } else {
        alert("Invalid login!");
    }
}

// ---------------- PREDICTION ----------------
async function predict() {
    const type = document.getElementById("type").value;

    let data = { type };

    document.querySelectorAll("input").forEach(input => {
        if (input.id !== "type") {
            data[input.id] = input.value;
        }
    });

    const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    document.getElementById("result").innerHTML = `
        Disease: ${result.disease}<br>
        Result: ${result.result}<br>
        Risk: ${result.risk}%<br>
        ${result.emergency ? "🚨 Emergency Alert!" : ""}
    `;
}

// ---------------- CHATBOT ----------------
async function sendMessage() {
    const msg = document.getElementById("msg").value;

    const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ msg })
    });

    const data = await res.json();

    const chatBox = document.getElementById("chat");

    chatBox.innerHTML += `<p><b>You:</b> ${msg}</p>`;
    chatBox.innerHTML += `<p><b>AI:</b> ${data.reply}</p>`;
}