const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('send-btn');
const aiText = document.getElementById('ai-text');

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
async function sendMessage() {   
    const userMessage = userInput.value.trim();

    if (!userMessage) {
        aiText.textContent = '请输入您的问题。';
        return;
    }

    sendBtn.disabled = true;
    aiText.textContent = '思考中...';

    try{
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) throw new Error('网络错误');

        const data = await response.json();

        if (!data.success) throw new Error(data.reply || '服务暂不可用');

        aiText.textContent = data.reply;

    } catch (error) {
        console.error('Error:', error);
        aiText.textContent = error.message || '出错了，未能获得回复。';
    } finally {
        sendBtn.disabled = false;
    }
}
