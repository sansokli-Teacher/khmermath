// Template 2 ("Pre-test", NGS summer-course style). Receives the helpers it needs from paper.js.
(function () {
  const LAT = ['A', 'B', 'C', 'D', 'E', 'F'];
  const LEVELS = [
    ['easy', 'កម្រិត ១៖ ចំណេះដឹងមូលដ្ឋាន'],
    ['medium', 'កម្រិត ២៖ ការគណនា និងអនុវត្ត'],
    ['hard', 'កម្រិត ៣៖ ការវិភាគ និងដោះស្រាយបញ្ហា'],
    ['pisa', 'កម្រិត ៤៖ បែប PISA'],
  ];
  const visLen = (t) => String(t).replace(/\\[A-Za-z]+/g, 'x').replace(/[\\{}()$^_]/g, '').length;
  const cssStr = (s) => `"${String(s || '').replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/[\r\n]+/g, ' ')}"`;

  // Footer = page-margin boxes (so the red page-number box can count pages): teacher | email | telegram | [page]
  function pageStyle(profile) {
    const left = profile.teacher ? profile.teacher.replace(/^បង្រៀនដោយ/, 'រៀបចំដោយ') : '';
    const center = profile.email ? `Email: ${profile.email}` : '';
    const right = profile.telegram ? `Telegram: ${profile.telegram}` : '';
    const base = "border-top: .8pt solid #000; padding-top: 1.5mm; vertical-align: top; font-size: 10pt;";
    return `@media print { @page pretest { size: A4; margin: 0 15mm 17mm 15mm;
      @bottom-left { content: ${cssStr(left)}; ${base} text-align: left; font-family: 'PaperHead', 'PaperBody', serif; }
      @bottom-center { content: ${cssStr(center)}; ${base} text-align: center; font-family: 'Times New Roman', serif; font-style: italic; }
      @bottom-right { content: ${cssStr(right)}; ${base} text-align: right; padding-right: 3mm; font-family: 'Times New Roman', serif; font-style: italic; }
      @bottom-right-corner { content: counter(page); color: #fff; background: #e00; background-clip: content-box; padding: 3.2mm 12mm 4.6mm 0; text-align: center; vertical-align: top; font: 700 10pt 'Times New Roman', serif; }
    } }`;
  }

  function header(ctx) {
    const { h, profile, logoSrc } = ctx;
    const right = [];
    if (profile.website) right.push(h('div', {}, [h('b', {}, 'Website: '), h('i', {}, profile.website)]));
    if (profile.facebook) right.push(h('div', {}, [h('b', {}, 'Facebook: '), h('i', {}, profile.facebook)]));
    return h('div', { class: 'pt-ph' }, [
      h('div', { class: 'pt-ph-left' }, [logoSrc() ? h('img', { src: logoSrc(), alt: '' }) : null, h('div', {}, profile.school || '')]),
      h('div', { class: 'pt-ph-right' }, right),
    ]);
  }
  function screenFooter(ctx) {
    const { h, profile } = ctx;
    return h('div', { class: 'pt-pf-screen' }, [
      h('span', { class: 't' }, (profile.teacher || '').replace(/^បង្រៀនដោយ/, 'រៀបចំដោយ')),
      profile.email ? h('span', {}, ['Email: ', h('i', {}, profile.email)]) : h('span'),
      h('span', {}, [profile.telegram ? ['Telegram: ', h('i', {}, profile.telegram)] : '', h('span', { class: 'pg' }, '1')]),
    ]);
  }
  function infoGrid(ctx, o, withNo) {
    const { h, kh, mcqPts, wPts } = ctx;
    const f = (label) => h('div', { class: 'f' }, [h('span', {}, label), h('i')]);
    return h('div', { class: 'pt-info' }, [
      f('ឈ្មោះសិស្ស:'), f('ថ្នាក់:'),
      f('កាលបរិច្ឆេទ:'),
      withNo ? f('លេខរៀង:') : h('div', { class: 'f' }, [h('span', {}, `រយៈពេល: ${kh(o.minutes)} នាទី   ពិន្ទុសរុប: ${kh(mcqPts + wPts)} ពិន្ទុ`)]),
    ]);
  }
  const page = (ctx, kids) => ctx.h('table', { class: 'flow' }, [
    ctx.h('thead', {}, ctx.h('tr', {}, ctx.h('td'))), ctx.h('tfoot', {}, ctx.h('tr', {}, ctx.h('td'))), ctx.h('tbody', {}, ctx.h('tr', {}, ctx.h('td', {}, kids))),
  ]);

  function examDoc(ctx, o) {
    const { h, mathEl, kh, mcq, writing, mcqPts, wPts, splitWriting, test } = ctx;
    const kids = [];
    kids.push(h('div', { class: 'pt-title' }, [h('div', { class: 'a' }, test.title), o.subtitle ? h('div', { class: 'b' }, o.subtitle) : null]));
    kids.push(infoGrid(ctx, o, false));
    const bullets = [];
    if (mcq.length) bullets.push(`ផ្នែកទី ១៖ ជ្រើសរើសចម្លើយត្រឹមត្រូវតែមួយ (${kh(mcqPts)} ពិន្ទុ)។`);
    if (writing.length) bullets.push(`ផ្នែកទី ២៖ បង្ហាញវិធីធ្វើ និងសរសេរឯកតាឱ្យបានត្រឹមត្រូវ (${kh(wPts)} ពិន្ទុ)។`);
    bullets.push('ប្រើខ្មៅដៃ ឬប៊ិចពណ៌ខ្មៅ។ កុំគូសលើសពីមួយចម្លើយក្នុងសំណួរនីមួយៗ។');
    kids.push(h('div', { class: 'pt-box' }, [h('b', {}, 'សេចក្ដីណែនាំ៖'), h('ul', {}, bullets.map((b) => h('li', {}, b)))]));

    // multiple choice
    let questions = mcq;
    if (mcq.length) {
      kids.push(h('div', { class: 'pt-sec' }, `ផ្នែកទី ១៖ សំណួរទម្រង់បិទ (${kh(mcqPts)} ពិន្ទុ)`));
      kids.push(h('div', { class: 'pt-note' }, o.omr ? 'សរសេរចម្លើយជា A, B, C, D លើសន្លឹកចម្លើយ។' : 'ជ្រើសរើសចម្លើយត្រឹមត្រូវ ហើយគូសរង្វង់ជុំវិញអក្សរ A, B, C ឬ D។'));
      let n = 0;
      const drawQ = (q) => {
        n += 1;
        const short = q.options.every((x) => visLen(x) <= 16);
        kids.push(h('div', { class: 'pt-q' }, [
          h('div', { class: 'stem' }, [h('span', { class: 'no' }, `${n}.`), mathEl('span', {}, q.stem_text)]),
          q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
          h('div', { class: `pt-opts ${short ? 'four' : 'two'}` }, q.options.map((x, j) => h('div', { class: 'o' }, [h('b', {}, `${LAT[j]}.`), mathEl('span', {}, x)]))),
        ]));
      };
      const tagged = mcq.some((q) => q.level);
      if (o.group && tagged) {
        LEVELS.forEach(([lv, label]) => {
          const grp = mcq.filter((q) => q.level === lv);
          if (!grp.length) return;
          const per = grp[0].points, tot = grp.reduce((a, q) => a + q.points, 0);
          kids.push(h('div', { class: 'pt-lvl' }, `${label} (${kh(grp.length)} សំណួរ, ${kh(per)} ពិន្ទុក្នុង ១ សំណួរ = ${kh(tot)} ពិន្ទុ)`));
          grp.forEach(drawQ);
        });
        mcq.filter((q) => !q.level).forEach(drawQ);
      } else mcq.forEach(drawQ);
    }
    // open questions (stem only; answers go on the ruled pages when the answer sheet is on)
    if (writing.length) {
      kids.push(h('div', { class: 'pt-sec' }, `ផ្នែកទី ២៖ សំណួរទម្រង់បើក (${kh(wPts)} ពិន្ទុ)`));
      kids.push(h('div', { class: 'pt-note' }, 'បង្ហាញវិធីធ្វើឱ្យបានច្បាស់លាស់ ហើយសរសេរឯកតា។'));
      writing.forEach((q, i) => {
        const { intro, subs } = splitWriting(q.stem_text);
        kids.push(h('div', { class: 'pt-wq' }, [
          h('div', { class: 'stem' }, [h('span', { class: 'no' }, `${i + 1}.`), h('span', {}, [mathEl('span', {}, intro || (subs.length ? '' : q.stem_text)), h('span', { class: 'pts' }, `  (${kh(q.points)} ពិន្ទុ)`)])]),
          ...subs.map((s) => h('div', { class: 'sub' }, [h('span', {}, `${s.l}.`), mathEl('span', {}, s.t)])),
          q.image_key ? h('img', { src: `/api/images/${q.image_key}`, alt: '' }) : null,
          !o.omr && o.space ? h('div', { class: 'pt-lines' }, [...Array(Math.min(8, Math.max(3, Math.round(q.points / 2)))).keys()].map(() => h('i'))) : null,
        ]));
      });
    }
    kids.push(h('div', { class: 'pt-end' }, '--- ចប់វិញ្ញាសា ---'));
    kids.push(h('table', { class: 'pt-total' }, h('tbody', {}, [
      mcq.length ? h('tr', {}, [h('td', {}, `ពិន្ទុផ្នែកទី ១ (${kh(mcqPts)})`), h('td')]) : null,
      writing.length ? h('tr', {}, [h('td', {}, `ពិន្ទុផ្នែកទី ២ (${kh(wPts)})`), h('td')]) : null,
      h('tr', {}, [h('td', {}, h('b', {}, `ពិន្ទុសរុបរួម (${kh(mcqPts + wPts)})`)), h('td')]),
    ])));

    // answer sheets for students: OMR bubbles + ruled pages
    if (o.omr) {
      if (mcq.length) {
        kids.push(h('div', { class: 'pt-break' }));
        kids.push(h('div', { class: 'pt-title' }, [h('div', { class: 'a' }, 'សន្លឹកចម្លើយសម្រាប់សិស្ស'), h('div', { class: 'b' }, test.title)]));
        kids.push(infoGrid(ctx, o, true));
        kids.push(h('div', { class: 'pt-sec' }, `ផ្នែកទី ១៖ សន្លឹកចម្លើយ OMR (${kh(mcqPts)} ពិន្ទុ)`));
        kids.push(h('div', { class: 'pt-note' }, 'គូសរង្វង់ឱ្យពេញ និងច្បាស់តែមួយក្នុងមួយសំណួរ។ កុំគូសលើសពីមួយចម្លើយ។'));
        const half = Math.ceil(mcq.length / 2);
        const tbl = (from, to) => h('table', { class: 'pt-omr' }, [
          h('thead', {}, h('tr', {}, [h('th', {}, 'No.'), ...['A', 'B', 'C', 'D'].map((x) => h('th', {}, x))])),
          h('tbody', {}, mcq.slice(from, to).map((_, i) => h('tr', {}, [h('td', { class: 'no' }, String(from + i + 1)), ...[0, 1, 2, 3].map(() => h('td', {}, h('span', { class: 'pt-bub' })))]))),
        ]);
        kids.push(h('div', { class: 'pt-omr-frame' }, [tbl(0, half), mcq.length > half ? tbl(half, mcq.length) : null, h('span', { class: 'c2', style: 'top:-1px;' }), h('span', { class: 'c2', style: 'bottom:-1px;' })]));
        kids.push(h('div', { class: 'pt-score-line' }, `ពិន្ទុផ្នែកទី ១: ________/${kh(mcqPts)}`));
      }
      if (writing.length) {
        kids.push(h('div', { class: 'pt-break' }));
        kids.push(h('div', { class: 'pt-title' }, [h('div', { class: 'a' }, 'សន្លឹកចម្លើយសម្រាប់សិស្ស'), h('div', { class: 'b' }, `ផ្នែកទី ២: ការអនុវត្ត និងហេតុផល (${kh(wPts)} ពិន្ទុ)`)]));
        kids.push(infoGrid(ctx, o, true));
        kids.push(h('div', { class: 'pt-note' }, 'បង្ហាញវិធីធ្វើឱ្យបានច្បាស់។'));
        writing.forEach((q, i) => {
          kids.push(h('div', { class: 'pt-ans-q' }, [
            h('div', {}, `${i + 1}.  សំណួរទី ${kh(i + 1)}`),
            h('div', { class: 'pt-lines' }, [...Array(Math.min(8, Math.max(3, Math.round(q.points / 2)))).keys()].map(() => h('i'))),
            h('div', { class: 'pt-lines-score' }, `ពិន្ទុ: ______/${kh(q.points)}`),
          ]));
        });
      }
    }
    return h('div', { class: 'sheet pt-doc' }, [header(ctx), page(ctx, kids), screenFooter(ctx)]);
  }

  // teacher key in the same style: red title, answer table, two-column worked solutions with score breakdown
  function keyDoc(ctx, o) {
    const { h, mathEl, kh, mcq, writing, mcqPts, wPts, test } = ctx;
    const kids = [];
    kids.push(h('div', { class: 'ptk-title' }, [h('div', { class: 'a' }, 'ចម្លើយ និងគោលការណ៍ដាក់ពិន្ទុសម្រាប់គ្រូ'), h('div', { class: 'b' }, test.title)]));
    kids.push(h('div', { class: 'ptk-note' }, 'ឯកសារនេះសម្រាប់គ្រូបង្រៀន។ មិនត្រូវចែកជូនសិស្សមុនពេលប្រឡង។'));
    if (mcq.length) {
      kids.push(h('h2', { class: 'ptk-h' }, `តារាងចម្លើយ ផ្នែកទី ១ (${kh(mcqPts)} ពិន្ទុ)`));
      const rows = Math.ceil(mcq.length / 3);
      const head = h('tr', {}, [0, 1, 2].flatMap(() => [h('th', {}, 'សំណួរ'), h('th', {}, 'ចម្លើយ')]));
      const body = [...Array(rows).keys()].map((r) => h('tr', {}, [0, 1, 2].flatMap((c) => {
        const i = c * rows + r, q = mcq[i];
        return q ? [h('td', { class: 'n' }, String(i + 1)), h('td', { class: 'k' }, LAT[q.correct_index] + (q.alt_correct_index != null ? `/${LAT[q.alt_correct_index]}` : ''))] : [h('td'), h('td')];
      })));
      kids.push(h('table', { class: 'ptk-table' }, [h('thead', {}, head), h('tbody', {}, body)]));
    }
    if (writing.length) {
      kids.push(h('h2', { class: 'ptk-h' }, `ដំណោះស្រាយ និងគោលការណ៍ដាក់ពិន្ទុ ផ្នែកទី ២ (${kh(wPts)} ពិន្ទុ)`));
      const items = writing.map((q, i) => {
        const lines = String(q.solution_text || '(មិនទាន់មានចម្លើយគំរូ)').split('\n').filter((l) => l.trim());
        const bullets = [];
        const body = lines.map((ln) => {
          const m = ln.match(/\(\s*([០-៩0-9]+)\s*ពិន្ទុ[^)]*\)/);
          const lab = ln.match(/^\s*([ក-ឃង-ច])\s*[\)\.]/);
          if (m) bullets.push(`${lab ? `${lab[1]}. ` : ''}${m[1]} ពិន្ទុ`);
          if (/^\s*ដូចនេះ/.test(ln)) return h('div', { class: 'ans' }, ln.trim().replace(/^ដូចនេះ\s*/, 'ចម្លើយ៖ '));
          const el = h('div'); el.innerHTML = Exam.mathHtml(ln); return el;
        });
        const title = h('div', { class: 'tt' });
        title.innerHTML = `${i + 1}. ${Exam.mathHtml((q.stem_text.split('\n')[0] || '').trim())}`;
        return h('div', { class: 'ptk-item' }, [
          title,
          ...body,
          h('div', { class: 'sc' }, `របាយពិន្ទុ (${kh(q.points)} ពិន្ទុ)៖`),
          bullets.length ? h('ul', {}, bullets.map((b) => h('li', {}, b))) : null,
        ]);
      });
      kids.push(h('div', { class: 'ptk-cols' }, items));
    }
    // difficulty map from the level tags
    const tagged = test.questions.some((q) => q.level);
    if (tagged) {
      const num = (list) => {
        const p1 = list.filter((q) => q.kind !== 'writing').map((q) => mcq.indexOf(q) + 1);
        const p2 = list.filter((q) => q.kind === 'writing').map((q) => writing.indexOf(q) + 1);
        return [p1.length ? `ផ្នែកទី ១ សំណួរទី ${p1.map(kh).join(', ')}` : '', p2.length ? `ផ្នែកទី ២ សំណួរទី ${p2.map(kh).join(', ')}` : ''].filter(Boolean).join(' · ');
      };
      kids.push(h('div', { class: 'ptk-banner' }, 'ផែនទីកម្រិតលំបាកសម្រាប់គ្រូបង្រៀន'));
      kids.push(h('ul', {}, [['easy', 'កម្រិតងាយស្រួល (Easy)'], ['medium', 'កម្រិតមធ្យម (Medium)'], ['hard', 'កម្រិតលំបាក (Hard)'], ['pisa', 'បែប PISA']].map(([lv, label]) => {
        const list = test.questions.filter((q) => q.level === lv);
        return list.length ? h('li', {}, [h('b', {}, `${label}៖ `), `${kh(list.length)} សំណួរ — ${num(list)}`]) : null;
      })));
    }
    return h('div', { class: 'sheet ptkey-doc' }, kids);
  }

  window.PaperPT = { examDoc, keyDoc, pageStyle };
})();
