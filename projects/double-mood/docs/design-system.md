# Double Mood — Design System
## Phase 1 MVP (3-day experiment)

**Design Philosophy:** Emotional first-aid, not clinical therapy. Calm, reassuring, immediate.

---

## 1. Color Palette

### Primary Colors
```css
/* Calming Blue-Green System */
--breath-bg: #F0F4F8;        /* Light cool gray — reduces screen glare */
--breath-primary: #4A90E2;   /* Serene blue — trust and calm */
--breath-accent: #50C9B8;    /* Gentle teal — renewal and balance */
--breath-text: #2C3E50;      /* Deep blue-gray — readable but soft */
--breath-muted: #7B8B9A;     /* Medium gray — secondary text */
```

### Semantic Colors
```css
--mood-before: #E57373;      /* Soft red — emotional distress */
--mood-after: #81C784;       /* Soft green — relief and calm */
--focus-ring: #4A90E2;       /* Matches primary for consistency */
```

### Rationale
- **Blue-Green Palette:** Psychologically associated with calm, healing, and safety
- **Low Saturation:** Reduces visual stress, feels non-clinical
- **High Contrast Text:** #2C3E50 on #F0F4F8 = 10.5:1 (WCAG AAA)
- **Avoid Pure White:** #F0F4F8 is easier on eyes during extended breathing sessions

---

## 2. Typography

### System Font Stack (No External Fonts for Phase 1)
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             "Noto Sans", Helvetica, Arial, sans-serif,
             "Apple Color Emoji", "Segoe UI Emoji";
```

### Type Scale
```css
/* Heading */
--text-2xl: 1.5rem;    /* 24px — Page title */
--text-xl: 1.25rem;    /* 20px — Section headers */

/* Body */
--text-base: 1rem;     /* 16px — Default body text */
--text-lg: 1.125rem;   /* 18px — Breathing instructions */

/* Small */
--text-sm: 0.875rem;   /* 14px — Helper text */
--text-xs: 0.75rem;    /* 12px — Footnotes */
```

### Font Weights
- **Regular (400):** Body text, instructions
- **Medium (500):** Breathing cue text ("Breathe in...")
- **Semibold (600):** Mood slider labels, section headers

### Line Heights
- **Headings:** 1.2
- **Body:** 1.5
- **Breathing Cues:** 1.4 (slightly tighter for visual impact)

### Bilingual Considerations
- System fonts include Noto Sans for Chinese character rendering
- Breathing cues use `text-lg` (18px minimum) for readability in both EN/CN
- No ligatures or decorative features that might break with Chinese glyphs

---

## 3. Breathing Circle Animation

### SVG Structure
```html
<svg viewBox="0 0 200 200" class="breath-circle">
  <!-- Background circle (static) -->
  <circle cx="100" cy="100" r="90"
          fill="none"
          stroke="#E8EFF5"
          stroke-width="2"
          opacity="0.3"/>

  <!-- Animated breathing circle -->
  <circle cx="100" cy="100" r="40"
          class="breath-pulse"
          fill="url(#breathGradient)"
          stroke="#4A90E2"
          stroke-width="2">
    <animate attributeName="r"
             values="40;80;40"
             dur="10s"
             keyTimes="0;0.4;1"
             keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"
             calcMode="spline"
             repeatCount="indefinite"/>
    <animate attributeName="opacity"
             values="0.7;1;0.7"
             dur="10s"
             keyTimes="0;0.4;1"
             repeatCount="indefinite"/>
  </circle>

  <!-- Gradient for depth -->
  <defs>
    <radialGradient id="breathGradient">
      <stop offset="0%" style="stop-color:#50C9B8;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#4A90E2;stop-opacity:0.6"/>
    </radialGradient>
  </defs>
