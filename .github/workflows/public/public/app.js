async function sendMsg() {
    const input = document.getElementById('user-input');
    const box = document.getElementById('chat-box');
    const text = input.value.trim();
    if (!text) return;
    
    box.innerHTML += `<div class="msg user">${text}</div>`;
    input.value = '';
    box.scrollTop = box.scrollHeight;
    
    const botMsg = document.createElement('div');
    botMsg.className = 'msg bot';
    botMsg.innerText = 'Soch raha hoon...';
    box.appendChild(botMsg);
    box.scrollTop = box.scrollHeight;
    
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        botMsg.innerText = data.reply;
    } catch (err) {
        botMsg.innerText = 'Error: Jawab laane mein pareshani hui.';
    }
    box.scrollTop = box.scrollHeight;
}

