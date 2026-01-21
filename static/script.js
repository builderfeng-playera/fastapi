// 配置 Marked.js
marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false,
    mangle: false
});

const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

let isThinking = false;

// 自动调整输入框高度
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// 发送消息
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isThinking) return;
    
    // 添加用户消息
    addMessage('user', message);
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // 显示思考动画
    const thinkingId = showThinking();
    isThinking = true;
    sendButton.disabled = true;
    
    try {
        // 调用 API
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: [
                    {
                        role: 'user',
                        content: message
                    }
                ],
                model: 'gpt-5',
                temperature: 0.7
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 移除思考动画
        removeThinking(thinkingId);
        
        // 添加 AI 回复
        const aiMessage = data.choices[0].message.content;
        addMessage('assistant', aiMessage);
        
    } catch (error) {
        console.error('Error:', error);
        removeThinking(thinkingId);
        addErrorMessage(error.message || '发送消息时出错，请稍后重试。');
    } finally {
        isThinking = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

// 添加消息到聊天容器
function addMessage(role, content) {
    // 移除欢迎消息
    const welcomeMessage = chatContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (role === 'assistant') {
        // 渲染 markdown
        messageContent.innerHTML = marked.parse(content);
    } else {
        // 用户消息直接显示文本
        messageContent.textContent = content;
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatContainer.appendChild(messageDiv);
    
    // 滚动到底部
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 显示思考动画
function showThinking() {
    // 移除欢迎消息
    const welcomeMessage = chatContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const thinkingId = 'thinking-' + Date.now();
    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = thinkingId;
    thinkingDiv.className = 'message assistant';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const thinkingContent = document.createElement('div');
    thinkingContent.className = 'thinking';
    
    const dots = document.createElement('div');
    dots.className = 'thinking-dots';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'thinking-dot';
        dots.appendChild(dot);
    }
    
    const text = document.createElement('span');
    text.className = 'thinking-text';
    text.textContent = '正在思考...';
    
    thinkingContent.appendChild(dots);
    thinkingContent.appendChild(text);
    
    thinkingDiv.appendChild(avatar);
    thinkingDiv.appendChild(thinkingContent);
    
    chatContainer.appendChild(thinkingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return thinkingId;
}

// 移除思考动画
function removeThinking(thinkingId) {
    const thinkingDiv = document.getElementById(thinkingId);
    if (thinkingDiv) {
        thinkingDiv.remove();
    }
}

// 添加错误消息
function addErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = '❌ ' + message;
    chatContainer.appendChild(errorDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 发送按钮点击事件
sendButton.addEventListener('click', sendMessage);

// 回车发送，Shift+Enter 换行
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 页面加载时聚焦输入框
window.addEventListener('load', function() {
    messageInput.focus();
});

