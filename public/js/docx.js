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
  // `ref` is either an uploaded-image key or a site path such as /ngs.png
  async function rasterize(ref) {
    const res = await fetch(String(ref).startsWith('/') ? ref : `/api/images/${ref}`); const blob = await res.blob();
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

  // template fonts (installed on the teacher's computer; Word substitutes if missing)
  const FT = { title: 'Khmer M1', head: 'Khmer OS Bokor' };
  const rprF = (cs, o = {}) => rpr(o).replace(`w:cs="${FONT_KH}"`, `w:cs="${cs}"`);
  const runF = (cs, text, o = {}) => run(text, o).replace(new RegExp(`w:cs="${FONT_KH}"`, 'g'), `w:cs="${cs}"`);
  const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV'];
  const NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"';
  const XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';

  // "ក) …" lines become indented sub-questions, like the NGS template
  function splitWriting(stem) {
    const intro = []; const subs = [];
    for (const line of String(stem).split('\n')) {
      const m = line.match(/^\s*([ក-ឃង-ច])\s*[\)\.]\s*(.*)$/);
      if (m) subs.push({ l: m[1], t: m[2] }); else if (subs.length) subs[subs.length - 1].t += `\n${line}`; else intro.push(line);
    }
    return { intro: intro.join('\n').trim(), subs };
  }

  async function build(test, opts = {}) {
    const minutes = opts.minutes || 70;
    const prof = opts.profile || {};
    const mcq = test.questions.filter((q) => q.kind !== 'writing');
    const writing = test.questions.filter((q) => q.kind === 'writing');
    const mcqPts = mcq.reduce((a, q) => a + q.points, 0), wPts = writing.reduce((a, q) => a + q.points, 0);
    const hasKey = mcq.every((q) => q.correct_index != null);
    const answers = !!(opts.answers || opts.showKey) && hasKey;
    const rast = opts.rasterize || rasterize;

    // pictures used in the body, plus the logo for the exam header
    const media = []; const images = {}; let imgNo = 0;
    const load = async (ref) => {
      if (images[ref]) return images[ref];
      try { const r = await rast(ref); imgNo += 1; images[ref] = { rid: `rIdImg${imgNo}`, n: imgNo, ...r }; media.push({ name: `word/media/image${imgNo}.png`, data: r.data }); return images[ref]; } catch { return null; }
    };
    if (!answers) for (const k of new Set(test.questions.map((q) => q.image_key).filter(Boolean))) await load(k);
    const logo = !answers && prof.logo ? await load(prof.logo) : null;
    const pic = (key) => {
      const im = images[key]; if (!im) return '';
      const maxW = 9.5 * 360000, maxH = 7 * 360000; let wE = im.w * 9525, hE = im.h * 9525;
      const f = Math.min(1, maxW / wE, maxH / hE); wE = Math.round(wE * f); hE = Math.round(hE * f);
      return para(image(im.rid, wE, hE, im.n), { left: 1871, after: 80 });
    };

    const body = []; const extra = []; let sect;
    const PAGE = '<w:pgSz w:w="11906" w:h="16838"/>';
    const year = kh(new Date().getFullYear());

    if (!answers) {
      // ----- exam paper -----
      body.push(P(test.title, { b: 1, sz: 34 }, { align: 'center', before: 80, after: 20 }).replace(`w:cs="${FONT_KH}"`, `w:cs="${FT.title}"`));
      if (opts.date) body.push(para(runF(FT.title, `សម័យប្រឡង ${opts.date}`, { b: 1, sz: 30 }), { align: 'center', after: 20 }));
      body.push(para(runF(FT.title, `វិញ្ញាសា ${prof.subject || 'គណិតវិទ្យា'}`, { b: 1, sz: 30 }), { align: 'center', after: 60 }));
      body.push(P(`រយៈពេល៖ ${kh(minutes)} នាទី        ពិន្ទុសរុប៖ ${kh(mcqPts + wPts)} ពិន្ទុ`, { sz: 24 }, { align: 'center', after: 100 }));
      body.push(P('ឈ្មោះ៖ ..............................................      ថ្នាក់៖ ................      លេខ៖ ................', { sz: 24 }, { before: 40, after: 100 }));
      body.push(P(`សូមអានសំណួរឱ្យបានល្អិតល្អន់។ ${mcq.length ? `ផ្នែក ក ជ្រើសរើសចម្លើយត្រឹមត្រូវ (${kh(mcqPts)} ពិន្ទុ)។ ` : ''}${writing.length ? `ផ្នែក ខ សរសេរចម្លើយលើក្រដាសឆ្លើយ ដោយបង្ហាញវិធីដោះស្រាយ (${kh(wPts)} ពិន្ទុ)។ ` : ''}មិនអនុញ្ញាតឱ្យប្រើទូរស័ព្ទ ឬម៉ាស៊ីនគណនាទេ។`, { sz: 23 }, { box: 1, after: 140 }));

      if (mcq.length) {
        body.push(para(run('ផ្នែក ក · ពហុជ្រើសរើស ', { b: 1, sz: 28 }) + run(`(${kh(mcq.length)} សំណួរ × ${kh(mcq[0].points)} ពិន្ទុ)`, { sz: 23 }), { underline: true, before: 100, after: 100, keep: 1 }));
        mcq.forEach((q, i) => {
          body.push(para(run(`${kh(i + 1)}.\t`, { b: 1 }) + run(q.stem_text), { left: 567, hanging: 567, tabs: [567], before: 60, after: 40, keep: 1 }));
          if (q.image_key) body.push(pic(q.image_key).replace('w:left="1871"', 'w:left="567"'));
          const short = q.options.every((o) => o.length <= 14);
          if (short) body.push(para(q.options.map((o, j) => (j ? tab() : '') + run(`${LET[j]}. `, { b: 1 }) + run(o)).join(''), { left: 567, tabs: [2400, 4200, 6000, 7800], after: 100 }));
          else { q.options.forEach((o, j) => body.push(para(run(`${LET[j]}. `, { b: 1 }) + run(o), { left: 1134, hanging: 567, after: 20 }))); body.push(P('', {}, { after: 60 })); }
        });
      }
      if (writing.length) {
        body.push(para(run('ផ្នែក ខ · សរសេរ ', { b: 1, sz: 28 }) + run(`(${kh(writing.length)} សំណួរ · ${kh(wPts)} ពិន្ទុ)`, { sz: 23 }), { underline: true, before: 200, after: 100, keep: 1 }));
        writing.forEach((q, i) => {
          const { intro, subs } = splitWriting(q.stem_text);
          // I.  (១០ពិន្ទុ)  question — Roman numeral, bold score, hanging text (NGS template)
          body.push(para(run(`${ROMAN[i] || i + 1}.`, { b: 1 }) + tab() + run(`(${kh(q.points)}ពិន្ទុ)`, { b: 1 }) + tab() + run(intro || (subs.length ? '' : q.stem_text)), { left: 1871, hanging: 1871, tabs: [680, 1871], before: 100, after: 30, keep: 1 }));
          subs.forEach((sq) => body.push(para(run(`${sq.l}.`) + tab() + run(sq.t), { left: 2381, hanging: 510, tabs: [2381], after: 20 })));
          if (q.image_key) body.push(pic(q.image_key));
          if (opts.space !== false) for (let n = 0; n < Math.min(12, Math.max(3, Math.round(q.points / 1.5))); n++) body.push(P('', {}, { after: 160 }));
        });
      }
      // header (logo + school | website, facebook) and footer (teacher | email | telegram | tel), as in the template
      const hRight = [prof.website && `Website: ${prof.website}`, prof.facebook && `Facebook: ${prof.facebook}`].filter(Boolean);
      const leftCell = (logo ? para(image(logo.rid, 468000, 468000, 900) + runF(FT.head, `  ${prof.school || ''}`, { sz: 25 }), { after: 0 }) : para(runF(FT.head, prof.school || '', { sz: 25 }), { after: 0 }));
      const rightCell = hRight.length ? hRight.map((l) => P(l, { sz: 20, i: 1 }, { align: 'right', after: 0 })).join('') : P('', {}, { after: 0 });
      const hdr = `${XML}<w:hdr ${NS}>${table([cell(leftCell, 5800) + cell(rightCell, 4518)], { width: 10318, grid: [5800, 4518] })}${para('', { underline: true, after: 60 })}</w:hdr>`;
      const fparts = [prof.teacher, prof.email && `Email: ${prof.email}`, prof.telegram && `Telegram: ${prof.telegram}`, prof.tel && `Tel: ${prof.tel}`].filter(Boolean);
      const ftr = `${XML}<w:ftr ${NS}><w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="10" w:space="4" w:color="000000"/></w:pBdr><w:tabs><w:tab w:val="left" w:pos="2700"/><w:tab w:val="center" w:pos="6700"/><w:tab w:val="right" w:pos="10318"/></w:tabs><w:spacing w:before="0" w:after="0"/></w:pPr>${fparts.map((t, i) => (i ? tab() : '') + (i === 0 && prof.teacher ? runF(FT.head, t, { sz: 17 }) : run(t, { sz: 17, i: 1 }))).join('')}</w:p></w:ftr>`;
      extra.push({ name: 'word/header1.xml', data: hdr }, { name: 'word/footer1.xml', data: ftr });
      sect = `<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr"/><w:footerReference w:type="default" r:id="rIdFtr"/>${PAGE}<w:pgMar w:top="1700" w:right="794" w:bottom="1134" w:left="794" w:header="454" w:footer="340" w:gutter="0"/></w:sectPr>`;
    } else {
      // ----- answer sheet (អត្រាកំណែ): school block, centred title, two columns, boxed conclusions -----
      const head = (l, r) => `<w:tr>${cell(P(l, { b: 1, sz: 24 }, { after: 0 }), 5200)}${cell(P(r, { b: 1, sz: 24 }, { align: 'right', after: 0 }), 4800)}</w:tr>`;
      body.push(`<w:tbl><w:tblPr><w:tblW w:w="10000" w:type="dxa"/></w:tblPr><w:tblGrid><w:gridCol w:w="5200"/><w:gridCol w:w="4800"/></w:tblGrid>${head(prof.school || '', `${prof.group || 'ក្រុមគ្រូគណិតវិទ្យា'} ឆ្នាំ ${year}`)}${head(`មុខវិជ្ជា៖ ${prof.subject || 'គណិតវិទ្យា'}`, `រយៈពេល៖ ${kh(minutes)} នាទី (ពិន្ទុ៖ ${kh(mcqPts + wPts)})`)}</w:tbl>`);
      body.push(para(runF(FT.title, 'អត្រាកំណែ', { b: 1, sz: 34 }), { align: 'center', before: 120, after: 0 }));
      body.push(para(runF(FT.title, `វិញ្ញាសា៖ ${prof.subject || 'គណិតវិទ្យា'}`, { b: 1, sz: 30 }), { align: 'center', after: 0 }));
      // the last paragraph of the one-column part carries the section break (the rest of the sheet is two columns)
      body.push(P(test.title, { sz: 22 }, { align: 'center', after: 120 }).replace('</w:pPr>', `<w:sectPr><w:footerReference w:type="default" r:id="rIdFtr"/>${PAGE}<w:pgMar w:top="1020" w:right="794" w:bottom="1000" w:left="794" w:header="454" w:footer="400" w:gutter="0"/></w:sectPr></w:pPr>`));
      if (mcq.length) {
        body.push(para(run(`ផ្នែក ក · ពហុជ្រើសរើស (${kh(mcqPts)}ពិន្ទុ)`, { b: 1, sz: 24 }), { before: 60, after: 40, keep: 1 }));
        const rows = []; const per = 5;
        for (let i = 0; i < mcq.length; i += per) rows.push(mcq.slice(i, i + per).map((q, k) => cell(P(`${kh(i + k + 1)}. ${LET[q.correct_index]}${q.alt_correct_index != null ? `/${LET[q.alt_correct_index]}` : ''}`, { b: 1, sz: 22 }, { align: 'center', after: 0 }), 950, { border: 1 })).join(''));
        body.push(table(rows, { border: 1, width: 4750, grid: Array(per).fill(950) }));
        body.push(P('', {}, { after: 80 }));
      }
      writing.forEach((q, i) => {
        body.push(para(run(`លំហាត់ទី${kh(i + 1)} (${kh(q.points)}ពិន្ទុ)`, { b: 1, sz: 24 }), { before: 100, after: 30, keep: 1 }));
        String(q.solution_text || '(មិនទាន់មានចម្លើយគំរូ)').split('\n').forEach((ln) => {
          if (/^\s*ដូចនេះ/.test(ln)) { body.push(para(run(ln.trim(), { sz: 22 }), { box: 1, align: 'center', before: 40, after: 80 })); return; }
          const m = ln.match(/^\s*([ក-ឃង-ច])\s*[\)\.]\s*(.*)$/);
          body.push(para((m ? run(`${m[1]}. `, { b: 1, sz: 22 }) : '') + run(m ? m[2] : ln, { sz: 22 }), { after: 40 }));
        });
      });
      const ftr = `${XML}<w:ftr ${NS}><w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="center"/></w:pPr><w:r>${rpr({ sz: 22 })}<w:fldChar w:fldCharType="begin"/></w:r><w:r>${rpr({ sz: 22 })}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r>${rpr({ sz: 22 })}<w:fldChar w:fldCharType="separate"/></w:r><w:r>${rpr({ sz: 22 })}<w:t>1</w:t></w:r><w:r>${rpr({ sz: 22 })}<w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>`;
      extra.push({ name: 'word/footer1.xml', data: ftr });
      sect = `<w:sectPr><w:footerReference w:type="default" r:id="rIdFtr"/><w:type w:val="continuous"/>${PAGE}<w:pgMar w:top="1020" w:right="794" w:bottom="1000" w:left="794" w:header="454" w:footer="400" w:gutter="0"/><w:cols w:num="2" w:space="510"/></w:sectPr>`;
    }

    const documentXml = `${XML}<w:document ${NS}><w:body>${body.join('')}${sect}</w:body></w:document>`;
    const stylesXml = `${XML}<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="${FONT_KH}"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:lang w:val="en-US" w:bidi="km-KH"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style></w:styles>`;
    const REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';
    const imgRel = (im) => `<Relationship Id="${im.rid}" Type="${REL}/image" Target="media/image${im.n}.png"/>`;
    const docRels = `${XML}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="${REL}/styles" Target="styles.xml"/>${answers ? '' : `<Relationship Id="rIdHdr" Type="${REL}/header" Target="header1.xml"/>`}<Relationship Id="rIdFtr" Type="${REL}/footer" Target="footer1.xml"/>${Object.entries(images).filter(([k]) => !logo || k !== prof.logo).map(([, im]) => imgRel(im)).join('')}</Relationships>`;
    const enc = new TextEncoder();
    const files = [
      { name: '[Content_Types].xml', data: enc.encode(`${XML}<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>${answers ? '' : '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'}<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>`) },
      { name: '_rels/.rels', data: enc.encode(`${XML}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${REL}/officeDocument" Target="word/document.xml"/></Relationships>`) },
      { name: 'word/document.xml', data: enc.encode(documentXml) },
      { name: 'word/styles.xml', data: enc.encode(stylesXml) },
      { name: 'word/_rels/document.xml.rels', data: enc.encode(docRels) },
      ...extra.map((e) => ({ name: e.name, data: enc.encode(e.data) })),
      ...(logo ? [{ name: 'word/_rels/header1.xml.rels', data: enc.encode(`${XML}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${imgRel(logo)}</Relationships>`) }] : []),
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
      a.download = `${String(test.title).replace(/[\\/:*?"<>|]/g, '_').slice(0, 80)}${opts.answers ? ' (អត្រាកំណែ)' : ''}.docx`;
      document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 5000);
    },
  };
  if (typeof window !== 'undefined') window.ExamDocx = api;
  if (typeof module !== 'undefined') module.exports = api;
})();
