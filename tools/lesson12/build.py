"""Build the Grade 7 Lesson 12 deck -> public/js/slides/g7/lesson12.js
   python3 tools/lesson12/build.py
The book text comes from base_deck.json (generated from Lesson/G7/lesson12.tex, then frozen here). This script adds the 46 figures the .tex
only describes («% Diagram:» notes) as exact vector drawings (vis12a.py, vis12b.py: every length is computed and asserted) and as shaded illustrations of the real
objects, and lays the long solutions out again with the same splitter as Lessons 2 and 3."""
import json, os, re, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'lesson2'))
from vis12a import *
from vis12b import *
from lib import stepify, slide, key, ex, prac, sol, m, dm, p, hl, fig, rvd
from tidy_sol import rebuild
from animate import animate_deck

OUT = os.path.join(HERE, '..', '..', 'public', 'js', 'slides', 'g7', 'lesson12.js')
base = json.load(open(os.path.join(HERE, 'base_deck.json'), encoding='utf-8'))


def K(i):
    mt = re.search(r'<p class="ts-kicker">(.*?)</p>', base[i - 1]['html'])
    return mt.group(1) if mt else ''


after, replace, append = {}, {}, {}
A = 'ចម្លើយ'


def vh(svg_html, v):
    """the picture's largest height as a share of the screen: a picture that shares its slide with text must be smaller, or the slide would be split in two"""
    return re.sub(r'max-height:\d+vh', f'max-height:{v}vh', svg_html)

# ================================================================ 1. shapes, points, lines, rays, planes
after[3] = [ex(K(3), 'រូបធរណីមាត្រក្នុងជីវិតប្រចាំថ្ងៃ', fig(solids()))]
after[4] = [ex(K(4), 'ស្នាមចុចនៃខ្មៅដៃ', fig(pencil_dot())), ex(K(4), 'ផ្កាយនៅលើមេឃ', fig(night_sky_dot())), ex(K(4), 'ការតាងចំណុច', fig(point_notations()))]
flower_svg, _names, _pts = flower_lines()
replace[7] = [sol(K(7), 'ដំណោះស្រាយ', p('គូសបន្ទាត់ 4 ឱ្យកាត់គ្នាជាបីជ្រុងនិងបន្ទាត់ពីរបន្ថែម ដូចរូប ហើយដាំដើមផ្កានៅត្រង់ចំណុចប្រសព្វទាំង 6 ។ ចំណុចនីមួយៗស្ថិតនៅលើបន្ទាត់ពីរ ដូច្នេះបន្ទាត់ 4 ជួរៗនីមួយៗមានចំណុច 3 ។') + fig(vh(flower_svg, 40)))]
after[10] = [ex(K(10), 'គូសបន្ទាត់ដោយបន្ទាត់ក្រិត', fig(ruler_pencil_line())), ex(K(10), 'ខ្សែអំបោះសន្ធឹង', fig(string_tight()))]
append[12] = fig(vh(line_with_points(['A', 'B', 'C', 'E'], above={'H': 2}), 30))
append[14] = fig(vh(line_with_points(['A', 'B', 'F', 'C'], above={'D': 1}, below={'E': 2}), 24))
append[16] = fig(vh(ray_pair(), 30))
append[18] = fig(vh(rays_two_points(), 30))
replace[21] = [sol(A, 'ដំណោះស្រាយ', p('ចំណុច ' + m('O') + ' ជាគល់នៃកន្លះបន្ទាត់ទាំងបួន ។ កន្លះបន្ទាត់ទាំងនោះគឺ ' + m('OA,\\ OB,\\ OE,\\ OF') + ' ។') + fig(crossing_lines()))]
append[22] = fig(vh(line_with_points(['A', 'B', 'C', 'D']), 22))
after[23] = [sol(A, 'ចំនួនកន្លះបន្ទាត់ទាំងអស់', fig(eight_rays()))]
after[24] = [ex(K(24), 'ផ្ទៃរាបស្មើនៅជុំវិញខ្លួន', fig(surfaces_room())), ex(K(24), 'ប្លង់ P ដែលមានបន្ទាត់ d', fig(plane_with_line())), ex(K(24), 'កន្លះប្លង់', fig(plane_half_planes()))]
after[29] = [ex(K(29), 'រូប ៖ ប្លង់ P និងចំណុច S', fig(plane_SABC()))]

