// Builds a Word (.docx) exam paper in the browser, no library needed.
//  - Khmer text stays Khmer (complex-script font set per run)
//  - math is left exactly as typed, i.e. LaTeX like \(\dfrac{3}{4}\), so it can be pasted into MathType / Overleaf
//  - pictures are embedded as PNG
(function () {
  const KH = '០១២៣៤៥៦៧៨៩';
  const kh = (n) => String(n).replace(/\d/g, (d) => KH[d]);
  const LET = ['ក', 'ខ', 'គ', 'ឃ', 'ង', 'ច'];
  const FONT_KH = 'Khmer OS Battambang';
  const esc = (s) => String(s == null ? '' : s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // ---------- tiny ZIP writer (stored, no compression) ----------
  const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  const crc32 = (b) => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
  function zip(files) {                       // files: [{name, data: Uint8Array}]
    const enc = new TextEncoder(); const parts = []; const central = []; let offset = 0;
    const u16 = (v) => [v & 255, (v >> 8) & 255]; const u32 = (v) => [v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >>> 24) & 255];
    for (const f of files) {
      const name = enc.encode(f.name); const crc = crc32(f.data); const size = f.data.length;
      const head = new Uint8Array([0x50, 0x4B, 3, 4, ...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0x21), ...u32(crc), ...u32(size), ...u32(size), ...u16(name.length), ...u16(0)]);
      parts.push(head, name, f.data);
      central.push(new Uint8Array([0x50, 0x4B, 1, 2, ...u16(20), ...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0x21), ...u32(crc), ...u32(size), ...u32(size), ...u16(name.length), ...u16(0), ...u16(0), ...u16(0), ...u16(0), ...u32(0), ...u32(offset)]), name);
      offset += head.length + name.length + size;
    }
    const cdSize = central.reduce((t, p) => t + p.length, 0);
    const end = new Uint8Array([0x50, 0x4B, 5, 6, 0, 0, 0, 0, ...u16(files.length), ...u16(files.length), ...u32(cdSize), ...u32(offset), 0, 0]);
    const all = [...parts, ...central, end]; const out = new Uint8Array(all.reduce((t, p) => t + p.length, 0)); let o = 0;
    for (const p of all) { out.set(p, o); o += p.length; }
    return out;
  }

  // ---------- WordprocessingML helpers ----------
  // size in half-points; every run carries Latin AND complex-script (Khmer) fonts/sizes
  const rpr = (o = {}) => `<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="${FONT_KH}"/>${o.b ? '<w:b/><w:bCs/>' : ''}${o.i ? '<w:i/><w:iCs/>' : ''}<w:sz w:val="${o.sz || 26}"/><w:szCs w:val="${o.sz || 26}"/><w:lang w:val="en-US" w:bidi="km-KH"/></w:rPr>`;
  const run = (text, o = {}) => {
    const lines = String(text).split('\n');
    return `<w:r>${rpr(o)}${lines.map((l, i) => `${i ? '<w:br/>' : ''}<w:t xml:space="preserve">${esc(l)}</w:t>`).join('')}</w:r>`;
  };
  const tab = (o = {}) => `<w:r>${rpr(o)}<w:tab/></w:r>`;
  function para(content, o = {}) {
    const ind = o.left != null || o.hanging != null ? `<w:ind w:left="${o.left || 0}"${o.hanging ? ` w:hanging="${o.hanging}"` : ''}/>` : '';
    const border = o.box ? '<w:pBdr><w:top w:val="single" w:sz="6" w:space="4" w:color="000000"/><w:left w:val="single" w:sz="6" w:space="4" w:color="000000"/><w:bottom w:val="single" w:sz="6" w:space="4" w:color="000000"/><w:right w:val="single" w:sz="6" w:space="4" w:color="000000"/></w:pBdr>' : o.underline ? '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="2" w:color="000000"/></w:pBdr>' : '';
    const tabs = o.tabs ? `<w:tabs>${o.tabs.map((t) => `<w:tab w:val="left" w:pos="${t}"/>`).join('')}</w:tabs>` : '';
    return `<w:p><w:pPr>${o.keep ? '<w:keepNext/>' : ''}${o.pageBreak ? '<w:pageBreakBefore/>' : ''}${border}${tabs}<w:spacing w:before="${o.before || 0}" w:after="${o.after == null ? 80 : o.after}"/>${ind}<w:jc w:val="${o.align || 'left'}"/></w:pPr>${content}</w:p>`;
  }
  const P = (text, ro = {}, po = {}) => para(run(text, ro), po);
  function image(rid, wEmu, hEmu, id) {
    return `<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="${wEmu}" cy="${hEmu}"/><wp:docPr id="${id}" name="Picture ${id}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="${id}" name="image${id}.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="${rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${wEmu}" cy="${hEmu}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>`;
  }
  const cell = (inner, w, o = {}) => `<w:tc><w:tcPr><w:tcW w:w="${w}" w:type="dxa"/>${o.border ? '<w:tcBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/></w:tcBorders>' : ''}</w:tcPr>${inner}</w:tc>`;
  const table = (rows, o = {}) => `<w:tbl><w:tblPr><w:tblW w:w="${o.width || 9638}" w:type="dxa"/>${o.border ? '<w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders>' : ''}</w:tblPr><w:tblGrid>${(o.grid || []).map((g) => `<w:gridCol w:w="${g}"/>`).join('')}</w:tblGrid>${rows.map((r) => `<w:tr>${r}</w:tr>`).join('')}</w:tbl>`;

  // ---------- picture -> PNG (browser only) ----------
  async function rasterize(key) {
    const res = await fetch(`/api/images/${key}`); const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    try {
      const img = await new Promise((ok, bad) => { const i = new Image(); i.onload = () => ok(i); i.onerror = bad; i.src = url; });
      const w = img.naturalWidth || 400, h = img.naturalHeight || 300, scale = 2;
      const c = document.createElement('canvas'); c.width = w * scale; c.height = h * scale;
      const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
      const png = await new Promise((ok) => c.toBlob(ok, 'image/png'));
      return { data: new Uint8Array(await png.arrayBuffer()), w, h };
    } finally { URL.revokeObjectURL(url); }
  }

  // ---------- the paper ----------
  async function build(test, opts = {}) {
    const minutes = opts.minutes || 70;
    const mcq = test.questions.filter((q) => q.kind !== 'writing');
    const writing = test.questions.filter((q) => q.kind === 'writing');
    const mcqPts = mcq.reduce((a, q) => a + q.points, 0), wPts = writing.reduce((a, q) => a + q.points, 0);
    const hasKey = mcq.every((q) => q.correct_index != null);
    const showKey = !!opts.showKey && hasKey;

    // pictures
    const images = {}; let imgNo = 0; const media = [];
    const keys = [...new Set(test.questions.map((q) => q.image_key).filter(Boolean))];
    for (const k of keys) {
      try { const r = opts.rasterize ? await opts.rasterize(k) : await rasterize(k); imgNo += 1; images[k] = { rid: `rIdImg${imgNo}`, n: imgNo, ...r }; media.push({ name: `word/media/image${imgNo}.png`, data: r.data }); } catch { /* skip a picture that cannot be read */ }
    }
    const pic = (key) => {
      const im = images[key]; if (!im) return '';
      const maxW = 9.5 * 360000, maxH = 7 * 360000; let wE = im.w * 9525, hE = im.h * 9525;      // 96 dpi -> EMU
      const f = Math.min(1, maxW / wE, maxH / hE); wE = Math.round(wE * f); hE = Math.round(hE * f);
      return para(image(im.rid, wE, hE, im.n), { left: 567, after: 80 });
    };

    const body = [];
    // header: two columns, no borders
    const head = (lines, align) => lines.map((l) => P(l, { sz: 24 }, { align, after: 0 })).join('');
    body.push(table([
      cell(head(['ក្រសួងអប់រំ យុវជន និងកីឡា', 'វិទ្យាល័យព្រះស៊ីសុវត្ថិ', 'សាលារៀនជំនាន់ថ្មី (NGS)'], 'center'), 4800) + cell(head(['ព្រះរាជាណាចក្រកម្ពុជា', 'ជាតិ សាសនា ព្រះមហាក្សត្រ'], 'center'), 4838),
    ], { grid: [4800, 4838] }));
    body.push(P(test.title, { b: 1, sz: 34 }, { align: 'center', before: 160, after: 60 }));
    body.push(P(`មុខវិជ្ជា៖ គណិតវិទ្យា        រយៈពេល៖ ${kh(minutes)} នាទី        ពិន្ទុសរុប៖ ${kh(mcqPts + wPts)} ពិន្ទុ${opts.date ? `        ${opts.date}` : ''}`, { sz: 25 }, { align: 'center', after: 120, underline: true }));
    body.push(P('ឈ្មោះ៖ ..............................................      ថ្នាក់៖ ................      លេខ៖ ................', { sz: 25 }, { before: 80, after: 120 }));
    body.push(P(`សូមអានសំណួរឱ្យបានល្អិតល្អន់។ ផ្នែក ក ជ្រើសរើសចម្លើយត្រឹមត្រូវ (${kh(mcqPts)} ពិន្ទុ)។ ផ្នែក ខ សរសេរចម្លើយលើក្រដាសឆ្លើយ ដោយបង្ហាញវិធីដោះស្រាយ (${kh(wPts)} ពិន្ទុ)។ មិនអនុញ្ញាតឱ្យប្រើទូរស័ព្ទ ឬម៉ាស៊ីនគណនាទេ។`, { sz: 24 }, { box: 1, after: 160 }));

    if (mcq.length) {
      body.push(para(run('ផ្នែក ក · ពហុជ្រើសរើស ', { b: 1, sz: 30 }) + run(`(${kh(mcq.length)} សំណួរ × ${kh(mcq[0].points)} ពិន្ទុ)`, { sz: 24 }), { underline: true, before: 120, after: 100, keep: 1 }));
      mcq.forEach((q, i) => {
        body.push(para(run(`${kh(i + 1)}.\t`, { b: 1 }) + run(q.stem_text), { left: 567, hanging: 567, tabs: [567], before: 60, after: 40, keep: 1 }));
        if (q.image_key) body.push(pic(q.image_key));
        const short = q.options.every((o) => o.length <= 14);
        if (short) {
          body.push(para(q.options.map((o, j) => (j ? tab() : '') + run(`${LET[j]}. `, { b: 1 }) + run(o)).join(''), { left: 567, tabs: [2400, 4200, 6000, 7800], after: 100 }));
        } else {
          q.options.forEach((o, j) => body.push(para(run(`${LET[j]}. `, { b: 1 }) + run(o), { left: 1134, hanging: 567, after: 20 })));
          body.push(P('', {}, { after: 60 }));
        }
      });
    }
    if (writing.length) {
      body.push(para(run('ផ្នែក ខ · សរសេរ ', { b: 1, sz: 30 }) + run(`(${kh(writing.length)} សំណួរ · ${kh(wPts)} ពិន្ទុ)`, { sz: 24 }), { underline: true, before: 240, after: 100, keep: 1 }));
      writing.forEach((q, i) => {
        body.push(para(run(`${kh(i + 1)}.\t`, { b: 1 }) + run(q.stem_text) + run(`   (${kh(q.points)} ពិន្ទុ)`, { b: 1, sz: 24 }), { left: 567, hanging: 567, tabs: [567], before: 80, after: 60, keep: 1 }));
        if (q.image_key) body.push(pic(q.image_key));
        if (opts.space !== false) for (let n = 0; n < Math.min(12, Math.max(3, Math.round(q.points / 1.5))); n++) body.push(P('', {}, { after: 160 }));
      });
    }
    if (showKey) {
      body.push(P(`ចម្លើយ — ${test.title}`, { b: 1, sz: 32 }, { align: 'center', pageBreak: 1, after: 160 }));
      if (mcq.length) {
        body.push(P('ផ្នែក ក · ចម្លើយពហុជ្រើសរើស', { b: 1, sz: 28 }, { underline: 1, after: 100 }));
        const rows = []; const per = 10;
        for (let i = 0; i < mcq.length; i += per) {
          const slice = mcq.slice(i, i + per);
          rows.push(slice.map((_, k) => cell(P(kh(i + k + 1), { b: 1, sz: 24 }, { align: 'center', after: 0 }), 960, { border: 1 })).join(''));
          rows.push(slice.map((q) => cell(P(LET[q.correct_index], { sz: 26 }, { align: 'center', after: 0 }), 960, { border: 1 })).join(''));
        }
        body.push(table(rows, { border: 1, width: 9600, grid: Array(10).fill(960) }));
      }
      if (writing.length) {
        body.push(P('ផ្នែក ខ · ចម្លើយ និងការដាក់ពិន្ទុ', { b: 1, sz: 28 }, { underline: 1, before: 240, after: 100 }));
        writing.forEach((q, i) => {
          body.push(para(run(`${kh(i + 1)}. `, { b: 1 }) + run(`(${kh(q.points)} ពិន្ទុ)`, { b: 1, sz: 24 }), { before: 80, after: 20, keep: 1 }));
          body.push(P(q.solution_text || '(មិនទាន់មានចម្លើយគំរូ)', { sz: 24 }, { left: 567, after: 80 }));
        });
      }
    }
    const sect = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>';
    const NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"';
    const documentXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${NS}><w:body>${body.join('')}${sect}</w:body></w:document>`;
    const stylesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="${FONT_KH}"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:lang w:val="en-US" w:bidi="km-KH"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style></w:styles>`;
    const rels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>${Object.values(images).map((im) => `<Relationship Id="${im.rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image${im.n}.png"/>`).join('')}</Relationships>`;
    const enc = new TextEncoder();
    const files = [
      { name: '[Content_Types].xml', data: enc.encode('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>') },
      { name: '_rels/.rels', data: enc.encode('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>') },
      { name: 'word/document.xml', data: enc.encode(documentXml) },
      { name: 'word/styles.xml', data: enc.encode(stylesXml) },
      { name: 'word/_rels/document.xml.rels', data: enc.encode(rels) },
      ...media,
    ];
    return zip(files);
  }

  const api = {
    build,
    async download(test, opts = {}) {
      const bytes = await build(test, opts);
      const blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${String(test.title).replace(/[\\/:*?"<>|]/g, '_').slice(0, 80)}.docx`;
      document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 5000);
    },
  };
  if (typeof window !== 'undefined') window.ExamDocx = api;
  if (typeof module !== 'undefined') module.exports = api;
})();
