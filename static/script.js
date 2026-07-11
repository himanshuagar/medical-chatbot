const input = document.getElementById("messageInput");
const button = document.getElementById("sendBtn");
const chatBody = document.getElementById("chatBody");

button.addEventListener("click", sendMessage);

input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {

    const message = input.value.trim();

    if (message === "") return;

    // User message
    chatBody.innerHTML += `
        <div class="message user">
            ${message}
        </div>
    `;

    input.value = "";

    chatBody.scrollTop = chatBody.scrollHeight;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Bot message
        chatBody.innerHTML += `
            <div class="message bot">
                ${data.answer}
            </div>
        `;

        chatBody.scrollTop = chatBody.scrollHeight;

    } catch (error) {

        console.error(error);

        chatBody.innerHTML += `
            <div class="message bot">
                Something went wrong.
            </div>
        `;
    }
}