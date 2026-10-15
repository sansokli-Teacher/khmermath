/* OMR answer sheet: one layout definition used both to DRAW the sheet and to READ a photo of it.
   Sheet space is a 180 x 236 mm rectangle. Four solid black squares sit in its corners (the bottom-right one is
   larger, so the sheet can be read upside-down too); the photo is mapped back to this rectangle with a perspective
   transform, then every bubble is looked at in the place where the layout says it should be. */
(function () {
  const W = 180, H = 236;
  const MARK = { tl: [4, 4, 8], tr: [176, 4, 8], bl: [4, 232, 8], br: [174.5, 230.5, 11] };   // centre x, y, size
  const R_BUB = 2.2, R_READ = 1.55;                // bubble radius drawn / radius read
  const ROWS = 20, COL_PITCH = 33.5, Q_Y0 = 108, Q_PITCH = 6;
  const ID_Y0 = 46, ID_PITCH = 5.0, ID_X0 = 16, ID_COL_PITCH = 6.2;
  const CODE_X0 = 20, CODE_Y = 231, CODE_PITCH = 4.6, CODE_BITS = 20;
  const MAX_Q = ROWS * 5;
  const KH_LET = ['ក', 'ខ', 'គ', 'ឃ', 'ង'];
  const LAT_LET = ['A', 'B', 'C', 'D', 'E'];
  const LEVELS = ['easy', 'medium', 'hard', 'pisa'];

  const optPitch = (optCount) => (optCount >= 5 ? 5.4 : 6.2);

  function layout(nQ, optCount, idDigits) {
    optCount = Math.min(5, Math.max(2, optCount || 4));
    idDigits = Math.min(12, Math.max(1, idDigits || 7));
    const q = [];
    for (let i = 0; i < Math.min(nQ, MAX_Q); i++) {
      const col = Math.floor(i / ROWS), row = i % ROWS;
      const x0 = 8 + col * COL_PITCH, y = Q_Y0 + row * Q_PITCH;
      q.push({ i, labelX: x0, y, bubbles: [...Array(optCount).keys()].map((k) => [x0 + 10 + k * optPitch(optCount), y]) });
    }
    const id = [];
    for (let c = 0; c < idDigits; c++) id.push([...Array(10).keys()].map((d) => [ID_X0 + c * ID_COL_PITCH, ID_Y0 + d * ID_PITCH]));
    const code = [...Array(CODE_BITS).keys()].map((b) => [CODE_X0 + b * CODE_PITCH, CODE_Y]);
    return { q, id, code, optCount, idDigits, cols: Math.ceil(Math.min(nQ, MAX_Q) / ROWS) };
  }

  // ---- header code: test id (14 bits) + grouped flag + id digits (4 bits) + parity ----
  function codeBits(testId, grouped, idDigits) {
    const bits = [];
    for (let b = 13; b >= 0; b--) bits.push((testId >> b) & 1);
    bits.push(grouped ? 1 : 0);
    for (let b = 3; b >= 0; b--) bits.push((idDigits >> b) & 1);
    bits.push(bits.reduce((a, x) => a ^ x, 0));
    return bits;
  }
  function parseBits(bits) {
    if (bits.length !== CODE_BITS || bits.reduce((a, x) => a ^ x, 0) !== 0) return null;
    let testId = 0; for (let b = 0; b < 14; b++) testId = (testId << 1) | bits[b];
    let idDigits = 0; for (let b = 15; b < 19; b++) idDigits = (idDigits << 1) | bits[b];
    return { testId, grouped: !!bits[14], idDigits };
  }

  // printed order of the multiple-choice questions (the same on the sheet, the paper and the scanner)
  function mcqOrder(mcq, grouped) {
    if (!grouped || !mcq.some((q) => q.level)) return mcq.slice();
    return [...LEVELS.flatMap((lv) => mcq.filter((q) => q.level === lv)), ...mcq.filter((q) => !q.level)];
  }

  // ---------------- drawing ----------------
  function sheetEl(h, o) {
    const { nQ, optCount, idDigits, testId, grouped, letters, title, subtitle, note } = o;
    const L = layout(nQ, optCount, idDigits);
    const lets = letters === 'latin' ? LAT_LET : KH_LET;
    const mm = (v) => `${v}mm`;
    const abs = (cls, x, y, w, hh, extra = '', kids = null, text = null) => h('div', { class: cls, style: `left:${mm(x)};top:${mm(y)};${w != null ? `width:${mm(w)};` : ''}${hh != null ? `height:${mm(hh)};` : ''}${extra}` }, text != null ? text : kids);
    const kids = [];
    for (const [cx, cy, s] of Object.values(MARK)) kids.push(abs('omr-mk', cx - s / 2, cy - s / 2, s, s));
    kids.push(abs('omr-title', 14, 2.5, 152, 12, '', null, title || ''));
    kids.push(abs('omr-sub', 14, 13.5, 152, 5, '', null, subtitle || ''));
    kids.push(abs('omr-fld', 14, 20, 74, 6, '', null, 'ឈ្មោះ៖'));
    kids.push(abs('omr-fld', 92, 20, 40, 6, '', null, 'ថ្នាក់៖'));
    kids.push(abs('omr-fld', 136, 20, 30, 6, '', null, 'កាលបរិច្ឆេទ៖'));
    // student id
    kids.push(abs('omr-cap', 8, 26.2, 92, 4.5, '', null, 'អត្តលេខ (សរសេរ រួចគូសរង្វង់)'));
    kids.push(abs('omr-hint', 8, 30.4, 90, 3.4, '', null, 'គូសរង្វង់ ១ ខ្ទង់ក្នុងមួយជួរឈរ ឱ្យត្រូវនឹងលេខដែលបានសរសេរ'));
    for (let c = 0; c < L.idDigits; c++) kids.push(abs('omr-write', ID_X0 + c * ID_COL_PITCH - 2.7, 34.5, 5.4, 7));
    for (let d = 0; d < 10; d++) kids.push(abs('omr-dl', ID_X0 - 8.5, ID_Y0 + d * ID_PITCH - 2, 5, 4, '', null, String(d)));
    L.id.forEach((col) => col.forEach(([x, y]) => kids.push(abs('omr-bub', x - R_BUB, y - R_BUB, 2 * R_BUB, 2 * R_BUB))));
    // marking instructions
    const ix = Math.max(100, ID_X0 + L.idDigits * ID_COL_PITCH + 6);
    if (ix < 150) {
      kids.push(abs('omr-note', ix, 30, 172 - ix, 62, '', [
        h('b', {}, 'របៀបគូស'), h('div', {}, note || 'ប្រើប៊ិចខ្មៅ ឬខ្មៅដៃ 2B។ គូសរង្វង់ឱ្យខ្មៅពេញ ១ ចម្លើយក្នុងមួយសំណួរ។ បើកែ សូមលុបឱ្យស្អាត។ កុំគូសក្រៅរង្វង់ កុំបត់សន្លឹក។'),
        h('div', { class: 'omr-ex' }, 'ឧទាហរណ៍៖ សំណួរមួយមានចម្លើយ ក ខ គ ឃ'),
        h('div', { class: 'omr-exrow omr-exhead' }, [h('span', { class: 'omr-exl' }), ...lets.slice(0, 4).map((t) => h('span', { class: 'omr-exh' }, t))]),
        ...[['✔ ត្រូវ (ចម្លើយ ខ)', [0, 1, 0, 0], ''], ['មិនទាន់គូស', [0, 0, 0, 0], ''], ['✗ ខុស៖ គូសមិនពេញ', [0, 0, 0, 0], 'half'], ['✗ ខុស៖ គូសជា X', [0, 0, 0, 0], 'x'], ['✗ ខុស៖ គូស ២ ចម្លើយ', [1, 1, 0, 0], '']].map(([lab, fills, kind], r) =>
          h('div', { class: 'omr-exrow' }, [h('span', { class: 'omr-exl' }, lab), ...fills.map((f, k) => h('span', { class: `omr-bub omr-ex-b${f ? ' omr-fill' : ''}${kind === 'half' && k === 2 ? ' omr-half' : ''}${kind === 'x' && k === 2 ? ' omr-x' : ''}` }))])),
      ]));
    }
    // answers
    kids.push(abs('omr-cap', 8, 94.3, 120, 4.5, '', null, `ចម្លើយពហុជ្រើសរើស (${nQ} សំណួរ)`));
    for (let c = 0; c < L.cols; c++) {
      const x0 = 8 + c * COL_PITCH;
      lets.slice(0, L.optCount).forEach((lt, k) => kids.push(abs('omr-hl', x0 + 10 + k * optPitch(L.optCount) - 3, Q_Y0 - 8, 6, 4.5, '', null, lt)));
    }
    L.q.forEach((r) => {
      kids.push(abs('omr-ql', r.labelX, r.y - 2.2, 6.3, 4.4, '', null, String(r.i + 1)));
      r.bubbles.forEach(([x, y]) => kids.push(abs('omr-bub', x - R_BUB, y - R_BUB, 2 * R_BUB, 2 * R_BUB)));
    });
    // header code (printed by the system — do not touch)
    const bits = codeBits(testId || 0, grouped, L.idDigits);
    L.code.forEach(([x, y], b) => kids.push(abs(`omr-bit${bits[b] ? ' on' : ''}`, x - 1.5, y - 1.5, 3, 3)));
    kids.push(abs('omr-cap', CODE_X0 + CODE_BITS * CODE_PITCH + 1, CODE_Y - 2.5, 60, 5, 'font-size:6.5pt;', null, `កូដ #${testId || 0}${grouped ? ' · តាមកម្រិត' : ''}`));
    return h('div', { class: 'omr-sheet', style: `width:${mm(W)};height:${mm(H)};` }, kids);
  }

  // ---------------- reading ----------------
  function solve8(A, b) {              // Gaussian elimination, 8x8
    const n = 8; const M = A.map((r, i) => [...r, b[i]]);
    for (let c = 0; c < n; c++) {
      let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      if (Math.abs(M[p][c]) < 1e-12) return null;
      [M[c], M[p]] = [M[p], M[c]];
      for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
    }
    return M.map((r, i) => r[n] / r[i]);
  }
  function homography(src, dst) {       // maps src (sheet mm) -> dst (image px)
    const A = [], b = [];
    src.forEach(([x, y], i) => {
      const [u, v] = dst[i];
      A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
      A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
    });
    const s = solve8(A, b); if (!s) return null;
    return (x, y) => { const d = s[6] * x + s[7] * y + 1; return [(s[0] * x + s[1] * y + s[2]) / d, (s[3] * x + s[4] * y + s[5]) / d]; };
  }

  function toGray(imgData, maxSide) {
    const { width: w0, height: h0, data } = imgData;
    const sc = Math.min(1, maxSide / Math.max(w0, h0));
    const w = Math.round(w0 * sc), h = Math.round(h0 * sc);
    const g = new Uint8Array(w * h);
    // (data is already at the wanted size when the caller drew it scaled)
    for (let i = 0, j = 0; i < w * h; i++, j += 4) g[i] = (data[j] * 77 + data[j + 1] * 150 + data[j + 2] * 29) >> 8;
    return { g, w, h };
  }

  function binarize(g, w, h) {          // Bradley adaptive threshold using an integral image
    const I = new Float64Array((w + 1) * (h + 1));
    for (let y = 0; y < h; y++) { let row = 0; for (let x = 0; x < w; x++) { row += g[y * w + x]; I[(y + 1) * (w + 1) + x + 1] = I[y * (w + 1) + x + 1] + row; } }
    const s = Math.max(15, Math.round(w / 14)) | 1, hs = s >> 1, t = 0.13;
    const bin = new Uint8Array(w * h);
    for (let y = 0; y < h; y++) {
      const y1 = Math.max(0, y - hs), y2 = Math.min(h - 1, y + hs);
      for (let x = 0; x < w; x++) {
        const x1 = Math.max(0, x - hs), x2 = Math.min(w - 1, x + hs);
        const cnt = (x2 - x1 + 1) * (y2 - y1 + 1);
        const sum = I[(y2 + 1) * (w + 1) + x2 + 1] - I[y1 * (w + 1) + x2 + 1] - I[(y2 + 1) * (w + 1) + x1] + I[y1 * (w + 1) + x1];
        bin[y * w + x] = g[y * w + x] * cnt < sum * (1 - t) && g[y * w + x] < 170 ? 1 : 0;
      }
    }
    return bin;
  }

  function blobs(bin, w, h) {            // 4-connected components, keeps only square-ish solid ones
    const seen = new Uint8Array(w * h), out = [], stack = new Int32Array(w * h);
    const minA = w * h * 0.00025, maxA = w * h * 0.03;
    for (let p0 = 0; p0 < w * h; p0++) {
      if (!bin[p0] || seen[p0]) continue;
      let sp = 0; stack[sp++] = p0; seen[p0] = 1;
      let area = 0, sx = 0, sy = 0, x1 = w, y1 = h, x2 = 0, y2 = 0, edge = false;
      while (sp) {
        const p = stack[--sp], x = p % w, y = (p / w) | 0;
        area++; sx += x; sy += y;
        if (x < x1) x1 = x; if (x > x2) x2 = x; if (y < y1) y1 = y; if (y > y2) y2 = y;
        if (x === 0 || y === 0 || x === w - 1 || y === h - 1) edge = true;
        if (x > 0 && bin[p - 1] && !seen[p - 1]) { seen[p - 1] = 1; stack[sp++] = p - 1; }
        if (x < w - 1 && bin[p + 1] && !seen[p + 1]) { seen[p + 1] = 1; stack[sp++] = p + 1; }
        if (y > 0 && bin[p - w] && !seen[p - w]) { seen[p - w] = 1; stack[sp++] = p - w; }
        if (y < h - 1 && bin[p + w] && !seen[p + w]) { seen[p + w] = 1; stack[sp++] = p + w; }
      }
      if (edge || area < minA || area > maxA) continue;
      const bw = x2 - x1 + 1, bh = y2 - y1 + 1, asp = bw / bh, fill = area / (bw * bh);
      if (asp < 0.7 || asp > 1.43 || fill < 0.8) continue;
      out.push({ area, cx: sx / area, cy: sy / area, bw, bh });
    }
    return out;
  }

  function pickMarkers(cands) {
    cands.sort((a, b) => b.area - a.area);
    const top = cands.slice(0, 9); let best = null;
    for (let a = 0; a < top.length; a++) for (let b = a + 1; b < top.length; b++) for (let c = b + 1; c < top.length; c++) for (let d = c + 1; d < top.length; d++) {
      const four = [top[a], top[b], top[c], top[d]];
      const big = four.reduce((m, x) => (x.area > m.area ? x : m)), others = four.filter((x) => x !== big);
      const avg = others.reduce((t, x) => t + x.area, 0) / 3;
      if (others.some((x) => x.area > avg * 1.4 || x.area < avg * 0.6)) continue;
      const ratio = big.area / avg; if (ratio < 1.3 || ratio > 2.8) continue;
      const mx = four.reduce((t, x) => t + x.cx, 0) / 4, my = four.reduce((t, x) => t + x.cy, 0) / 4;
      const ang = (p) => Math.atan2(p.cy - my, p.cx - mx);
      const ord = four.slice().sort((p, q) => ang(p) - ang(q));       // clockwise on screen
      const k = ord.indexOf(big);
      const seq = [ord[k], ord[(k + 1) % 4], ord[(k + 2) % 4], ord[(k + 3) % 4]];   // BR, BL, TL, TR
      const dx1 = seq[1].cx - seq[2].cx, dy1 = seq[1].cy - seq[2].cy, dx2 = seq[0].cx - seq[3].cx, dy2 = seq[0].cy - seq[3].cy;   // BL-TL vs BR-TR
      const dx3 = seq[3].cx - seq[2].cx, dy3 = seq[3].cy - seq[2].cy, dx4 = seq[0].cx - seq[1].cx, dy4 = seq[0].cy - seq[1].cy;   // TR-TL vs BR-BL
      const err = (Math.hypot(dx1 - dx2, dy1 - dy2) + Math.hypot(dx3 - dx4, dy3 - dy4)) / (Math.hypot(dx1, dy1) + Math.hypot(dx3, dy3));
      const sheetAspect = Math.hypot(dx3, dy3) / Math.hypot(dx1, dy1);          // width / height should be about 172/228 = 0.754
      if (sheetAspect < 0.4 || sheetAspect > 1.2) continue;
      const score = err + Math.abs(sheetAspect - 0.754) * 0.5;
      if (!best || score < best.score) best = { score, seq };
    }
    if (!best || best.score > 0.35) return null;
    const [br, bl, tl, tr] = best.seq;
    return { tl, tr, bl, br };
  }

  function read(imgData, opt) {
    const { nQ, optCount } = opt;
    const { g, w, h } = toGray(imgData, 4000);
    const bin = binarize(g, w, h);
    const mk = pickMarkers(blobs(bin, w, h));
    if (!mk) return { ok: false, reason: 'markers' };
    const src = [[MARK.tl[0], MARK.tl[1]], [MARK.tr[0], MARK.tr[1]], [MARK.bl[0], MARK.bl[1]], [MARK.br[0], MARK.br[1]]];
    const dst = [[mk.tl.cx, mk.tl.cy], [mk.tr.cx, mk.tr.cy], [mk.bl.cx, mk.bl.cy], [mk.br.cx, mk.br.cy]];
    const map = homography(src, dst); if (!map) return { ok: false, reason: 'markers' };
    const pxPerMm = Math.hypot(dst[1][0] - dst[0][0], dst[1][1] - dst[0][1]) / (MARK.tr[0] - MARK.tl[0]);
    const darkness = (x, y, rad) => {
      let n = 0, d = 0; const step = 0.45;
      for (let yy = -rad; yy <= rad + 1e-9; yy += step) for (let xx = -rad; xx <= rad + 1e-9; xx += step) {
        if (xx * xx + yy * yy > rad * rad) continue;
        const [px, py] = map(x + xx, y + yy), ix = Math.round(px), iy = Math.round(py);
        n++; if (ix >= 0 && iy >= 0 && ix < w && iy < h && bin[iy * w + ix]) d++;
      }
      return n ? d / n : 0;
    };
    const code = parseBits(layout(1, 4, 1).code.map(([x, y]) => (darkness(x, y, 1.0) > 0.5 ? 1 : 0)));
    if (!code) return { ok: false, reason: 'code', map, w, h, pxPerMm };
    const L = layout(nQ, optCount, code.idDigits);
    const decide = (vals) => {
      const marked = vals.map((v, i) => [v, i]).filter(([v]) => v >= 0.3).sort((a, b) => b[0] - a[0]);
      if (!marked.length) return { sel: null, flag: 'blank' };
      if (marked.length === 1) return { sel: marked[0][1], flag: marked[0][0] < 0.45 ? 'light' : 'ok' };
      if (marked[0][0] >= 0.55 && marked[0][0] - marked[1][0] >= 0.25) return { sel: marked[0][1], flag: 'unsure' };
      return { sel: null, flag: 'multi' };
    };
    const answers = L.q.map((r) => { const s = r.bubbles.map(([x, y]) => darkness(x, y, R_READ)); return { ...decide(s), s }; });
    const idCols = L.id.map((col) => { const s = col.map(([x, y]) => darkness(x, y, R_READ)); return { ...decide(s), s }; });
    const sid = idCols.map((c) => (c.sel == null ? '?' : String(c.sel))).join('');
    return { ok: true, testId: code.testId, grouped: code.grouped, idDigits: code.idDigits, studentId: sid, idCols, answers, layout: L, map, w, h, pxPerMm };
  }

  // Run on an <img>/<canvas>/<video>: scale to a working size and read it. Tries the 4 right-angle turns too.
  function scan(source, opt) {
    const sw = source.naturalWidth || source.videoWidth || source.width, sh = source.naturalHeight || source.videoHeight || source.height;
    const sc = Math.min(1, 1800 / Math.max(sw, sh));
    const cv = document.createElement('canvas'); cv.width = Math.round(sw * sc); cv.height = Math.round(sh * sc);
    const ctx = cv.getContext('2d', { willReadFrequently: true }); ctx.drawImage(source, 0, 0, cv.width, cv.height);
    const res = read(ctx.getImageData(0, 0, cv.width, cv.height), opt);
    res.canvas = cv;
    return res;
  }

  window.OMR = { W, H, MAX_Q, layout, codeBits, parseBits, mcqOrder, sheetEl, scan, read, R_BUB, R_READ, KH_LET, LAT_LET };
})();
