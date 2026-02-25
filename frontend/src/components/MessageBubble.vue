<script setup>
defineProps({
  message: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="bubble-row" :class="message.sender">
    <div class="avatar" v-if="message.sender === 'bot'">
      <v-icon name="fa-robot" scale="1.2" />
    </div>
    <div class="bubble">
      <p>{{ message.text }}</p>
    </div>
  </div>
</template>

<style scoped>
.bubble-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  max-width: 72%;
  animation: fadeUp 0.2s ease both;
}

.bubble-row.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.bubble-row.bot {
  align-self: flex-start;
}

.avatar {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--bg-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
}

.bubble {
  padding: 10px 15px;
  border-radius: var(--radius-lg);
  font-size: 0.9rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.bubble-row.user .bubble {
  background: var(--primary);
  color: #fff;
  border-bottom-right-radius: var(--radius-sm);
}

.bubble-row.bot .bubble {
  background: var(--bg-elevated);
  color: var(--text-primary);
  border-bottom-left-radius: var(--radius-sm);
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
