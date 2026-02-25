<script setup>
const emit = defineEmits(['close'])

const navItems = [
  { id: 'home', label: 'Home', icon: 'md-school-round' },
  { id: 'about', label: 'About', icon: 'bi-info-square-fill' }
]
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="logo">
        <v-icon name="md-school-round" scale="1.3" />
        <span class="brand-name">UPY</span>
      </div>
      <button class="mobile-close" @click="emit('close')" aria-label="Close sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li v-for="item in navItems" :key="item.id" class="nav-item">
          <button class="nav-link" :class="{ active: item.id === 'home' }">
            <span class="nav-icon"><v-icon :name="item.icon" scale="1.1" /></span>
            <span class="nav-label">{{ item.label }}</span>
          </button>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <div class="user-status">
        <div class="status-indicator online"></div>
        <span class="status-name">Counseling Mode</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.sidebar-header {
  padding: 24px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.mobile-close {
  display: none;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
}

.nav-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: none;
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-family: var(--font);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.nav-link:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.nav-link.active {
  background: var(--primary-dim);
  color: var(--primary-light);
}

.nav-icon {
  font-size: 1.1rem;
  width: 24px;
  display: flex;
  justify-content: center;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid var(--border);
}

.user-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator.online {
  background: #34d399;
  box-shadow: 0 0 6px rgba(52, 211, 153, 0.4);
}

.status-name {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

@media (max-width: 1024px) {
  .mobile-close {
    display: block;
  }
}
</style>
