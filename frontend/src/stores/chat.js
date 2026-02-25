import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/api/chat'

let _id = 0
const mkMsg = (text, sender) => ({ id: ++_id, text, sender })

export const useChatStore = defineStore('chat', () => {
  const sessionId = ref(null)
  const messages = ref([])
  const isLoading = ref(false)
  const isConcluded = ref(false)
  const sessionStarted = ref(false)
  const connectionError = ref(null)

  async function startSession(anonymous = true, userProfile = null) {
    isLoading.value = true
    connectionError.value = null
    try {
      const data = await api.startSession(anonymous, userProfile)
      sessionId.value = data.session_id
      sessionStarted.value = true
      messages.value.push(mkMsg(data.greeting, 'bot'))
    } catch {
      connectionError.value = 'Could not connect to the server. Please refresh the page.'
    } finally {
      isLoading.value = false
    }
  }

  async function sendMessage(text) {
    if (!sessionId.value || isConcluded.value || isLoading.value) return
    messages.value.push(mkMsg(text, 'user'))
    isLoading.value = true
    try {
      const data = await api.sendMessage(sessionId.value, text)
      messages.value.push(mkMsg(data.reply, 'bot'))
      if (data.is_final) {
        isConcluded.value = true
      }
    } catch {
      messages.value.push(mkMsg('Sorry, something went wrong. Please try again.', 'bot'))
    } finally {
      isLoading.value = false
    }
  }

  return {
    sessionId,
    messages,
    isLoading,
    isConcluded,
    sessionStarted,
    connectionError,
    startSession,
    sendMessage,
  }
})
