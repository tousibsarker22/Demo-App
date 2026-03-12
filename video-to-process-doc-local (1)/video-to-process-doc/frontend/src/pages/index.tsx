import React, { useState } from 'react';
import UploadCard from '../components/UploadCard';
import PreviewEditor from '../components/PreviewEditor';

interface ProcessModel { [key: string]: any }

export default function Home() {
  const API = process.env.NEXT_PUBLIC_API_BASE as string;
  const [transcript, setTranscript] = useState('');
  const [sourceName, setSourceName] = useState('');
  const [title, setTitle] = useState('');
  const [processData, setProcessData] = useState<ProcessModel | null>(null);
  const [author, setAuthor] = useState('');
  const [busy, setBusy] = useState(false);

  const onTranscribed = (t: string, src: string) => {
    setTranscript(t);
    setSourceName(src);
  };

  const extract = async () => {
    setBusy(true);
    try {
      const res = await fetch(`${API}/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript, title, tone: 'simple' })
      });
      const data = await res.json();
      if (res.ok) setProcessData(data.process); else alert(data.detail || 'Extraction failed');
    } catch (e: any) {
      alert(e.message);
    } finally { setBusy(false); }
  };

  const exportDoc = async () => {
    if (!processData) return;
    const res = await fetch(`${API}/document`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ process: processData, author, source_name: sourceName })
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      alert(data.detail || 'Export failed');
      return;
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${processData.title || 'process'}.docx`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container">
      <h1>Video → Process Document</h1>

      <div className="row">
        <div style={{ flex: 1 }}>
          <UploadCard onTranscribed={onTranscribed} />
          <div className="card" style={{ marginTop: 16 }}>
            <h3>Or Paste Transcript</h3>
            <textarea className="textarea" value={transcript} onChange={(e) => setTranscript(e.target.value)} placeholder="Paste transcript here…" />
          </div>
        </div>
        <div style={{ flex: 1 }}>
          <div className="card">
            <h3>Settings</h3>
            <label>Title</label>
            <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Optional title" />
            <label>Author</label>
            <input className="input" value={author} onChange={(e) => setAuthor(e.target.value)} placeholder="Your name" />
            <button className="btn" onClick={extract} disabled={!transcript || busy}>
              {busy ? 'Extracting…' : 'Build Process'}
            </button>
          </div>
        </div>
      </div>

      <div style={{ height: 16 }} />
      <PreviewEditor process={processData} setProcess={setProcessData as any} />

      {processData && (
        <div className="card" style={{ marginTop: 16 }}>
          <button className="btn" onClick={exportDoc}>Export Word (.docx)</button>
        </div>
      )}
    </div>
  );
}
