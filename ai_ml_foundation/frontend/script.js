const input = document.querySelector('#input');
const askBtn = document.querySelector('#ask-btn');
const clearBtn = document.querySelector('#clear-btn');
const chatContainer = document.querySelector('#chat-container');
const emptyState = document.querySelector('#empty-state');
const suggestionChips = document.querySelectorAll('.suggestion-chip');

function genThreadId() {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
}

let threadId = genThreadId();

let isGenerating = false;

// Auto-resize textarea & toggle send button state
input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = `${input.scrollHeight}px`;
  updateButtonState();
});

function updateButtonState() {
  askBtn.disabled = isGenerating || input.value.trim().length === 0;
}

// Send on Enter (allow Shift+Enter for new lines)
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!askBtn.disabled) submitMessage();
  }
});

// Send on button click
askBtn.addEventListener('click', submitMessage);

// Clear chat history
clearBtn.addEventListener('click', () => {
  if (isGenerating) return;

  // Generate a new thread ID
  threadId = genThreadId();

  chatContainer.innerHTML = '';
  emptyState.classList.remove('hidden');

  
  input.focus();
});

// Quick prompt suggestion chips
suggestionChips.forEach(chip => {
  chip.addEventListener('click', () => {
    input.value = chip.dataset.prompt;
    updateButtonState();
    submitMessage();
  });
});

function appendMessage(text, sender = 'user', isError = false) {
  emptyState.classList.add('hidden');

  const wrapper = document.createElement('div');
  wrapper.className =
    sender === 'user' ? 'flex w-full justify-end' : 'flex w-full items-start gap-3 justify-start';

  if (sender === 'assistant') {
    const avatar = document.createElement('div');
    avatar.className =
      'mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border border-neutral-800 bg-neutral-900 text-indigo-400';
    avatar.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-3.5 w-3.5">
        <path fill-rule="evenodd" d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5z" clip-rule="evenodd" />
      </svg>`;
    wrapper.appendChild(avatar);
  }

  const msg = document.createElement('div');
  if (sender === 'user') {
    msg.className =
      'max-w-[85%] sm:max-w-[75%] rounded-2xl rounded-br-sm bg-neutral-800 border border-neutral-700/60 px-4 py-2.5 text-sm sm:text-base leading-relaxed text-neutral-100 break-words whitespace-pre-wrap shadow-sm';
  } else if (isError) {
    msg.className =
      'max-w-[85%] sm:max-w-[80%] rounded-2xl rounded-tl-sm bg-red-950/40 border border-red-900/60 px-4 py-2.5 text-sm sm:text-base leading-relaxed text-red-300 break-words whitespace-pre-wrap';
  } else {
    msg.className =
      'max-w-[85%] sm:max-w-[80%] rounded-2xl rounded-tl-sm bg-neutral-900/80 border border-neutral-800/90 px-4 py-2.5 text-sm sm:text-base leading-relaxed text-neutral-200 break-words whitespace-pre-wrap';
  }

  msg.textContent = text;
  wrapper.appendChild(msg);
  chatContainer.appendChild(wrapper);

  scrollToBottom();
}

function showTypingIndicator() {
  const wrapper = document.createElement('div');
  wrapper.id = 'typing-indicator';
  wrapper.className = 'flex w-full items-start gap-3 justify-start';
  wrapper.innerHTML = `
    <div class="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border border-neutral-800 bg-neutral-900 text-indigo-400">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-3.5 w-3.5">
        <path fill-rule="evenodd" d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5z" clip-rule="evenodd" />
      </svg>
    </div>
    <div class="flex items-center gap-1.5 rounded-2xl rounded-tl-sm border border-neutral-800/90 bg-neutral-900/80 px-4 py-3.5">
      <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-neutral-400 [animation-delay:-0.3s]"></span>
      <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-neutral-400 [animation-delay:-0.15s]"></span>
      <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-neutral-400"></span>
    </div>
  `;
  chatContainer.appendChild(wrapper);
  scrollToBottom();
}

function removeTypingIndicator() {
  const indicator = document.querySelector('#typing-indicator');
  if (indicator) indicator.remove();
}

function scrollToBottom() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth',
  });
}

async function submitMessage() {
  const text = input.value.trim();
  if (!text || isGenerating) return;

  input.value = '';
  input.style.height = 'auto';
  await generate(text);
}

async function generate(text) {
  isGenerating = true;
  updateButtonState();
  appendMessage(text, 'user');
  showTypingIndicator();

  try {
    const assistantMessage = await callServer(text);
    removeTypingIndicator();
    appendMessage(assistantMessage, 'assistant');
  } catch (err) {
    console.error(err);
    removeTypingIndicator();
    appendMessage('Sorry, something went wrong while reaching the server.', 'assistant', true);
  } finally {
    isGenerating = false;
    updateButtonState();
    input.focus();
  }
}

async function callServer(inputText) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: inputText, thread_id: threadId }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}: Error generating the response.`);
  }

  const result = await response.json();
  return result.reply;
}
