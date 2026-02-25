const BASE = import.meta.env.VITE_API_URL ?? '/api/v1'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail ?? `HTTP ${res.status}`)
  }
  return res.json()
}

export function startSession(anonymous = true, userProfile = null) {
  return request('/sessions/start', {
    method: 'POST',
    body: JSON.stringify({ anonymous, user_profile: userProfile }),
  })
}

export function sendMessage(sessionId, message) {
  return request('/chat/message', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, message }),
  })
}

export function endSession(sessionId) {
  return request(`/sessions/${sessionId}/end`, { method: 'POST' })
}
