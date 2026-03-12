import React, { useState } from 'react';

export default function UploadCard({ onTranscribed }: { onTranscribed: (t: string, sourceName: string) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const API = process.env.NEXT_PUBLIC_API_BASE as string;

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append('file', file);

    try {
      const res = await fetch(`${API}/transcribe`, { method: 'POST', body: form });
      const data = await res.json();
      if (res.ok) {
        onTranscribed(data.transcript, file.name);
      } else {
        alert(data.detail || 'Transcription failed');
      }
    } catch (e: any) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Import Video or Audio</h3>
      <p>Drag & drop or browse to upload a file. We'll auto-transcribe it.</p>
      <input type="file" accept="video/*,audio/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <div style={{ height: 12 }} />
      <button className="btn" onClick={handleUpload} disabled={!file || loading}>
        {loading ? 'Transcribing…' : 'Transcribe'}
      </button>
    </div>
  );
}
