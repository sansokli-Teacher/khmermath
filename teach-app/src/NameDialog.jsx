import { useState } from 'react';
import Modal from './Modal.jsx';

// Write your own name the way you want it shown (e.g. SAN SOKLI -> សាន សុខលី): reports, slides and class lists use it.
export default function NameDialog({ current, onSave, onClose }) {
  const [v, setV] = useState(current);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  async function submit(e) {
    e.preventDefault();
    const name = v.trim();
    if (!name) { setErr('សូមបញ្ចូលឈ្មោះ។'); return; }
    if (name === current) { onClose(); return; }
    setBusy(true); setErr('');
    try { await onSave(name); } catch (x) { setErr(x.message || 'មិនអាចរក្សាទុកបានទេ។'); setBusy(false); }
  }
  return (
    <Modal title="✏️ ឈ្មោះរបស់ខ្ញុំ" sub="បង្ហាញលើរបាយការណ៍អវត្តមាន ស្លាយ និងបញ្ជីថ្នាក់" onClose={onClose}>
      <form onSubmit={submit} className="name-form">
        <div className="field">
          <label htmlFor="my-name">ឈ្មោះ</label>
          <input id="my-name" type="text" maxLength={60} value={v} onChange={(e) => setV(e.target.value)} autoFocus placeholder="ឧ. សាន សុខលី" />
        </div>
        {err && <p className="alert">{err}</p>}
        <div className="name-act">
          <button type="button" className="btn ghost" onClick={onClose}>បោះបង់</button>
          <button type="submit" className="btn primary" disabled={busy}>{busy ? 'កំពុងរក្សាទុក…' : 'រក្សាទុក'}</button>
        </div>
      </form>
    </Modal>
  );
}
