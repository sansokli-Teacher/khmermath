"""Grade 8 Lesson 12 «ការប្រៀបធៀបត្រីកោណ» -> public/js/slides/g8/lesson12.js        python3 tools/lesson8_12/build.py
Follows the MoEYS textbook lesson 12 (pp. 141-157): 1 congruent triangles (definition, ម.ជ.ម, ជ.ម.ជ, ជ.ជ.ជ, right triangles អ.ម and អ.ជ),
2 mediator of a segment and the isosceles triangle, 3 inequalities in a triangle, 4 perpendicular and slanted segments.
The cases are taught in the same order and with the same wording as the author's class slides (ESC_មេរៀនទី១២-01 / -02).
Every picture is computed from coordinates (geo8.py) and the facts it shows are asserted; every numeric answer is checked here."""
import math, json, os, sys, re
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'lesson1'))
sys.path.insert(0, HERE)
from lib import stepify, slide, part, key, ex, prac, m, dm, p, ul, ol, hl, fig, rvd, cols
import geo8 as G

OUT = os.path.join(HERE, '..', '..', 'public', 'js', 'slides', 'g8', 'lesson12.js')
S = []
NAVY, TEAL, ORANGE, GREEN, PURPLE, RED = '#0f5173', '#2b8a87', '#e8590c', '#2f9e44', '#ae3ec9', '#ee0000'


def hl(t, color='#ee0000'):          # the red of the class slides is EE0000
    return f'<b style="color:{color}">{t}</b>'

_BOX = '<div style="border:3px solid #0f5173;border-radius:14px;padding:.4em 1em;background:#f2f2f2;margin:.3em 0">'


def kh(n):
    return str(n).translate(str.maketrans('0123456789', '០១២៣៤៥៦៧៨៩'))


def lines(items):
    """one line per press of →: step 1, 2, 3 ... (the same numbers as the picture's steps)"""
    return ''.join(rvd(i, h) for i, h in enumerate(items, 1))


def lines0(items):
    """the first line is on the slide from the start (picture step 0), the others follow with the pictures steps 1, 2, ..."""
    return items[0] + ''.join(rvd(i, h) for i, h in enumerate(items[1:], 1))


def exfig(kick, title, svgstr, items, given='', first_visible=False):
    return ex(kick, title, (p(given) if given else '') + cols(fig(svgstr), lines0(items) if first_visible else lines(items)))


def whole(svgstr):
    """a picture with every step showing at once"""
    return re.sub(r' data-(step|until)="\d+"', '', svgstr)


def theorem(kick, title, rule, svgstr, cond=''):
    """a rule in a box, its picture beside it"""
    return ex(kick, title, cols(fig(whole(svgstr), cond), _BOX + rule + '</div>'))


def box3(a, b, c, mid_note='', arrows=('→', '→')):
    """សម្មតិកម្ម → សន្និដ្ឋាន → វិបាក, one box per press of →"""
    def one(head, body, col, step):
        return rvd(step, f'<div style="border:4px solid {col};border-radius:16px;background:#fff;overflow:hidden;text-align:center">'
                         f'<div style="background:{col};color:#fff;font-weight:800;padding:.2em .4em">{head}</div>'
                         f'<div style="padding:.3em .5em;min-height:6.6em;display:flex;flex-direction:column;justify-content:center">{body}</div></div>')
    def arrow(step, t):
        return rvd(step, f'<div style="align-self:center;font-size:2em;color:#868e96;text-align:center;padding-top:1.6em">{t}</div>')
    row = (f'<div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:.3em;align-items:start">'
           + one('សម្មតិកម្ម', a, NAVY, 1) + arrow(2, arrows[0]) + one('សន្និដ្ឋាន', b, NAVY, 2) + arrow(3, arrows[1]) + one('វិបាក', c, RED, 3) + '</div>')
    return row


def gridn(n, *items, gap='.5em'):
    return f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:{gap};align-items:start">' + ''.join(f'<div>{x}</div>' for x in items) + '</div>'


def gr(t):
    return hl(t, '#595959')


def ask(q, ans, step):
    """a question for the pupils (step) and its answer on the next click"""
    return (rvd(step, f'<div class="ask">សួរសិស្ស៖ {q}</div>') + rvd(step + 1, f'<div class="ask ans">{ans}</div>'))


def mline(*items):
    return ''.join(p(m(x)) for x in items)


def cond(name):
    return hl(name, NAVY)


# ================================================================ the opening, in the order of the class slides (ESC_មេរៀនទី១២-02)
def part(idx, num, title, top, hook='', band=None):
    """the divider of a part (the template's slide 4): navy block, framed name, ornament.  data-part = the number in the lesson's list of parts"""
    return {'k': 'title', 'c': 'esc', 'part': idx, 'band': band or f'{num} {title}',
            'html': f'<div class="esc-div" data-part="{idx}"><div class="esc-div-top">{top}</div><div class="esc-div-box"><h1>{(num + ' ') if num else ''}{title}</h1></div>'
                    f'<img class="esc-orn" src="/img/esc-ornament.png" alt=""><div class="esc-div-sub">{hook}</div></div>'}


def _card(t, svgstr, cap, col):
    return (f'<div style="border:3px solid {col};border-radius:14px;background:#fff;overflow:hidden;text-align:center">'
            f'<div style="background:{col};color:#fff;font-weight:800;padding:.2em">{t}</div><div style="width:78%;margin:auto">{fig(svgstr)}</div>'
            f'<div style="padding:0 .4em .4em;font-weight:700">{cap}</div></div>')


def _PF(top, key, a, b):
    return (f'<div class="pf-r" style="top:{top}%"><span data-edit="{key}_l">{a}</span><span>:</span><span data-edit="{key}_v">{b}</span></div>')


S.append({'k': 'title', 'c': 'esc-profile', 'raw': True,
          'html': '<div class="pf-t" data-edit="title">ប្រវត្តិរូបសង្ខេប</div>' + _PF(32, 'grade', 'បង្រៀនថ្នាក់', 'ទី៨') + _PF(46, 'subject', 'មុខវិជ្ជា', 'គណិតវិទ្យា')
                  + _PF(60, 'level', 'ក្របខណ្ឌបង្រៀន', 'គ្រូកម្រិតមូលដ្ឋាន') + _PF(74, 'exp', 'បទពិសោធន៍បង្រៀន', '១០ឆ្នាំ')
                  + '<div class="pf-name" data-edit="name">លោកគ្រូ សាន សុខលី</div>'
                  + '<div class="pf-img pf-photo" data-img="photo" title="ចុចដើម្បីដូររូបថត"><span>ដូររូបថត</span></div>'
                  + '<div class="pf-img pf-logo" data-img="logo" title="ចុចដើម្បីដូរឡូហ្គោសាលា"><span>ដូរឡូហ្គោ</span><div class="pf-logos">' + ''.join(f'<button type="button" data-logo="{u}" title="{t}"><img src="{u}" alt=""><i>{t}</i></button>' for t, u in (('SW', '/img/logos/sw.png'), ('YK', '/img/logos/yk.png'), ('BT', '/img/logos/bt.png'), ('ESC', '/img/esc/logo.png'))) + '<button type="button" data-logo="upload" title="រូបផ្ទាល់ខ្លួន"><b>+</b><i>រូបខ្លួន</i></button></div></div>'
                  + '<div class="pf-hint">ចុចលើអក្សរ ឬរូបភាព ដើម្បីកែ · <button type="button" data-pf-reset>កំណត់ដើមវិញ</button></div>'})

S.append({'k': 'ex', 'raw': True, 'nostep': True, 'html': '<p class="ts-kicker">សៀវភៅសិក្សាគោល គណិតវិទ្យាថ្នាក់ទី៨</p>'
          '<div class="esc-book"><img src="/img/esc/textbook.jpg" alt=""><div class="bk-t">ប្អូនៗអាចសិក្សាបន្ថែមនៅក្នុង<br>សៀវភៅសិក្សាគោល<br>គណិតវិទ្យាថ្នាក់ទី៨<br><b>ទំព័រ ១៤១-១៥៧</b></div></div>'})

S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">រំលឹកមេរៀន</p><h2>❑ ចំណេះដឹងដែលយើងនឹងប្រើក្នុងមេរៀនថ្ងៃនេះ</h2>'
          + gridn(3, _card('មុំទល់កំពូល', G.recall_vertical(), 'មុំទល់កំពូល ' + hl('ប៉ុនគ្នា'), NAVY),
                  _card('មុំឆ្លាស់ក្នុង', G.recall_alt(), 'បើ ' + m(r'a\parallel b') + ' មុំឆ្លាស់ក្នុង ' + hl('ប៉ុនគ្នា'), NAVY),
                  _card('ផលបូកមុំក្នុងត្រីកោណ', G.recall_sum(), m(r'\angle A+\angle B+\angle C=180^\circ'), NAVY))
          + '<div style="border:3px solid #0f5173;border-radius:14px;background:#f2f2f2;padding:.3em 1em;margin-top:.5em">'
          + p(hl('សំណួរ ៖', RED) + ' ' + m(r'\Delta ABC') + ' មាន ' + m(r'\angle A=60^\circ') + ' និង ' + m(r'\angle B=40^\circ') + ' ។ រក ' + m(r'\angle C') + ' ?')
          + rvd(1, p(hl('ចម្លើយ ៖', RED) + ' ' + m(r'\angle C=180^\circ-(60^\circ+40^\circ)=') + hl(m(r'80^\circ')))) + '</div>'})
assert 180 - (60 + 40) == 80

S.append({'k': 'title', 'c': 'esc', 'raw': True,
          'html': '<div class="esc-div"><div class="esc-div-top">មេរៀនទី ១២</div><div class="esc-div-box"><h1>ការប្រៀបធៀបត្រីកោណ</h1></div>'
                  '<img class="esc-orn" src="/img/esc-ornament.png" alt=""></div>'})

S.append({'k': 'ex', 'raw': True, 'nostep': True, 'html': '<p class="ts-kicker">វត្ថុបំណងមេរៀន</p><h2>❑ បន្ទាប់ពីបានសិក្សាមេរៀននេះចប់ប្អូនៗ៖</h2>'
          + ''.join(p(hl(a_, RED) + ' ' + b_) for a_, b_ in [
              ('វិជ្ជាសម្បទា :', 'ចង្អុលបង្ហាញត្រីកោណប៉ុនគ្នា ទំនាក់ទំនងរវាងជ្រុងនិងមុំក្នុងត្រីកោណ និងវិសមភាពត្រីកោណបានច្បាស់លាស់ តាមរយៈការសង្កេតរូប និងការឆ្លើយសំណួររបស់គ្រូ។'),
              ('បំណិនសម្បទា :', 'សង់ និងប្រៀបធៀបត្រីកោណតាមលក្ខខណ្ឌ ម.ជ.ម ជ.ម.ជ ជ.ជ.ជ អ.ម និង អ.ជ ហើយទាញរកវិបាក ដើម្បីដោះស្រាយលំហាត់បានត្រឹមត្រូវ។'),
              ('ចរិយាសម្បទា :', 'មានស្មារតីម៉ត់ចត់ យកចិត្តទុកដាក់ និងសហការគ្នា ក្នុងការសង់រូប និងដោះស្រាយលំហាត់។')])})

# ================================================================ 1. congruent triangles
S.append({'mark': 'S11'})

S.append(ex('១.១', 'ឧទាហរណ៍ ៖ ',
    cols(p('គូសត្រីកោណ ' + m('ABC') + ' មួយនៅលើក្រដាសកាតុង ហើយកាត់វាចេញ ។ ប្រើរូប ' + m('ABC') + ' ជាគំរូ ដើម្បីគូស និងកាត់ត្រីកោណ ' + m("A'B'C'") + ' ។')
         + rvd(1, p('ដាក់ ' + m('ABC') + ' ត្រួតលើ ' + m("A'B'C'") + ' ៖ ធាតុនីមួយៗត្រួតស៊ីគ្នានឹងធាតុត្រូវគ្នា ។'))
         + rvd(2, '<div style="border:3px solid #0f5173;border-radius:14px;background:#f2f2f2;padding:.3em 1em;text-align:center">គេថា ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' ជា' + hl('ត្រីកោណប៉ុនគ្នា') + ' ។</div>')
         + ask('តើធាតុ (មុំ និងជ្រុង) ដែលត្រួតស៊ីគ្នាមានប៉ុន្មានគូ?', 'ធាតុ ' + hl('៦') + ' គូ ៖ មុំ ៣ គូ និងជ្រុង ៣ គូ ។', 3),
         '<div class="cfig"><div style="text-align:center;color:#595959">ក្រដាសកាតុងទី១</div>' + '<div class="bigfig">' + fig(G.cong_vert_move()) + '</div>' + '<div style="text-align:center;color:#595959">ក្រដាសកាតុងទី២</div>'
         + rvd(1, 'ត្រួតស៊ីគ្នា ✓', 'late okmid') + '</div>')))

def _row(st, l, r):
    return rvd(st, f'<div class="cmrow"><span>{m(l)}</span><span>{m(r)}</span></div>')


S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p>'
    '<p>គេកំណត់សរសេរ ' + m(r"\Delta ABC\cong\Delta A'B'C'") + ' ។ ធាតុត្រូវគ្នាប៉ុនគ្នាដូចខាងក្រោម៖</p>'
    '<div class="cmgrid"><div class="cmtab"><div class="cmhead"><span>មុំត្រូវគ្នា</span><span>ជ្រុងត្រូវគ្នា</span></div>'
    + _row(1, r"\angle A=\angle A'", "AB=A'B'") + _row(2, r"\angle B=\angle B'", "AC=A'C'") + _row(3, r"\angle C=\angle C'", "BC=B'C'") + '</div>'
    '<div class="cmfig">' + fig(G.cong_marks2()) + '<div class="cmcap">សញ្ញាដូចគ្នា = ធាតុប៉ុនគ្នា</div></div></div>'
    + rvd(4, '<div class="cmbox">ធាតុត្រូវគ្នា = មុំ ៣ + ជ្រុង ៣ (សរុប ' + hl('ធាតុ ៦') + ')</div>')})

S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p>'
    '<div class="defbox">' + hl('និយមន័យ៖') + ' ត្រីកោណពីរជាត្រីកោណប៉ុនគ្នា លុះត្រាតែធាតុត្រូវគ្នាជាធាតុប៉ុនគ្នា ។</div>'
    '<div class="defrow"><div class="deffig">' + fig(G.def_pair()) + '<div class="defcap">' + m(r"\Delta ABC\cong\Delta A'B'C'") + '</div></div>'
    + rvd(1, '<div class="defarrow"><svg viewBox="0 0 120 60" width="100%"><polygon points="0,30 38,0 38,18 82,18 82,0 120,30 82,60 82,42 38,42 38,60" fill="#d9291c"/></svg></div>')
    + rvd(1, '<div class="defeq">' + p(m(r"\angle A=\angle A'\ ,\ AB=A'B'")) + p(m(r"\angle B=\angle B'\ ,\ AC=A'C'")) + p(m(r"\angle C=\angle C'\ ,\ BC=B'C'")) + '</div>') + '</div>'
    + rvd(2, p(hl('ចំណាំ៖') + ' សរសេរកំពូលត្រូវគ្នាតាមលំដាប់ដូចគ្នា ' + m(r"A\leftrightarrow A'\ ,\ B\leftrightarrow B'\ ,\ C\leftrightarrow C'") + ' ។'))})

def _bul(x):
    return f'<p class="bul"><span class="dia">❖</span>{x}</p>'


S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p>'
    '<h2><span class="h-lab">លំហាត់គំរូ៖</span> <span class="h-txt">បើត្រីកោណពីរជាត្រីកោណប៉ុនគ្នា តើអ្នកអាចសន្និដ្ឋានបានដូចម្តេច? ចូរឱ្យឧទាហរណ៍ពន្យល់ចម្លើយរបស់អ្នក ។</h2>'.replace('</h2>', '') + '</span></h2>'
    '<div class="sqgrid"><div>'
    + rvd(1, '<h2 class="solh"><span class="h-lab">ដំណោះស្រាយ៖</span></h2>' + p('ធាតុត្រូវគ្នានីមួយៗសុទ្ធតែជាធាតុប៉ុនគ្នា ។') + p('បើ ' + m(r"\Delta ABC\cong\Delta A'B'C'") + ' នោះ៖')
          + _bul(m(r"\angle A=\angle A'\ ,\ AB=A'B'")) + _bul(m(r"\angle B=\angle B'\ ,\ AC=A'C'")) + _bul(m(r"\angle C=\angle C'\ ,\ BC=B'C'\ ។")))
    + '</div><div class="sqfig">' + fig(G.pair_ticks()) + '</div></div>'})