# ================================================================ 2. segments
after[32] = [ex(K(32), 'អង្កត់ MN', fig(segment_MN())), ex(K(32), 'វាស់អង្កត់ដោយបន្ទាត់ក្រិត', fig(ruler_measure()))]
after[34] = [ex(K(34), 'ប្រើដែកឈានផ្ទេរប្រវែង', fig(compass_transfer()))]
after[35] = [ex(K(35), 'ភ្ជាប់ចំណុចពីរៗ', fig(polygons_segments()))]
after[37] = [ex(K(37), 'ប្រៀបធៀបអង្កត់ពីរ ៖ ស្មើគ្នា', fig(superpose(True))), ex(K(37), 'ប្រៀបធៀបអង្កត់ពីរ ៖ មិនស្មើគ្នា', fig(superpose(False)))]
after[39] = [sol(A, 'ចម្លើយតាមរូប', fig(compare_ab_cd()))]
after[41] = [sol(A, 'ចម្លើយតាមរូប', fig(compare_practice()))]
after[42] = [ex(K(42), 'ផលបូកអង្កត់', fig(sum_segments())), ex(K(42), 'ផលដកអង្កត់', fig(diff_segments()))]
after[44] = [ex(K(44), 'រូប ៖ កីឡាករបីនាក់រត់បណ្តាក់គ្នា', fig(runners_track()))]
after[47] = [sol(A, 'ចម្លើយតាមរូប', fig(mid_example()))]
after[48] = [ex(K(48), 'ផលគុណ និងផលចែកអង្កត់', fig(multiples()))]
after[50] = [sol(A, 'ចម្លើយតាមរូប', fig(quarters()))]
after[51] = [ex(K(51), 'រូប ៖ អ្នកជិះកង់ និងអ្នកជិះម៉ូតូជួបគ្នា', fig(road_meeting()))]
after[54] = [sol(A, 'ចម្លើយតាមរូប', fig(xyz_example()))]
after[55] = [ex(K(55), 'រូប ៖ កន្លែងជួបគ្នា', fig(road_two_thirds()))]

# ================================================================ exercises: the third part of the lesson board
replace[57] = [{'k': 'title', 'html': '<h1>3. លំហាត់</h1><p class="ts-sub">១១ លំហាត់</p>'}]
after[59] = [sol(A, 'លំហាត់ទី ១ ៖ តាមរូប', fig(ex1_three_lines()))]
after[61] = [sol(A, 'លំហាត់ទី ២ ៖ តាមរូប', fig(ex2_equal_segments()))]
after[62] = [ex(A and 'លំហាត់', 'រូប ៖ ដែកចាក់ទម្លុះបាល់', fig(ex3_sphere_rod()))]
after[65] = [sol(A, 'លំហាត់ទី ៤ ៖ តាមរូប', fig(ex4_sum_difference()))]
after[67] = [sol(A, 'លំហាត់ទី ៥ ៖ តាមរូប', fig(ex5_midpoints()))]
after[69] = [sol(A, 'លំហាត់ទី ៦ ៖ តាមរូប', fig(ex6_ab_2bc()))]
after[71] = [sol(A, 'លំហាត់ទី ៧ ៖ តាមរូប', fig(ex7_four_points()))]
after[73] = [sol(A, 'លំហាត់ទី ៨ ៖ តាមរូប', fig(ex8_difference_twice()))]
after[75] = [sol(A, 'លំហាត់ទី ៩ ៖ តាមរូប', fig(ex9_spool_needle()))]
after[77] = [sol(A, 'លំហាត់ទី ១០ ៖ តាមរូប', fig(ex10_snail_well()))]
after[79] = [sol(A, 'លំហាត់ទី ១១ ៖ តាមរូប', fig(pentagram()))]

# exercise 10: the book's table is too small to read from the back of the room
replace[77] = [dict(base[76], html=base[76]['html'].replace('<table class="ts-table">', '<table class="ts-table" style="font-size:26px;margin:10px 0">'))]

# ================================================================ assemble
out = []
for n, s_ in enumerate(base, 1):
    if n in replace:
        out.extend(replace[n])
    elif n in append:
        out.append(dict(s_, html=s_['html'] + append[n]))
    else:
        out.append(s_)
    out.extend(after.get(n, []))
out = rebuild(out)                                                    # long solutions: one group of sub-questions per slide
out = [stepify(x) if x.get('k') == 'sol' and 'data-step' not in x['html'] else x for x in out]
out = animate_deck(out)                                               # lines draw themselves, points pop in, arrowheads arrive last
js = ('// Hand-designed deck for Grade 7 Lesson 12: tools/lesson12/*.py — do not edit by hand.\n'
      + "window.TEACH_SLIDES = window.TEACH_SLIDES || {};\n"
      + "window.TEACH_SLIDES['7-12'] = " + json.dumps(out, ensure_ascii=False) + ';\n')
open(OUT, 'w', encoding='utf8').write(js)
print(len(base), '->', len(out), 'slides ->', os.path.abspath(OUT), len(js) // 1024, 'KB')
