/**
 * Agri Link — AI Assistant Component Logic
 * Component: /components/ai-assistant/ai_assistant.js
 * Manages conversation state, rich markdown rendering, weather widget, and API integration.
 */

(function () {
    'use strict';

    // In-memory conversation state
    let conversationHistory = [];
    let isWaitingResponse = false;
    let selectedAttachment = null;

    const INITIAL_GREETING = 
        "Namaste! 👋 I am your **Agri Link AI Farming Assistant**.\n\n" +
        "I am here to provide expert farming advice, crop cultivation guides, pest & disease detection solutions, " +
        "soil health guidance, and official Indian government scheme updates.\n\n" +
        "How can I help you today? You can type your question below or choose a topic:";

    const PROMPT_SUGGESTIONS = [
        { icon: "bi-flower1 text-success", label: "Paddy Fertilizer Schedule", query: "What is the best fertilizer and NPK dosage for paddy crop?" },
        { icon: "bi-bug text-danger", label: "Tomato Early Blight Cure", query: "How do I detect and cure Early Blight disease in tomato plants?" },
        { icon: "bi-card-checklist text-primary", label: "PM-KISAN Scheme Guide", query: "What are the latest eligibility requirements for PM-KISAN 17th installment?" },
        { icon: "bi-droplet-fill text-info", label: "Drip Irrigation Schedule", query: "What is the optimal drip irrigation schedule for sugarcane during summer?" }
    ];

    // Helper: format current time as "10:24 AM"
    function getFormattedTimestamp() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12;
        const minsStr = minutes < 10 ? '0' + minutes : minutes;
        return `${hours}:${minsStr} ${ampm}`;
    }

    // Markdown → HTML parser supporting headings, bold labels, lists, and tables
    function renderMarkdown(raw) {
        if (!raw || typeof raw !== 'string') return '';

        const lines = raw.replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim().split('\n');
        const out = [];
        let inUl = false;
        let inOl = false;

        function closeLists() {
            if (inUl) { out.push('</ul>'); inUl = false; }
            if (inOl) { out.push('</ol>'); inOl = false; }
        }

        function formatInline(str) {
            if (!str) return '';
            let s = str
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/(\*{2}|_{2})(.*?)\1/g, '<strong>$2</strong>')
                .replace(/\*(?!\*)(.+?)\*(?!\*)/g, '<em>$1</em>')
                .replace(/`([^`]+)`/g, '<code class="bg-light px-1 border rounded font-monospace small">$1</code>');
            return s;
        }

        for (let i = 0; i < lines.length; i++) {
            const rawLine = lines[i];
            const trimmed = rawLine.trim();

            if (!trimmed) {
                closeLists();
                continue;
            }

            // Headings: ### Title or ## Title
            if (trimmed.startsWith('### ') || trimmed.startsWith('## ') || trimmed.startsWith('# ')) {
                closeLists();
                const titleText = trimmed.replace(/^#+\s*/, '');
                out.push(`<div class="ai-md-h3">${formatInline(titleText)}</div>`);
                continue;
            }

            // Numbered list item: 1. Item
            const numMatch = trimmed.match(/^(\d+)\.\s+(.+)$/);
            if (numMatch) {
                if (inUl) { out.push('</ul>'); inUl = false; }
                if (!inOl) { out.push('<ol>'); inOl = true; }
                out.push(`<li>${formatInline(numMatch[2])}</li>`);
                continue;
            }

            // Bullet list item: * Item or - Item or • Item
            const bulletMatch = trimmed.match(/^[-*+•]\s+(.+)$/);
            if (bulletMatch) {
                if (inOl) { out.push('</ol>'); inOl = false; }
                if (!inUl) { out.push('<ul>'); inUl = true; }
                out.push(`<li>${formatInline(bulletMatch[1])}</li>`);
                continue;
            }

            // Plain paragraph
            closeLists();
            out.push(`<p>${formatInline(trimmed)}</p>`);
        }

        closeLists();
        return out.join('');
    }

    // Initialize Component
    function initAIAssistant() {
        const messagesArea = document.getElementById('ai-chat-messages');
        const chatForm = document.getElementById('ai-chat-form');
        const chatInput = document.getElementById('ai-chat-input');
        const sendBtn = document.getElementById('ai-chat-send-btn');
        const clearBtn = document.getElementById('ai-clear-chat-btn');
        const attachBtn = document.getElementById('ai-chat-attach-btn');
        const fileInput = document.getElementById('ai-chat-file-input');
        const attachBadge = document.getElementById('ai-attachment-badge');
        const attachFileName = document.getElementById('ai-attached-filename');
        const removeFileBtn = document.getElementById('ai-remove-file-btn');

        if (!messagesArea || !chatInput) {
            return; // Not on AI Assistant view
        }

        // 1. Populate Page Header Data (Weather & User)
        loadPageHeaderData();

        // 2. Initial Greeting Message
        resetChat(messagesArea);

        // 3. Clear Chat Handler
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                if (confirm('Are you sure you want to clear this conversation?')) {
                    resetChat(messagesArea);
                }
            });
        }

        // 4. File Attachment Handler
        if (attachBtn && fileInput) {
            attachBtn.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', (e) => {
                if (e.target.files && e.target.files[0]) {
                    selectedAttachment = e.target.files[0];
                    if (attachFileName) attachFileName.textContent = selectedAttachment.name;
                    if (attachBadge) attachBadge.classList.remove('d-none');
                }
            });
        }

        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', () => {
                selectedAttachment = null;
                if (fileInput) fileInput.value = '';
                if (attachBadge) attachBadge.classList.add('d-none');
            });
        }

        // 5. Textarea Auto-expand & Enter Key Submission
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });

        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                submitMessage();
            }
        });

        // 6. Form Submission
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                submitMessage();
            });
        }

        // Submit message routine
        async function submitMessage() {
            if (isWaitingResponse) return;

            const message = chatInput.value.trim();
            if (!message && !selectedAttachment) return;

            const displayMsg = message || (selectedAttachment ? `[Attached file: ${selectedAttachment.name}]` : '');
            const timestamp = getFormattedTimestamp();

            // Append User Message to UI
            appendUserBubble(messagesArea, displayMsg, timestamp, selectedAttachment ? selectedAttachment.name : null);
            conversationHistory.push({ role: 'user', text: displayMsg, timestamp: timestamp });

            // Reset inputs
            chatInput.value = '';
            chatInput.style.height = 'auto';
            const attachedFile = selectedAttachment;
            selectedAttachment = null;
            if (fileInput) fileInput.value = '';
            if (attachBadge) attachBadge.classList.add('d-none');

            // Show typing indicator
            isWaitingResponse = true;
            if (sendBtn) sendBtn.disabled = true;
            const typingId = showTypingIndicator(messagesArea);

            try {
                let fullPrompt = message;
                if (attachedFile) {
                    fullPrompt += ` (Note: Farmer attached file '${attachedFile.name}')`;
                }

                const token = localStorage.getItem('token');
                const headers = { 'Content-Type': 'application/json' };
                if (token) headers['Authorization'] = `Token ${token}`;

                // Primary call: dedicated /api/ai-assistant/chat
                let reply = null;
                const activeLang = (window.currentLanguage || (localStorage.getItem('userLanguage') === 'Tamil' ? 'ta' : 'en'));
                try {
                    const response = await fetch('/api/ai-assistant/chat/', {
                        method: 'POST',
                        headers: headers,
                        body: JSON.stringify({
                            message: fullPrompt,
                            language: activeLang,
                            conversationHistory: conversationHistory
                        })
                    });
                    if (response.ok) {
                        const data = await response.json();
                        reply = data.reply || (data.data && data.data.reply);
                    }
                } catch (firstErr) {
                    console.warn('Dedicated endpoint error, trying fallback:', firstErr);
                }

                // Fallback call: /api/v1/ai/chatbot/
                if (!reply) {
                    const fallbackResp = await fetch('/api/v1/ai/chatbot/', {
                        method: 'POST',
                        headers: headers,
                        body: JSON.stringify({
                            message: fullPrompt,
                            language: activeLang,
                            history: conversationHistory.map(t => ({
                                role: t.role === 'assistant' ? 'bot' : 'user',
                                message: t.text
                            }))
                        })
                    });
                    if (fallbackResp.ok) {
                        const fbData = await fallbackResp.json();
                        reply = (fbData.data && fbData.data.reply) || fbData.reply;
                    }
                }

                removeTypingIndicator(typingId);

                if (!reply) {
                    reply = "I'm sorry, I could not process your query at this moment. Please check your internet connection or try asking again.";
                }

                const botTimestamp = getFormattedTimestamp();
                appendBotBubble(messagesArea, reply, botTimestamp);
                conversationHistory.push({ role: 'assistant', text: reply, timestamp: botTimestamp });

            } catch (err) {
                removeTypingIndicator(typingId);
                const botTimestamp = getFormattedTimestamp();
                const errMsg = "Connection to Agri Link AI service interrupted. Please try again.";
                appendBotBubble(messagesArea, errMsg, botTimestamp);
                conversationHistory.push({ role: 'assistant', text: errMsg, timestamp: botTimestamp });
            } finally {
                isWaitingResponse = false;
                if (sendBtn) sendBtn.disabled = false;
                scrollMessages(messagesArea);
            }
        }
    }

    // Append User Message Bubble
    function appendUserBubble(container, text, timestamp, attachedFileName) {
        const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
        const attachHtml = attachedFileName
            ? `<div class="small text-muted mt-1 d-flex align-items-center gap-1"><i class="bi bi-paperclip"></i> Attached: <em>${attachedFileName}</em></div>`
            : '';

        const html = `
            <div class="ai-msg-row-user">
                <div class="d-flex flex-column align-items-end" style="max-width: 82%;">
                    <div class="ai-bubble-user">
                        ${escaped}
                        ${attachHtml}
                    </div>
                    <div class="ai-msg-time text-end">${timestamp}</div>
                </div>
                <div class="ai-msg-avatar-user" title="You">
                    <i class="bi bi-person-fill"></i>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
        scrollMessages(container);
    }

    // Append AI Bot Message Bubble
    function appendBotBubble(container, rawMarkdown, timestamp) {
        const rendered = renderMarkdown(rawMarkdown);
        const html = `
            <div class="ai-msg-row-bot">
                <div class="ai-msg-avatar-bot" title="Agri Link AI">
                    <i class="bi bi-robot"></i>
                </div>
                <div class="d-flex flex-column align-items-start" style="max-width: 88%;">
                    <div class="ai-bubble-bot">
                        ${rendered}
                    </div>
                    <div class="ai-msg-time text-start">${timestamp}</div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
        scrollMessages(container);
    }

    // Show Typing Indicator
    function showTypingIndicator(container) {
        const id = 'typing-' + Date.now();
        const html = `
            <div class="ai-msg-row-bot" id="${id}">
                <div class="ai-msg-avatar-bot">
                    <i class="bi bi-robot"></i>
                </div>
                <div class="ai-typing-indicator-wrap">
                    <div class="spinner-grow spinner-grow-sm text-success" role="status" style="width: 10px; height: 10px;"></div>
                    <span>Agri Link AI is consulting agronomy database…</span>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
        scrollMessages(container);
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    // Reset Chat to Initial Greeting
    function resetChat(container) {
        conversationHistory = [];
        selectedAttachment = null;
        const initialTime = "Just now";

        container.innerHTML = `
            <div class="ai-msg-row-bot" id="ai-initial-greeting">
                <div class="ai-msg-avatar-bot">
                    <i class="bi bi-robot"></i>
                </div>
                <div class="d-flex flex-column align-items-start" style="max-width: 82%;">
                    <div class="ai-bubble-bot">
                        ${renderMarkdown(INITIAL_GREETING)}
                        <div class="ai-prompt-chips-wrapper mt-3" id="ai-quick-chips">
                            ${PROMPT_SUGGESTIONS.map(s => `
                                <button type="button" class="ai-prompt-chip" data-query="${s.query}">
                                    <i class="bi ${s.icon} me-1"></i> ${s.label}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                    <div class="ai-msg-time text-start">${initialTime}</div>
                </div>
            </div>
        `;

        // Bind Quick Chips
        const chips = container.querySelectorAll('.ai-prompt-chip');
        const chatInput = document.getElementById('ai-chat-input');
        const chatForm = document.getElementById('ai-chat-form');

        chips.forEach(chip => {
            chip.addEventListener('click', (e) => {
                e.preventDefault();
                const query = chip.getAttribute('data-query');
                if (query && chatInput && chatForm) {
                    chatInput.value = query;
                    chatForm.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
                }
            });
        });

        scrollMessages(container);
    }

    function scrollMessages(container) {
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 50);
    }

    // Load Header Data (Weather and User Profile)
    async function loadPageHeaderData() {
        // User Profile
        const userNameEl = document.getElementById('ai-user-name');
        const userRoleEl = document.getElementById('ai-user-role');
        const userAvatarEl = document.getElementById('ai-user-avatar');

        const savedName = localStorage.getItem('userName') || 'Ravi Kumar';
        const savedRole = localStorage.getItem('userRole') || 'Farmer';

        if (userNameEl) userNameEl.textContent = savedName;
        if (userRoleEl) userRoleEl.textContent = savedRole;
        if (userAvatarEl) {
            const savedAvatar = localStorage.getItem('userAvatar');
            if (savedAvatar) userAvatarEl.src = savedAvatar;
        }

        // Weather Data
        const weatherTempEl = document.getElementById('ai-weather-temp');
        const weatherLocEl = document.getElementById('ai-weather-loc');
        const weatherIconEl = document.getElementById('ai-weather-icon');

        try {
            const resp = await fetch('/api/v1/weather/current/?city=Coimbatore');
            if (resp.ok) {
                const data = await resp.json();
                if (data.success && data.data) {
                    const w = data.data;
                    if (weatherTempEl) {
                        weatherTempEl.textContent = `${w.temperature || 28}°C · ${w.condition || 'Sunny'}`;
                    }
                    if (weatherLocEl) {
                        weatherLocEl.textContent = w.location || 'Coimbatore, Tamil Nadu';
                    }
                    if (weatherIconEl) {
                        const isRain = /rain|drizzle/i.test(w.condition || '');
                        const isCloud = /cloud/i.test(w.condition || '');
                        if (isRain) {
                            weatherIconEl.innerHTML = '<i class="bi bi-cloud-rain-fill text-primary"></i>';
                        } else if (isCloud) {
                            weatherIconEl.innerHTML = '<i class="bi bi-cloud-sun-fill text-warning"></i>';
                        } else {
                            weatherIconEl.innerHTML = '<i class="bi bi-sun-fill text-warning"></i>';
                        }
                    }
                    return;
                }
            }
        } catch (e) {
            console.debug('Using fallback weather in AI Assistant header:', e);
        }

        // Fallback default
        if (weatherTempEl) weatherTempEl.textContent = '28°C · Clear Sky';
        if (weatherLocEl) weatherLocEl.textContent = 'Coimbatore, Tamil Nadu';
        if (weatherIconEl) weatherIconEl.innerHTML = '<i class="bi bi-sun-fill text-warning"></i>';
    }

    // Expose global initializer
    window.initAIAssistantModule = initAIAssistant;

    // Auto-init on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAIAssistant);
    } else {
        initAIAssistant();
    }
})();