S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p>'
    '<h2><span class="h-lab">ប្រតិបត្តិ៖</span> <span class="h-txt">ពន្យល់ថា ហេតុអ្វីបានជាត្រីកោណទាំងពីរនេះមិនប៉ុនគ្នា?</span></h2><span class="esc-chip tr">គិត ២ នាទី</span>'
    '<div class="pfig">' + fig(G.pair_angles()) + '</div>'
    + rvd(2, '<div class="ansbox">' + hl('ចម្លើយ៖') + ' មុំត្រូវគ្នា ' + '<span class="plain">∠S = 50° ≠ ∠D = 60°</span>' + ' ដូចនេះ ' + m(r'\Delta STR') + ' និង ' + m(r'\Delta DEF') + ' មិនប៉ុនគ្នា ។</div>')})
assert 50 != 60

S.append({'mark': 'OVERVIEW'})
# ---- 1.2 the three conditions
S.append(ex('១.២', 'លក្ខខណ្ឌនៃត្រីកោណប៉ុនគ្នា',
    p('ត្រីកោណពីរប៉ុនគ្នា កាលណាធាតុត្រូវគ្នា' + hl('ទាំង ៦') + ' ប៉ុនគ្នា។ ប៉ុន្តែ គេសិក្សាតែ' + hl('ធាតុ ៣') + ' ប៉ុនរៀងគ្នា តាមលក្ខខណ្ឌខាងក្រោម៖')
    + gridn(3, rvd(1, _card('ម.ជ.ម', G.mini('asa'), 'ជ្រុងមួយប៉ុនគ្នាជាប់និងមុំពីរប៉ុនរៀងគ្នា', '#1c7ed6')),
            rvd(2, _card('ជ.ម.ជ', G.mini('sas'), 'មុំមួយប៉ុនគ្នាអមដោយជ្រុងពីរប៉ុនរៀងគ្នា', '#2b8a87')),
            rvd(3, _card('ជ.ជ.ជ', G.mini('sss'), 'ជ្រុងទាំងបីប៉ុនរៀងគ្នា', '#f08c00')))))

S.append({'mark': 'ASA'})
# ---- 1.2.1 ម.ជ.ម
def _step(n, html, st):
    t = f'<div class="esc-step"><span class="num">{kh(n)}</span><span>{html}</span></div>'
    return t if st == 0 else rvd(st, t)


S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p><p class="esc-sec">❑ ១.២.១. ជ្រុងមួយ និងមុំពីរជាប់គ្នាប៉ុនរៀងគ្នា (ម.ជ.ម)</p>'
    '<p><span class="h-lab">ឧទាហរណ៍៖</span> សង់ ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' ដែល ' + m(r"\angle A=\angle A'=60^\circ") + ' , ' + m(r"\angle B=\angle B'=40^\circ") + ' និង ' + m(r"AB=A'B'=6\text{ cm}") + ' រួចប្រៀបធៀបត្រីកោណទាំងពីរ ។</p>'
    '<div class="cgrid"><div>'
    + _step(1, 'គូសអង្កត់ ' + m(r'AB=6\text{ cm}') + ' នៅលើបន្ទាត់ ' + m('l'), 0)
    + _step(2, 'ប្រើរ៉ាប់ទ័រ គូសមុំ ' + m(r'60^\circ') + ' ត្រង់ ' + m('A') + ' និង ' + m(r'40^\circ') + ' ត្រង់ ' + m('B'), 1)
    + _step(3, 'ជ្រុងនៃមុំទាំងពីរជួបគ្នាត្រង់ ' + m('C') + ' ➜ បាន ' + m(r'\Delta ABC'), 3)
    + _step(4, 'សង់ ' + m(r"\Delta A'B'C'") + ' តាមរបៀបដូចគ្នា', 4)
    + '</div><div class="cfig">' + fig(G.asa_construct2()) + '</div></div>'})

S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p><p class="esc-sec">❑ ១.២.១. ជ្រុងមួយ និងមុំពីរជាប់គ្នាប៉ុនរៀងគ្នា (ម.ជ.ម)</p>'
    '<p><span class="h-lab">ឧទាហរណ៍៖</span> សង់ ' + m(r"\Delta A'B'C'") + ' តាមរបៀបដូចគ្នានឹង ' + m(r'\Delta ABC') + ' ។</p>'
    '<div class="cgrid"><div>'
    + _step(1, 'គូសអង្កត់ ' + m(r"A'B'=6\text{ cm}") + ' នៅលើបន្ទាត់ ' + m('l'), 0)
    + _step(2, 'ប្រើរ៉ាប់ទ័រ គូសមុំ ' + m(r'60^\circ') + ' ត្រង់ ' + m("A'") + ' និង ' + m(r'40^\circ') + ' ត្រង់ ' + m("B'"), 1)
    + _step(3, 'ជ្រុងនៃមុំទាំងពីរជួបគ្នាត្រង់ ' + m("C'") + ' ➜ បាន ' + m(r"\Delta A'B'C'"), 3)
    + _step(4, 'ប្រៀបធៀប ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' (ស្លាយបន្ទាប់)', 4)
    + '</div><div class="cfig">' + fig(G.asa_construct2(True)) + '</div></div>'})


S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p><p class="esc-sec">❑ ប្រៀបធៀប ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + '</p>'
    '<div class="cgrid" style="grid-template-columns:54% 1fr"><div><p>យក ' + m(r'\Delta ABC') + ' ដាក់ត្រួតលើ ' + m(r"\Delta A'B'C'") + ' ដោយឱ្យ ' + m('AB') + ' ត្រួតលើ ' + m("A'B'") + '</p>'
    + rvd(2, _bul(m('AC') + ' ត្រួតលើ ' + m("A'C'") + ' ព្រោះ ' + m(r"\angle A=\angle A'=60^\circ")))
    + rvd(3, _bul(m('BC') + ' ត្រួតលើ ' + m("B'C'") + ' ព្រោះ ' + m(r"\angle B=\angle B'=40^\circ")))
    + rvd(4, '<div class="cmbox">ធាតុត្រូវគ្នាប៉ុនគ្នា ➜ ' + m(r"\Delta ABC\cong\Delta A'B'C'", ) + '</div>')
    + '</div><div class="cfig">' + fig(G.overlay_vert()) + rvd(4, '<div class="okmid" style="top:40%">ត្រួតស៊ីគ្នា ✓</div>') + '</div></div>'})

def theorem_slide(case, rule, fg, cap_case):
    """class slide 16: the theorem in a big grey box, the two marked triangles under it, a «វិបាក» card on the right"""
    return {'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p>'
            f'<div class="defbox" style="text-align:left">{hl(f"ទ្រឹស្តីបទ ({case})៖")} {rule}</div>'
            '<div class="throw"><div class="thfig">' + fig(fg) + '<div class="defcap" style="font-weight:800;font-style:italic">' + m(r"\Delta ABC\cong\Delta A'B'C'") + f' ({case})</div></div>'
            + rvd(1, '<div class="thcard"><div class="thh">វិបាក</div><div class="thb"><div>បន្ទាប់ពីប្រៀបធៀបឱ្យត្រីកោណពីរប៉ុនគ្នារួច គេទាញបាន' + hl('ធាតុត្រូវគ្នាដទៃទៀតប៉ុនគ្នា', NAVY) + ' ហៅថា ' + hl('វិបាក') + ' ។</div></div></div>') + '</div>'}


S.append(theorem_slide('ម.ជ.ម', 'ត្រីកោណពីរជាត្រីកោណប៉ុនគ្នា កាលណាវាមាន' + hl('ជ្រុងមួយប៉ុនគ្នា', NAVY) + ' និង' + hl('មុំពីរជាប់នឹងជ្រុងនោះប៉ុនរៀងគ្នា', NAVY) + ' ។', G.pair_asa(), 'ម.ជ.ម'))

S.append(ex('វិបាក', 'ពីលក្ខខណ្ឌ ម.ជ.ម យើងទាញបានវិបាកដូចខាងក្រោម',
    box3(mline(r"\angle A=\angle A'", "AB=A'B'", r"\angle B=\angle B'"), p(m(r"\Delta ABC\cong\Delta A'B'C'")) + p(hl('(តាមលក្ខខណ្ឌ ម.ជ.ម)', RED)),
         mline("AC=A'C'", "BC=B'C'", r"\angle C=\angle C'"))
    + rvd(3, p('ចំណាំ ៖ ' + hl('វិបាក') + ' គឺជាធាតុត្រូវគ្នា ៣ ទៀត ដែលមិនទាន់ស្គាល់ក្នុងសម្មតិកម្ម ។'))))

_ASA_Q = ('គេឱ្យអង្កត់ ' + m('AB') + ' និង ' + m('CD') + ' ប្រសព្វគ្នាត្រង់ចំណុច ' + m('E') + ' ដែល ' + m('EA=EB') + ' និងអង្កត់ ' + m('AD') + ' ស្របនឹងអង្កត់ ' + m('CB') + ' ។')
S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p><p><span class="h-lab">លំហាត់គំរូ៖</span> ' + _ASA_Q + '</p>'
    '<div class="cgrid" style="grid-template-columns:52% 1fr"><div>'
    + p(hl('ក.', NAVY) + ' ប្រៀបធៀបត្រីកោណ ' + m('AED') + ' និង ' + m('BEC')) + p(hl('ខ.', NAVY) + ' ទាញបញ្ជាក់ថា ' + m('ED=EC') + ' ។')
    + rvd(1, '<div class="cmbox" style="text-align:left;margin-top:3cqh">' + hl('ជំនួយ៖') + ' រកធាតុ ៣ ដែលប៉ុនគ្នា<div style="text-align:center;font-weight:700">មុំទល់កំពូល &nbsp;•&nbsp; មុំឆ្លាស់ក្នុង &nbsp;•&nbsp; សម្មតិកម្ម</div></div>')
    + '</div><div class="cfig">' + fig(G.asa_ex_draw()) + '<div class="defcap" style="font-style:italic;color:#595959">' + m(r'AD\parallel CB\ ,\ EA=EB') + '</div></div></div>'})

S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p>'
    '<div class="cgrid" style="grid-template-columns:56% 1fr"><div>' + rvd(1,
    '<h2 class="solh" style="margin-top:0"><span class="h-lab">ដំណោះស្រាយ៖</span></h2>'
    + p(hl('ក.', NAVY) + ' ក្នុង ' + m(r'\Delta AED') + ' និង ' + m(r'\Delta BEC') + ' មាន៖')
    + p(m(r'\angle AED=\angle BEC') + ' ' + gr('(មុំទល់កំពូល)')) + p(m('EA=EB') + ' ' + gr('(សម្មតិកម្ម)'))
    + p(m(r'\angle EAD=\angle EBC') + ' ' + gr('(មុំឆ្លាស់ក្នុង ព្រោះ ' + m(r'AD\parallel BC') + ')'))
    + p('ដូចនេះ ' + hl(m(r'\Delta AED\cong\Delta BEC')) + ' (ម.ជ.ម)')
    + p(hl('ខ.', NAVY) + ' ដោយ ' + m(r'\Delta AED\cong\Delta BEC') + ' នោះ ជ្រុងត្រូវគ្នាប៉ុនរៀងគ្នា (វិបាក)')
    + p('ដូចនេះ ' + hl(m('ED=EC')))) + '</div><div class="cfig">' + fig(G.asa_ex_draw()) + '</div></div>'})

def prob_sol(band, label, problem, subq, sol, fg, chip='គិត ៥ នាទី'):
    """class slides 20-21: the problem on top, the solution on one click, the figure on the right, a «គិត ៥ នាទី» chip under the figure"""
    return {'k': 'ex', 'raw': True, 'html': f'<p class="ts-kicker">{band}</p><p><span class="h-lab">{label}៖</span> {problem}</p>' + (f'<div class="subq">{subq}</div>' if subq else '')
            + '<div class="cgrid" style="grid-template-columns:58% 1fr;align-items:start"><div>' + rvd(1, '<h2 class="solh" style="margin-top:0"><span class="h-lab">ដំណោះស្រាយ៖</span></h2>' + sol)
            + '</div><div class="cfig">' + fig(whole(fg)) + f'</div></div><span class="esc-chip br">{chip}</span>'}


def pc(text):
    """the conclusion of part ក. on these slides: bold, no box (the class slides)"""
    return f'<p class="pc">{text}</p>'


S.append(prob_sol('១. ត្រីកោណប៉ុនគ្នា', 'ប្រតិបត្តិ', 'រូបខាងស្តាំមាន ' + m(r'\angle ABC=\angle AED') + ' និង ' + m('AB=AE') + ' ។ បង្ហាញថា ' + m(r'\Delta ABC\cong\Delta AED') + ' និង ' + m('AD=AC') + ' ។', '',
    p(hl('ក.', NAVY) + ' ក្នុង ' + m(r'\Delta ABC') + ' និង ' + m(r'\Delta AED') + ' មាន៖')
    + p(m(r'\angle BAC=\angle EAD') + ' ' + gr('(មុំរួម)')) + p(m('AB=AE') + ' ' + gr('(សម្មតិកម្ម)')) + p(m(r'\angle ABC=\angle AED') + ' ' + gr('(សម្មតិកម្ម)'))
    + pc('ដូចនេះ ' + hl(m(r'\Delta ABC\cong\Delta AED')) + ' (ម.ជ.ម)')
    + p(hl('ខ.', NAVY) + ' ដោយ ' + m(r'\Delta ABC\cong\Delta AED') + ' នោះ ជ្រុងត្រូវគ្នាប៉ុនរៀងគ្នា (វិបាក) ។')
    + p('ដូចនេះ ' + hl(m('AD=AC'))), G.asa_prac()))

S.append({'mark': 'SAS'})
# ---- 1.2.2 ជ.ម.ជ
S.append(exfig('១.២.២', 'ជ.ម.ជ ៖ សង់ត្រីកោណ', G.sas_construct2(), [
    p(hl('១.') + ' ប្រើបន្ទាត់ក្រឹតគូសជ្រុង ' + m('AB') + ' មានប្រវែង ' + m(r'4\text{ cm}') + ' ។'),
    p(hl('២.') + ' ប្រើរ៉ាប់ទ័រគូសមុំ ' + m(r'\angle BAx=60^\circ') + ' ។'),
    p(hl('៣.') + ' ប្រើបន្ទាត់ក្រឹតដៅចំណុច ' + m('C') + ' នៅលើកន្លះបន្ទាត់ ' + m('Ax') + ' ដែលជ្រុង ' + m('AC') + ' មានប្រវែង ' + m(r'6\text{ cm}') + ' ។'),
    p(hl('៤.') + ' ភ្ជាប់ ' + m('BC') + ' ➜ បាន ' + m(r'\Delta ABC') + ' ។ សង់ ' + m(r"\Delta A'B'C'") + ' តាមរបៀបដូចគ្នា ។')],
    'សង់ ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' ដែល ' + m(r"\angle A=\angle A'=60^\circ") + ' , ' + m(r"AB=A'B'=4\text{ cm}") + ' និង ' + m(r"AC=A'C'=6\text{ cm}") + ' រួចប្រៀបធៀបត្រីកោណទាំងពីរនេះ។',
    first_visible=True))

