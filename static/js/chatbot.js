document.addEventListener('DOMContentLoaded', () => {
    const chatBubble = document.getElementById('ai-chat-bubble');
    const chatWindow = document.getElementById('ai-chat-window');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');
    const visionSidebar = document.getElementById('vision-sidebar');

    if (!chatBubble) return;

    // Toggle Chat Window
    chatBubble.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
        chatWindow.classList.toggle('animate-in');
        if (!chatWindow.classList.contains('hidden')) {
            chatInput.focus();
        }
    });

    // Send Message
    const sendMessage = async () => {
        const text = chatInput.value.trim();
        if (!text) return;

        // Add user message
        addMessage(text, 'user');
        chatInput.value = '';

        // Typing indicator
        const typingId = addMessage('...', 'ai', true);

        try {
            const response = await fetch('/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            
            // Remove typing indicator and add response
            document.getElementById(typingId).remove();
            addMessage(data.response, 'ai');
        } catch (error) {
            document.getElementById(typingId).remove();
            addMessage("Sorry, I'm having trouble connecting right now.", 'ai');
        }
    };

    const addMessage = (text, sender, isTyping = false) => {
        const id = 'msg-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-4 bubble-animate`;
        msgDiv.innerHTML = `
            <div class="${sender === 'user' ? 'bg-indigo-600 text-white rounded-l-2xl rounded-tr-2xl' : 'bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-white rounded-r-2xl rounded-tl-2xl'} px-4 py-2 max-w-[80%] text-sm shadow-sm glass-effect">
                ${text}
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    };

    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Vision Sidebar Logic (Elite Feature)
    if (visionSidebar) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            if (scrolled > 300) {
                visionSidebar.classList.add('active');
            } else {
                visionSidebar.classList.remove('active');
            }
        });
    }
});
