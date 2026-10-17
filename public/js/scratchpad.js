/* =========================================================================
   Student Scratchpad (ក្ដារព្រាងគណនា)
   Interactive floating blackboard & coordinate grid paper for calculations
   and geometry drawings during exam or practice.
   ========================================================================= */
(function () {
  const COLORS = [
    { name: 'ស', hex: '#f8fafc' },
    { name: 'លឿង', hex: '#fde047' },
    { name: 'ផ្ទៃមេឃ', hex: '#38bdf8' },
    { name: 'បៃតង', hex: '#4ade80' },
    { name: 'ផ្កាឈូក', hex: '#f472b6' }
  ];

  const SIZES = [
    { label: 'S', width: 2.2 },
    { label: 'M', width: 4.2 },
    { label: 'L', width: 7.5 }
  ];

  let state = {
    open: false,
    expanded: false,
    tool: 'pen', // 'pen' | 'line' | 'eraser'
    color: '#f8fafc',
    size: 2.2,
    grid: true,
    hasDrawing: false,
    history: []
  };

  let dom = {};
  let ctx = null;
  let isDrawing = false;
  let startX = 0, startY = 0;
  let lastX = 0, lastY = 0;
  let savedImageData = null;

  function init() {
    if (document.getElementById('exam-scratchpad-panel')) return;

    // Create FAB
    const fab = document.createElement('button');
    fab.id = 'exam-scratchpad-fab';
    fab.className = 'scratchpad-fab';
    fab.type = 'button';
    fab.title = 'បើកក្ដារព្រាងគណនា (Scratchpad)';
    fab.innerHTML = '<span>✏️</span><span>ក្ដារព្រាង</span>';
    fab.onclick = toggle;
    document.body.appendChild(fab);
    dom.fab = fab;

    // Create Panel
    const panel = document.createElement('div');
    panel.id = 'exam-scratchpad-panel';
    panel.className = 'scratchpad-panel';
    panel.hidden = true;

    panel.innerHTML = `
      <div class="scratchpad-header">
        <div class="scratchpad-title">
          <span>✏️</span>
          <span>ក្ដារព្រាងគណនា</span>
        </div>
        <div class="scratchpad-actions">
          <button type="button" class="scratchpad-btn-icon" id="sp-btn-grid" title="បិទ/បើក ក្រដាសក្រឡា (Grid)">
            # ក្រឡា
          </button>
          <button type="button" class="scratchpad-btn-icon" id="sp-btn-expand" title="ពង្រីកពេញអេក្រង់ / បង្រួម">
            ⤢
          </button>
          <button type="button" class="scratchpad-btn-icon" id="sp-btn-close" title="បិទ (Esc)">
            ✕
          </button>
        </div>
      </div>
      <div class="scratchpad-canvas-wrap grid-bg" id="sp-canvas-wrap">
        <canvas class="scratchpad-canvas" id="sp-canvas"></canvas>
      </div>
      <div class="scratchpad-toolbar">
        <div class="scratchpad-tool-group">
          <button type="button" class="scratchpad-btn-icon active" id="sp-tool-pen" title="ប៊ិចគូស (Pen)">🖊 ប៊ិច</button>
          <button type="button" class="scratchpad-btn-icon" id="sp-tool-line" title="បន្ទាត់ត្រង់ (Straight Line)">📏 បន្ទាត់</button>
          <button type="button" class="scratchpad-btn-icon" id="sp-tool-eraser" title="ជ័រលុប (Eraser)">🧽 ជ័រលុប</button>
        </div>
        <div class="scratchpad-tool-group" id="sp-sizes"></div>
        <div class="scratchpad-tool-group" id="sp-colors"></div>
        <div class="scratchpad-tool-group">
          <button type="button" class="scratchpad-btn-icon" id="sp-btn-undo" title="ត្រឡប់ក្រោយ (Ctrl+Z)">↺ ថយ</button>
          <button type="button" class="scratchpad-btn-icon" id="sp-btn-clear" title="លុបទាំងអស់ (Clear All)">🗑️ សម្អាត</button>
        </div>
      </div>
    `;

    document.body.appendChild(panel);
    dom.panel = panel;
    dom.wrap = document.getElementById('sp-canvas-wrap');
    dom.canvas = document.getElementById('sp-canvas');
    ctx = dom.canvas.getContext('2d', { willReadFrequently: true });

    // Build size buttons
    const sizesContainer = document.getElementById('sp-sizes');
    SIZES.forEach((s) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'scratchpad-size-pill' + (s.width === state.size ? ' active' : '');
      btn.textContent = s.label;
      btn.title = `ទំហំប៊ិច៖ ${s.label}`;
      btn.onclick = () => {
        state.size = s.width;
        sizesContainer.querySelectorAll('.scratchpad-size-pill').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
      };
      sizesContainer.appendChild(btn);
    });

    // Build color buttons
    const colorsContainer = document.getElementById('sp-colors');
    COLORS.forEach((c) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'scratchpad-color-dot' + (c.hex === state.color ? ' active' : '');
      btn.style.backgroundColor = c.hex;
      btn.title = `ពណ៌ ${c.name}`;
      btn.onclick = () => {
        state.color = c.hex;
        if (state.tool === 'eraser') setTool('pen');
        colorsContainer.querySelectorAll('.scratchpad-color-dot').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
      };
      colorsContainer.appendChild(btn);
    });

    // Header buttons
    document.getElementById('sp-btn-close').onclick = hide;
    document.getElementById('sp-btn-expand').onclick = toggleExpand;
    document.getElementById('sp-btn-grid').onclick = toggleGrid;

    // Tools
    document.getElementById('sp-tool-pen').onclick = () => setTool('pen');
    document.getElementById('sp-tool-line').onclick = () => setTool('line');
    document.getElementById('sp-tool-eraser').onclick = () => setTool('eraser');

    // Actions
    document.getElementById('sp-btn-undo').onclick = undo;
    document.getElementById('sp-btn-clear').onclick = clear;

    // Canvas Events
    setupCanvasEvents();

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      if (!state.open) return;
      if (e.key === 'Escape') {
        hide();
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
        e.preventDefault();
        undo();
      }
    });

    // Handle Window Resize
    window.addEventListener('resize', () => {
      if (state.open) resizeCanvas(true);
    });
  }

  function setTool(t) {
    state.tool = t;
    ['pen', 'line', 'eraser'].forEach((name) => {
      const btn = document.getElementById(`sp-tool-${name}`);
      if (btn) btn.classList.toggle('active', t === name);
    });
  }

  function toggleGrid() {
    state.grid = !state.grid;
    dom.wrap.classList.toggle('grid-bg', state.grid);
    document.getElementById('sp-btn-grid').classList.toggle('active', state.grid);
  }

  function toggleExpand() {
    state.expanded = !state.expanded;
    dom.panel.classList.toggle('expanded', state.expanded);
    const expandBtn = document.getElementById('sp-btn-expand');
    if (expandBtn) expandBtn.textContent = state.expanded ? '⤡' : '⤢';
    setTimeout(() => resizeCanvas(true), 260);
  }

  function show() {
    init();
    state.open = true;
    dom.panel.hidden = false;
    dom.fab.style.display = 'none';
    resizeCanvas(true);
  }

  function hide() {
    if (!state.open) return;
    state.open = false;
    dom.panel.hidden = true;
    dom.fab.style.display = 'inline-flex';
    updateFabBadge();
  }

  function toggle() {
    if (state.open) hide();
    else show();
  }

  function updateFabBadge() {
    if (dom.fab) {
      dom.fab.classList.toggle('has-drawing', state.hasDrawing);
    }
  }

  function resizeCanvas(preserve) {
    if (!dom.canvas || !dom.wrap) return;
    const rect = dom.wrap.getBoundingClientRect();
    const w = Math.floor(rect.width);
    const h = Math.floor(rect.height);
    if (!w || !h) return;

    let backup = null;
    if (preserve && dom.canvas.width && dom.canvas.height) {
      try {
        backup = ctx.getImageData(0, 0, dom.canvas.width, dom.canvas.height);
      } catch (e) {}
    }

    const dpr = window.devicePixelRatio || 1;
    dom.canvas.width = w * dpr;
    dom.canvas.height = h * dpr;
    ctx.scale(dpr, dpr);

    if (backup) {
      try {
        ctx.putImageData(backup, 0, 0);
      } catch (e) {}
    }
  }

  function saveSnapshot() {
    if (!dom.canvas) return;
    try {
      const snap = ctx.getImageData(0, 0, dom.canvas.width, dom.canvas.height);
      state.history.push(snap);
      if (state.history.length > 18) state.history.shift();
      state.hasDrawing = true;
      updateFabBadge();
    } catch (e) {}
  }

  function undo() {
    if (!state.history.length) {
      clear(false);
      return;
    }
    const snap = state.history.pop();
    ctx.putImageData(snap, 0, 0);
    state.hasDrawing = state.history.length > 0;
    updateFabBadge();
  }

  function clear(recordHistory = true) {
    if (recordHistory) saveSnapshot();
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, dom.canvas.width, dom.canvas.height);
    ctx.restore();
    state.hasDrawing = false;
    updateFabBadge();
  }

  function getPos(e) {
    const rect = dom.canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  }

  function setupCanvasEvents() {
    const c = dom.canvas;

    c.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      c.setPointerCapture(e.pointerId);
      isDrawing = true;
      const pos = getPos(e);
      startX = pos.x;
      startY = pos.y;
      lastX = pos.x;
      lastY = pos.y;

      saveSnapshot();

      if (state.tool === 'line') {
        savedImageData = ctx.getImageData(0, 0, c.width, c.height);
      } else {
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, state.size / 2, 0, Math.PI * 2);
        ctx.fillStyle = state.tool === 'eraser' ? '#090d16' : state.color;
        if (state.tool === 'eraser') {
          ctx.globalCompositeOperation = 'destination-out';
        } else {
          ctx.globalCompositeOperation = 'source-over';
        }
        ctx.fill();
      }
    });

    c.addEventListener('pointermove', (e) => {
      if (!isDrawing) return;
      e.preventDefault();
      const pos = getPos(e);

      if (state.tool === 'line') {
        if (savedImageData) {
          ctx.putImageData(savedImageData, 0, 0);
        }
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(pos.x, pos.y);
        ctx.strokeStyle = state.color;
        ctx.lineWidth = state.size;
        ctx.lineCap = 'round';
        ctx.globalCompositeOperation = 'source-over';
        ctx.stroke();
        ctx.restore();
      } else {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.strokeStyle = state.color;
        ctx.lineWidth = state.tool === 'eraser' ? state.size * 3.5 : state.size;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        if (state.tool === 'eraser') {
          ctx.globalCompositeOperation = 'destination-out';
        } else {
          ctx.globalCompositeOperation = 'source-over';
        }
        ctx.stroke();
        ctx.restore();
        lastX = pos.x;
        lastY = pos.y;
      }
    });

    const stopDrawing = (e) => {
      if (!isDrawing) return;
      isDrawing = false;
      savedImageData = null;
      try { c.releasePointerCapture(e.pointerId); } catch (err) {}
    };

    c.addEventListener('pointerup', stopDrawing);
    c.addEventListener('pointercancel', stopDrawing);
  }

  // Expose API
  window.Scratchpad = {
    init,
    show,
    hide,
    toggle,
    clear,
    undo
  };

  // Auto-init when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
