/* Visitor counter shared by khmermath.org, pisa.khmermath.org and cba.khmermath.org.
 * Counts this page at stats.khmermath.org (a browser counts as one visitor per day, Cambodia time),
 * then fills the [data-vc] elements with the live numbers. The server keeps only the country and the
 * day; the km_day cookie holds only today's date, so the three sites count a visitor once.
 * Local copies (file:, localhost) only read the numbers. */
(function () {
  'use strict';
  var API = 'https://stats.khmermath.org';
  var FLAGS = 'https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/flags/4x3/';
  var MONTHS = ['មករា', 'កុម្ភៈ', 'មីនា', 'មេសា', 'ឧសភា', 'មិថុនា', 'កក្កដា', 'សីហា', 'កញ្ញា', 'តុលា', 'វិច្ឆិកា', 'ធ្នូ'];
  var me = document.currentScript;
  var site = (me && me.getAttribute('data-site')) || 'main';
  var live = /(^|\.)khmermath\.org$/.test(location.hostname);
  var day = new Date(Date.now() + 7 * 3600e3).toISOString().slice(0, 10);

  var isNew = true;
  try {
    var m = /(?:^|;\s*)km_day=([\d-]+)/.exec(document.cookie);
    var last = m ? m[1] : localStorage.getItem('km-day');
    isNew = last !== day;
    if (isNew && live) {
      document.cookie = 'km_day=' + day + '; domain=khmermath.org; path=/; max-age=172800; SameSite=Lax; Secure';
      localStorage.setItem('km-day', day);
    }
  } catch (e) { /* storage blocked: count as new */ }

  var num = function (n) { return String(n); };
  try {
    var nf = new Intl.NumberFormat('km-KH', { numberingSystem: 'khmr' });
    num = function (n) { return nf.format(n); };
  } catch (e) { /* old browser */ }
  // Khmer country names (CLDR, via Intl.DisplayNames 'km'): not every browser ships them
  var KM = {"AC":"កោះអាសេនសិន","AD":"អង់ដូរ៉ា","AE":"អេមីរ៉ាតអារ៉ាប់រួម","AF":"អាហ្វហ្កានីស្ថាន","AG":"អង់ទីហ្គា និង បាប៊ុយដា","AI":"អង់ហ្គីឡា","AL":"អាល់បានី","AM":"អាមេនី","AN":"កូរ៉ាកៅ","AO":"អង់ហ្គោឡា","AQ":"អង់តាក់ទិក","AR":"អាហ្សង់ទីន","AS":"សាម័រ អាមេរិកាំង","AT":"អូទ្រីស","AU":"អូស្ត្រាលី","AW":"អារូបា","AX":"កោះអាឡង់","AZ":"អាស៊ែបៃហ្សង់","BA":"បូស្ន៊ី និងហឺហ្ស៊ីហ្គូវីណា","BB":"បាបាដុស","BD":"បង់ក្លាដែស","BE":"បែលហ្ស៊ិក","BF":"បួគីណាហ្វាសូ","BG":"ប៊ុលហ្ការី","BH":"បារ៉ែន","BI":"ប៊ូរុនឌី","BJ":"បេណាំង","BL":"សាំងបាថេឡេមី","BM":"ប៊ឺមុយដា","BN":"ព្រុយណេ","BO":"បូលីវី","BQ":"ហូឡង់ ការ៉ាប៊ីន","BR":"ប្រេស៊ីល","BS":"បាហាម៉ា","BT":"ប៊ូតង់","BU":"មីយ៉ាន់ម៉ា (ភូមា)","BV":"កោះប៊ូវ៉េត","BW":"បុតស្វាណា","BY":"បេឡារុស","BZ":"បេលី","CA":"កាណាដា","CC":"កោះកូកូស (គីលីង)","CD":"កុងហ្គោ- គីនស្ហាសា","CF":"សាធារណរដ្ឋអាហ្វ្រិកកណ្ដាល","CG":"កុងហ្គោ - ប្រាហ្សាវីល","CH":"ស្វ៊ីស","CI":"កូតឌីវ័រ","CK":"កោះខូក","CL":"ស៊ីលី","CM":"កាមេរូន","CN":"ចិន","CO":"កូឡុំប៊ី","CP":"កោះឃ្លីភឺតុន","CR":"កូស្តារីកា","CS":"សែប៊ី","CU":"គុយបា","CV":"កាប់វែរ","CW":"កូរ៉ាកៅ","CX":"កោះគ្រីស្មាស","CY":"ស៊ីប","CZ":"ឆែក","DD":"អាល្លឺម៉ង់","DE":"អាល្លឺម៉ង់","DG":"ឌៀហ្គោហ្គាស៊ី","DJ":"ជីប៊ូទី","DK":"ដាណឺម៉ាក","DM":"ដូមីនីក","DO":"សាធារណរដ្ឋដូមីនីក","DY":"បេណាំង","DZ":"អាល់ហ្សេរី","EA":"ជឺតា និងម៉េលីឡា","EC":"អេក្វាទ័រ","EE":"អេស្តូនី","EG":"អេហ្ស៊ីប","EH":"សាហារ៉ាខាងលិច","ER":"អេរីត្រេ","ES":"អេស្ប៉ាញ","ET":"អេត្យូពី","EU":"សហភាពអឺរ៉ុប","EZ":"តំបន់ចាយលុយអឺរ៉ូ","FI":"ហ្វាំងឡង់","FJ":"ហ្វីជី","FK":"កោះហ្វក់ឡែន","FM":"មីក្រូណេស៊ី","FO":"កោះហ្វារ៉ូ","FR":"បារាំង","FX":"បារាំង","GA":"ហ្គាបុង","GB":"ចក្រភពអង់គ្លេស","GD":"ហ្គ្រើណាដ","GE":"ហ្សកហ្ស៊ី","GF":"ហ្គីអាណា បារាំង","GG":"ហ្គេនស៊ី","GH":"ហ្គាណា","GI":"ហ្ស៊ីប្រាល់តា","GL":"ហ្គ្រោអង់ឡង់","GM":"ហ្គំប៊ី","GN":"ហ្គីណេ","GP":"ហ្គោដឺឡុប","GQ":"ហ្គីណេអេក្វាទ័រ","GR":"ក្រិក","GS":"កោះហ្សកហ្ស៊ីខាងត្បូង និង សង់វិចខាងត្បូង","GT":"ក្វាតេម៉ាឡា","GU":"ហ្គាំ","GW":"ហ្គីណេប៊ីស្សូ","GY":"ហ្គីយ៉ាន","HK":"ហុងកុង","HM":"កោះហឺដនិងម៉ាក់ដូណាល់","HN":"ហុងឌូរ៉ាស","HR":"ក្រូអាស៊ី","HT":"ហៃទី","HU":"ហុងគ្រី","HV":"បួគីណាហ្វាសូ","IC":"កោះកាណារី","ID":"ឥណ្ឌូណេស៊ី","IE":"អៀរឡង់","IL":"អ៊ីស្រាអែល","IM":"អែលអុហ្វមែន","IN":"ឥណ្ឌា","IO":"ដែនដីអង់គ្លេសនៅមហាសមុទ្រឥណ្ឌា","IQ":"អ៊ីរ៉ាក់","IR":"អ៊ីរ៉ង់","IS":"អ៊ីស្លង់","IT":"អ៊ីតាលី","JE":"ជើស៊ី","JM":"ហ្សាម៉ាអ៊ីក","JO":"ហ៊្សកដានី","JP":"ជប៉ុន","KE":"កេនយ៉ា","KG":"កៀហ្ស៊ីស៊ីស្ថាន","KH":"កម្ពុជា","KI":"គិរីបាទី","KM":"កូម័រ","KN":"សាំងគីត និង ណេវីស","KP":"កូរ៉េខាងជើង","KR":"កូរ៉េខាងត្បូង","KW":"កូវ៉ែត","KY":"កោះកៃម៉ង់","KZ":"កាហ្សាក់ស្ថាន","LA":"ឡាវ","LB":"លីបង់","LC":"សាំងលូស៊ី","LI":"លិចតិនស្ដាញ","LK":"ស្រីលង្កា","LR":"លីបេរីយ៉ា","LS":"ឡេសូតូ","LT":"លីទុយអានី","LU":"លុចសំបួ","LV":"ឡេតូនី","LY":"លីប៊ី","MA":"ម៉ារ៉ុក","MC":"ម៉ូណាកូ","MD":"ម៉ុលដាវី","ME":"ម៉ុងតេណេហ្គ្រោ","MF":"សាំងម៉ាទីន","MG":"ម៉ាដាហ្គាស្កា","MH":"កោះម៉ាស់សល","MK":"ម៉ាសេដ្វានខាងជើង","ML":"ម៉ាលី","MM":"មីយ៉ាន់ម៉ា (ភូមា)","MN":"ម៉ុងហ្គោលី","MO":"ម៉ាកាវ","MP":"កោះម៉ារីណាខាងជើង","MQ":"ម៉ាទីនីក","MR":"ម៉ូរីតានី","MS":"ម៉ុងស៊ែរ៉ា","MT":"ម៉ាល់ត៍","MU":"ម៉ូរីស","MV":"ម៉ាល់ឌីវ","MW":"ម៉ាឡាវី","MX":"ម៉ិកស៊ិក","MY":"ម៉ាឡេស៊ី","MZ":"ម៉ូសំប៊ិក","NA":"ណាមីប៊ី","NC":"នូវែលកាឡេដូនី","NE":"នីហ្សេ","NF":"កោះណ័រហ្វក់","NG":"នីហ្សេរីយ៉ា","NH":"វ៉ានូទូ","NI":"នីការ៉ាហ្គា","NL":"ហូឡង់","NO":"ន័រវែស","NP":"នេប៉ាល់","NR":"ណូរូ","NU":"ណៀ","NZ":"នូវែលសេឡង់","OM":"អូម៉ង់","PA":"ប៉ាណាម៉ា","PE":"ប៉េរូ","PF":"ប៉ូលីណេស៊ីបារាំង","PG":"ប៉ាពូអាស៊ីនូវែលហ្គីណេ","PH":"ហ្វ៊ីលីពីន","PK":"ប៉ាគីស្ថាន","PL":"ប៉ូឡូញ","PM":"សង់ព្យែរ និងមីគីឡុង","PN":"កោះភីតកាន","PR":"ព័រតូរីកូ","PS":"ដែនដីប៉ាឡេស្ទីន","PT":"ព័រទុយហ្កាល់","PW":"ផៅឡូ","PY":"ប៉ារ៉ាហ្គាយ","QA":"កាតា","QO":"តំបន់ជាយអូសេអានី","RE":"រេអុយញ៉ុង","RH":"ស៊ីមបាវ៉េ","RO":"រូម៉ានី","RS":"សែប៊ី","RU":"រុស្ស៊ី","RW":"រវ៉ាន់ដា","SA":"អារ៉ាប៊ីសាអូឌីត","SB":"កោះសូឡូម៉ុង","SC":"សីស្ហែល","SD":"ស៊ូដង់","SE":"ស៊ុយអែត","SG":"សិង្ហបុរី","SH":"សង់ហេឡេណា","SI":"ស្លូវេនី","SJ":"ស្វាលបាដ និង ហ្សង់ម៉ាយេន","SK":"ស្លូវ៉ាគី","SL":"សៀរ៉ាឡេអូន","SM":"សានម៉ារីណូ","SN":"សេណេហ្គាល់","SO":"សូម៉ាលី","SR":"សូរីណាម","SS":"ស៊ូដង់ខាងត្បូង","ST":"សៅតូម៉េ និង ប្រាំងស៊ីប","SU":"រុស្ស៊ី","SV":"អែលសាល់វ៉ាឌ័រ","SX":"សីងម៉ាធីន","SY":"ស៊ីរី","SZ":"ស្វាស៊ីឡង់","TA":"ទ្រីស្តង់ដាចូនហា","TC":"កោះទួគ និង កៃកូស","TD":"ឆាដ","TF":"ដែនដីបារាំងនៅភាគខាងត្បូង","TG":"តូហ្គោ","TH":"ថៃ","TJ":"តាហ្ស៊ីគីស្ថាន","TK":"តូខេឡៅ","TL":"ទីម័រលេស្តេ","TM":"តួកម៉េនីស្ថាន","TN":"ទុយនីស៊ី","TO":"តុងហ្គា","TP":"ទីម័រលេស្តេ","TR":"តួកគី","TT":"ទ្រីនីដាត និងតូបាហ្គោ","TV":"ទូវ៉ាលូ","TW":"តៃវ៉ាន់","TZ":"តង់សានី","UA":"អ៊ុយក្រែន","UG":"អ៊ូហ្គង់ដា","UK":"ចក្រភពអង់គ្លេស","UM":"កោះអៅឡាយីងអាមេរិក","UN":"អង្គការសហប្រជាជាតិ","US":"សហរដ្ឋអាមេរិក","UY":"អ៊ុយរូហ្គាយ","UZ":"អ៊ូសបេគីស្ថាន","VA":"បុរីវ៉ាទីកង់","VC":"សាំងវ៉ាំងសង់ និង ហ្គ្រេណាឌីន","VD":"វៀតណាម","VE":"វ៉េណេស៊ុយអេឡា","VG":"កោះវឺជិនចក្រភពអង់គ្លេស","VI":"កោះវឺជីនអាមេរិក","VN":"វៀតណាម","VU":"វ៉ានូទូ","WF":"វ៉ាលីស និងហ្វូទូណា","WS":"សាម័រ","XK":"កូសូវ៉ូ","YD":"យេម៉ែន","YE":"យេម៉ែន","YT":"ម៉ាយុត","YU":"សែប៊ី","ZA":"អាហ្វ្រិកខាងត្បូង","ZM":"សំប៊ី","ZR":"កុងហ្គោ- គីនស្ហាសា","ZW":"ស៊ីមបាវ៉េ","ZZ":"តំបន់មិនស្គាល់"};
  var names = null;
  try { names = new Intl.DisplayNames(['km', 'en'], { type: 'region' }); } catch (e) { /* old browser */ }
  function countryName(cc) {
    if (cc === 'XX') return 'មិនស្គាល់';
    if (KM[cc]) return KM[cc];
    try { return (names && names.of(cc)) || cc; } catch (e) { return cc; }
  }
  function flag(cc) {
    if (cc === 'XX' || !/^[A-Z]{2}$/.test(cc)) return '<span class="vc-flag vc-flag-x" aria-hidden="true">?</span>';
    return '<img class="vc-flag" src="' + FLAGS + cc.toLowerCase() + '.svg" alt="" width="24" height="18" loading="lazy">';
  }
  var digits = function (s) { return String(s).replace(/\d/g, function (d) { return '០១២៣៤៥៦៧៨៩'[d]; }); };
  function khDate(iso) {
    var p = iso.split('-');
    return digits(Number(p[2])) + ' ' + MONTHS[Number(p[1]) - 1] + ' ' + digits(p[0]);
  }
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  function render(s) {
    var val = {
      visitors: num(s.visitors), views: num(s.views), today: num(s.today.visitors),
      countries: num(s.countries.length), since: khDate(s.since),
    };
    document.querySelectorAll('[data-vc]').forEach(function (el) {
      var k = el.getAttribute('data-vc');
      if (k in val) el.textContent = val[k];
    });
    var top = s.countries[0] ? s.countries[0][1] : 1;
    document.querySelectorAll('[data-vc-list]').forEach(function (ul) {
      var max = Number(ul.getAttribute('data-vc-list')) || 10;
      ul.innerHTML = s.countries.slice(0, max).map(function (c) {
        var name = esc(countryName(c[0]));
        return '<li>' + flag(c[0]) + '<span class="vc-name">' + name + '</span>' +
          '<span class="vc-bar"><i style="width:' + Math.max(3, Math.round(100 * c[1] / top)) + '%"></i></span>' +
          '<b>' + num(c[1]) + '</b></li>';
      }).join('') || '<li class="vc-empty">មិនទាន់មានទិន្នន័យ</li>';
    });
    document.querySelectorAll('[data-vc-flags]').forEach(function (el) {
      var max = Number(el.getAttribute('data-vc-flags')) || 8;
      el.innerHTML = s.countries.slice(0, max).map(function (c) {
        return '<span class="vc-chip" title="' + esc(countryName(c[0])) + ' · ' + num(c[1]) + '">' + flag(c[0]) + '</span>';
      }).join('');
    });
    document.querySelectorAll('[data-vc-box]').forEach(function (el) { el.hidden = false; el.classList.add('vc-ready'); });
  }

  // pages drawn later (the CBA app's home page) ask for the numbers again
  var got = null;
  window.kmVisits = { refresh: function () { if (got) render(got); } };

  var req = live
    ? fetch(API + '/hit?new=' + (isNew ? 1 : 0) + '&site=' + encodeURIComponent(site), { method: 'POST', credentials: 'omit' })
    : fetch(API + '/stats', { credentials: 'omit' });
  req.then(function (r) { return r.ok ? r.json() : null; })
    .then(function (s) { if (s && s.countries) { got = s; render(s); } })
    .catch(function () { /* offline or blocked: the counters simply stay hidden */ });
})();
