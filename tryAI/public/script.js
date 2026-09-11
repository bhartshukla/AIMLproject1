// tryAI frontend — Bharat
(() => {
  const $ = (id) => document.getElementById(id);

  const sidebar = $("sidebar");
  const sidebarToggle = $("sidebarToggle");
  const themeToggle = $("themeToggle");
  const newChatBtn = $("newChatBtn");
  const historyList = $("historyList");
  const chatScroll = $("chatScroll");
  const emptyState = $("emptyState");
  const messagesEl = $("messages");
  const promptInput = $("promptInput");
  const sendBtn = $("sendBtn");
  const suggestions = $("suggestions");

  const STORAGE_KEY = "tryai_conversations";
  const THEME_KEY = "tryai_theme";

  let conversations = loadConversations();
  let activeId = conversations.length ? conversations[0].id : null;
  let isStreaming = false;

  // ---------- Theme ----------
  const savedTheme = localStorage.getItem(THEME_KEY) || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem(THEME_KEY, next);
  });

  // ---------- Sidebar ----------
  sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("collapsed"));

  function loadConversations() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function saveConversations() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  }

  function createConversation() {
    const convo = { id: crypto.randomUUID(), title: "New chat", messages: [] };
    conversations.unshift(convo);
    activeId = convo.id;
    saveConversations();
    renderHistory();
    renderMessages();
  }

  function getActive() {
    return conversations.find((c) => c.id === activeId) || null;
  }

  function deleteConversation(id, evt) {
    evt.stopPropagation();
    conversations = conversations.filter((c) => c.id !== id);
    if (activeId === id) {
      activeId = conversations.length ? conversations[0].id : null;
    }
    saveConversations();
    renderHistory();
    renderMessages();
  }

  function renderHistory() {
    historyList.innerHTML = "";
    conversations.forEach((c) => {
      const item = document.createElement("div");
      item.className = "history-item" + (c.id === activeId ? " active" : "");
      item.innerHTML = `
        <span class="title">${escapeHtml(c.title || "New chat")}</span>
        <button class="delete-btn" aria-label="Delete chat" title="Delete">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0-1 14a2 2 0 01-2 2H7a2 2 0 01-2-2L4 6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>`;
      item.addEventListener("click", () => {
        activeId = c.id;
        renderHistory();
        renderMessages();
      });
      item.querySelector(".delete-btn").addEventListener("click", (e) => deleteConversation(c.id, e));
      historyList.appendChild(item);
    });
  }

  newChatBtn.addEventListener("click", createConversation);

  // ---------- Rendering ----------
  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // Very small markdown-ish renderer: fenced code blocks + inline code + paragraphs
  function renderContent(raw) {
    const escaped = escapeHtml(raw);
    const withCodeBlocks = escaped.replace(/```(\w*)\n([\s\S]*?)```/g, (_m, lang, code) => {
      return `<pre><code data-lang="${lang}">${code}</code></pre>`;
    });
    const withInlineCode = withCodeBlocks.replace(/`([^`\n]+)`/g, "<code>$1</code>");
    const paragraphs = withInlineCode
      .split(/\n{2,}/)
      .map((block) => {
        if (block.startsWith("<pre>")) return block;
        return `<p>${block.replace(/\n/g, "<br>")}</p>`;
      })
      .join("");
    return paragraphs;
  }

  function renderMessages() {
    const convo = getActive();
    messagesEl.innerHTML = "";

    if (!convo || convo.messages.length === 0) {
      emptyState.style.display = "flex";
      return;
    }
    emptyState.style.display = "none";

    convo.messages.forEach((m) => {
      messagesEl.appendChild(buildMessageEl(m.role, m.content));
    });
    scrollToBottom();
  }

  function buildMessageEl(role, content) {
    const wrap = document.createElement("div");
    wrap.className = `msg ${role}`;
    const avatar = document.createElement("div");
    avatar.className = "msg-avatar";
    avatar.textContent = role === "user" ? "You" : "AI";
    const body = document.createElement("div");
    body.className = "msg-body";
    const contentEl = document.createElement("div");
    contentEl.className = "msg-content";
    contentEl.innerHTML = renderContent(content);
    body.appendChild(contentEl);
    wrap.appendChild(avatar);
    wrap.appendChild(body);
    return wrap;
  }

  function scrollToBottom() {
    chatScroll.scrollTop = chatScroll.scrollHeight;
  }

  // ---------- Composer ----------
  promptInput.addEventListener("input", () => {
    promptInput.style.height = "auto";
    promptInput.style.height = Math.min(promptInput.scrollHeight, 200) + "px";
    sendBtn.disabled = !promptInput.value.trim() || isStreaming;
  });

  promptInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  sendBtn.addEventListener("click", handleSend);

  suggestions.addEventListener("click", (e) => {
    const chip = e.target.closest(".suggestion-chip");
    if (!chip) return;
    promptInput.value = chip.dataset.prompt;
    promptInput.dispatchEvent(new Event("input"));
    handleSend();
  });

  async function handleSend() {
    const text = promptInput.value.trim();
    if (!text || isStreaming) return;

    if (!getActive()) createConversation();
    const convo = getActive();

    if (convo.messages.length === 0) {
      convo.title = text.slice(0, 40) + (text.length > 40 ? "…" : "");
    }
    convo.messages.push({ role: "user", content: text });
    saveConversations();
    renderHistory();
    renderMessages();

    promptInput.value = "";
    promptInput.style.height = "auto";
    sendBtn.disabled = true;
    isStreaming = true;

    // typing indicator
    const assistantMsgEl = buildMessageEl("assistant", "");
    assistantMsgEl.querySelector(".msg-content").innerHTML =
      '<div class="typing-dots"><span></span><span></span><span></span></div>';
    messagesEl.appendChild(assistantMsgEl);
    scrollToBottom();

    let fullText = "";
    let firstToken = true;

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: convo.messages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });

      if (!res.ok || !res.body) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const chunks = buffer.split("\n\n");
        buffer = chunks.pop();

        for (const chunk of chunks) {
          const line = chunk.trim();
          if (!line.startsWith("data:")) continue;
          const jsonStr = line.slice(5).trim();
          if (!jsonStr) continue;

          let payload;
          try {
            payload = JSON.parse(jsonStr);
          } catch {
            continue;
          }

          if (payload.error) throw new Error(payload.error);
          if (payload.done) continue;

          if (payload.token) {
            if (firstToken) {
              assistantMsgEl.querySelector(".msg-content").innerHTML = "";
              firstToken = false;
            }
            fullText += payload.token;
            assistantMsgEl.querySelector(".msg-content").innerHTML = renderContent(fullText);
            scrollToBottom();
          }
        }
      }

      convo.messages.push({ role: "assistant", content: fullText || "(no response)" });
      saveConversations();
      renderHistory();
    } catch (err) {
      assistantMsgEl.querySelector(".msg-content").innerHTML =
        `<span class="error-text">Something went wrong: ${escapeHtml(err.message)}</span>`;
      convo.messages.push({ role: "assistant", content: `[Error: ${err.message}]` });
      saveConversations();
    } finally {
      isStreaming = false;
      sendBtn.disabled = !promptInput.value.trim();
    }
  }

  // ---------- Init ----------
  renderHistory();
  renderMessages();
})();
