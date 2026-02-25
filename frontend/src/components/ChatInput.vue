<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: Boolean,
})

const emit = defineEmits(['send'])
const text = ref('')
const textarea = ref(null)

function autoResize() {
  const el = textarea.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 120) + 'px'
}

function submit() {
  const val = text.value.trim()
  if (!val || props.disabled) return
  emit('send', val)
  text.value = ''
  if (textarea.value) {
    textarea.value.style.height = 'auto'
  }
}

function onKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <div class="input-bar">
    <textarea
      ref="textarea"
      v-model="text"
      :disabled="disabled"
      placeholder="Type your message…"
      rows="1"
      @input="autoResize"
      @keydown="onKeydown"
    />
    <button class="send-btn" :disabled="disabled || !text.trim()" @click="submit" aria-label="Send">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M22 2L15 22l-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.input-bar {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  padding: 14px 18px;
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
}

textarea {
  flex: 1;
  resize: none;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  font-family: var(--font);
  font-size: 0.9rem;
  color: var(--text-primary);
  line-height: 1.5;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  overflow: hidden;
}

textarea::placeholder {
  color: var(--text-muted);
}

textarea:focus {
  border-color: var(--primary);
  box-shadow: var(--shadow-purple);
}

textarea:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.send-btn {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: var(--primary-dim);
  color: var(--primary-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.18s, color 0.18s, transform 0.1s;
}

.send-btn:hover:not(:disabled) {
  background: var(--primary);
  color: #fff;
}

.send-btn:active:not(:disabled) {
  transform: scale(0.92);
}

.send-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>
