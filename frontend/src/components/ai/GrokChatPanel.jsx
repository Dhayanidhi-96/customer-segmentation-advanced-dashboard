import { useState } from 'react'
import { askAI } from '../../api/ai'

function GrokChatPanel() {
  const [sessionId, setSessionId] = useState('')
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim()) return
    setLoading(true)
    const userText = input
    setMessages((prev) => [...prev, { role: 'user', content: userText }])
    setInput('')
    try {
      const res = await askAI({ session_id: sessionId || null, message: userText })
      setSessionId(res.session_id)
      setMessages((prev) => [...prev, { role: 'assistant', content: res.response }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-2xl border border-zinc-100 p-4 h-[560px] flex flex-col">
      <h3 className="font-display mb-3">Grok AI Chat</h3>
      <div className="flex-1 overflow-auto space-y-2">
        {messages.map((m, idx) => (
          <div key={idx} className={`p-2 rounded-lg text-sm ${m.role === 'user' ? 'bg-ink text-cream ml-8' : 'bg-zinc-100 mr-8'}`}>
            {m.content}
          </div>
        ))}
      </div>
      <div className="mt-3 flex gap-2">
        <input
          className="flex-1 border rounded-lg px-3 py-2"
          value={input}
          placeholder="Ask about segment shifts and campaigns..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
        />
        <button className="px-4 py-2 bg-coral text-white rounded-lg" disabled={loading} onClick={send}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default GrokChatPanel
