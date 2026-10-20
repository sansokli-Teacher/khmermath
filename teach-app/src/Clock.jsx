import { useEffect, useState } from 'react';
import { kh } from './api.js';

const DAYS = ['អាទិត្យ', 'ច័ន្ទ', 'អង្គារ', 'ពុធ', 'ព្រហស្បតិ៍', 'សុក្រ', 'សៅរ៍'];

export default function Clock({ compact }) {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 15000);
    return () => clearInterval(t);
  }, []);
  const p = (n) => String(n).padStart(2, '0');
  return (
    <div className={`clock${compact ? ' compact' : ''}`} aria-label="ម៉ោងបច្ចុប្បន្ន">
      <b>{kh(`${p(now.getHours())}:${p(now.getMinutes())}`)}</b>
      <span>ថ្ងៃ{DAYS[now.getDay()]} · {kh(`${p(now.getDate())}/${p(now.getMonth() + 1)}/${now.getFullYear()}`)}</span>
    </div>
  );
}