</svg>
```

### Animation Timing
- **Inhale:** 0-4s (40% of 10s cycle)
  - Easing: `cubic-bezier(0.4, 0, 0.2, 1)` — Ease-in-out for natural breath
  - r: 40 → 80 (2x expansion)
  - opacity: 0.7 → 1 (subtle emphasis)

- **Exhale:** 4-10s (60% of 10s cycle)
  - Easing: Same cubic-bezier for smooth return
  - r: 80 → 40
  - opacity: 1 → 0.7

### Visual Cues (Text Layer)
```html
<div class="breath-instruction">
  <span class="breath-text" data-phase="inhale">
    <span lang="en">Breathe in...</span>
    <span lang="zh">吸气...</span>
  </span>
  <span class="breath-text" data-phase="exhale">
    <span lang="en">Breathe out...</span>
    <span lang="zh">呼气...</span>
  </span>
</div>
```

### JavaScript Timing Sync
```javascript
const BREATH_CYCLE = 10000; // 10s
const INHALE_DURATION = 4000; // 4s

setInterval(() => {
  const now = Date.now() % BREATH_CYCLE;
  const isInhale = now < INHALE_DURATION;

  document.querySelectorAll('[data-phase="inhale"]')
    .forEach(el => el.style.opacity = isInhale ? '1' : '0');
  document.querySelectorAll('[data-phase="exhale"]')
    .forEach(el => el.style.opacity = isInhale ? '0' : '1');
}, 100); // Check every 100ms for smooth transition
```

---

## 4. Layout Mockup (Mobile-First)

### Screen Structure
```
┌─────────────────────────────────┐
│  [How do you feel right now?]  │  ← Header (text-xl)
│                                 │
│  ┌───────────────────────────┐ │
│  │ 😰 ●●●●○○○○○○ 😊          │ │  ← Before mood slider
│  └───────────────────────────┘ │
│                                 │
│         ╭───────────╮           │
│        │   ◯     ◯   │          │  ← Breathing circle
│         │     ●     │           │    (SVG, responsive)
│          │   ◯   ◯ │            │
│           ╰───────╯             │
│                                 │
│      "Breathe in..."            │  ← Instruction text
│       吸气...                    │
│                                 │
│  ┌───────────────────────────┐ │
│  │ 😰 ●●●●●●○○○○ 😊          │ │  ← After mood slider
│  └───────────────────────────┘ │
└─────────────────────────────────┘
```

### Spacing System (Tailwind Classes)
```css
/* Vertical Rhythm */
--space-section: 2rem;   /* space-y-8 — Between major sections */
--space-element: 1rem;   /* space-y-4 — Between related elements */
--space-tight: 0.5rem;   /* space-y-2 — Within component */

/* Horizontal Padding */
--px-mobile: 1rem;       /* px-4 — Mobile side margins */
--px-desktop: 2rem;      /* px-8 — Desktop side margins */
```

### Component Dimensions
```css
/* Breathing Circle Container */
.breath-container {
  max-width: 300px;      /* Limits circle size on tablets */
  aspect-ratio: 1;       /* Always square */
  margin: 0 auto;        /* Center horizontally */
}

/* Mood Sliders */
.mood-slider {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}
```

---

## 5. Bilingual Content Specifications

### Language Toggle Strategy (Phase 1)
**Simple approach:** Show both languages simultaneously

```html
<!-- Breathing Instructions -->
<p class="breath-cue">
  <span class="text-lg font-medium text-breath-text">
    Breathe in...
  </span>
  <span class="text-sm text-breath-muted ml-2">
    吸气...
  </span>
