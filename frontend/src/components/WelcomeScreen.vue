<script setup>
import { ref } from 'vue'

const emit = defineEmits(['start'])
const showForm = ref(false)
const name = ref('')
const major = ref('')
const quarter = ref('')

function chooseAnonymous() {
  emit('start', { anonymous: true })
}

function showIdentifyForm() {
  showForm.value = true
}

function startIdentified() {
  if (!name.value.trim() || !major.value.trim() || !quarter.value.trim()) {
    return
  }
  emit('start', {
    anonymous: false,
    userProfile: {
      name: name.value.trim(),
      major: major.value.trim(),
      quarter: quarter.value.trim(),
    },
  })
}
</script>

<template>
  <div class="welcome">
    <div class="welcome-icon"><v-icon name="fa-robot" scale="3.5" fill="var(--primary-light)" /></div>
    <h2 class="welcome-title">Welcome to Trupy AI</h2>
    <p class="welcome-sub">Psychology Department · UPY University</p>
    <p class="welcome-desc">How would you like to proceed today?</p>

    <div v-if="!showForm" class="btn-group">
      <button class="btn btn-ghost" @click="chooseAnonymous">
        <span class="btn-icon">🕵️</span>
        Stay Anonymous
      </button>
      <button class="btn btn-primary" @click="showIdentifyForm">
        <span class="btn-icon">🪪</span>
        Identify Yourself
      </button>
    </div>

    <Transition name="form-slide">
      <div v-if="showForm" class="identify-form">
        <div class="form-group">
          <label for="inp-name">Name</label>
          <input
            id="inp-name"
            v-model="name"
            type="text"
            placeholder="e.g. María García"
          />
        </div>
        <div class="form-group">
          <label for="inp-major">Major</label>
          <input
            id="inp-major"
            v-model="major"
            type="text"
            placeholder="e.g. Computer Science"
          />
        </div>
        <div class="form-group">
          <label for="inp-quarter">Quarter / Semester</label>
          <input
            id="inp-quarter"
            v-model="quarter"
            type="text"
            placeholder="e.g. 5th"
          />
        </div>
        <div class="form-actions">
          <button class="btn btn-ghost btn-sm" @click="showForm = false">← Back</button>
          <button
            class="btn btn-primary btn-sm"
            :disabled="!name.trim() || !major.trim() || !quarter.trim()"
            @click="startIdentified"
          >
            Start Chat →
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  padding: 60px 40px;
  text-align: center;
  animation: fadeIn 0.4s ease;
}

.welcome-icon {
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 0 24px var(--primary-glow));
}

.welcome-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
  letter-spacing: -0.02em;
}

.welcome-sub {
  font-size: 0.88rem;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.welcome-desc {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

.btn-group {
  display: flex;
  gap: 14px;
  width: 100%;
  max-width: 480px;
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 13px 18px;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font);
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon {
  font-size: 1.1rem;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
}
.btn-primary:hover:not(:disabled) {
  background: var(--primary-light);
  box-shadow: 0 4px 18px rgba(124, 58, 237, 0.35);
}
.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-ghost {
  background: var(--bg-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border);
}
.btn-ghost:hover {
  background: var(--bg-input);
  color: var(--text-primary);
  border-color: rgba(255, 255, 255, 0.12);
}

.btn-sm {
  padding: 10px 18px;
  font-size: 0.84rem;
}

.identify-form {
  width: 100%;
  max-width: 480px;
  text-align: left;
}

.form-group {
  margin-bottom: 14px;
}

.form-group label {
  display: block;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 6px;
  letter-spacing: 0.02em;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-family: var(--font);
  font-size: 0.88rem;
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input::placeholder {
  color: var(--text-muted);
}

.form-group input:focus {
  border-color: var(--primary);
  box-shadow: var(--shadow-purple);
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 18px;
}

.form-actions .btn {
  flex: 1;
}

/* Transition */
.form-slide-enter-active {
  transition: all 0.3s ease;
}
.form-slide-leave-active {
  transition: all 0.2s ease;
}
.form-slide-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.form-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
