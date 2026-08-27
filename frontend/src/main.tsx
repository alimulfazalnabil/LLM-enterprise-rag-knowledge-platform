import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Search, ShieldCheck, Upload, Activity, Database } from 'lucide-react';
import './styles.css';

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
function App() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const ask = async () => {
    setLoading(true);
    const login = await fetch(`${API}/api/v1/auth/login`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({tenant_id:'demo', user_id:'alice', password:'demo-password'}) });
    const { access_token } = await login.json();
    const response = await fetch(`${API}/api/v1/chat`, { method: 'POST', headers: {'Content-Type':'application/json', Authorization:`Bearer ${access_token}`}, body: JSON.stringify({question: query}) });
    setAnswer(await response.json()); setLoading(false);
  };
  return <main><header><div className="brand"><span className="mark">ER</span><div><strong>Enterprise RAG</strong><small>Knowledge Platform</small></div></div><div className="status"><Activity size={15}/> Local environment <b>●</b></div></header><section className="hero"><p className="eyebrow">ACME CLOUD / KNOWLEDGE OPERATIONS</p><h1>Answers with a paper trail.</h1><p className="lede">Search authorized enterprise knowledge, inspect the evidence, and keep every response grounded.</p><div className="query"><Search size={21}/><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()} placeholder="Ask about policy, operations, security..."/><button onClick={ask} disabled={loading||!query}>{loading?'Working':'Ask assistant'}</button></div></section><section className="grid"><article><div className="label"><ShieldCheck size={17}/> TRUST BOUNDARY</div><h2>Tenant-scoped by default</h2><p>Authorization is applied before dense or sparse retrieval. Sources are verified again before they reach the answer.</p></article><article><div className="label"><Database size={17}/> RETRIEVAL</div><h2>Hybrid evidence</h2><p>Lexical matching catches identifiers and exact terms while semantic matching finds concepts. RRF fuses both paths.</p></article><article><div className="label"><Upload size={17}/> INGESTION</div><h2>Ready for your corpus</h2><p>Upload a UTF-8 text or Markdown file to create a versioned, traceable source chunk.</p></article></section>{answer&&<section className="answer"><div className="answer-head"><span>ASSISTANT RESPONSE</span><b className={answer.grounded?'grounded':'ungrounded'}>{answer.grounded?'GROUNDED':'INSUFFICIENT EVIDENCE'}</b></div><p>{answer.answer}</p>{answer.citations?.length>0&&<div className="sources"><strong>Verified sources</strong>{answer.citations.map((c:any)=><div className="source" key={c.chunk_id}><span>[1]</span><div><b>{c.section}</b><small>{c.document_id} · {c.version_id}{c.page?` · page ${c.page}`:''}</small></div></div>)}</div>}</section>}</main>
}
createRoot(document.getElementById('root')!).render(<App />);
