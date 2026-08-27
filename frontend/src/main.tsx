import React from 'react'
import ReactDOM from 'react-dom/client'

const App = () => (
  <main style={{ fontFamily: 'sans-serif', padding: 24 }}>
    <h1>Enterprise RAG Knowledge Platform</h1>
    <p>Dashboard scaffold for multi-tenant enterprise RAG.</p>
  </main>
)

ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
