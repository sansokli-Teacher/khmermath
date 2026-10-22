# Pen smoothness (teaching mode), 2026-10-22
Cause of the roughness: every pen event repainted the whole stroke (the pressure pen re-stroked every segment of the stroke so far), read the canvas box (forced layout) and moved the on-screen pen cursor.
Changes (public/js/teachshow.js):
- The live stroke paints only the new segments (same curve and widths as the final repaint); the finished stroke is repainted once when the pen lifts.
- One paint per screen frame (requestAnimationFrame), however many events (coalesced) arrive.
- Input filter: slow movement is smoothed more, fast movement follows the pen; pressure is smoothed (no width wobble); the last point snaps to the real pen position on lift.
- The canvas box is cached while drawing; the pen cursor moves once per frame; the canvas is created with `desynchronized: true` (lower latency where supported).
Measured (simulated pen, 1500 pressure events, 1920 px window): handler cost per event 3.24 ms -> 0.14 ms; worst event 82 ms -> 13 ms.
NOT measured: a real Wacom/tablet (latency, tilt, hover), only synthetic pointer events. Highlighter, marker, brush, pencil and chalk still repaint the stroke each frame (batched), not incrementally.
