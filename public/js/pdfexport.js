/* "Download PDF" without the print dialog: the rendered paper is cut into real A4 pages (header and footer on every
   page, page numbers), each page is drawn to an image and the images are put into a PDF. Runs entirely in the
   browser, so it uses the fonts installed on this computer (Khmer OS Battambang, Khmer M1, Mathcad UniMath). */
(function () {
  const MM = 96 / 25.4;
  const KEEP_NEXT = /(^|\s)(p-part|pt-sec|pt-lvl|pt-note|ptk-h|ptk-banner|pt-title|ans-title|ptk-title)(\s|$)/;
  const SPLIT = /(^|\s)(ans-cols|ptk-cols)(\s|$)/;
  const KH = ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩'];
  const kh = (n) => String(n).replace(/\d/g, (d) => KH[d]);

  function loadScript(src) {
    return new Promise((ok, bad) => {
      if (document.querySelector(`script[data-lib="${src}"]`)) return ok();
      const s = document.createElement('script'); s.src = src; s.dataset.lib = src; s.onload = ok; s.onerror = () => bad(new Error('មិនអាចផ្ទុក ' + src));
      document.head.append(s);
    });
  }

  function spec(sheet) {
    const c = sheet.classList;
    if (c.contains('answers-doc')) return { cls: 'answers-doc', top: 20, bottom: 15, side: 15, num: 'khmer' };
    if (c.contains('ptkey-doc')) return { cls: 'ptkey-doc', top: 20, bottom: 15, side: 15, num: 'latin' };
    if (c.contains('pt-doc')) return { cls: 'pt-doc', top: 26, bottom: 15, side: 15, header: '.pt-ph', footer: '.pt-pf-screen' };
    return { cls: '', top: 32, bottom: 20, side: 15, header: '.ph', footer: '.pf' };
  }
  const kidsOf = (sheet, sp) => (sp.header ? [...sheet.querySelector('.flow tbody td').children] : [...sheet.children]);

  function paginate(sheet, host) {
    const sp = spec(sheet);
    const pages = [];
    const cap = (sp.top + sp.bottom);
    const newPage = () => {
      const page = document.createElement('div');
      page.className = `pdf-page sheet-fonts ${sp.cls}`;
      const body = document.createElement('div'); body.className = 'pdf-body';
      body.style.cssText = `top:${sp.top}mm;bottom:${sp.bottom}mm;left:${sp.side}mm;right:${sp.side}mm;`;
      page.append(body);
      host.append(page); pages.push({ page, body });
      return pages[pages.length - 1];
    };
    const over = (b) => b.scrollHeight > b.clientHeight + 1;
    let cur = newPage();
    const breakBefore = () => {
      // keep headings together with what follows them
      const tail = [];
      while (cur.body.children.length > 1 && KEEP_NEXT.test(cur.body.lastElementChild.className)) tail.unshift(cur.body.lastElementChild), cur.body.lastElementChild.remove();
      cur = newPage(); tail.forEach((t) => cur.body.append(t));
    };
    let force = false;
    for (const kid of kidsOf(sheet, sp)) {
      if (kid.classList.contains('pt-break')) { force = true; continue; }
      if (force && cur.body.children.length) { cur = newPage(); }
      force = false;
      if (SPLIT.test(kid.className)) {
        let box = kid.cloneNode(false); cur.body.append(box);
        for (const item of [...kid.children]) {
          const copy = item.cloneNode(true); box.append(copy);
          if (over(cur.body) && (box.children.length > 1 || cur.body.children.length > 1)) {
            copy.remove();
            if (!box.children.length) box.remove();
            breakBefore();
            box = kid.cloneNode(false); cur.body.append(box); box.append(copy);
          }
        }
        continue;
      }
      const copy = kid.cloneNode(true); cur.body.append(copy);
      if (over(cur.body) && cur.body.children.length > 1) { copy.remove(); breakBefore(); cur.body.append(copy); }
    }
    // header / footer / numbers on every page
    const n = pages.length;
    pages.forEach(({ page }, i) => {
      if (sp.header) {
        const hd = sheet.querySelector(`:scope > ${sp.header}`).cloneNode(true); hd.classList.add('pdf-hdr'); hd.style.left = hd.style.right = `${sp.side}mm`; page.append(hd);
        const ft = sheet.querySelector(`:scope > ${sp.footer}`).cloneNode(true); ft.classList.add('pdf-ftr'); ft.style.left = ft.style.right = `${sp.side}mm`;
        const pg = ft.querySelector('.pg');
        if (pg) pg.textContent = String(i + 1);
        else { const s = document.createElement('span'); s.textContent = `ទំព័រ ${kh(i + 1)}/${kh(n)}`; ft.append(s); }
        page.append(ft);
      } else {
        const ft = document.createElement('div'); ft.className = 'pdf-ftr pdf-num'; ft.textContent = sp.num === 'khmer' ? kh(i + 1) : String(i + 1); page.append(ft);
      }
    });
    return pages.map((p) => p.page);
  }

  async function download({ sheet, title, onProgress, ready }) {
    if (ready) await ready;
    await Promise.all([loadScript('js/html2canvas.min.js'), loadScript('js/jspdf.umd.min.js')]);
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    const host = document.createElement('div'); host.className = 'pdf-host'; document.body.append(host);
    try {
      const pages = paginate(sheet, host);
      await new Promise((r) => setTimeout(r, 150));   // let images / fonts settle
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF({ unit: 'mm', format: 'a4', compress: true });
      for (let i = 0; i < pages.length; i++) {
        if (onProgress) onProgress(i + 1, pages.length);
        const canvas = await window.html2canvas(pages[i], { scale: 2.2, backgroundColor: '#ffffff', useCORS: true, logging: false, windowWidth: Math.ceil(210 * MM) + 20 });
        if (i) pdf.addPage('a4', 'portrait');
        pdf.addImage(canvas.toDataURL('image/jpeg', 0.92), 'JPEG', 0, 0, 210, 297, undefined, 'FAST');
        canvas.width = canvas.height = 0;
        await new Promise((r) => setTimeout(r, 0));
      }
      const name = String(title || 'វិញ្ញាសា').replace(/[\\/:*?"<>|]+/g, ' ').trim().slice(0, 80) || 'exam';
      pdf.save(`${name}.pdf`);
      return pages.length;
    } finally { host.remove(); }
  }
  window.PdfExport = { download, paginate };
})();
