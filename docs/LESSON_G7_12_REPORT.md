# Grade 7 Lesson 12 «សញ្ញាណដំបូងនៃរូបធរណីមាត្រ» (2026-10-21)

## What was built (tools/lesson12: build.py, vis12a.py, vis12b.py, base_deck.json)
- The book text is kept (frozen from lesson12.tex). 80 -> 121 authored slides (124 on screen with the school slide and auto-splits).
- 46 slides now carry a picture; the .tex had 46 «% Diagram:» notes and the deck had none.
- Real objects are drawn as shaded vector illustrations: box, tin can, pyramid, pencil on paper, star sky, ruler + pencil, two pins with two threads,
  a table / whiteboard / water, a compass, a ruler, a ball pierced by a rod, a wire spool + a 35 mm needle (to scale), a snail in a well,
  a cyclist and a motorcyclist on a road, relay runners.
- Geometry figures are generated from coordinates, with asserts in the code: the 4 lines / 6 flower points / 3 per line, the 5 tips + 5 inner points of the
  pentagram on 5 lines of 4, collinear points, equal segments really equal, every ruler tick, the runners drawn to scale (576 : 648 : 835),
  8 cm on the ruler, 6.15 + 18.45 = 24.6, 52 500 / 35 = 1 500, 42 000 / 35 = 1 200, XS = 14 = (8 + 20) / 2, MN = 29.
- Numbers and letters in the pictures are italic Times maths (like Lesson 3). Constructions show the tool (compass legs, needle, pencil foot, arcs).
- «3. លំហាត់» is a numbered part (the part board opens it); Lesson 12 gets the school / teacher intro slide.
- Audit (every slide stepped): no overflow, no text under 17 px, no picture smaller than 170 px high.

## Checked against your textbook (pages 118-126 of the PDF, rendered and measured)
- The flower figure, the rays, the crossing lines, the rod through the ball (dashed inside), the runners' flags at A and D, the road scene: same structure.
- The segment-comparison figures: I measured the dot positions in the book at 300 dpi. Sample figure: AB = 210, CD = 203 (equal, as the book says).
  Practice figure: AB : BC : CD = 101 : 203 : 214, so CD is slightly longer than BC, as the answer says. My figures use these proportions.
- The book's pictures themselves are NOT reproduced or published (MoEYS copyright); they were used only to check mine.

## Could not do / not verified
- **Real photographs.** Magnific is on the Free plan with 0 credits, so no AI or stock photos could be made. I drew the objects as vector illustrations
  instead (your choice when asked). They are not photographs.
- The «photo beside the geometry drawing» pairing exists only for some pictures (pencil → point, pins and string → line, ruler → segment, solids);
  it is not done for every object.
- Only about 20 of the 124 slides were looked at on screen; the sheet of all 42 figures was looked at as a contact sheet. The rest were measured, not viewed.
- Not checked on a projector or phone; desktop browser only. Reveal steps were exercised by stepping through, not by a person teaching.
- The book's exercise 11 says 6 rows of 4 cannot be made with 10 trees and needs at least 11. I did not prove that (it matches the known orchard-planting
  results, but I did not check it independently). The slide follows the book.
- Khmer wording I wrote: «រូបធរណីមាត្រក្នុងជីវិតប្រចាំថ្ងៃ», «ស្នាមចុចនៃខ្មៅដៃ», «ប្រើដែកឈានផ្ទេរប្រវែង», «ផ្ទៃរាបស្មើនៅជុំវិញខ្លួន» and the slide titles with «រូប ៖». Check against MoEYS terms.
