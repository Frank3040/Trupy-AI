<script setup>
import { ref, watch, nextTick, inject } from 'vue'
import { useChatStore } from '@/stores/chat'
import WelcomeScreen from './WelcomeScreen.vue'
import MessageBubble from './MessageBubble.vue'
import ChatInput from './ChatInput.vue'

const store = useChatStore()
const messagesEl = ref(null)
const layout = inject('layout')

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

watch(() => store.messages.length, scrollToBottom)
watch(() => store.isLoading, scrollToBottom)

function handleStart({ anonymous, userProfile }) {
  store.startSession(anonymous, userProfile ?? null)
}
</script>

<template>
  <div class="chat-window">
    <header class="header">
      <div class="header-left">
        <button class="menu-toggle" @click="layout.toggleSidebar()" aria-label="Toggle menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="logo">
          <v-icon name="fa-robot" scale="1.2" />
        </div>
        <div>
          <h1 class="title">Trupy AI</h1>
          <p class="subtitle">UPY · Counseling Support</p>
        </div>
      </div>
      <div class="status" :class="{ active: store.sessionStarted && !store.isConcluded }">
        <span class="dot" />
        <span>{{ store.isConcluded ? 'Session ended' : store.sessionStarted ? 'Online' : 'Offline' }}</span>
      </div>
    </header>

    <!-- Welcome screen (before session starts) -->
    <WelcomeScreen v-if="!store.sessionStarted && !store.isLoading && !store.connectionError" @start="handleStart" />

    <!-- Loading / error / chat area -->
    <template v-else>
      <div class="messages" ref="messagesEl">
        <div v-if="store.connectionError" class="state-msg error">
          {{ store.connectionError }}
        </div>

        <div v-else-if="!store.sessionStarted && store.isLoading" class="state-msg">
          <span class="spinner" />
          Connecting to Trupy AI…
        </div>

        <template v-else>
          <div class="messages-inner">
            <TransitionGroup name="msg" tag="div" class="msg-list">
              <MessageBubble
                v-for="msg in store.messages"
                :key="msg.id"
                :message="msg"
              />
            </TransitionGroup>

            <div v-if="store.isLoading" class="typing">
              <span /><span /><span />
            </div>

            <div v-if="store.isConcluded" class="concluded-notice">
              This session has concluded. Thank you for reaching out.
            </div>
          </div>
        </template>
      </div>

      <footer class="chat-footer">
        <div class="footer-inner">
          <ChatInput
            :disabled="!store.sessionStarted || store.isLoading || store.isConcluded"
            @send="store.sendMessage"
          />
        </div>
      </footer>
    </template>
  </div>
</template>

<style scoped>
.chat-window {
  width: 100%;
  height: 100%;
  background: var(--bg-surface);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-surface);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 4px;
  margin-right: 4px;
}

.logo {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--primary-dim);
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.subtitle {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 1px;
}

.status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: background 0.3s;
}

.status.active .dot {
  background: #34d399;
  box-shadow: 0 0 6px rgba(52, 211, 153, 0.5);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  scroll-behavior: smooth;
}

.chat-footer {
  width: 100%;
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.footer-inner {
  width: 100%;
  max-width: 760px;
  padding: 0 20px;
}

.messages-inner {
  width: 100%;
  max-width: 760px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.msg-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.state-msg {
  margin: auto;
  color: var(--text-muted);
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.state-msg.error {
  color: #f87171;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

.typing {
  display: flex;
  gap: 5px;
  padding: 10px 15px;
  background: var(--bg-elevated);
  border-radius: var(--radius-lg);
  border-bottom-left-radius: var(--radius-sm);
  width: fit-content;
  align-self: flex-start;
}

.typing span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--text-muted);
  animation: bounce 1.2s ease-in-out infinite;
}

.typing span:nth-child(2) { animation-delay: 0.15s; }
.typing span:nth-child(3) { animation-delay: 0.3s; }

.concluded-notice {
  text-align: center;
  font-size: 0.78rem;
  color: var(--text-muted);
  padding: 12px;
  border-top: 1px solid var(--border);
  margin-top: 8px;
}

.msg-enter-active {
  transition: all 0.2s ease;
}
.msg-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 1024px) {
  .menu-toggle {
    display: block;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-5px); }
}
</style>
