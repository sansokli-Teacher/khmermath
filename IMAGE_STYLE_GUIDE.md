# KhmerMath Question Bank: Image & Diagram Style Guide
*(សៀវភៅណែនាំស្តង់ដារូបភាព និងដ្យាក្រាមសម្រាប់ធនាគារសំណួរ និងវិញ្ញាសា KhmerMath)*

---

## 1. Core Philosophy & Design Aesthetic

All images and diagrams created for the **KhmerMath Question Bank** (`exam.khmermath.org`) must strictly adhere to this style standard:

> **Style Standard:**
> **"Clean vector illustration, isolated, no background, flat colors, educational textbook style."**

### Key Characteristics:
1. **Isolated & No Background (Transparent Background)**:
   - Zero background scenery, no gradients, no artificial cards, and no drop-shadow boxes.
   - For SVGs: No `<rect fill="#ffffff"/>` background tag. The vector elements float freely so they seamlessly adapt to any background, dark/light UI modes, or printed A4 papers.
   - For AI Image Prompts: Always specify *"isolated, no background, pure white void, no shadows, no ground line"*.
2. **2D Flat Colors & Crisp Outlines (Print-Friendly)**:
   - Thin, clean, uniform black contour lines with flat solid color fills.
   - High contrast for black-and-white photocopy / risograph printing (no muddy gradients).
3. **Educational Textbook Aesthetic**:
   - Clean, professional, and mathematically accurate (resembling Cambridge, Singapore Math, MOEYS, and OECD PISA publications).

---

## 2. Typography Rules (Mathcad Italic Standard)

| Element Type | Font Family & Weight | Style | Examples |
|:---|:---|:---|:---|
| **Variables & Unknowns** | `Mathcad UniMath Italic` / Serif Math | *Italic* | $d$, $x$, $y$, $h$, $r$, $t$, $v$, $c$ |
| **Geometric Points & Vertices** | `Mathcad UniMath Italic` / Serif Math | *Italic* | $A$, $B$, $C$, $M$, $N$, $P$ |
| **Angles & Greek Letters** | `Mathcad UniMath Italic` / Serif Math | *Italic* | $\theta$, $\alpha$, $\beta$, $\phi$ |
| **Numbers & Measurements** | `Times New Roman` / Serif Upright | **Upright (Bold optional)** | $1$, $2.5$, $12$, $90^\circ$ |
| **Units of Measure** | `Times New Roman` / Serif Upright | Regular Upright | $\text{m}$, $\text{cm}$, $\text{mm}$, $\text{km/h}$, $\text{s}$ |

---

## 3. The Master Prompt Formula

When generating graphics via AI image models (Imagen, Midjourney, DALL-E), use this exact prompt structure:

```text
Clean vector illustration of [SUBJECT & CONTEXT], isolated, no background, flat colors, educational textbook style. Crisp thin black outlines, flat 2D color fills, no shadows, no ground line, minimal clean line art. All mathematical variable labels ([VARIABLES]) in Mathcad italic serif math font. Measurement numbers and units ([DIMENSIONS]) in upright serif font with technical dimension arrows. No photorealism, no 3D reflections, no watermarks.
```

---

## 4. Reusable Prompt Library by Math Topic

### A. Pythagorean Theorem & Word Problems (ទ្រឹស្តីបទពីតាគ័រ)
* **Door Diagonal (សំណួរទ្វារបន្ទប់):**
  ```text
  Clean vector illustration of a wooden door with dimensions 1 meter wide and 2 meters tall, isolated, no background, flat colors, educational textbook style. Crisp thin black outlines, flat solid wood colors. Red dashed diagonal line connecting bottom-left to top-right corner, labeled "d" in Mathcad italic font. Dimension lines at the bottom show "1 m" and along the right show "2 m" in upright serif font. Small square right-angle mark at the bottom-left corner. No shadows, no ground, no watermarks.
  ```
* **Ladder on a Wall (ជណ្ដើរផ្អែកជញ្ជាំង):**
  ```text
  Clean vector illustration of an aluminum ladder leaning against a vertical wall, isolated, no background, flat colors, educational textbook style. Crisp thin outlines. Ground distance labeled "3 m", wall height labeled "4 m", ladder length labeled "L" in Mathcad italic font. Right angle indicator at the base. No ground scenery, no drop shadows.
  ```

### B. Motion, Speed, and Velocity (ចលនា និងល្បឿន)
* **Modern Sedan Car (រថយន្តទំនើប):**
  ```text
  Clean vector illustration of a modern blue sedan car, isolated, no background, flat colors, educational textbook style. Crisp thin black outlines, side profile view, minimal 2D line art, no shadows, no ground line, no reflections.
  ```
* **Two Moving Vehicles (រថយន្តធ្វើដំណើរបញ្ច្រាសទិសគ្នា):**
  ```text
  Clean vector illustration of a blue car moving east labeled "v1 = 60 km/h" and a red truck moving west labeled "v2 = 40 km/h" on a single horizontal axis, isolated, no background, flat colors, educational textbook style. Total distance labeled "D" in Mathcad italic font.
  ```

### C. Trigonometry & Angles of Elevation / Depression (ត្រីកោណមាត្រ)
* **Angle of Elevation to a Building (មុំងើបទៅកំពូលអគារ):**
  ```text
  Clean vector illustration of an observer looking up at the top of a modern school building, isolated, no background, flat colors, educational textbook style. Crisp thin outlines. Dashed right triangle connecting observer's eye, ground base, and building top. Building height labeled "h" in Mathcad italic font, ground distance labeled "15 m", angle of elevation labeled "theta" in Mathcad italic font. No background scenery.
  ```

### D. Solid Geometry & Containers (សូលីត និងមាឌ)
* **Cylindrical Water Tank (ធុងទឹកស៊ីឡាំង):**
  ```text
  Clean vector illustration of a vertical cylinder water tank, isolated, no background, flat colors, educational textbook style. Crisp black outlines, transparent light-blue fill. Radius dashed line on top circle labeled "r" in Mathcad italic font, height dimension arrow labeled "h" in Mathcad italic font. No shadows, no floor.
  ```

---

## 5. Technical Specifications for Native SVG

To ensure an SVG has **no background** and scales natively:

1. **Do not include `<rect width="100%" height="100%" fill="..."/>`** at the root of the SVG.
2. **Keep the `viewBox` tightly bound** to the illustration elements to avoid unwanted outer white margins.
3. **SVG Font Tags:**
   ```xml
   <!-- Math Variable in Mathcad Italic -->
   <text font-family="'Mathcad UniMath Italic', 'Mathcad UniMath', 'Times New Roman', serif" 
         font-style="italic" font-size="18" fill="#dc2626">d</text>

   <!-- Number and Unit in Upright Serif -->
   <text font-family="'Times New Roman', serif" 
         font-style="normal" font-weight="bold" font-size="14" fill="#111827">1 m</text>
   ```
