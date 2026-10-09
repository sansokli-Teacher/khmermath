/* Textbook lessons: maths and the "in this lesson" menu. */
(function () {
  'use strict';
  var paper = document.querySelector('.ls-paper') || document.querySelector('.legend');
  if (window.renderMathInElement && paper) {
    window.renderMathInElement(paper, {
      delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
      ],
      macros: { '\\arc': '\\overset{\\frown}{#1}', '\\overparen': '\\overset{\\frown}{#1}' },
      throwOnError: false,
      strict: 'ignore',
    });
  }

  
  // Toggle answer/solution details summary between «មើល...» and «លាក់...»
  function updateAnsSummary(d) {
    var s = d.querySelector('summary');
    if (!s) return;
    var base = s.getAttribute('data-base-label');
    if (!base) {
      base = s.textContent.trim();
      s.setAttribute('data-base-label', base);
    }
    var isSolution = base.indexOf('ដំណោះស្រាយ') !== -1;
    var openLabel = isSolution ? 'លាក់ដំណោះស្រាយ' : 'លាក់ចម្លើយ';
    var closeLabel = isSolution ? 'មើលដំណោះស្រាយ' : 'មើលចម្លើយ';

    s.textContent = d.open ? openLabel : closeLabel;
  }

  function initAnsToggles() {
    document.querySelectorAll('details.ans').forEach(updateAnsSummary);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnsToggles);
  } else {
    initAnsToggles();
  }

  document.addEventListener('toggle', function (e) {
    var target = e.target;
    if (target && target.matches && target.matches('details.ans')) {
      updateAnsSummary(target);
    }
  }, true);

  // mark the section being read, and keep it visible in the menu without moving the page
  var links = Array.prototype.slice.call(document.querySelectorAll('.ls-toc a'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  var heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting || !byId[en.target.id]) return;
      links.forEach(function (a) { a.classList.remove('here'); });
      var a = byId[en.target.id];
      a.classList.add('here');
      var list = a.closest('.ls-toc');
      if (window.matchMedia('(max-width: 960px)').matches) {
        list.scrollLeft = a.parentNode.offsetLeft - 12;
      } else {
        var box = a.closest('.ls-side-box');
        if (a.offsetTop < box.scrollTop || a.offsetTop + a.offsetHeight > box.scrollTop + box.clientHeight) {
          box.scrollTop = a.offsetTop - box.clientHeight / 2;
        }
      }
    });
  }, { rootMargin: '-15% 0px -75% 0px' });
  heads.forEach(function (h) { obs.observe(h); });

  /* -------------------------------------------------- Interactive Calculator -- */
  function initCalculator() {
    var calcEl = document.querySelector('.calc-device');
    if (!calcEl) return;

    var disp = document.getElementById('calc-disp');
    var hist = document.getElementById('calc-hist');
    var guideText = document.getElementById('calc-guide-text');
    var guideBar = document.getElementById('calc-guide-bar');
    var sampleBtns = document.querySelectorAll('.calc-sample-btn');

    var currentInput = '0';
    var prevInput = '';
    var operator = null;
    var justCalculated = false;
    var currentExpr = '';
    var isRunningDemo = false;
    var demoTimer = null;

    // Web Audio API click tone for tactile feel
    var audioCtx = null;
    function playClickSound() {
      try {
        if (!audioCtx) {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
        var osc = audioCtx.createOscillator();
        var gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(650, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.04);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.04);
      } catch (e) {
        // audio context failed or not allowed, ignore gracefully
      }
    }

    function updateDisplay() {
      if (!disp) return;
      disp.textContent = currentInput;
      if (hist) {
        hist.textContent = currentExpr;
      }
    }

    function setGuide(msg, isSuccess) {
      if (!guideText) return;
      guideText.innerHTML = msg;
      if (guideBar) {
        if (isSuccess) {
          guideBar.classList.add('success');
        } else {
          guideBar.classList.remove('success');
        }
      }
    }

    function flashKey(keyName) {
      var btn = calcEl.querySelector('[data-key="' + keyName + '"]');
      if (btn) {
        btn.classList.add('key-active');
        setTimeout(function () {
          btn.classList.remove('key-active');
        }, 150);
      }
    }

    function handleNumber(num) {
      if (justCalculated) {
        currentInput = num;
        currentExpr = '';
        justCalculated = false;
      } else if (currentInput === '0') {
        currentInput = num;
      } else {
        if (currentInput.length < 15) {
          currentInput += num;
        }
      }
      updateDisplay();
    }

    function handleDot() {
      if (justCalculated) {
        currentInput = '0.';
        currentExpr = '';
        justCalculated = false;
      } else if (currentInput.indexOf('.') === -1) {
        currentInput += '.';
      }
      updateDisplay();
    }

    function handleOperator(op) {
      var opSymbols = { '+': '+', '-': '−', '*': '×', '/': '÷' };
      var sym = opSymbols[op] || op;

      if (operator && !justCalculated) {
        calculate(false);
      }
      prevInput = currentInput;
      operator = op;
      currentExpr = prevInput + ' ' + sym;
      justCalculated = true;
      updateDisplay();
    }

    function calculate(isFinal) {
      if (!operator || prevInput === '') return;
      var a = parseFloat(prevInput);
      var b = parseFloat(currentInput);
      var res = 0;

      if (operator === '+') res = a + b;
      else if (operator === '-') res = a - b;
      else if (operator === '*') res = a * b;
      else if (operator === '/') {
        if (b === 0) {
          currentInput = 'Error';
          currentExpr = '';
          operator = null;
          prevInput = '';
          justCalculated = true;
          updateDisplay();
          setGuide('⚠️ មិនអាចចែកនឹងសូន្យ (Division by Zero) បានទេ!', false);
          return;
        }
        res = a / b;
      }

      // Round floating point inaccuracies e.g. 0.1 + 0.2
      res = Math.round(res * 1e10) / 1e10;

      var opSymbols = { '+': '+', '-': '−', '*': '×', '/': '÷' };
      var sym = opSymbols[operator] || operator;

      if (isFinal) {
        currentExpr = prevInput + ' ' + sym + ' ' + currentInput + ' =';
        operator = null;
        prevInput = '';
      } else {
        prevInput = String(res);
        currentExpr = prevInput;
      }

      currentInput = String(res);
      justCalculated = true;
      updateDisplay();
    }

    function handleClear() {
      currentInput = '0';
      prevInput = '';
      operator = null;
      currentExpr = '';
      justCalculated = false;
      updateDisplay();
      setGuide('បានលុបទាំងអស់ (AC) ។ ចុចលេខដើម្បីចាប់ផ្តើមគណនាថ្មី ។', false);
    }

    function handleDelete() {
      if (justCalculated || currentInput === 'Error') {
        handleClear();
        return;
      }
      if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
      } else {
        currentInput = '0';
      }
      updateDisplay();
    }

    function handleSqrt() {
      var val = parseFloat(currentInput);
      if (isNaN(val) || val < 0) {
        currentInput = 'Error';
        currentExpr = '';
        justCalculated = true;
        updateDisplay();
        setGuide('⚠️ មិនអាចរកឫសការ៉េនៃចំនួនអវិជ្ជមានបានទេ!', false);
        return;
      }
      var res = Math.sqrt(val);
      res = Math.round(res * 1e10) / 1e10;
      currentExpr = '√(' + currentInput + ') =';
      currentInput = String(res);
      justCalculated = true;
      updateDisplay();
      setGuide('√' + val + ' = <b>' + res + '</b> (ព្រោះ ' + res + '² = ' + val + ')', true);
    }

    function handleSquare() {
      var val = parseFloat(currentInput);
      if (isNaN(val)) return;
      var res = val * val;
      res = Math.round(res * 1e10) / 1e10;
      currentExpr = 'sqr(' + currentInput + ') =';
      currentInput = String(res);
      justCalculated = true;
      updateDisplay();
      setGuide(val + '² = <b>' + res + '</b> (ព្រោះ ' + val + ' × ' + val + ' = ' + res + ')', true);
    }

    function handleCube() {
      var val = parseFloat(currentInput);
      if (isNaN(val)) return;
      var res = val * val * val;
      res = Math.round(res * 1e10) / 1e10;
      currentExpr = 'cube(' + currentInput + ') =';
      currentInput = String(res);
      justCalculated = true;
      updateDisplay();
      setGuide(val + '³ = <b>' + res + '</b> (ព្រោះ ' + val + ' × ' + val + ' × ' + val + ' = ' + res + ')', true);
    }

    function handlePlusMinus() {
      var val = parseFloat(currentInput);
      if (isNaN(val) || val === 0) return;
      currentInput = String(-val);
      updateDisplay();
    }

    function onKeyAction(key) {
      playClickSound();
      flashKey(key);

      if (key >= '0' && key <= '9') {
        handleNumber(key);
      } else if (key === '.') {
        handleDot();
      } else if (key === '+' || key === '-' || key === '*' || key === '/') {
        handleOperator(key);
      } else if (key === '=') {
        calculate(true);
      } else if (key === 'clear') {
        handleClear();
      } else if (key === 'del') {
        handleDelete();
      } else if (key === 'sqrt') {
        handleSqrt();
      } else if (key === 'sqr') {
        handleSquare();
      } else if (key === 'cube') {
        handleCube();
      } else if (key === 'pm') {
        handlePlusMinus();
      }
    }

    // Attach click events on calculator keypad
    calcEl.querySelectorAll('.calc-key').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (isRunningDemo) {
          clearTimeout(demoTimer);
          isRunningDemo = false;
        }
        var k = btn.getAttribute('data-key');
        onKeyAction(k);
      });
    });

    // Run interactive animated demo for sample problems
    function runDemo(keys, guideMsg) {
      if (isRunningDemo) {
        clearTimeout(demoTimer);
      }
      isRunningDemo = true;
      handleClear();
      setGuide('កំពុងបង្ហាញការចុច ៖ ' + guideMsg, false);

      var idx = 0;
      function step() {
        if (!isRunningDemo || idx >= keys.length) {
          isRunningDemo = false;
          setGuide('✓ ' + guideMsg, true);
          return;
        }
        var k = keys[idx++];
        onKeyAction(k);
        demoTimer = setTimeout(step, 200);
      }
      demoTimer = setTimeout(step, 300);
    }

    // Sample example buttons
    sampleBtns.forEach(function (sBtn) {
      sBtn.addEventListener('click', function () {
        sampleBtns.forEach(function (b) { b.classList.remove('active'); });
        sBtn.classList.add('active');

        var action = sBtn.getAttribute('data-action');
        var expr = sBtn.getAttribute('data-expr');
        var label = sBtn.getAttribute('data-label');

        if (action === 'sqrt') {
          var keys = expr.split('').concat(['sqrt']);
          runDemo(keys, '<b>គំរូ គ ៖</b> ចុច 625 រួចចុចប៊ូតុង [√] ➔ ទទួលបានលទ្ធផល <b>25</b>');
        } else if (action === 'sqr') {
          var keys = expr.split('').concat(['sqr']);
          runDemo(keys, '<b>គំរូ ឃ ៖</b> ចុច 9 រួចចុចប៊ូតុង [x²] ➔ ទទួលបានលទ្ធផល <b>81</b>');
        } else if (action === 'cube') {
          var keys = expr.split('').concat(['cube']);
          runDemo(keys, '<b>គំរូ ង ៖</b> ចុច 11 រួចចុចប៊ូតុង [x³] ➔ ទទួលបានលទ្ធផល <b>1331</b>');
        } else if (expr) {
          var keySeq = [];
          for (var i = 0; i < expr.length; i++) {
            keySeq.push(expr[i]);
          }
          keySeq.push('=');
          if (expr.indexOf('4027') !== -1) {
            runDemo(keySeq, '<b>គំរូ ក ៖</b> ចុច 321 [+] 4027 [−] 2902 [=] ➔ ទទួលបានលទ្ធផល <b>1446</b>');
          } else if (expr.indexOf('150') !== -1) {
            runDemo(keySeq, '<b>គំរូ ខ ៖</b> ចុច 150 [×] 12 [÷] 18 [=] ➔ ទទួលបានលទ្ធផល <b>100</b>');
          } else {
            runDemo(keySeq, '<b>' + label + '</b>');
          }
        }
      });
    });

    // Keyboard support when focused on calculator or mouse inside
    window.addEventListener('keydown', function (e) {
      if (!calcEl.matches(':hover') && document.activeElement !== calcEl && !calcEl.contains(document.activeElement)) {
        return;
      }
      var k = e.key;
      if (k >= '0' && k <= '9') {
        e.preventDefault();
        onKeyAction(k);
      } else if (k === '+' || k === '-' || k === '*' || k === '/') {
        e.preventDefault();
        onKeyAction(k);
      } else if (k === 'Enter' || k === '=') {
        e.preventDefault();
        onKeyAction('=');
      } else if (k === 'Backspace') {
        e.preventDefault();
        onKeyAction('del');
      } else if (k === 'Escape' || k === 'c' || k === 'C') {
        e.preventDefault();
        onKeyAction('clear');
      } else if (k === '.') {
        e.preventDefault();
        onKeyAction('.');
      }
    });

    updateDisplay();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCalculator);
  } else {
    initCalculator();
  }

})();