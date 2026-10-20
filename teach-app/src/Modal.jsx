import { useEffect } from 'react';

// Pop-up on desktop/tablet, full screen on phones. Esc and the backdrop close it.
export default function Modal({ title, sub, onClose, wide, children }) {
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => { window.removeEventListener('keydown', onKey); document.body.style.overflow = ''; };
  }, [onClose]);
  return (
    <div className="modal-back" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <section className={`modal${wide ? ' wide' : ''}`} role="dialog" aria-modal="true" aria-label={title}>
        <header className="modal-hd">
          <div><h2>{title}</h2>{sub && <p>{sub}</p>}</div>
          <button className="x" onClick={onClose} aria-label="បិទ">✕</button>
        </header>
        <div className="modal-body">{children}</div>
      </section>
    </div>
  );
}
