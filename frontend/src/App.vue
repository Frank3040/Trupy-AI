<script setup>
import { ref, provide } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ChatWindow from './components/ChatWindow.vue'

const isSidebarOpen = ref(false)

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

function closeSidebar() {
  isSidebarOpen.value = false
}

// Provide toggle method to children (ChatWindow)
provide('layout', {
  toggleSidebar,
  closeSidebar
})
</script>

<template>
  <div class="app-layout" :class="{ 'sidebar-open': isSidebarOpen }">
    <!-- Overlay for mobile when sidebar is open -->
    <div class="mobile-overlay" @click="closeSidebar" />

    <Sidebar class="app-sidebar" @close="closeSidebar" />

    <main class="app-workspace">
      <ChatWindow />
    </main>
  </div>
</template>

<style>
:root {
  --primary: #7c3aed;
  --primary-light: #9f67ff;
  --primary-glow: rgba(124, 58, 237, 0.18);
  --primary-dim: rgba(124, 58, 237, 0.1);
  --bg-page: #0d0d12;
  --bg-surface: #16161e;
  --bg-elevated: #1e1e2b;
  --bg-input: #1a1a27;
  --text-primary: #ededf2;
  --text-secondary: #8888a4;
  --text-muted: #52526a;
  --border: rgba(255, 255, 255, 0.06);
  --shadow-purple: 0 0 0 3px rgba(124, 58, 237, 0.2);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 22px;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body,
#app {
  height: 100%;
  overflow: hidden;
}

body {
  background: var(--bg-page);
  font-family: var(--font);
  -webkit-font-smoothing: antialiased;
  color: var(--text-primary);
}

.app-layout {
  display: flex;
  height: 100%;
}

.app-workspace {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.mobile-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 40;
}

@media (max-width: 1024px) {
  .app-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 50;
    transform: translateX(-100%);
  }

  .sidebar-open .app-sidebar {
    transform: translateX(0);
  }

  .sidebar-open .mobile-overlay {
    display: block;
  }
}

::-webkit-scrollbar {
  width: 4px;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
}
</style>
