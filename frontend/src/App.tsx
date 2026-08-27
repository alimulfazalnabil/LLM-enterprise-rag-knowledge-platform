import React, { useState } from 'react'

export function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      const data = await res.json()
      setResponse(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>Enterprise RAG Knowledge Platform</h1>
      <form onSubmit={handleSearch} style={{ display: 'flex', gap: 8, marginTop: 12 }}>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask an enterprise question" />
        <button type="submit" disabled={loading}>{loading ? 'Searching...' : 'Ask AI'}</button>
      </form>
      {response && <pre style={{ marginTop: 12 }}>{JSON.stringify(response, null, 2)}</pre>}
    </div>
  )
}

export default App
