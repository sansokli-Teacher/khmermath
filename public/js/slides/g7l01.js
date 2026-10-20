window.TEACH_LESSONS = window.TEACH_LESSONS || {};
window.TEACH_LESSONS['7'] = ['ចំនួនគត់', 'តួចែកនិងពហុគុណ', 'ចំនួនគត់រ៉ឺឡាទីប', 'ប្រភាគ', 'ចំនួនទសភាគ', 'ភាគរយ', 'រង្វាស់រង្វាល់', 'កន្សោមពីជគណិត', 'សមីការដឺក្រេទីមួយមានមួយអញ្ញាត', 'វិសមភាព', 'ផលធៀបនិងសមាមាត្រ', 'សញ្ញាណដំបូងនៃធរណីមាត្រ'];

window.TEACH_SLIDES = window.TEACH_SLIDES || {};
window.TEACH_SLIDES['7-1'] = [
  {
    k: 'title',
    html: String.raw`<p class="ts-kicker">ថ្នាក់ទី ៧ · មេរៀនទី ១</p>
      <h1>ចំនួនគត់</h1>
      <p class="ts-sub">សំណុំ \(\mathbb{Z}\) · អ័ក្សចំនួន · ប្រមាណវិធី</p>`,
  },
  {
    html: String.raw`<h2>គោលបំណង</h2>
      <ul class="ts-bullets">
        <li>ស្គាល់ចំនួនគត់វិជ្ជមាន អវិជ្ជមាន និងសូន្យ</li>
        <li>តំណាងចំនួនគត់លើអ័ក្ស</li>
        <li>ប្រៀបធៀប និងគណនា \(+\ -\ \times\ \div\)</li>
        <li>ប្រើតម្លៃដាច់ខាត \(|n|\)</li>
      </ul>`,
  },
  {
    html: String.raw`<h2>តើចំនួនគត់ជាអ្វី?</h2>
      <p>ចំនួនគត់គឺចំនួនដែលគ្មានផ្នែកប្រភាគ។ សំណុំចំនួនគត់សរសេរ \(\mathbb{Z}\)</p>
      <p class="ts-eq">\(\mathbb{Z} = \{\ldots,-3,-2,-1,0,1,2,3,\ldots\}\)</p>
      <div class="ts-3">
        <div class="ts-card"><b>វិជ្ជមាន</b><span>\(1, 2, 3, \ldots\)</span></div>
        <div class="ts-card"><b>សូន្យ</b><span>\(0\)</span></div>
        <div class="ts-card"><b>អវិជ្ជមាន</b><span>\(-1, -2, -3, \ldots\)</span></div>
      </div>`,
  },
  {
    html: String.raw`<h2>អ័ក្សចំនួនគត់</h2>
      <p>ចំនួនធំជាងស្ថិតនៅខាងស្ដាំ។ ចំនួនតូចជាងស្ថិតនៅខាងឆ្វេង។</p>
      <div class="ts-axis" aria-hidden="true">
        <span>−4</span><span>−3</span><span>−2</span><span>−1</span><span class="z">0</span><span>1</span><span>2</span><span>3</span><span>4</span>
      </div>
      <p class="ts-note">គម្លាតរវាងចំនួនជាប់គ្នា ស្មើ ១ គ្រប់គូ។</p>`,
  },
  {
    html: String.raw`<h2>តម្លៃដាច់ខាត</h2>
      <p>\(|n|\) គឺចម្ងាយពី \(n\) ដល់ \(0\) លើអ័ក្ស (តម្លៃមិនអវិជ្ជមាន)។</p>
      <p class="ts-eq">\(|5| = 5 \qquad |-5| = 5 \qquad |0| = 0\)</p>
      <ul class="ts-bullets">
        <li>ប្រសិន \(n \ge 0\) នោះ \(|n| = n\)</li>
        <li>ប្រសិន \(n < 0\) នោះ \(|n| = -n\)</li>
      </ul>`,
  },
  {
    html: String.raw`<h2>ការប្រៀបធៀប</h2>
      <p>លើអ័ក្ស លេខខាងឆ្វេងតូចជាង លេខខាងស្ដាំធំជាង។</p>
      <p class="ts-eq">\(-7 < -2 < 0 < 3 < 10\)</p>
      <div class="ts-2">
        <div class="ts-card"><b>ឧទាហរណ៍</b><span>\(-8 < -1\)</span></div>
        <div class="ts-card"><b>ឧទាហរណ៍</b><span>\(4 > -9\)</span></div>
      </div>`,
  },
  {
    html: String.raw`<h2>ការបូកចំនួនគត់</h2>
      <ul class="ts-bullets">
        <li>សញ្ញាដូចគ្នា៖ បូកតម្លៃដាច់ខាត រក្សាសញ្ញា</li>
        <li>សញ្ញាផ្ទុយគ្នា៖ ដកតម្លៃដាច់ខាត យកសញ្ញាចំនួនធំ</li>
      </ul>
      <p class="ts-eq">\(6+9=15 \qquad (-6)+(-9)=-15\)</p>
      <p class="ts-eq">\(12+(-5)=7 \qquad (-12)+5=-7\)</p>`,
  },
  {
    html: String.raw`<h2>ការដកចំនួនគត់</h2>
      <p>ដក \(b\) គឺបូកចំនួនផ្ទុយនៃ \(b\)</p>
      <p class="ts-eq">\(a - b = a + (-b)\)</p>
      <p class="ts-eq">\(8-3=5 \qquad 3-8=-5 \qquad -4-7=-11\)</p>
      <p class="ts-eq">\(-4-(-7)=-4+7=3\)</p>`,
  },
  {
    html: String.raw`<h2>គុណចំនួនគត់</h2>
      <div class="ts-2">
        <div class="ts-card"><b>សញ្ញាដូច</b><span>លទ្ធផលវិជ្ជមាន</span></div>
        <div class="ts-card"><b>សញ្ញាផ្ទុយ</b><span>លទ្ធផលអវិជ្ជមាន</span></div>
      </div>
      <p class="ts-eq">\((+4)\times(+3)=12 \qquad (-4)\times(-3)=12\)</p>
      <p class="ts-eq">\((+4)\times(-3)=-12 \qquad (-4)\times(+3)=-12\)</p>`,
  },
  {
    html: String.raw`<h2>ចែកចំនួនគត់</h2>
      <p>ក្បួនសញ្ញាដូចគុណ។ មិនចែកនឹង \(0\)។</p>
      <p class="ts-eq">\(18\div 3=6 \qquad (-18)\div(-3)=6\)</p>
      <p class="ts-eq">\(18\div(-3)=-6 \qquad (-18)\div 3=-6\)</p>
      <p class="ts-note">ប្រសិនលទ្ធផលមិនមែនចំនួនគត់ នោះវាជាប្រភាគ (មេរៀនក្រោយ)។</p>`,
  },
  {
    html: String.raw`<h2>លំហាត់ថ្នាក់</h2>
      <ol class="ts-ex">
        <li>គណនា \( (-15)+8 \)</li>
        <li>គណនា \( 6-(-9) \)</li>
        <li>គណនា \( (-7)\times(-4) \)</li>
        <li>គណនា \( (-36)\div 9 \)</li>
        <li>តើ \(-11\) និង \(-3\) មួយណាធំជាង?</li>
      </ol>`,
  },
  {
    html: String.raw`<h2>ចម្លើយលំហាត់</h2>
      <ol class="ts-ex">
        <li>\(-7\)</li>
        <li>\(15\)</li>
        <li>\(28\)</li>
        <li>\(-4\)</li>
        <li>\(-3 > -11\)</li>
      </ol>`,
  },
  {
    html: String.raw`<h2>សង្ខេប</h2>
      <ul class="ts-bullets">
        <li>\(\mathbb{Z}\) មានវិជ្ជមាន អវិជ្ជមាន និង \(0\)</li>
        <li>អ័ក្ស៖ ឆ្វេងតូច ស្ដាំធំ</li>
        <li>\(|n|\) = ចម្ងាយពីសូន្យ</li>
        <li>ដក = បូកចំនួនផ្ទុយ · សញ្ញាគុណ/ចែកដូចគ្នា</li>
      </ul>
      <p class="ts-foot">KhmerMath · ថ្នាក់ទី ៧ · មេរៀនទី ១</p>`,
  },
];