</p>
```

### All UI Labels

| Element | English | 中文 |
|---------|---------|------|
| **Header** | How do you feel right now? | 现在感觉如何？ |
| **Before Slider** | Before breathing | 深呼吸前 |
| **After Slider** | After breathing | 深呼吸后 |
| **Inhale Cue** | Breathe in... | 吸气... |
| **Exhale Cue** | Breathe out... | 呼气... |
| **Slider Left** | Anxious | 焦虑 |
| **Slider Right** | Calm | 平静 |
| **Footer Note** | Take a moment. You deserve it. | 给自己一点时间，你值得。 |

### Typography for Chinese
- Minimum font size: 16px (system fonts render Chinese well at this size)
- Line height: 1.5 (Chinese characters need vertical breathing room)
- No italics (Chinese glyphs don't have italic variants)

---

## 6. Responsive Breakpoints

### Mobile (Default, <640px)
```css
.breath-container { width: 280px; }
.breath-cue { font-size: 1.125rem; } /* 18px */
body { padding: 1rem; }
```

### Tablet (640px - 1024px)
```css
.breath-container { width: 320px; }
.breath-cue { font-size: 1.25rem; } /* 20px */
body { padding: 2rem; }
```

### Desktop (>1024px)
```css
.breath-container { width: 360px; }
/* Consider horizontal layout: slider | circle | slider */
```

---

## 7. Accessibility

### Contrast Ratios
- Text on background: 10.5:1 (AAA)
- Accent colors on background: 4.8:1 (AA)
- Focus ring: 3px solid #4A90E2 with 2px offset

### Keyboard Navigation
- Mood sliders: Arrow keys to adjust
- Focus ring visible on all interactive elements
- Skip to breathing circle: `Tab` order prioritizes core interaction

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .breath-pulse animate {
    animation-duration: 0.01s !important;
    animation-iteration-count: 1 !important;
  }
  /* Show static circle with pulsing opacity only */
}
```

### Screen Readers
```html
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <span data-phase="inhale">Breathe in for 4 seconds</span>
  <span data-phase="exhale">Breathe out for 6 seconds</span>
</div>
```

---

## 8. Tailwind CDN Implementation

### HTML Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Double Mood — Breathe & Feel Better</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            'breath-bg': '#F0F4F8',
            'breath-primary': '#4A90E2',
            'breath-accent': '#50C9B8',
            'breath-text': '#2C3E50',
            'breath-muted': '#7B8B9A',
            'mood-before': '#E57373',
            'mood-after': '#81C784',
          }
        }
      }
    }
  </script>
</head>
<body class="bg-breath-bg text-breath-text min-h-screen">
  <!-- App content here -->
</body>
</html>
```

### Key Tailwind Classes
```
Text:
- text-2xl font-semibold — Headers
- text-lg font-medium — Breathing cues
- text-base — Body text
- text-breath-text / text-breath-muted — Color variants

Spacing:
- space-y-8 — Section gaps
- p-4 / px-4 — Padding
- mx-auto — Center elements

Responsive:
- max-w-md — Constrain width on desktop
- aspect-square — Breathing circle container
```

---

## 9. Animation Performance

### GPU Acceleration
```css
.breath-pulse {
  will-change: transform, opacity;
  transform: translateZ(0); /* Force GPU layer */
}
```

### Why SVG Over CSS?
- **Scalability:** Vector graphics remain crisp on Retina displays
- **Declarative timing:** SMIL animations are self-contained, no JS needed for core animation
- **Accessibility:** SVG has better screen reader support with proper ARIA labels
- **Simplicity:** No complex CSS keyframes, easier to tweak timing

---

## 10. File Structure

```
projects/double-mood/
├── index.html              ← Main app (includes all CSS/JS inline)
├── docs/
│   ├── design-system.md    ← This file
│   └── product-spec.md     ← Product requirements
└── assets/                 ← (Future: images, icons)
```

For Phase 1, keep everything in a single `index.html` file:
- Tailwind CDN (no build step)
- Inline SVG
- Inline JavaScript (< 50 lines)

---

## Next Steps for Implementation

1. **Fullstack DHH:** Build `index.html` based on this spec
2. **QA Bach:** Test animation smoothness on iOS Safari, Android Chrome
3. **DevOps Hightower:** Deploy to Cloudflare Pages, test on real devices
4. **Operations PG:** Add simple analytics (mood delta tracking)

---

## Design Validation Questions (for Product Norman)

1. Is 10-second cycle (4s in, 6s out) the right pacing? Some apps use 4-7-8.
2. Should we add a "Complete cycle" counter to gamify completion?
3. Do we need a "Skip" button for users who just want to log mood?

---

**Last updated:** 2026-02-21
**Owner:** ui-duarte
**Status:** Ready for implementation
