const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("send-btn");
const aiText = document.getElementById("ai-text");
const heroTypingEl = document.getElementById("hero-title");

//标题打字机效果
const typingPhrase = 'I am Yang, a software developer';
const typingSpeed = 90;
let charIndex = 0;

function animateHeroTyping() {
  if (!heroTypingEl) return;

  heroTypingEl.textContent = typingPhrase.slice(0, charIndex);

  if (charIndex < typingPhrase.length) {
    charIndex += 1;
    setTimeout(animateHeroTyping, typingSpeed);
  }
}

animateHeroTyping();

// AI问答输入框
function handleKeyPress(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
}

async function sendMessage() {
  const userMessage = userInput.value.trim();

  if (!userMessage) {
    aiText.textContent = "请输入您的问题。";
    return;
  }

  sendBtn.disabled = true;
  aiText.textContent = "思考中...";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) throw new Error("网络错误");

    const data = await response.json();

    if (!data.success) throw new Error(data.reply || "服务暂不可用");

    aiText.textContent = data.reply;
  } catch (error) {
    console.error("Error:", error);
    aiText.textContent = error.message || "出错了，未能获得回复。";
  } finally {
    sendBtn.disabled = false;
  }
}
