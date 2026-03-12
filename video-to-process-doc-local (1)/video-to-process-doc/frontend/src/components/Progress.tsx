export default function Progress({ percent }: { percent: number }) {
  return (
    <div className="progress"><div style={{ width: `${percent}%` }} /></div>
  );
}
