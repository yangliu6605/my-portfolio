//Gemini API调用
function sendMessage() {
    // 这里是发送消息到AI的逻辑
    console.log("sendMessage function called");
    const userInput = document.getElementById('userInput').value;
    const aiText = document.getElementById('ai-text');
    
    if (userInput) {
        aiText.textContent = `你输入了: ${userInput}`;
    } else {
        aiText.textContent = '请输入内容后再发送。';
    }
}