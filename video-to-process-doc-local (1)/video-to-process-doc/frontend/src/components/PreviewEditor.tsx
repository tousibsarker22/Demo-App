import React from 'react';

interface Step { number: number; action: string; details?: string; role?: string; tools?: string[] }
interface Decision { condition: string; path_yes?: string; path_no?: string }
interface ProcessModel {
  title: string; summary: string; purpose: string; scope?: string;
  roles: string[]; tools: string[]; steps: Step[]; decisions: Decision[]; notes?: string[]
}

export default function PreviewEditor({ process, setProcess }: {
  process: ProcessModel | null,
  setProcess: (p: ProcessModel) => void,
}) {
  if (!process) return null;

  const onField = (key: keyof ProcessModel, value: any) => setProcess({ ...process, [key]: value });

  return (
    <div className="card">
      <h3>Preview & Edit</h3>
      <label>Title</label>
      <input className="input" value={process.title} onChange={e => onField('title', e.target.value)} />

      <label>Summary</label>
      <textarea className="textarea" value={process.summary} onChange={e => onField('summary', e.target.value)} />

      <label>Purpose</label>
      <textarea className="textarea" value={process.purpose} onChange={e => onField('purpose', e.target.value)} />

      <label>Steps</label>
      {process.steps.map((s, i) => (
        <div key={i} className="card" style={{ background: '#fafafa' }}>
          <input className="input" value={s.action} onChange={e => {
            const steps = [...process.steps];
            steps[i] = { ...steps[i], action: e.target.value };
            onField('steps', steps);
          }} />
          <textarea className="textarea" value={s.details || ''} onChange={e => {
            const steps = [...process.steps];
            steps[i] = { ...steps[i], details: e.target.value };
            onField('steps', steps);
          }} />
        </div>
      ))}
    </div>
  );
}