S.append(exfig('១.២.២', 'ប្រៀបធៀប ' + '\\(\\Delta ABC\\)' + ' និង ' + "\\(\\Delta A'B'C'\\)", G.overlay_pair2('sas'), [
    p('យក ' + m(r'\Delta ABC') + ' ទៅដាក់ត្រួតពីលើ ' + m(r"\Delta A'B'C'") + ' ដោយឱ្យមុំ ' + m(r'\angle A') + ' ត្រួតស៊ីគ្នានឹង ' + m(r"\angle A'") + ' យើងសង្កេតឃើញថា ៖'),
    p('ជ្រុង ' + m('AB') + ' ត្រួតស៊ីគ្នាលើជ្រុង ' + m("A'B'") + ' ព្រោះ ' + m(r"AB=A'B'=4\text{ cm}") + ' ។'),
    p('ជ្រុង ' + m('AC') + ' ត្រួតស៊ីគ្នាលើជ្រុង ' + m("A'C'") + ' ព្រោះ ' + m(r"AC=A'C'=6\text{ cm}") + ' ។'),
    p('ដោយ ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' មានធាតុត្រូវគ្នាប៉ុនគ្នា តាមនិយមន័យត្រីកោណទាំងពីរនេះប៉ុនគ្នា ។')]))

S.append(theorem('១.២.២', 'ទ្រឹស្តីបទ (ជ.ម.ជ)', hl('ទ្រឹស្តីបទ ៖') + ' ត្រីកោណពីរប៉ុនគ្នា កាលណាវាមាន' + hl('មុំមួយប៉ុនគ្នា') + ' អមដោយ' + hl('ជ្រុងពីរប៉ុនរៀងគ្នា') + ' ។', G.theorem_pair('sas'),
    m(r"\Delta ABC\cong\Delta A'B'C'") + ' (ជ.ម.ជ)'))

S.append(ex('វិបាក', 'ពីលក្ខខណ្ឌ ជ.ម.ជ យើងទាញបានវិបាកដូចខាងក្រោម',
    box3(mline("AB=A'B'", r"\angle A=\angle A'", "AC=A'C'"), p(m(r"\Delta ABC\cong\Delta A'B'C'")) + p(hl('(តាមលក្ខខណ្ឌ ជ.ម.ជ)', RED)),
         mline(r"\angle B=\angle B'", r"\angle C=\angle C'", "BC=B'C'"))))

_SAS_Q = ('គូស ' + m(r'\angle XOY') + ' មួយ និងកន្លះបន្ទាត់ ' + m('OZ') + ' ជាកន្លះបន្ទាត់ពុះនៃមុំនេះ។ នៅលើកន្លះបន្ទាត់ ' + m('OX') + ' និង ' + m('OY') + ' គេដៅចំណុច ' + m('A') + ' និង ' + m('B') + ' រៀងគ្នាដែល ' + m('OA=OB') + ' ។ នៅលើកន្លះបន្ទាត់ ' + m('OZ') + ' គេដៅចំណុច ' + m('M') + ' មួយ។')
S.append({'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p><p><span class="h-lab">លំហាត់គំរូ៖</span> ' + _SAS_Q + '</p>'
    '<div class="cgrid" style="grid-template-columns:52% 1fr"><div>'
    + p(hl('ក.', NAVY) + ' ប្រៀបធៀបត្រីកោណ ' + m('OMA') + ' និង ' + m('OMB')) + p(hl('ខ.', NAVY) + ' ទាញវិបាក ។')
    + rvd(1, '<div class="cmbox" style="text-align:left;margin-top:3cqh">' + hl('ជំនួយ៖') + ' រកធាតុ ៣ ដែលប៉ុនគ្នា<div style="text-align:center;font-weight:700">សម្មតិកម្ម &nbsp;•&nbsp; មុំពុះ &nbsp;•&nbsp; ជ្រុងរួម</div></div>')
    + '</div><div class="cfig">' + fig(whole(G.sas_ex())) + '</div></div>'})
S.append(exfig('ដំណោះស្រាយ', '', G.sas_ex(), [
    p('ក្នុង ' + m(r'\Delta OMA') + ' និង ' + m(r'\Delta OMB') + ' មាន') + p(m('OA=OB') + ' ' + hl('(សម្មតិកម្ម)', '#595959')),
    p(m(r'\angle AOM=\angle BOM') + ' ' + gr('(' + m('OM') + ' ជាកន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle XOY') + ')')),
    p(m('OM') + ' ជាជ្រុងរួមនៃត្រីកោណទាំងពីរ') + p('ដូចនេះ ' + hl(m(r'\Delta OMA\cong\Delta OMB')) + ' (តាមលក្ខខណ្ឌ ជ.ម.ជ)') + p('វិបាក ៖ ' + hl(m(r'MA=MB\ ,\ \angle OAM=\angle OBM\ ,\ \angle OMA=\angle OMB')))]))

_PR_ITEMS = [
    p('ក្នុង ' + m(r'\Delta OAB') + ' និង ' + m(r"\Delta OA'B'") + ' មាន') + p(m("OA=OA'") + ' ' + gr("(" + m("A'") + ' ជាចំណុចឆ្លុះនៃ ' + m('A') + ' ធៀបនឹង ' + m('O') + ')')),
    p(m("OB=OB'") + ' ' + gr("(" + m("B'") + ' ជាចំណុចឆ្លុះនៃ ' + m('B') + ' ធៀបនឹង ' + m('O') + ')')),
    p(m(r"\angle AOB=\angle A'OB'") + ' ' + hl('(មុំទល់កំពូល)', '#595959')) + p('ដូចនេះ ' + hl(m(r"\Delta OAB\cong\Delta OA'B'")) + ' (តាមលក្ខខណ្ឌ ជ.ម.ជ) ។')]
_PR_Q = ('គូស ' + m(r'\Delta AOB') + ' មួយ ' + m("A'") + ' ជាចំណុចឆ្លុះនៃ ' + m('A') + ' ធៀបនឹង ' + m('O') + ' និង ' + m("B'") + ' ជាចំណុចឆ្លុះនៃ ' + m('B') + ' ធៀបនឹង ' + m('O') + ' ។ ស្រាយបំភ្លឺថា ' + m(r"\Delta OAB\cong\Delta OA'B'") + ' ។')
S.append(prob_sol('១. ត្រីកោណប៉ុនគ្នា', 'ប្រតិបត្តិ', _PR_Q, '', ''.join(_PR_ITEMS), G.sas_prac()))

S.append({'mark': 'SSS'})
# ---- 1.2.3 ជ.ជ.ជ
S.append(exfig('១.២.៣', 'ជ.ជ.ជ ៖ សង់ត្រីកោណ', G.sss_construct(), [
    p(hl('១.') + ' សង់ជ្រុង ' + m('AB') + ' នៅលើបន្ទាត់ ' + m('l') + ' ដែល ' + m(r'AB=6\text{ cm}') + ' ។'),
    p(hl('២.') + ' ប្រើដែកឈាន យក ' + m('A') + ' ជាផ្ចិតគូសធ្នូរង្វង់មួយមានកាំស្មើនឹង ' + m(r'5\text{ cm}') + ' ។'),
    p(hl('៣.') + ' យក ' + m('B') + ' ជាផ្ចិតគូសធ្នូរង្វង់មួយមានកាំស្មើនឹង ' + m(r'3\text{ cm}') + ' ។ តាង ' + m('C') + ' ជាចំណុចប្រសព្វនៃធ្នូទាំងពីរ ។'),
    p(hl('៤.') + ' ភ្ជាប់ ' + m('AC') + ' និង ' + m('BC') + ' ➜ បាន ' + m(r'\Delta ABC') + ' ។ សង់ ' + m(r"\Delta A'B'C'") + ' តាមរបៀបដូចគ្នា ។')],
    'សង់ ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' ដែល ' + m(r"AB=A'B'=6\text{ cm}") + ' , ' + m(r"AC=A'C'=5\text{ cm}") + ' និង ' + m(r"BC=B'C'=3\text{ cm}") + ' រួចប្រៀបធៀបត្រីកោណទាំងពីរនេះ។',
    first_visible=True))
assert 3 + 5 > 6

S.append(exfig('១.២.៣', 'ប្រៀបធៀប ' + '\\(\\Delta ABC\\)' + ' និង ' + "\\(\\Delta A'B'C'\\)", G.overlay_pair2('sss'), [
    p('យើងយក ' + m(r'\Delta ABC') + ' ទៅដាក់លើ ' + m(r"\Delta A'B'C'") + ' ដោយឱ្យជ្រុង ' + m('AB') + ' ត្រួតស៊ីគ្នាលើជ្រុង ' + m("A'B'") + ' ។'),
    p('យើងឃើញថា កំពូល ' + m('C') + ' និង ' + m("C'") + ' ត្រួតលើគ្នា ឋិតនៅម្ខាងតែមួយនៃជ្រុង ' + m('AB') + ' ។'),
    p('ហើយប្រវែងជ្រុងទាំងបីកំណត់បានទីតាំងនៃត្រីកោណតែមួយគត់ មានន័យថាត្រីកោណ ' + m('ABC') + ' និង ' + m("A'B'C'") + ' ត្រួតស៊ីគ្នា ព្រោះជ្រុងត្រូវគ្នាទាំងបីគូមានប្រវែងស្មើគ្នា ។'),
    p('ដូចនេះត្រីកោណទាំងពីរនេះ' + hl('ប៉ុនគ្នា') + ' ។')]))

S.append(theorem('១.២.៣', 'ទ្រឹស្តីបទ (ជ.ជ.ជ)', hl('ទ្រឹស្តីបទ ៖') + ' ត្រីកោណពីរប៉ុនគ្នា កាលណាវាមាន' + hl('ជ្រុងទាំងបីប៉ុនរៀងគ្នា') + ' ។', G.theorem_pair('sss'),
    m(r"\Delta ABC\cong\Delta A'B'C'") + ' (ជ.ជ.ជ)'))

S.append(ex('វិបាក', 'ពីលក្ខខណ្ឌ ជ.ជ.ជ យើងទាញបានវិបាកដូចខាងក្រោម',
    box3(mline("AB=A'B'", "AC=A'C'", "BC=B'C'"), p(m(r"\Delta ABC\cong\Delta A'B'C'")) + p(hl('(តាមលក្ខខណ្ឌ ជ.ជ.ជ)', RED)),
         mline(r"\angle A=\angle A'", r"\angle B=\angle B'", r"\angle C=\angle C'"))))

S.append(exfig('លំហាត់គំរូ', 'ជ.ជ.ជ', G.sss_ex(), [
    p('គេមាន ' + m('FJ=GK') + ' ' + hl('(សម្មតិកម្ម)', '#595959')) + p(m('FG=FJ+JG') + ' (1)') + p(m('JK=JG+GK') + ' (2)') + p('តាម (1) និង (2) នាំឱ្យ ' + hl(m('FG=JK'))),
    p('ក្នុង ' + m(r'\Delta EFG') + ' និង ' + m(r'\Delta HKJ') + ' មាន') + p(m('EF=HK') + ' , ' + m('EG=HJ') + ' ' + hl('(សម្មតិកម្ម)', '#595959')) + p(m('FG=JK') + ' ' + hl('(សម្រាយខាងលើ)', '#595959'))
    + p('ដូចនេះ ' + hl(m(r'\Delta EFG\cong\Delta HKJ')) + ' (តាមលក្ខខណ្ឌ ជ.ជ.ជ)')],
    'រូបខាងស្តាំនេះគេឱ្យ ' + m('EF=HK') + ' , ' + m('FJ=GK') + ' និង ' + m('EG=HJ') + ' ។ បង្ហាញថា ' + m(r'\Delta EFG\cong\Delta HKJ') + ' ។'))

S.append(exfig('ប្រតិបត្តិ', 'ជ.ជ.ជ', G.sss_prac(), [
    p('ក្នុង ' + m(r'\Delta RZT') + ' និង ' + m(r'\Delta VWS') + ' មាន') + p(m('RZ=VW') + ' , ' + m('TZ=SW') + ' ' + hl('(សម្មតិកម្ម)', '#595959'))
    + p(m('RT=RS+ST') + ' , ' + m('VS=VT+TS') + ' ហើយ ' + m('RS=TV') + ' នាំឱ្យ ' + hl(m('RT=VS')))
    + p('ដូចនេះ ' + hl(m(r'\Delta RZT\cong\Delta VWS')) + ' ' + hl('(ករណី ជ.ជ.ជ)'))],
    'រូបខាងស្តាំនេះគេឱ្យ ' + m('RZ=VW') + ' , ' + m('TZ=SW') + ' និង ' + m('RS=TV') + ' ។ ប្រៀបធៀប ' + m(r'\Delta RZT') + ' និង ' + m(r'\Delta VWS') + ' ។'))

S.append({'mark': 'RT'})
# ---- 1.3 right triangles
S.append(ex('១.៣', 'លក្ខខណ្ឌចំពោះត្រីកោណកែងប៉ុនគ្នា',
    p('ត្រីកោណកែងពីរប៉ុនគ្នា មានពីរលក្ខខណ្ឌដូចខាងក្រោម ៖')
    + cols(rvd(1, _card('អ.ម', G.mini('ha'), 'អ៊ីប៉ូតេនុសប៉ុនគ្នានិងមុំស្រួចមួយប៉ុនគ្នា', '#1c7ed6')),
           rvd(2, _card('អ.ជ', G.mini('hl'), 'អ៊ីប៉ូតេនុសប៉ុនគ្នានិងជ្រុងមុំកែងមួយប៉ុនគ្នា', '#2b8a87')))))

S.append(exfig('១.៣.១', 'អ.ម ៖ អ៊ីប៉ូតេនុសប៉ុនគ្នានិងមុំស្រួចមួយប៉ុនគ្នា', G.ha_proof(), [
    p('ក្នុងត្រីកោណកែង ' + m('ABC') + ' ៖ ' + m(r'\angle B+\angle C=90^\circ\Rightarrow\angle B=90^\circ-\angle C') + ' ។') + p('ក្នុងត្រីកោណកែង ' + m("A'B'C'") + ' ៖ ' + m(r"\angle B'=90^\circ-\angle C'") + ' ។'),
    p('ដោយ ' + m(r"\angle C=\angle C'") + ' នោះ ' + hl(m(r"\angle B=\angle B'")) + ' ។'),
    p('ក្នុង ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' មាន ' + m(r"\angle A=\angle A'=90^\circ") + ' , ' + m("BC=B'C'") + ' , ' + m(r"\angle C=\angle C'") + ' ។')
    + p('ដូចនេះ ' + hl(m(r"\Delta ABC\cong\Delta A'B'C'")) + ' (តាមលក្ខខណ្ឌ ម.ជ.ម) ។')],
    'ក្នុង ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' មាន ' + m(r"\angle A=\angle A'=90^\circ") + ' , ' + m(r"\angle C=\angle C'") + ' , ' + m("BC=B'C'") + ' ។ បង្ហាញថា ' + m(r"\Delta ABC\cong\Delta A'B'C'") + ' ។'))

S.append(ex('១.៣.១', 'ទ្រឹស្តីបទ (អ.ម)',
    cols(fig(G.mini('ha')), _BOX + hl('ទ្រឹស្តីបទ ៖') + ' ត្រីកោណកែងពីរប៉ុនគ្នា កាលណាវាមាន' + hl('អ៊ីប៉ូតេនុសប៉ុនគ្នា') + ' និង' + hl('មុំស្រួចមួយប៉ុនគ្នា') + ' ។</div>')))

S.append(exfig('លំហាត់គំរូ', 'អ.ម ៖ ចំណុចនៅលើកន្លះបន្ទាត់ពុះមុំ', G.ha_ex(), [
    p('ត្រីកោណកែង ' + m('OMA') + ' និងត្រីកោណកែង ' + m('OMB') + ' មាន') + p(m('OM') + ' ជាអ៊ីប៉ូតេនុសរួម'),
    p(m(r'\angle MOA=\angle MOB') + ' ' + gr('(' + m('OM') + ' ជាកន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle AOB') + ')')) + p('ដូចនេះ ' + hl(m(r'\Delta OMA\cong\Delta OMB')) + ' (តាមលក្ខខណ្ឌ អ.ម)'),
    p('វិបាក ៖ ' + hl(m('MA=MB')) + ' ។')],
    'គេឱ្យ ' + m('M') + ' ជាចំណុចមួយឋិតនៅលើកន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle XOY') + ' ។ តាមចំណុច ' + m('M') + ' គេគូសបន្ទាត់កែងនឹង ' + m('OX') + ' ត្រង់ ' + m('A') + ' និង ' + m('OY') + ' ត្រង់ ' + m('B') + ' ។ បង្ហាញថា ' + m('MA=MB') + ' ។'))

S.append(theorem('១.៣.១', 'ជាទូទៅ ៖ កន្លះបន្ទាត់ពុះមុំ',
    ul(['គ្រប់ចំណុចឋិតនៅលើកន្លះបន្ទាត់ពុះនៃមុំមួយ ត្រូវឋិតនៅស្មើចម្ងាយពីជ្រុងទាំងពីរនៃមុំនោះ ។',
        'ច្រាសមកវិញ គ្រប់ចំណុចដែលមានចម្ងាយស្មើទៅនឹងជ្រុងទាំងពីរនៃមុំមួយ ត្រូវឋិតនៅលើកន្លះបន្ទាត់ពុះនៃមុំនោះ ។']), G.ha_ex()))

S.append(exfig('ប្រតិបត្តិ', 'អ.ម', G.ha_prac(), [
    p('ក្នុងត្រីកោណកែង ' + m('BDC') + ' និង ' + m('CEB') + ' មាន') + p(m('BC') + ' ជាអ៊ីប៉ូតេនុសរួម') + p(m(r'\angle DCB=\angle EBC') + ' ' + hl('(មុំបាតនៃត្រីកោណសមបាត)', '#595959'))
    + p('ដូចនេះ ' + hl(m(r'\Delta BDC\cong\Delta CEB')) + ' (តាមលក្ខខណ្ឌ អ.ម)') + p('វិបាក ៖ ' + hl(m('BD=CE')) + ' និង ' + hl(m('BE=CD')) + ' ។')],
    m('ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + m('A') + ' ។ កម្ពស់គូសចេញពីកំពូល ' + m('B') + ' និង ' + m('C') + ' កាត់ជ្រុង ' + m('AC') + ' និង ' + m('AB') + ' ត្រង់ ' + m('D') + ' និង ' + m('E') + ' រៀងគ្នា ។ បង្ហាញថា ' + m('BD=CE') + ' និង ' + m('BE=CD') + ' ។'))

_HLQ = ('ក្នុង ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' មាន ' + m(r"\angle A=\angle A'=90^\circ") + ' , ' + m("AB=A'B'") + ' , ' + m("BC=B'C'") + ' ។ តើត្រីកោណកែងទាំងពីរនេះប៉ុនគ្នាឬទេ?')
S.append(
    ex('១.៣.២', 'អ.ជ ៖ អ៊ីប៉ូតេនុសប៉ុនគ្នានិងជ្រុងកែងមួយប៉ុនគ្នា', p(_HLQ) + cols(fig(G.hl_proof('base')), lines([
        p('ដាក់ ' + m(r"\Delta A'B'C'") + ' ជាប់នឹង ' + m(r'\Delta ABC') + ' ឱ្យ ' + m("A'B'") + ' ត្រួតលើ ' + m('AB') + ' ហើយ ' + m('C') + ' និង ' + m("C'") + ' នៅសងខាង ' + m('AB') + ' ។'),
        p(m(r"\angle CAB+\angle BAC'=90^\circ+90^\circ=180^\circ") + ' នោះ ' + m("C,A,C'") + ' នៅលើបន្ទាត់តែមួយ ។')]))))

S.append(exfig('១.៣.២', 'អ.ជ ៖ អ៊ីប៉ូតេនុសប៉ុនគ្នានិងជ្រុងកែងមួយប៉ុនគ្នា', G.hl_proof(), [
    p('ក្នុង ' + m(r"\Delta BCC'") + ' មាន ' + m("BC=BC'") + ' នោះជាត្រីកោណសមបាតកំពូល ' + m('B') + ' ។ ដូចនេះ ' + hl(m(r"\angle C=\angle C'")) + ' ។'),
    p('ក្នុងត្រីកោណកែង ' + m('ABC') + ' និង ' + m("ABC'") + ' មាន ' + m("BC=BC'") + ' , ' + m(r"\angle C=\angle C'") + ' ។') + p('ដូចនេះ ' + hl(m(r"\Delta ABC\cong\Delta A'B'C'")) + ' (តាមលក្ខខណ្ឌ អ.ម) ។')],
    'តាមរូបខាងស្តាំ ' + m("BC=BC'") + ' ព្រោះ ' + m("BC=B'C'") + ' ។'))

S.append(ex('១.៣.២', 'ទ្រឹស្តីបទ (អ.ជ)',
    cols(fig(G.mini('hl')), _BOX + hl('ទ្រឹស្តីបទ ៖') + ' ត្រីកោណកែងពីរប៉ុនគ្នា កាលណាវាមាន' + hl('អ៊ីប៉ូតេនុសប៉ុនគ្នា') + ' និង' + hl('ជ្រុងមួយនៃមុំកែងប៉ុនគ្នា') + ' ។</div>')))

_INQ = ('កន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle B') + ' និង ' + m(r'\angle C') + ' ក្នុងត្រីកោណ ' + m('ABC') + ' ប្រសព្វគ្នាត្រង់ ' + m('I') + ' ។ តាម ' + m('I') + ' គេគូសបន្ទាត់កែងទៅនឹងជ្រុង ' + m('AB') + ' , ' + m('BC') + ' និង ' + m('AC') + ' ត្រង់ ' + m('D') + ' , ' + m('E') + ' និង ' + m('F') + ' រៀងគ្នា ។')
S.append(exfig('លំហាត់គំរូ', 'អ.ម និង អ.ជ ៖ ផ្ចិតរង្វង់ចារឹកក្នុង (ក)', G.incenter_fig('a'), [
    p('ក្នុងត្រីកោណកែង ' + m('BEI') + ' និង ' + m('BDI') + ' មាន ' + m('BI') + ' ជាអ៊ីប៉ូតេនុសរួម ហើយ ' + m(r'\angle IBE=\angle IBD') + ' ។')
    + p('ដូចនេះ ' + m(r'\Delta BEI\cong\Delta BDI') + ' (តាមលក្ខខណ្ឌ អ.ម) នាំឱ្យ ' + hl(m('ID=IE')) + ' (1)') ,
    p('ដូចគ្នា ក្នុងត្រីកោណកែង ' + m('CEI') + ' និង ' + m('CFI') + ' មាន ' + m('CI') + ' ជាអ៊ីប៉ូតេនុសរួម ហើយ ' + m(r'\angle ICE=\angle ICF') + ' ។')
    + p(m(r'\Delta CEI\cong\Delta CFI') + ' (អ.ម) នាំឱ្យ ' + hl(m('IE=IF')) + ' (2)') + p('តាម (1) និង (2) ៖ ' + hl(m('ID=IE=IF')) + ' ។')],
    _INQ + ' ក. បង្ហាញថា ' + m('ID=IE=IF') + ' ។'))
S.append(exfig('លំហាត់គំរូ', 'អ.ម និង អ.ជ ៖ ផ្ចិតរង្វង់ចារឹកក្នុង (ខ)', G.incenter_fig('b'), [
    p('ក្នុងត្រីកោណកែង ' + m('IDA') + ' និង ' + m('IFA') + ' មាន ' + m('AI') + ' ជាអ៊ីប៉ូតេនុសរួម និង ' + m('ID=IF') + ' (សម្រាយខាងលើ) ។')
    + p('ដូចនេះ ' + m(r'\Delta IDA\cong\Delta IFA') + ' (តាមលក្ខខណ្ឌ អ.ជ) នាំឱ្យ ' + m(r'\angle IAD=\angle IAF') + ' ។'),
    p('ដូចនេះ ' + hl(m('AI')) + ' ជាកន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle BAC') + ' ។ ម្យ៉ាងទៀត ' + m('ID=IE=IF') + ' នោះ ' + m('I') + ' នៅស្មើចម្ងាយពីជ្រុងទាំងបី ។')],
    'ខ. បង្ហាញថា កន្លះបន្ទាត់ ' + m('AI') + ' ជាកន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle BAC') + ' ។', first_visible=False))

S.append(theorem('១.៣.២', 'ទ្រឹស្តីបទ ៖ កន្លះបន្ទាត់ពុះមុំទាំងបី', hl('ទ្រឹស្តីបទ ៖') + ' កន្លះបន្ទាត់ពុះមុំក្នុងទាំងបីនៃត្រីកោណមួយ' + hl('ប្រសព្វគ្នាត្រង់ចំណុចតែមួយ') + ' ដែលឋិតនៅ' + hl('ស្មើចម្ងាយពីជ្រុងទាំងបី') + 'នៃត្រីកោណនោះ ។',
    G.incenter_fig('b')))

S.append(exfig('ប្រតិបត្តិ', 'អ.ជ', G.hl_prac(), [
    p('ក្នុងត្រីកោណកែង ' + m('BDM') + ' និង ' + m('CEM') + ' មាន') + p(m('BM=CM') + ' ' + gr('(' + m('M') + ' ជាចំណុចកណ្តាលនៃ ' + m('BC') + ')')) + p(m('MD=ME') + ' ' + hl('(សម្មតិកម្ម)', '#595959'))
    + p('ដូចនេះ ' + hl(m(r'\Delta BDM\cong\Delta CEM')) + ' (តាមលក្ខខណ្ឌ អ.ជ)') + p('វិបាក ៖ ' + hl(m(r'\angle B=\angle C')) + ' ។')],
    m('ABC') + ' ជាត្រីកោណមួយនិង ' + m('M') + ' ជាចំណុចកណ្តាលនៃជ្រុង ' + m('BC') + ' ។ តាម ' + m('M') + ' គេគូសបន្ទាត់កែងទៅនឹងជ្រុង ' + m('AB') + ' និង ' + m('AC') + ' ត្រង់ ' + m('D') + ' និង ' + m('E') + ' រៀងគ្នា ។ បង្ហាញថា បើ ' + m('MD=ME') + ' នោះ ' + m(r'\angle B=\angle C') + ' ។'))

_ROW = lambda a, b: f'<tr><td style="font-weight:800;color:#0f5173">{a}</td><td>{b}</td></tr>'
S.append(ex('សង្ខេប', 'ករណីប៉ុនគ្នានៃត្រីកោណ',
    '<table style="margin:.4em auto;border-collapse:collapse;font-size:1.05em" class="sumtab"><tr><th>ករណី</th><th>លក្ខខណ្ឌ</th></tr>'
    + _ROW('ម.ជ.ម', 'ជ្រុងមួយប៉ុនគ្នាជាប់និងមុំពីរប៉ុនរៀងគ្នា ប៉ុនរៀងគ្នា')
    + _ROW('ជ.ម.ជ', 'មុំមួយប៉ុនគ្នាអមដោយជ្រុងពីរប៉ុនរៀងគ្នា')
    + _ROW('ជ.ជ.ជ', 'ជ្រុងទាំងបី ប៉ុនរៀងគ្នា')
    + _ROW('អ.ម', 'ត្រីកោណកែង ៖ អ៊ីប៉ូតេនុស និងមុំស្រួចមួយ ប៉ុនរៀងគ្នា')
    + _ROW('អ.ជ', 'ត្រីកោណកែង ៖ អ៊ីប៉ូតេនុស និងជ្រុងកែងមួយ ប៉ុនរៀងគ្នា') + '</table>'
    + rvd(1, p('បន្ទាប់ពីប្រៀបធៀបឱ្យត្រីកោណពីរប៉ុនគ្នារួច គេទាញបាន' + hl('ធាតុត្រូវគ្នាដទៃទៀតប៉ុនគ្នា') + ' ហៅថា ' + hl('វិបាក') + ' ។'))))

S.append({'mark': 'END1'})
# ================================================================ 2. mediator and isosceles triangle
S.append(part(4, '២.', 'មេដ្យាទ័រនៃអង្កត់ និងត្រីកោណសមបាត', 'ផ្នែកទី ២', '<p class="ts-sub">២.១ លក្ខណៈមេដ្យាទ័រនៃអង្កត់ · ២.២ លក្ខណៈត្រីកោណសមបាត</p>'))

S.append(exfig('២.១', 'ឧទាហរណ៍ ៖ មេដ្យាទ័រនៃអង្កត់', G.pb_fig(), [
    p(m('I') + ' ជាចំណុចកណ្តាលនៃអង្កត់ ' + m('BC') + ' ។ បន្ទាត់ ' + m(r'\Delta') + ' មួយកែងនឹងអង្កត់ ' + m('BC') + ' ត្រង់ ' + m('I') + ' គឺជា' + hl('មេដ្យាទ័រ') + 'នៃអង្កត់ ' + m('BC') + ' ។'),
    p('ចំណុច ' + m('M') + ' មួយឋិតនៅលើ ' + m(r'\Delta') + ' ។ ក្នុងត្រីកោណកែង ' + m('MIB') + ' និង ' + m('MIC') + ' មាន ' + m('IM') + ' ជាជ្រុងរួម ។') + p(m(r'\angle MIB=\angle MIC=90^\circ') + ' , ' + m('IB=IC') + ' ។'),
    p('ដូចនេះ ' + hl(m(r'\Delta MIB\cong\Delta MIC')) + ' (តាមលក្ខខណ្ឌ ជ.ម.ជ)') + p('វិបាក ៖ ' + hl(m(r'MB=MC\ ,\ \angle IMB=\angle IMC\ ,\ \angle IBM=\angle ICM')))],
    '', first_visible=False))

S.append(theorem('២.១', 'ជាទូទៅ ៖ មេដ្យាទ័រនៃអង្កត់',
    ul(['គ្រប់ចំណុចឋិតនៅលើមេដ្យាទ័រនៃអង្កត់មួយ ត្រូវឋិតនៅស្មើចម្ងាយពីចុងទាំងពីរនៃអង្កត់នោះ ។',
        'គ្រប់ចំណុចដែលឋិតនៅស្មើចម្ងាយពីចុងទាំងពីរនៃអង្កត់មួយ ចំណុចទាំងនោះឋិតនៅលើមេដ្យាទ័រនៃអង្កត់នោះ ។']), G.pb_fig()))

S.append(exfig('២.២', 'លក្ខណៈត្រីកោណសមបាត', G.isosceles_fig(), [
    p('តាមសម្រាយខាងលើ ' + m('MB=MC') + ' នោះ ' + m(r'\Delta BMC') + ' ជា' + hl('ត្រីកោណសមបាត') + 'កំពូល ' + m('M') + ' ។ មុំបាតទាំងពីរ ' + m(r'\angle B=\angle C') + ' ។'),
    p(m(r'\angle IMB=\angle IMC') + ' នោះ ' + m('MI') + ' ជាកន្លះបន្ទាត់ពុះនៃ ' + m(r'\angle M') + ' ។ ' + m('IB=IC') + ' នោះ ' + m('MI') + ' ជាមេដ្យាន ។ ' + m(r'MI\perp BC') + ' នោះ ' + m('MI') + ' ជាកម្ពស់ និងជាមេដ្យាទ័រ ។')],
    'ក្នុងត្រីកោណ ' + m('BMC') + ' ដែល ' + m('MB=MC') + ' ។ តើមានលក្ខណៈអ្វីខ្លះ?'))

S.append(ex('២.២', 'ជាទូទៅ ៖ ត្រីកោណសមបាត',
    cols(fig(whole(G.isosceles_fig())), _BOX + p('ក្នុងត្រីកោណសមបាតមាន') + ul(['មុំបាតទាំងពីរជាមុំប៉ុនគ្នា',
        'មេដ្យាទ័រ មេដ្យាន កម្ពស់គូសចេញពីកំពូល និងកន្លះបន្ទាត់ពុះនៃមុំកំពូលនោះ ឋិតនៅលើបន្ទាត់តែមួយ ។']) + '</div>')))

_CQ = 'មេដ្យាទ័ររបស់ជ្រុង ' + m('AB') + ' និង ' + m('BC') + ' នៃត្រីកោណ ' + m('ABC') + ' ប្រសព្វគ្នាត្រង់ ' + m('O') + ' ។ '
S.append(exfig('លំហាត់គំរូ', 'មេដ្យាទ័រជ្រុងទាំងបី (ក)', G.circum_fig('a'), [
    p(m('O') + ' ឋិតនៅលើមេដ្យាទ័រនៃ ' + m('AB') + ' នោះ ' + hl(m('OA=OB')) + ' ។'),
    p(m('O') + ' ឋិតនៅលើមេដ្យាទ័រនៃ ' + m('BC') + ' នោះ ' + hl(m('OB=OC')) + ' ។') + p('ដូចនេះ ' + hl(m('OA=OB=OC')) + ' ។')],
    _CQ + 'ក. បង្ហាញថា ' + m('OA=OB=OC') + ' ។'))
S.append(exfig('លំហាត់គំរូ', 'មេដ្យាទ័រជ្រុងទាំងបី (ខ)', G.circum_fig('b'), [
    p(m('OA=OC') + ' នោះ ' + m(r'\Delta AOC') + ' ជាត្រីកោណសមបាតកំពូល ' + m('O') + ' ។ ' + m('N') + ' ជាចំណុចកណ្តាលនៃ ' + m('AC') + ' នោះ ' + m('ON') + ' ជាមេដ្យាននៃ ' + m('AC') + ' ។'),
    p('តាមលក្ខណៈត្រីកោណសមបាត ' + m('ON') + ' ក៏ជាមេដ្យាទ័រនៃ ' + m('AC') + ' ។ ដូចនេះ ' + hl(m(r'ON\perp AC')) + ' ។')],
    'ខ. បើ ' + m('N') + ' ជាចំណុចកណ្តាលនៃ ' + m('AC') + ' បង្ហាញថា ' + m(r'ON\perp AC') + ' ។ (ដោយ ' + m('OA=OB=OC') + ' ពីសម្រាយ ក)'))

S.append(theorem('២.២', 'ទ្រឹស្តីបទ ៖ មេដ្យាទ័រជ្រុងទាំងបី', hl('ទ្រឹស្តីបទ ៖') + ' មេដ្យាទ័រជ្រុងទាំងបីនៃត្រីកោណមួយ' + hl('ប្រសព្វគ្នាត្រង់ចំណុចតែមួយ') + ' ដែលឋិតនៅ' + hl('ស្មើចម្ងាយពីកំពូលទាំងបី') + 'នៃត្រីកោណនោះ ។',
    G.circum_fig('b'), m('OA=OB=OC')))

# ================================================================ 3. inequalities in a triangle
S.append(part(5, '៣.', 'វិសមភាពក្នុងត្រីកោណ', 'ផ្នែកទី ៣', '<p class="ts-sub">៣.១ វិសមភាពរវាងជ្រុងនិងមុំឈម · ៣.២ វិសមភាពត្រីកោណ</p>'))

S.append(exfig('៣.១', 'ជ្រុងវែងជាង ឈមនឹងមុំធំជាង', G.ineq_proof(), [
    p('នៅលើជ្រុង ' + m('AC') + ' ដៅចំណុច ' + m('D') + ' មួយដែល ' + m('AD=AB') + ' ។'),
    p(m('AB=AD') + ' នោះ ' + m(r'\Delta ABD') + ' សមបាតកំពូល ' + m('A') + ' នាំឱ្យ ' + m(r'\angle B_2=\angle D_2') + ' ។'),
    p(m(r'\angle D_2') + ' ជាមុំក្រៅនៃ ' + m(r'\Delta BCD') + ' ៖ ' + m(r'\angle D_2=\angle B_1+\angle C') + ' នាំឱ្យ ' + m(r'\angle D_2>\angle C') + ' ។')
    + p('ដូចនេះ ' + m(r'\angle B_2>\angle C') + ' ហើយ ' + m(r'\angle B=\angle B_1+\angle B_2>\angle B_2') + ' ។ ដូចនេះ ' + hl(m(r'\angle B>\angle C')) + ' ។')],
    'ក្នុងត្រីកោណ ' + m('ABC') + ' ជ្រុង ' + m('AC') + ' ឈមនឹង ' + m(r'\angle B') + ' ជ្រុង ' + m('AB') + ' ឈមនឹង ' + m(r'\angle C') + ' ដែល ' + m('AC>AB') + ' ។ បង្ហាញថា ' + m(r'\angle B>\angle C') + ' ។'))

S.append(ex('៣.១', 'ទ្រឹស្តីបទ',
    _BOX + hl('ទ្រឹស្តីបទ ៖') + ' ក្នុងត្រីកោណមួយ' + ol(['បើជ្រុងពីរមិនប៉ុនគ្នា មុំដែលឈមនឹងជ្រុងទាំងពីរនេះក៏មិនប៉ុនគ្នាដែរ ហើយមុំដែលឈមនឹងជ្រុងធំជាង ជាមុំធំជាង ។',
        'ច្រាសមកវិញ បើមុំពីរមិនប៉ុនគ្នា ជ្រុងដែលឈមនឹងមុំទាំងពីរនេះក៏មិនប៉ុនគ្នាដែរ ហើយជ្រុងដែលឈមនឹងមុំធំជាង ជាជ្រុងធំជាង ។']) + '</div>'))

S.append(exfig('លំហាត់គំរូ', 'រៀបជ្រុងតាមលំដាប់', G.angles_triangle(), [
    p('ក្នុង ' + m(r'\Delta ABC') + ' គេបាន ' + m(r'\angle A+\angle B+\angle C=180^\circ') + ' ។') + dm(r'(6x+4)+(7x+12)+(6x-7)=180') + dm(r'19x+9=180\ \Rightarrow\ x=\dfrac{171}{19}=9'),
    p(m(r'\angle A=6(9)+4=58^\circ') + ' , ' + m(r'\angle B=7(9)+12=75^\circ') + ' , ' + m(r'\angle C=6(9)-7=47^\circ') + ' ។'),
    p('ដោយ ' + m(r'\angle B>\angle A>\angle C') + ' គេបាន ' + hl(m('AC>BC>AB')) + ' ។')],
    'ក្នុង ' + m(r'\Delta ABC') + ' មាន ' + m(r'\angle A=6x+4^\circ') + ' , ' + m(r'\angle B=7x+12^\circ') + ' និង ' + m(r'\angle C=6x-7^\circ') + ' ។ រៀបជ្រុងនៃ ' + m(r'\Delta ABC') + ' តាមលំដាប់ពីធំទៅតូច ។'))
assert (6 + 7 + 6) * 9 + 4 + 12 - 7 == 180 and 6 * 9 + 4 == 58 and 7 * 9 + 12 == 75 and 6 * 9 - 7 == 47 and 75 > 58 > 47

S.append(exfig('ប្រតិបត្តិ', 'វិសមភាពមុំនិងជ្រុង', G.ineq_prac(), [
    p('ក្នុង ' + m(r'\Delta ABC') + ' មាន ' + m(r'\angle ABC<\angle BAC') + ' នាំឱ្យ ' + m('AC<BC') + ' ' + hl('(ជ្រុងឈមនឹងមុំតូចជាងជាជ្រុងខ្លីជាង)', '#595959')),
    p('ដោយ ' + m('BD=AC') + ' ' + gr('(' + m('AB=AC=BD') + ')')) + p('ដូចនេះ ' + hl(m('BD<BC')) + ' ។')],
    'រូបខាងស្តាំនេះគេឱ្យ ' + m('AB=AC=BD') + ' និង ' + m(r'\angle ABC<\angle BAC') + ' ។ បង្ហាញថា ' + m('BD<BC') + ' ។'))

S.append(exfig('៣.២', 'វិសមភាពត្រីកោណ', G.tri_ineq_proof(), [
    p(m('ABC') + ' ជាត្រីកោណមួយ ។ គេបន្តជ្រុង ' + m('BC') + ' ឱ្យបាន ' + m('CM') + ' ដែល ' + m('CM=CA') + ' ។ ប្រៀបធៀប ' + m('AB') + ' និង ' + m('BC+AC') + ' ។'),
    p('ក្នុង ' + m(r'\Delta ACM') + ' មាន ' + m('CM=CA') + ' សមបាតកំពូល ' + m('C') + ' នាំឱ្យ ' + m(r'\angle CAM=\angle CMA') + ' ។'),
    p('ក្នុង ' + m(r'\Delta ABM') + ' ៖ ' + m(r'\angle BAM=\angle BAC+\angle CAM>\angle CAM=\angle BMA') + ' នាំឱ្យ ' + m('BM>AB') + ' ។'),
    p('ដោយ ' + m('BM=BC+CM=BC+AC') + ' ដូចនេះ ' + hl(m('AC+BC>AB')) + ' ។')]))

S.append(ex('៣.២', 'ទ្រឹស្តីបទ ៖ វិសមភាពត្រីកោណ', _BOX + hl('ទ្រឹស្តីបទ ៖') + ' ' + hl('ផលបូកជ្រុងពីរនៃត្រីកោណមួយធំជាងជ្រុងមួយទៀត ។') + '</div>'
    + p(m('AB+BC>AC') + ' , ' + m('BC+CA>AB') + ' , ' + m('CA+AB>BC'))))

def _sticks(a, b, c, label):
    ok = max(a, b, c) < a + b + c - max(a, b, c)
    return ok


_TR = [(2, 4.5, 5.8), (2, 4.5, 10.2), (2, 5.8, 10.2), (4.5, 5.8, 10.2)]
_OK = [t[0] + t[1] > t[2] and t[0] + t[2] > t[1] and t[1] + t[2] > t[0] for t in _TR]
assert _OK == [True, False, False, True]
_n = lambda v: ('%g' % v)
def _chk(x, y, z, ok):
    return p(m('%s+%s>%s' % (_n(x), _n(y), _n(z))) + ' ពិតឬទេ? ' + ('(ពិត)' if ok else '(មិនពិត)'))


def _stick_card(lab_, t, ok, step, all3=True):
    """one case: the three sticks, the checks of the triangle inequality and the picture (as the book does: all three checks when it works, the failing one when it does not)"""
    s_ = sorted(t)
    if ok:
        ls = _chk(t[0], t[1], t[2], True) + _chk(t[1], t[2], t[0], t[1] + t[2] > t[0]) + _chk(t[0], t[2], t[1], t[0] + t[2] > t[1]) if False else ''.join(
            _chk(*c, True) for c in ((s_[0], s_[1], s_[2]), (s_[1], s_[2], s_[0]), (s_[0], s_[2], s_[1])))
    else:
        ls = _chk(s_[0], s_[1], s_[2], False)
    cap = ('កំណាត់ឈើទាំងបីនេះអាចប្រើដើម្បីបង្កើតត្រីកោណមួយបាន ។' if ok else 'កំណាត់ឈើទាំងបីនេះមិនអាចប្រើដើម្បីបង្កើតត្រីកោណមួយបានទេ ។')
    return rvd(step, p(hl(lab_ + '.') + ' ' + m(r'\text{' + ' , '.join(_n(v) for v in t) + r'}')) + ls + '<div style="width:62%;margin:0 auto">' + fig(G.stick_tri(t[0], t[1], t[2], ok)) + '</div>')


S.append(ex('លំហាត់គំរូ', 'កំណាត់ឈើទាំងបួន',
    p('គ្រូម្នាក់បានឱ្យឈើបួនកំណាត់ទៅសុខាដើម្បីបង្កើតត្រីកោណមួយសម្រាប់ធ្វើជាគ្រោងស៊ុមព័ទ្ធសួនផ្កាមួយកន្លែង ។ ប្រវែងនៃកំណាត់ឈើមាន ' + m(r'2\text{ m}') + ' , ' + m(r'4.5\text{ m}') + ' , ' + m(r'5.8\text{ m}') + ' និង ' + m(r'10.2\text{ m}') + ' ។ តើសុខាអាចបង្កើតត្រីកោណខុសៗគ្នាបានប៉ុន្មាន?')
    + gridn(4, *[_stick_card('កខគឃ'[i], t, _OK[i], i + 1) for i, t in enumerate(_TR)])
    + rvd(5, p('ដូចនេះសុខាអាចបង្កើតត្រីកោណបាន ' + hl('២ របៀប') + ' គឺ ' + hl('ក') + ' និង ' + hl('ឃ') + ' ។'))))

_PR = [(12, 11, 17), (1, 2, 3), (4.7, 9, 4.1)]
_PROK = [True, False, False]
S.append(ex('ប្រតិបត្តិ', 'តើរង្វាស់ជ្រុងដែលឱ្យក្នុងករណីនីមួយៗខាងក្រោមនេះអាចគូសបានត្រីកោណមួយឬទេ? ព្រោះអ្វី?',
    gridn(3, *[_stick_card('កខគ'[i], t, _PROK[i], i + 1) for i, t in enumerate(_PR)])))
assert 11 + 12 > 17 and not 1 + 2 > 3 and not 4.1 + 4.7 > 9

# ================================================================ 4. perpendicular and slanted segments
S.append(part(6, '៤.', 'ការប្រៀបធៀបអង្កត់', 'ផ្នែកទី ៤', '<p class="ts-sub">៤.១ អង្កត់កែងនិងអង្កត់ទ្រេត · ៤.២ ប្រៀបធៀបអង្កត់ទ្រេតនិងអង្កត់កែង · ៤.៣ ប្រៀបធៀបអង្កត់ទ្រេតនិងអង្កត់ទ្រេត</p>'))

S.append(exfig('៤.១', 'អង្កត់កែង និងអង្កត់ទ្រេត', G.perp_slant(), [
    p('ចំណុច ' + m('A') + ' មួយមិនឋិតនៅលើបន្ទាត់ ' + m(r'\Delta') + ' ។ គេគូសអង្កត់ ' + m(r'AH\perp\Delta') + ' ។ ' + m('AH') + ' ហៅថា' + hl('អង្កត់កែង') + 'នឹងបន្ទាត់ ' + m(r'\Delta') + ' ។ ' + m('H') + ' ហៅថា' + hl('ជើងចំណោលកែង') + 'នៃចំណុច ' + m('A') + ' លើបន្ទាត់ ' + m(r'\Delta') + ' ។ ' + m('AH') + ' ជាចម្ងាយពី ' + m('A') + ' ទៅបន្ទាត់ ' + m(r'\Delta') + ' ។'),
    p('ចំណុច ' + m('B') + ' ឋិតនៅលើ ' + m(r'\Delta') + ' ផ្សេងពី ' + m('H') + ' ។ ' + m('AB') + ' ហៅថា' + hl('អង្កត់ទ្រេត') + 'ដែល ' + m('B') + ' ជាជើងអង្កត់ទ្រេត ។'),
    p(m('HB') + ' ហៅថា' + hl('ចំណោលកែង') + 'នៃអង្កត់ ' + m('AB') + ' លើ ' + m(r'\Delta') + ' ។ ចម្ងាយ ' + m('HB') + ' ជា' + hl('គម្លាត') + 'រវាងអង្កត់កែងនិងអង្កត់ទ្រេត ។')]))

S.append(exfig('៤.២', 'ប្រៀបធៀបអង្កត់ទ្រេតនិងអង្កត់កែង', G.right_tri_hyp(), [
    p(m(r'\Delta AHB') + ' ជាត្រីកោណកែងត្រង់ ' + m('H') + ' ។ គេបាន'),
    p(m(r'\angle H>\angle A') + ' នាំឱ្យ ' + hl(m('AB>BH')) + ' ។'),
    p(m(r'\angle H>\angle B') + ' នាំឱ្យ ' + hl(m('AB>AH')) + ' ។ ដូចនេះក្នុងត្រីកោណកែង អ៊ីប៉ូតេនុសវែងជាងជ្រុងពីរទៀត ។')]))

S.append(theorem('៤.២', 'ជាទូទៅ ៖ អង្កត់កែង', hl('អង្កត់កែងមានប្រវែងខ្លីជាងអង្កត់ទ្រេត ។'), G.right_tri_hyp()))

S.append(exfig('៤.៣', 'អង្កត់ទ្រេតពីរ ៖ ករណី B និង C នៅម្ខាង', G.slant_same_side(), [
    p('ចំណុច ' + m('B') + ' និង ' + m('C') + ' ឋិតនៅលើ ' + m(r'\Delta') + ' ហើយ ' + m(r'AH\perp\Delta') + ' ។ បើ ' + m('B') + ' និង ' + m('C') + ' នៅម្ខាងនៃ ' + m('H') + ' ដែល ' + m('HB<HC') + ' ។ ប្រៀបធៀប ' + m('AB') + ' និង ' + m('AC') + ' ។'),
    p('ក្នុង ' + m(r'\Delta AHB') + ' មាន ' + m(r'\angle ABC') + ' ជាមុំក្រៅនៃ ' + m(r'\angle ABH') + ' ។ គេបាន ' + m(r'\angle ABC=90^\circ+\angle HAB') + ' ជាមុំទាល ។ ដូចនេះក្នុង ' + m(r'\Delta ABC') + ' ៖ ' + m(r'\angle ABC>\angle ACB') + ' នាំឱ្យ ' + hl(m('AC>AB')) + ' ។')]))

S.append(exfig('៤.៣', 'អង្កត់ទ្រេតពីរ ៖ ករណី B និង C នៅសងខាង', G.slant_two_sides(), [
    p('បើ ' + m('B') + ' និង ' + m('C') + ' នៅសងខាង ' + m('H') + ' ។ ដៅចំណុច ' + m("C'") + ' មួយនៅលើ ' + m(r'\Delta') + ' ដែល ' + m("HC'=HC") + ' ។'),
    p('គេបាន ' + m("AC=AC'>AB") + ' ' + gr('(' + m("HB<HC'=HC") + ')') + ' ។ ដូចនេះ ' + hl(m('AC>AB')) + ' ។')]))

S.append(exfig('៤.៣', 'ករណីគម្លាតស្មើគ្នា', G.equal_gaps(), [
    p('បើ ' + m('HB=HC') + ' នោះបន្ទាត់ ' + m('AH') + ' ជាមេដ្យាទ័រនៃអង្កត់ ' + m('BC') + ' នាំឱ្យ ' + hl(m('AB=AC')) + ' ។'),
    p('បើ ' + m('AB=AC') + ' នោះ ' + m('ABC') + ' ជាត្រីកោណសមបាត ។ គេទាញបានបន្ទាត់ ' + m('AH') + ' ជាមេដ្យាទ័រនៃបាត ' + m('BC') + ' ។ ដូចនេះ ' + hl(m('HB=HC')) + ' ។')],
    'ចំណុច ' + m('B') + ' និង ' + m('C') + ' ឋិតនៅលើបន្ទាត់ ' + m(r'\Delta') + ' និងអង្កត់ ' + m(r'AH\perp\Delta') + ' ។'))

S.append(ex('៤.៣', 'ជាទូទៅ ៖ អង្កត់ទ្រេតនិងអង្កត់ទ្រេត',
    cols(fig(whole(G.slant_two_sides())), _BOX + ol(['អង្កត់ទ្រេតពីរប៉ុនគ្នា មានគម្លាតស្មើគ្នា ។', 'អង្កត់ទ្រេតពីរដែលមានគម្លាតស្មើគ្នា ជាអង្កត់ទ្រេតប៉ុនគ្នា ។']) + '</div>'
         + _BOX + hl('ជាទូទៅ ៖') + ol(['រវាងអង្កត់ទ្រេតពីរ អង្កត់ទ្រេតមានគម្លាតធំជាអង្កត់ទ្រេតធំ ។', 'រវាងអង្កត់ទ្រេតពីរ អង្កត់ទ្រេតធំជាអង្កត់ទ្រេតដែលមានគម្លាតធំ ។']) + '</div>')))

S.append(exfig('លំហាត់គំរូ', 'AH < AO < AC', G.ex_ao(), [
    p('អង្កត់ ' + m('AH') + ' ជាអង្កត់កែង ហើយ ' + m('AO') + ' ជាអង្កត់ទ្រេត គេបាន ' + hl(m('AO>AH')) + ' (1) ។'),
    p('ដោយ ' + m('AB<AC') + ' ហើយចំណុច ' + m('H') + ' ឋិតនៅចន្លោះ ' + m('B') + ' និង ' + m('O') + ' គេទាញបាន ' + m('HO<HC') + ' នាំឱ្យ ' + hl(m('AO<AC')) + ' (2) ។'),
    p('តាម (1) និង (2) គេបាន ' + hl(m('AH<AO<AC')) + ' ។')],
    'គេឱ្យ ' + m('ABC') + ' ជាត្រីកោណមួយដែល ' + m('AB<AC') + ' ។ នៅក្នុងត្រីកោណនេះ គេគូសកម្ពស់ ' + m('AH') + ' និងមេដ្យាន ' + m('AO') + ' ។ ប្រៀបធៀប ' + m('AH') + ' , ' + m('OA') + ' និង ' + m('AC') + ' ។'))

S.append(exfig('ប្រតិបត្តិ', 'ផលបូកជ្រុង និងកម្ពស់', G.altitudes_fig(), [
    p('ក្នុងត្រីកោណ ' + m('ABC') + ' កម្ពស់ជាអង្កត់កែង ហើយជ្រុងជាអង្កត់ទ្រេត ៖'),
    p(m('AD<AB') + ' , ' + m('BE<BC') + ' , ' + m('CF<CA') + ' ' + hl('(អង្កត់កែងខ្លីជាងអង្កត់ទ្រេត)', '#595959')),
    p('ដូចនេះ ' + hl(m('AB+BC+AC>AD+BE+CF')) + ' ។')],
    'គេឱ្យអង្កត់ ' + m('AD') + ' , ' + m('BE') + ' និង ' + m('CF') + ' ជាកម្ពស់នៃ ' + m(r'\Delta ABC') + ' ។ បង្ហាញថា ' + m('AB+BC+AC>AD+BE+CF') + ' ។'))

# ================================================================ end
S.append(ex('សង្ខេបមេរៀន', 'អ្វីដែលយើងបានរៀនថ្ងៃនេះ',
    ul(['ត្រីកោណប៉ុនគ្នា ៖ ធាតុត្រូវគ្នា ៦ ប៉ុនគ្នា ។ ករណី ' + hl('ម.ជ.ម') + ' , ' + hl('ជ.ម.ជ') + ' , ' + hl('ជ.ជ.ជ') + ' ហើយចំពោះត្រីកោណកែង ' + hl('អ.ម') + ' , ' + hl('អ.ជ') + ' ។',
        'មេដ្យាទ័រនៃអង្កត់ ៖ ចំណុចលើមេដ្យាទ័រស្មើចម្ងាយពីចុងអង្កត់ ។ ត្រីកោណសមបាត ៖ មុំបាតស្មើគ្នា ។',
        'ក្នុងត្រីកោណ ជ្រុងវែងជាងឈមនឹងមុំធំជាង ។ ' + m('AB+BC>AC') + ' (វិសមភាពត្រីកោណ) ។',
        'អង្កត់កែងខ្លីជាងអង្កត់ទ្រេត ។ អង្កត់ទ្រេតមានគម្លាតធំជាអង្កត់ទ្រេតធំ ។'])))
S.append({'k': 'title', 'html': '<h1>ចប់មេរៀន</h1><p class="ts-sub">ការប្រៀបធៀបត្រីកោណ</p>'})

# ================================================================ Part 1 = three sub-parts of two hours each, every one a full set like the class slides
BAND1 = '១. ត្រីកោណប៉ុនគ្នា'


def _ix(name):
    return next(i for i, x in enumerate(S) if x.get('mark') == name)


def _clean(lst):
    return [x for x in lst if 'mark' not in x]


def textbook(pages):
    return {'k': 'ex', 'raw': True, 'nostep': True, 'html': '<p class="ts-kicker">សៀវភៅសិក្សាគោល គណិតវិទ្យាថ្នាក់ទី៨</p>'
            '<div class="esc-book"><img src="/img/esc/textbook.jpg" alt=""><div class="bk-t">ប្អូនៗអាចសិក្សាបន្ថែមនៅក្នុង<br>សៀវភៅសិក្សាគោល<br>គណិតវិទ្យាថ្នាក់ទី៨<br><b>ទំព័រ ' + pages + '</b></div></div>'}


def objectives(vj, bn, ch):
    row = lambda a, b: f'<p class="ob"><span class="ob-l">{a}</span> : {b}</p>'
    return {'k': 'ex', 'raw': True, 'nostep': True, 'html': '<p class="ts-kicker">វត្ថុបំណងមេរៀន</p><h2>❑ បន្ទាប់ពីបានសិក្សាមេរៀននេះចប់ប្អូនៗ៖</h2><div class="esc-obj">'
            + row('វិជ្ជាសម្បទា', vj) + row('បំណិនសម្បទា', bn) + row('ចរិយាសម្បទា', ch) + '</div>'}


_CH = 'មានស្មារតីម៉ត់ចត់ យកចិត្តទុកដាក់ និងសហការគ្នា ក្នុងការសង់រូប និងដោះស្រាយលំហាត់។'


def plan(cards):
    """ផែនការបង្រៀន ១២០ នាទី: five time cards and a bar whose widths follow the minutes"""
    mins = [10, 30, 45, 25, 10]
    heads = ['០–១០', '១០–៤០', '៤០–៨៥', '៨៥–១១០', '១១០–១២០']
    out = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:.4em">'
    for k, (a, b, c) in enumerate(cards):
        col = '#6b8ea3' if k in (0, 4) else NAVY
        out += (f'<div style="border:3px solid {NAVY};background:#fff;text-align:center;font-size:.92em"><div style="background:{col};color:#fff;font-weight:800;padding:.25em">{heads[k]} នាទី</div>'
                f'<div style="padding:.3em .3em;min-height:9em"><div style="color:#595959">{a}</div><div style="font-weight:800;margin:.1em 0">{b}</div><div style="color:#595959;font-size:.9em;line-height:1.4">{c}</div></div></div>')
    out += '</div><div style="display:flex;margin-top:.7em">'
    for k, mn in enumerate(mins):
        col = '#6b8ea3' if k in (0, 4) else NAVY
        out += f'<div style="flex:{mn};background:{col};color:#fff;text-align:center;font-weight:800;border-right:2px solid #fff">{kh(mn)}</div>'
    out += '</div>' + p('រយៈពេលនីមួយៗគិតជានាទី (សរុប ១២០ នាទី)', '')
    return {'k': 'ex', 'raw': True, 'nostep': True, 'html': '<p class="ts-kicker">ផែនការបង្រៀន ១២០ នាទី</p>' + out}


def overview(today):
    """the three conditions (class slide 12): the one taught today has a navy header and border, the others are grey with «មេរៀនបន្ទាប់»"""
    spec = [('asa', 'ម.ជ.ម', 'ជ្រុងមួយ និងមុំពីរជាប់នឹងជ្រុងនោះ'), ('sas', 'ជ.ម.ជ', 'មុំមួយ អមដោយជ្រុងពីរ'), ('sss', 'ជ.ជ.ជ', 'ជ្រុងទាំងបីប៉ុនរៀងគ្នា')]
    order = ['asa', 'sas', 'sss']
    cards = []
    for k, (kind, t, cap) in enumerate(spec):
        diff = order.index(kind) - order.index(today)
        on = diff == 0
        col = NAVY if on else '#808080'
        tag = ('ថ្ងៃនេះ', RED) if on else (('មេរៀនមុន' if diff < 0 else 'មេរៀនបន្ទាប់'), '#808080')
        cards.append(rvd(k + 1, f'<div class="ovc" style="border-color:{col}"><div class="ovh" style="background:{col}">{t}</div>'
                                f'<div class="ovf">{fig(G.mini(kind, grey=not on))}</div><div class="ovt">{cap}</div>'
                                f'<div class="ovg" style="color:{tag[1]}">{tag[0]}</div></div>'))
    return {'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">១. ត្រីកោណប៉ុនគ្នា</p><p class="esc-sec">❑ ១.២. លក្ខខណ្ឌនៃត្រីកោណប៉ុនគ្នា</p>'
            '<p>ត្រីកោណពីរប៉ុនគ្នា កាលណាធាតុត្រូវគ្នា' + hl('ទាំង ៦', NAVY) + ' ប៉ុនគ្នា។ ប៉ុន្តែ គេសិក្សាតែ' + hl('ធាតុ ៣') + ' ប៉ុនរៀងគ្នា តាមលក្ខខណ្ឌខាងក្រោម៖</p>'
            + '<div class="ovgrid">' + ''.join(cards) + '</div>'}


def homework(c1, c2, bar):
    box = lambda x: f'<div style="border:3px solid {NAVY};border-radius:14px;background:#fff;padding:.4em .7em">{x}</div>'
    return {'k': 'ex', 'raw': True, 'nostep': True, 'html': '<p class="ts-kicker">កិច្ចការផ្ទះ និងបណ្តាំផ្ញើ</p>' + gridn(2, box(c1), box(c2), gap='.7em')
            + f'<div style="background:{NAVY};color:#fff;font-weight:800;border-radius:14px;padding:.35em 1em;margin-top:.6em">{hl("បណ្តាំផ្ញើ៖", "#fff")} {bar}</div>'}


def titled(x, band):
    x['band'] = band
    return x


# ---------------- sub-part 1 (ESC_មេរៀនទី១២-01): 1.1 definition and 1.2.1 ម.ជ.ម
D1 = part(1, '', 'ការប្រៀបធៀបត្រីកោណ', 'មេរៀនទី ១២', band=BAND1)
O1 = objectives('ចង្អុលបង្ហាញត្រីកោណប៉ុនគ្នា និងធាតុត្រូវគ្នានៃត្រីកោណប៉ុនគ្នាបានច្បាស់លាស់ តាមរយៈការសង្កេតរូប និងការឆ្លើយសំណួររបស់គ្រូ។',
                'សង់ និងប្រៀបធៀបត្រីកោណពីរតាមលក្ខខណ្ឌ ម.ជ.ម ហើយទាញរកវិបាក ដើម្បីដោះស្រាយលំហាត់បានត្រឹមត្រូវ។', _CH)
P1 = plan([('ចាប់ផ្តើម', 'ស្វាគមន៍', 'រំលឹកមេរៀន ណែនាំវត្ថុបំណង'), ('១.១', 'និយមន័យ', 'ឧទាហរណ៍ លំហាត់គំរូ ប្រតិបត្តិ'),
           ('១.២.១', 'ករណី ម.ជ.ម', 'សង់ ប្រៀបធៀប ទ្រឹស្តីបទ លំហាត់គំរូ'), ('អនុវត្ត', 'ប្រតិបត្តិ ម.ជ.ម', 'ប្រតិបត្តិ ពង្រឹងពុទ្ធិ ដោះស្រាយលំហាត់ និងកែតម្រូវ'),
           ('បញ្ចប់', 'សង្ខេបមេរៀន', 'សំណួរ-ចម្លើយ កិច្ចការផ្ទះ')])
X1 = prob_sol('ពង្រឹងពុទ្ធិ', 'លំហាត់', 'ចតុកោណ ' + m('ABCD') + ' មានអង្កត់ទ្រូង ' + m('AC') + ' ដែល ' + m(r'\angle BAC=\angle DAC') + ' និង ' + m(r'\angle BCA=\angle DCA') + ' ។',
    p(hl('ក.', NAVY) + ' ប្រៀបធៀប ' + m(r'\Delta ABC') + ' និង ' + m(r'\Delta ADC')) + p(hl('ខ.', NAVY) + ' ទាញបញ្ជាក់ថា ' + m('AB=AD') + ' និង ' + m('CB=CD')),
    p(hl('ក.', NAVY) + ' ក្នុង ' + m(r'\Delta ABC') + ' និង ' + m(r'\Delta ADC') + ' មាន៖')
    + p(m(r'\angle BAC=\angle DAC') + ' ' + gr('(សម្មតិកម្ម)')) + p(m('AC=AC') + ' ' + gr('(ជ្រុងរួម)')) + p(m(r'\angle BCA=\angle DCA') + ' ' + gr('(សម្មតិកម្ម)'))
    + pc('ដូចនេះ ' + hl(m(r'\Delta ABC\cong\Delta ADC')) + ' (ម.ជ.ម)')
    + '<p class="concl fin" style="width:auto;margin-left:1cqw">' + hl('ខ.', NAVY) + ' តាមវិបាក ដូចនេះ ' + hl(m('AB=AD')) + ' និង ' + hl(m('CB=CD')) + '</p>', G.quad_diag())
H1 = homework(
    hl('លំហាត់ ១ ៖') + ' គេឱ្យ ' + m(r'\Delta ABC\cong\Delta DEF') + ' ដែល ' + m(r'\angle A=50^\circ') + ' និង ' + m(r'\angle E=70^\circ') + ' ។ រករង្វាស់មុំ ' + m(r'\angle B\ ,\ \angle C\ ,\ \angle D') + ' និង ' + m(r'\angle F') + ' ។' + fig(G.hw_cong()),
    hl('លំហាត់ ២ ៖') + ' ' + m('M') + ' ជាចំណុចកណ្តាលនៃ ' + m('AB') + ' ។ ' + m(r'Ax\parallel By') + ' ហើយបន្ទាត់កាត់តាម ' + m('M') + ' កាត់ ' + m('Ax') + ' ត្រង់ ' + m('C') + ' និង ' + m('By') + ' ត្រង់ ' + m('D') + ' ។ បង្ហាញថា ' + m(r'\Delta AMC\cong\Delta BMD') + ' និង ' + m('MC=MD') + ' ។' + fig(G.hw_mid()),
    'មេរៀនបន្ទាប់ ករណី ជ.ម.ជ — សូមត្រៀមបន្ទាត់ រ៉ាប់ទ័រ និងក្រដាសកាតុង')
assert (180 - 50 - 70, 70, 50) == (60, 70, 50)

# ---------------- sub-part 2 (ESC_មេរៀនទី១២-02): 1.2.2 ជ.ម.ជ
D2 = part(2, '', 'ការប្រៀបធៀបត្រីកោណ', 'មេរៀនទី ១២', band=BAND1)
R2 = {'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">រំលឹកមេរៀន</p><h2>❑ ចំណេះដឹងដែលយើងនឹងប្រើក្នុងមេរៀនថ្ងៃនេះ</h2>'
      + gridn(3, _card('ត្រីកោណប៉ុនគ្នា', G.mini('sss'), 'ធាតុត្រូវគ្នា ៦ ប៉ុនគ្នា', NAVY), _card('ម.ជ.ម', G.mini('asa'), 'ជ្រុងមួយប៉ុនគ្នាជាប់និងមុំពីរប៉ុនរៀងគ្នា', NAVY),
              _card('វិបាក', G.mini('asa'), 'ធាតុ ៣ ទៀតក៏ប៉ុនគ្នា', NAVY))
      + '<div style="border:3px solid #0f5173;border-radius:14px;background:#f2f2f2;padding:.3em 1em;margin-top:.5em">'
      + p(hl('សំណួរ ៖', RED) + ' ' + m(r'\Delta ABC\cong\Delta DEF') + ' (ម.ជ.ម) ដែល ' + m(r'AB=5\text{ cm}') + ' និង ' + m(r'\angle C=70^\circ') + ' ។ រក ' + m('DE') + ' និង ' + m(r'\angle F') + ' ?')
      + rvd(1, p(hl('ចម្លើយ ៖', RED) + ' ' + m(r'DE=AB=5\text{ cm}') + ' , ' + m(r'\angle F=\angle C=70^\circ'))) + '</div>'}
O2 = objectives('ចង្អុលបង្ហាញមុំអមដោយជ្រុងពីរ និងបញ្ជាក់ត្រីកោណប៉ុនគ្នាតាមលក្ខខណ្ឌ ជ.ម.ជ បានច្បាស់លាស់ តាមរយៈការសង្កេតរូប និងការឆ្លើយសំណួររបស់គ្រូ។',
                'សង់ និងប្រៀបធៀបត្រីកោណពីរតាមលក្ខខណ្ឌ ជ.ម.ជ ហើយទាញរកវិបាក ដើម្បីដោះស្រាយលំហាត់បានត្រឹមត្រូវ។', _CH)
P2_CARDS = [('ចាប់ផ្តើម', 'ស្វាគមន៍', 'រំលឹកមេរៀន ណែនាំវត្ថុបំណង'), ('១.២', 'មុំអម', 'ឧទាហរណ៍ និយមន័យ លំហាត់គំរូ ប្រតិបត្តិ'),
           ('១.២.២', 'ករណី ជ.ម.ជ', 'សង់ ប្រៀបធៀប ទ្រឹស្តីបទ លំហាត់គំរូ'), ('អនុវត្ត', 'ប្រតិបត្តិ ជ.ម.ជ', 'ប្រតិបត្តិ ពង្រឹងពុទ្ធិ ដោះស្រាយលំហាត់ និងកែតម្រូវ'),
           ('បញ្ចប់', 'សង្ខេបមេរៀន', 'សំណួរ-ចម្លើយ កិច្ចការផ្ទះ')]
P2 = plan(P2_CARDS)
HAND2 = exfig('១.២', 'ឧទាហរណ៍ ៖ កាត់ត្រីកោណត្រួតលើគ្នា', G.cutout(), [
    p('ដាក់ ' + m('ABC') + ' ត្រួតលើ ' + m("A'B'C'") + ' ៖ ធាតុនីមួយៗត្រួតស៊ីគ្នា ឬទេ?'),
    p('គេថា ' + m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' ជា' + hl('ត្រីកោណប៉ុនគ្នា') + ' ព្រោះមានជ្រុង ២ និងមុំអម ១ ប៉ុនគ្នា ។')],
    'គូសត្រីកោណ ' + m('ABC') + ' មួយដែល ' + m(r'AB=4\text{ cm}') + ' , ' + m(r'AC=6\text{ cm}') + ' និង ' + m(r'\angle A=60^\circ') + ' នៅលើក្រដាសកាតុង ហើយកាត់វាចេញ។ ប្រើជាគំរូ គូស និងកាត់ត្រីកោណ ' + m("A'B'C'") + ' ដែលមានធាតុដូចគ្នា។')
_T2 = lambda a, b: f'<tr><td>{m(a)}</td><td>{m(b)}</td></tr>'
TAB2 = ex('១.២', 'ធាតុដែលឱ្យ និងវិបាក', cols(fig(whole(G.theorem_pair('sas'))),
         p(m(r'\Delta ABC') + ' និង ' + m(r"\Delta A'B'C'") + ' មានធាតុប៉ុនគ្នា ៣ (ជ្រុង ២ និងមុំអម ១) នោះធាតុដែលនៅសល់ក៏ប៉ុនគ្នាដែរ ៖')
         + '<table class="sumtab" style="margin:.3em auto;border-collapse:collapse"><tr><th>សម្មតិកម្ម</th><th>' + hl('វិបាក') + '</th></tr>'
         + _T2("AB=A'B'", r"\angle B=\angle B'") + _T2(r"\angle A=\angle A'", r"\angle C=\angle C'") + _T2("AC=A'C'", "BC=B'C'") + '</table>')
         + _BOX + 'ជ.ម.ជ ៖ ធាតុត្រូវគ្នាដែលប៉ុនគ្នា = ' + hl('ជ្រុង ២') + ' + ' + hl('មុំអម ១') + ' (សរុប ធាតុ ៣)</div>')
DEF2 = ex('និយមន័យ', 'មុំអម', cols(fig(G.incl_angle()), _BOX + hl('និយមន័យ ៖') + ' មុំអមដោយជ្រុងពីរ គឺជាមុំដែលឋិតនៅរវាងជ្រុងទាំងពីរនោះ (ត្រង់កំពូលរួមនៃជ្រុងទាំងពីរ) ។</div>'
          + p(m('AB') + ' និង ' + m('AC') + ' ➜ មុំអម ' + hl(m(r'\angle A'))) + p(m('AB') + ' និង ' + m('BC') + ' ➜ មុំអម ' + hl(m(r'\angle B'))) + p(m('AC') + ' និង ' + m('BC') + ' ➜ មុំអម ' + hl(m(r'\angle C'))))
          + p('ចំណាំ ៖ ជ.ម.ជ ត្រូវការមុំអម (នៅរវាងជ្រុងទាំងពីរ) មិនមែនមុំណាមួយទេ ។'))
EX2 = exfig('លំហាត់គំរូ', 'រកមុំអម', G.incl_ex(), [
    p('ជ្រុង ' + m('DE') + ' និង ' + m('DF') + ' ជួបគ្នាត្រង់ ' + m('D') + ' នោះមុំអមគឺ ' + hl(m(r'\angle D'))) + p('ជ្រុង ' + m('DE') + ' និង ' + m('EF') + ' ជួបគ្នាត្រង់ ' + m('E') + ' នោះមុំអមគឺ ' + hl(m(r'\angle E')))
    + p('ជ្រុង ' + m('DF') + ' និង ' + m('EF') + ' ជួបគ្នាត្រង់ ' + m('F') + ' នោះមុំអមគឺ ' + hl(m(r'\angle F')))],
    'ក្នុង ' + m(r'\Delta DEF') + ' ចូរកំណត់មុំអមដោយជ្រុងពីរនីមួយៗ ។')
PR2 = exfig('ប្រតិបត្តិ', 'ពន្យល់ថា ហេតុអ្វីមិនអាចសន្និដ្ឋានថា ΔABC ≅ ΔDEF តាម ជ.ម.ជ ?', G.sas_not(), [
    p('ក្នុង ' + m(r'\Delta ABC') + ' មុំ ' + m(r'40^\circ') + ' (' + m(r'\angle A') + ') នៅរវាង ' + m('AB') + ' និង ' + m('AC') + ' ✓') + p('ក្នុង ' + m(r'\Delta DEF') + ' មុំ ' + m(r'40^\circ') + ' (' + m(r'\angle D') + ') មិននៅរវាង ' + m('DE') + ' និង ' + m('EF') + ' ទេ ដូចនេះមិនអាចប្រើ ជ.ម.ជ បានឡើយ ។')])
X2 = prob_sol('ពង្រឹងពុទ្ធិ', 'លំហាត់', m('AB') + ' និង ' + m('CD') + ' ប្រសព្វគ្នាត្រង់ ' + m('O') + ' ជាចំណុចកណ្តាលរបស់អង្កត់ទាំងពីរ ។',
    p(hl('ក.', NAVY) + ' ប្រៀបធៀប ' + m(r'\Delta AOC') + ' និង ' + m(r'\Delta BOD')) + p(hl('ខ.', NAVY) + ' ទាញបញ្ជាក់ថា ' + m('AC=BD')),
    p(hl('ក.', NAVY) + ' ក្នុង ' + m(r'\Delta AOC') + ' និង ' + m(r'\Delta BOD') + ' មាន៖')
    + p(m('OA=OB') + ' ' + gr('(O ជាចំណុចកណ្តាលនៃ AB)')) + p(m('OC=OD') + ' ' + gr('(O ជាចំណុចកណ្តាលនៃ CD)')) + p(m(r'\angle AOC=\angle BOD') + ' ' + gr('(មុំទល់កំពូល)'))
    + pc('ដូចនេះ ' + hl(m(r'\Delta AOC\cong\Delta BOD')) + ' (ជ.ម.ជ)')
    + '<p class="concl fin" style="width:auto;margin-left:1cqw">' + hl('ខ.', NAVY) + ' តាមវិបាក ដូចនេះ ' + hl(m('AC=BD')) + ' ។</p>', G.sas_extra())
H2 = homework(
    hl('លំហាត់ ១ ៖') + ' ក្នុងរូប ' + m('AB=DE') + ' , ' + m('BC=EF') + ' , ' + m(r'\angle B=\angle E=70^\circ') + ' និង ' + m(r'\angle A=50^\circ') + ' ។ បញ្ជាក់ថា ' + m(r'\Delta ABC\cong\Delta DEF') + ' (ជ.ម.ជ) រួចរកមុំ ' + m(r'\angle D') + ' និង ' + m(r'\angle F') + ' ។' + fig(G.hw_sas1()),
    hl('លំហាត់ ២ ៖') + ' ' + m('ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + m('A') + ' ។ ' + m('E') + ' នៅលើ ' + m('AB') + ' និង ' + m('F') + ' នៅលើ ' + m('AC') + ' ដែល ' + m('AE=AF') + ' ។ បង្ហាញថា ' + m('BF=CE') + ' ។' + fig(G.hw_sas2()),
    'មេរៀនបន្ទាប់ ករណី ជ.ជ.ជ — សូមត្រៀមបន្ទាត់ ដែកឈាន និងក្រដាសកាតុង')

# ---------------- sub-part 3: ជ.ជ.ជ and right triangles (the content built before; the full 2-hour set is still to do)
D3 = part(3, '', 'ការប្រៀបធៀបត្រីកោណ', 'មេរៀនទី ១២', band=BAND1)
O3 = objectives('ចង្អុលបង្ហាញត្រីកោណប៉ុនគ្នាតាមលក្ខខណ្ឌ ជ.ជ.ជ និងចំពោះត្រីកោណកែងតាមលក្ខខណ្ឌ អ.ម និង អ.ជ បានច្បាស់លាស់ តាមរយៈការសង្កេតរូប និងការឆ្លើយសំណួររបស់គ្រូ។',
                'សង់ និងប្រៀបធៀបត្រីកោណតាមលក្ខខណ្ឌ ជ.ជ.ជ អ.ម និង អ.ជ ហើយទាញរកវិបាក ដើម្បីដោះស្រាយលំហាត់បានត្រឹមត្រូវ។', _CH)

_o = _clean(S[:_ix('S11')])
profile = _o[0]
recall1 = _o[2]
sl11 = _clean(S[_ix('S11'):_ix('OVERVIEW')])
sl_asa = _clean(S[_ix('ASA'):_ix('SAS')])
sl_sas = _clean(S[_ix('SAS'):_ix('SSS')])
sl_sss = _clean(S[_ix('SSS'):_ix('END1')])
tail = _clean(S[_ix('END1'):])
# ---------------- summary slide (the class slide «សង្ខេបមេរៀន»): three steps and an exit ticket of three questions
def summary(case, steps, note, qa):
    st = ''.join(f'<div class="esc-step"><span class="num">{kh(i)}</span><span>{t}</span></div>' for i, t in enumerate(steps, 1))
    nb = f'<div style="border:3px solid #0f5173;border-radius:14px;background:#f2f2f2;padding:.3em 1em;margin-top:.6em">{hl("ចំណាំ៖")} {note}</div>'
    ex_ = ''.join(f'<div class="q">{hl(kh(i) + ".", NAVY)} {q}</div>' + rvd(i, f'<div style="margin-left:1.4em">{hl("ចម្លើយ៖")} {a_}</div>') for i, (q, a_) in enumerate(qa, 1))
    return {'k': 'ex', 'raw': True, 'html': f'<p class="ts-kicker">សង្ខេបមេរៀន</p><h2>❑ ជំហាន ៣ ដើម្បីស្រាយថាត្រីកោណពីរប៉ុនគ្នា ({case})</h2>'
            f'<div class="esc-steps"><div>{st}{nb}</div><div class="esc-exit"><div class="hd">សំណួរបញ្ចប់មេរៀន (៣ សំណួរ)</div><div class="bd">{ex_}</div></div></div>'}


SUM1 = summary('ម.ជ.ម', ['រក ' + hl('ជ្រុងមួយ') + ' ដែលប៉ុនគ្នា', 'រក ' + hl('មុំពីរជាប់') + 'នឹងជ្រុងនោះ ប៉ុនរៀងគ្នា', hl('សន្និដ្ឋាន') + ' ' + m(r"\Delta ABC\cong\Delta A'B'C'") + ' (ម.ជ.ម) រួចទាញ ' + hl('វិបាក')],
               'ផ្គូផ្គងកំពូល ' + m(r"A\leftrightarrow A'\ ,\ B\leftrightarrow B'\ ,\ C\leftrightarrow C'") + ' និងសរសេរហេតុផលក្នុងវង់ក្រចក ។',
               [('ត្រីកោណពីរប៉ុនគ្នា មានធាតុត្រូវគ្នាប៉ុនគ្នាប៉ុន្មាន?', 'ធាតុ ៦ (មុំ ៣ និងជ្រុង ៣)'),
                (m(r'\Delta MNP\cong\Delta XYZ') + ' ។ ជ្រុង ' + m('NP') + ' ត្រូវនឹងជ្រុងណា?', m('NP=YZ')),
                (m(r'\Delta ABC') + ' និង ' + m(r'\Delta DEF') + ' មាន ' + m(r'\angle A=\angle D') + ' , ' + m('AB=DE') + ' , ' + m(r'\angle B=\angle E') + ' ។ តើប៉ុនគ្នាទេ?', m(r'\Delta ABC\cong\Delta DEF') + ' (ម.ជ.ម)')])
SUM2 = summary('ជ.ម.ជ', ['រក ' + hl('ជ្រុងពីរ') + ' ដែលប៉ុនរៀងគ្នា', 'រក ' + hl('មុំអម') + 'រវាងជ្រុងទាំងពីរនោះ ប៉ុនគ្នា', hl('សន្និដ្ឋាន') + ' ' + m(r"\Delta ABC\cong\Delta A'B'C'") + ' (ជ.ម.ជ) រួចទាញ ' + hl('វិបាក')],
               'មុំត្រូវនៅ ' + hl('រវាង') + ' ជ្រុងទាំងពីរ ។ បើមុំនៅក្រៅ មិនអាចប្រើ ជ.ម.ជ បានទេ ។',
               [('ជ.ម.ជ ត្រូវការធាតុអ្វីខ្លះ?', 'ជ្រុង ២ ប៉ុនរៀងគ្នា និងមុំអមរវាងជ្រុងទាំងពីរ'),
                (m(r'\Delta ABC\cong\Delta DEF') + ' (ជ.ម.ជ) ។ មុំ ' + m(r'\angle C') + ' ត្រូវនឹងមុំណា?', m(r'\angle F')),
                (m('AB=DE') + ' , ' + m('AC=DF') + ' , ' + m(r'\angle A=\angle D') + ' ។ តើប៉ុនគ្នាទេ?', m(r'\Delta ABC\cong\Delta DEF') + ' (ជ.ម.ជ)')])
SUM3 = summary('ជ.ជ.ជ អ.ម អ.ជ', ['រកជ្រុងទាំងបី ដែលប៉ុនរៀងគ្នា (' + hl('ជ.ជ.ជ') + ')', 'ត្រីកោណកែង ៖ រកអ៊ីប៉ូតេនុស និង ' + hl('មុំស្រួច') + ' (អ.ម) ឬ ' + hl('ជ្រុងមុំកែង') + ' (អ.ជ)', hl('សន្និដ្ឋាន') + ' ប៉ុនគ្នា រួចទាញ ' + hl('វិបាក')],
               'ជ.ជ.ជ មិនត្រូវការមុំទេ ។ អ.ម និង អ.ជ ប្រើបានតែត្រីកោណកែង ។',
               [('ជ.ជ.ជ ត្រូវការធាតុប៉ុន្មាន?', 'ជ្រុង ៣ ប៉ុនរៀងគ្នា'),
                ('ត្រីកោណកែងពីរមានអ៊ីប៉ូតេនុសប៉ុនគ្នា និងមុំស្រួចមួយប៉ុនគ្នា ។ ប្រើករណីអ្វី?', 'អ.ម'),
                ('ត្រីកោណកែងពីរមានអ៊ីប៉ូតេនុសប៉ុនគ្នា និងជ្រុងមុំកែងមួយប៉ុនគ្នា ។ ប្រើករណីអ្វី?', 'អ.ជ')])

# ---------------- homework solutions (shown at the start of the next sub-part, before the new lesson)
def hwsol(title, fg, items, given):
    return titled(exfig('ដំណោះស្រាយ', title, fg, items, given), 'ដំណោះស្រាយកិច្ចការផ្ទះ')


SOL1 = [
    hwsol('លំហាត់ ១', G.hw_cong_sol(), [
        p('ដោយ ' + m(r'\Delta ABC\cong\Delta DEF') + ' ធាតុត្រូវគ្នាប៉ុនគ្នា ៖ ' + m(r'\angle A=50^\circ') + ' ត្រូវនឹង ' + m(r'\angle D') + ' ហើយ ' + m(r'\angle E=70^\circ') + ' ត្រូវនឹង ' + m(r'\angle B') + ' ។'),
        p(hl(m(r'\angle B=\angle E=70^\circ')) + ' , ' + hl(m(r'\angle D=\angle A=50^\circ'))),
        p('ក្នុង ' + m(r'\Delta ABC') + ' ៖ ' + m(r'\angle C=180^\circ-50^\circ-70^\circ=') + hl(m(r'60^\circ'))) + p(m(r'\angle F=\angle C=') + hl(m(r'60^\circ')) + ' ។')],
        hl('លំហាត់ ១ ៖') + ' គេឱ្យ ' + m(r'\Delta ABC\cong\Delta DEF') + ' ដែល ' + m(r'\angle A=50^\circ') + ' និង ' + m(r'\angle E=70^\circ') + ' ។ រករង្វាស់មុំ ' + m(r'\angle B\ ,\ \angle C\ ,\ \angle D') + ' និង ' + m(r'\angle F') + ' ។'),
    hwsol('លំហាត់ ២', G.hw_mid_sol(), [
        p('ក្នុង ' + m(r'\Delta AMC') + ' និង ' + m(r'\Delta BMD') + ' មាន') + p(m('AM=BM') + ' ' + gr('(M ជាចំណុចកណ្តាលនៃ AB)')),
        p(m(r'\angle AMC=\angle BMD') + ' ' + gr('(មុំទល់កំពូល)')),
        p(m(r'\angle MAC=\angle MBD') + ' ' + gr('(មុំឆ្លាស់ក្នុង ព្រោះ ' + m(r'Ax\parallel By') + ')')) + p('ដូចនេះ ' + hl(m(r'\Delta AMC\cong\Delta BMD')) + ' (តាមលក្ខខណ្ឌ ម.ជ.ម)'),
        p('តាមវិបាក ជ្រុងត្រូវគ្នាប៉ុនគ្នា ដូចនេះ ' + hl(m('MC=MD')) + ' ។')],
        hl('លំហាត់ ២ ៖') + ' ' + m('M') + ' ជាចំណុចកណ្តាលនៃ ' + m('AB') + ' ។ ' + m(r'Ax\parallel By') + ' ហើយបន្ទាត់កាត់តាម ' + m('M') + ' កាត់ ' + m('Ax') + ' ត្រង់ ' + m('C') + ' និង ' + m('By') + ' ត្រង់ ' + m('D') + ' ។ បង្ហាញថា ' + m(r'\Delta AMC\cong\Delta BMD') + ' និង ' + m('MC=MD') + ' ។')]
SOL2 = [
    hwsol('លំហាត់ ១', G.hw_sas1_sol(), [
        p('ក្នុង ' + m(r'\Delta ABC') + ' និង ' + m(r'\Delta DEF') + ' មាន') + p(m('AB=DE') + ' , ' + m('BC=EF') + ' ' + gr('(សម្មតិកម្ម)')) + p(m(r'\angle B=\angle E=70^\circ') + ' (មុំអម) ដូចនេះ ' + hl(m(r'\Delta ABC\cong\Delta DEF')) + ' (តាមលក្ខខណ្ឌ ជ.ម.ជ)'),
        p('តាមវិបាក ' + hl(m(r'\angle D=\angle A=50^\circ')) + ' ។'),
        p(m(r'\angle F=\angle C=180^\circ-50^\circ-70^\circ=') + hl(m(r'60^\circ')) + ' ។')],
        hl('លំហាត់ ១ ៖') + ' ក្នុងរូប ' + m('AB=DE') + ' , ' + m('BC=EF') + ' , ' + m(r'\angle B=\angle E=70^\circ') + ' និង ' + m(r'\angle A=50^\circ') + ' ។ បញ្ជាក់ថា ' + m(r'\Delta ABC\cong\Delta DEF') + ' (ជ.ម.ជ) រួចរកមុំ ' + m(r'\angle D') + ' និង ' + m(r'\angle F') + ' ។'),
    hwsol('លំហាត់ ២', G.hw_sas2_sol(), [
        p('ក្នុង ' + m(r'\Delta ABF') + ' និង ' + m(r'\Delta ACE') + ' មាន'),
        p(m('AB=AC') + ' ' + gr('(ត្រីកោណសមបាតកំពូល A)')),
        p(m('AF=AE') + ' ' + gr('(សម្មតិកម្ម)')),
        p(m(r'\angle BAF=\angle CAE') + ' ' + gr('(មុំរួម)')) + p('ដូចនេះ ' + hl(m(r'\Delta ABF\cong\Delta ACE')) + ' (តាមលក្ខខណ្ឌ ជ.ម.ជ) នាំឱ្យ ' + hl(m('BF=CE')) + ' ។')],
        hl('លំហាត់ ២ ៖') + ' ' + m('ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + m('A') + ' ។ ' + m('E') + ' នៅលើ ' + m('AB') + ' និង ' + m('F') + ' នៅលើ ' + m('AC') + ' ដែល ' + m('AE=AF') + ' ។ បង្ហាញថា ' + m('BF=CE') + ' ។')]
assert 180 - 50 - 70 == 60

THANKS = {'k': 'title', 'c': 'esc-end', 'raw': True, 'html': '<h1>សូមអរគុណ</h1>'}
_P0 = ('ចាប់ផ្តើម', 'ស្វាគមន៍', 'ពិនិត្យកិច្ចការផ្ទះ រំលឹកមេរៀន ណែនាំវត្ថុបំណង')

# ---------------- sub-part 3 (full set): ជ.ជ.ជ and right triangles
R3 = {'k': 'ex', 'raw': True, 'html': '<p class="ts-kicker">រំលឹកមេរៀន</p><h2>❑ ចំណេះដឹងដែលយើងនឹងប្រើក្នុងមេរៀនថ្ងៃនេះ</h2>'
      + gridn(3, _card('ម.ជ.ម', G.mini('asa'), 'ជ្រុងមួយប៉ុនគ្នាជាប់និងមុំពីរប៉ុនរៀងគ្នា', NAVY), _card('ជ.ម.ជ', G.mini('sas'), 'មុំមួយប៉ុនគ្នាអមដោយជ្រុងពីរប៉ុនរៀងគ្នា', NAVY),
              _card('ត្រីកោណសមបាត', G.recall_sum(), 'មុំបាតទាំងពីរប៉ុនគ្នា', NAVY))
      + '<div style="border:3px solid #0f5173;border-radius:14px;background:#f2f2f2;padding:.3em 1em;margin-top:.5em">'
      + p(hl('សំណួរ ៖', RED) + ' ' + m(r'\Delta ABC\cong\Delta DEF') + ' (ជ.ម.ជ) ដែល ' + m(r'BC=7\text{ cm}') + ' និង ' + m(r'\angle B=40^\circ') + ' ។ រក ' + m('EF') + ' និង ' + m(r'\angle E') + ' ?')
      + rvd(1, p(hl('ចម្លើយ ៖', RED) + ' ' + m(r'EF=BC=7\text{ cm}') + ' , ' + m(r'\angle E=\angle B=40^\circ'))) + '</div>'}
P3 = plan([_P0, ('១.២.៣', 'ករណី ជ.ជ.ជ', 'សង់ ប្រៀបធៀប ទ្រឹស្តីបទ លំហាត់គំរូ'), ('១.៣', 'ត្រីកោណកែង', 'អ.ម អ.ជ លំហាត់គំរូ ប្រតិបត្តិ'),
           ('អនុវត្ត', 'ប្រតិបត្តិ អ.ម អ.ជ', 'ប្រតិបត្តិ ពង្រឹងពុទ្ធិ ដោះស្រាយលំហាត់ និងកែតម្រូវ'), ('បញ្ចប់', 'សង្ខេបមេរៀន', 'សំណួរ-ចម្លើយ កិច្ចការផ្ទះ')])
X3 = titled(exfig('ពង្រឹងពុទ្ធិ', '', G.iso_median(), [
    p('ក្នុង ' + m(r'\Delta ABD') + ' និង ' + m(r'\Delta ACD') + ' មាន') + p(m('AB=AC') + ' ' + gr('(ត្រីកោណសមបាត)')),
    p(m('BD=DC') + ' ' + gr('(D ជាចំណុចកណ្តាលនៃ BC)')),
    p(m('AD') + ' ជាជ្រុងរួម ដូចនេះ ' + hl(m(r'\Delta ABD\cong\Delta ACD')) + ' (តាមលក្ខខណ្ឌ ជ.ជ.ជ)'),
    p('តាមវិបាក ' + m(r'\angle ADB=\angle ADC') + ' ហើយ ' + m(r'\angle ADB+\angle ADC=180^\circ') + ' ដូចនេះ ' + hl(m(r'\angle ADB=90^\circ')) + ' ពោលគឺ ' + hl(m(r'AD\perp BC')) + ' ។')],
    hl('លំហាត់ ៖') + ' ' + m('ABC') + ' ជាត្រីកោណសមបាតកំពូល ' + m('A') + ' ហើយ ' + m('D') + ' ជាចំណុចកណ្តាលនៃ ' + m('BC') + ' ។ ក. ប្រៀបធៀប ' + m(r'\Delta ABD') + ' និង ' + m(r'\Delta ACD') + ' ។ ខ. បង្ហាញថា ' + m(r'AD\perp BC') + ' ។'), 'ពង្រឹងពុទ្ធិ')
H3 = homework(
    hl('លំហាត់ ១ ៖') + ' ក្នុងចតុកោណ ' + m('ABCD') + ' មាន ' + m('AB=CD') + ' និង ' + m('AD=BC') + ' ។ គូសអង្កត់ទ្រូង ' + m('BD') + ' ។ បង្ហាញថា ' + m(r'\Delta ABD\cong\Delta CDB') + ' និង ' + m(r'\angle A=\angle C') + ' ។' + fig(G.quad_sss()),
    hl('លំហាត់ ២ ៖') + ' ' + m(r'\Delta ABC') + ' និង ' + m(r'\Delta DEF') + ' ជាត្រីកោណកែងត្រង់ ' + m('A') + ' និង ' + m('D') + ' ដែល ' + m('BC=EF') + ' និង ' + m('AB=DE') + ' ។ បង្ហាញថា ' + m(r'\Delta ABC\cong\Delta DEF') + ' និង ' + m(r'\angle C=\angle F') + ' ។' + fig(G.rt_pair()),
    'មេរៀនបន្ទាប់ ត្រីកោណសមបាត និងមេដ្យាទ័រនៃអង្កត់ — សូមត្រៀមបន្ទាត់ និងដែកឈាន')

_RT = [x for x in sl_sss if not (x.get('html', '').startswith('<p class="ts-kicker">សង្ខេប'))]
S = ([profile, textbook('១៤១-១៤៤'), recall1, D1, O1, P1] + sl11 + [overview('asa')] + sl_asa + [X1, SUM1, H1, THANKS]
     + [profile, textbook('១៤៤-១៤៥')] + SOL1 + [R2, D2, O2, plan([_P0] + P2_CARDS[1:]), overview('sas'), HAND2, TAB2, DEF2, EX2, PR2] + sl_sas + [X2, SUM2, H2, THANKS]
     + [profile, textbook('១៤៦-១៥០')] + SOL2 + [R3, D3, O3, P3, overview('sss')] + sl_sss + [X3, SUM3, H3, THANKS]
     + tail)

# ---------------------------------------------------------------- write: the look of the class slides
for s in S:
    s.setdefault('k', '')
    s['html'] = re.sub(r'(\\\((?:(?!\\\)).)*\\\)) ។', lambda mo: '<span style="white-space:nowrap">' + mo.group(1) + ' ។</span>', s['html'])

_TAG = {'១.១': '១.១. និយមន័យនៃត្រីកោណប៉ុនគ្នា', '១.២': '១.២ លក្ខខណ្ឌនៃត្រីកោណប៉ុនគ្នា', '១.២.១': '១.២.១ ជ្រុងមួយប៉ុនគ្នាជាប់និងមុំពីរប៉ុនរៀងគ្នា (ម.ជ.ម)',
        '១.២.២': '១.២.២ មុំមួយប៉ុនគ្នាអមដោយជ្រុងពីរប៉ុនរៀងគ្នា (ជ.ម.ជ)', '១.២.៣': '១.២.៣ ជ្រុងទាំងបីប៉ុនរៀងគ្នា (ជ.ជ.ជ)',
        '១.៣': '១.៣ លក្ខខណ្ឌចំពោះត្រីកោណកែងប៉ុនគ្នា', '១.៣.១': '១.៣.១ អ៊ីប៉ូតេនុសប៉ុនគ្នានិងមុំស្រួចមួយប៉ុនគ្នា (អ.ម)',
        '១.៣.២': '១.៣.២ អ៊ីប៉ូតេនុសប៉ុនគ្នានិងជ្រុងមុំកែងមួយប៉ុនគ្នា (អ.ជ)', '២.១': '២.១ លក្ខណៈមេដ្យាទ័រនៃអង្កត់', '២.២': '២.២ លក្ខណៈត្រីកោណសមបាត',
        '៣.១': '៣.១ វិសមភាពចំពោះជ្រុងនិងមុំឈមនៃត្រីកោណមួយ', '៣.២': '៣.២ វិសមភាពត្រីកោណ', '៤.១': '៤.១ ប្រៀបធៀបអង្កត់កែងនិងអង្កត់ទ្រេត',
        '៤.២': '៤.២ ការប្រៀបធៀបអង្កត់ទ្រេតនិងអង្កត់កែង', '៤.៣': '៤.៣ ការប្រៀបធៀបអង្កត់ទ្រេតនិងអង្កត់ទ្រេត'}
_LABELS = {'ដំណោះស្រាយ', 'ឧទាហរណ៍', 'លំហាត់គំរូ', 'ប្រតិបត្តិ', 'វិបាក', 'និយមន័យ', 'សង្ខេប', 'លំហាត់'}


def _esc_slide(x, band):
    """kicker -> the title band; a section tag -> «❑ ១.២.១ …» line; a label (ឧទាហរណ៍ ...) -> red bold-italic label in front of the heading"""
    mt = re.match(r'^<p class="ts-kicker">([^<]*)</p>(?:<h2>(.*?)</h2>)?', x['html'], re.S)
    if not mt:
        return x
    kick, h2 = mt.group(1), mt.group(2) or ''
    rest = x['html'][mt.end():]
    title = x.get('band') or ('សង្ខេបមេរៀន' if kick == 'សង្ខេបមេរៀន' else band)
    sec, head = '', ''
    if kick in _LABELS:
        head = f'<h2><span class="h-lab">{kick} ៖</span> <span class="h-txt">{h2}</span></h2>' if h2 else ''
    else:
        sec = f'<p class="esc-sec">❑ {_TAG.get(kick, kick)}</p>' if kick in _TAG else ''
        if ' ៖ ' in h2:
            a_, r_ = h2.split(' ៖ ', 1)
            head = f'<h2><span class="h-lab">{a_} ៖</span> <span class="h-txt">{r_}</span></h2>'
        elif h2 and not (sec and h2 in sec):
            head = f'<h2>{"" if sec else "❑ "}{h2}</h2>'
    chip = ''
    if kick == 'ប្រតិបត្តិ':
        chip = '<span class="esc-chip">គិត ៥ នាទី</span>'
    return {**x, 'html': f'<p class="ts-kicker">{title}</p>{sec}{head}{rest}{chip}'}


band = ''
out = []
for x in S:
    if x.get('part'):
        band = x['band']
    if x.get('raw') or x.get('part'):
        out.append(x)
        continue
    if x.get('c') == 'esc-end':
        out.append(x); continue
    out.append(_esc_slide(x, band))
S = out
# the end slide
S[-1] = {'k': 'title', 'c': 'esc-end', 'html': '<h1>ចប់មេរៀន</h1><div class="esc-div-sub">សូមអរគុណ</div>'}
_RS = re.compile(r'<p>(\\\((?:(?!\\\)).)*\\\))\s<b style="color:#595959">(.*?)</b></p>', re.S)
for x in S:      # the book writes «equality  (reason)» with the reasons in a column
    x['html'] = _RS.sub(lambda mo: f'<p class="rs"><span class="rs-e">{mo.group(1)}</span><span class="rs-r">{mo.group(2)}</span></p>', x['html'])
for x in S:      # the class slides write «ដំណោះស្រាយ៖» (no space before the colon); a sub-question line (ក. ខ.) is bold; a conclusion sits in a grey box
    h = x['html'].replace(' ៖', '៖').replace('\u00a0៖', '៖')
    h = h.replace('(វិបាក) ។', '(វិបាក)\u00a0។')
    h = re.sub(r'<p>((?:ក|ខ|គ|ឃ)\. (?:(?!</p>).)*?) (ដូចនេះ (?:(?!</p>).)*?)</p>', r'<p>\1</p><p>\2</p>', h, flags=re.S)   # «ខ. … ដូចនេះ ED = EC» -> the result gets its own box
    h = re.sub(r'<p>((?:ក|ខ|គ|ឃ)\. )', r'<p class="sq">\1', h)
    h = re.sub(r'<p>(ដូចនេះ )((?:(?!</p>).)*?)</p>', lambda mo: ('<p class="concl">' if '\\cong' in mo.group(2) else '<p class="concl fin">') + mo.group(1) + mo.group(2) + '</p>', h, flags=re.S)
    x['html'] = h
_NB = re.compile(r'(និង) (\\\((?:(?!\\\)).)*\\\))')
for x in S:      # «និង AB = A'B' = 6 cm» stays on one line: the word and the maths after it are kept together
    x['html'] = _NB.sub(lambda mo: '<span style="white-space:nowrap">' + mo.group(1) + ' ' + mo.group(2) + '</span>', x['html'])
for x in S:      # «តាមលក្ខខណ្ឌខាងក្រោម៖» is never split between two lines
    x['html'] = x['html'].replace('តាមលក្ខខណ្ឌខាងក្រោម៖', '<span style="white-space:nowrap">តាមលក្ខខណ្ឌខាងក្រោម៖</span>')
for x in S:      # the word លំហាត់ (and its full stop) must never be split between two lines
    x['html'] = re.sub(r'លំហាត់។?', lambda mo: '<span style="white-space:nowrap">' + mo.group(0) + '</span>', x['html'])
out = [stepify(x) if x.get('k') in ('sol', 'ex', 'key', 'prac') and 'data-step' not in x['html'] and not x.get('nostep') else x for x in S]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
js = ('// Deck for Grade 8 Lesson 12 (follows the MoEYS textbook), in the look of the class slides ESC_មេរៀនទី១២-02: tools/lesson8_12/build.py — do not edit by hand.\n'
      + 'window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n'
      + "window.TEACH_SLIDES['8-12'] = " + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(out), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
