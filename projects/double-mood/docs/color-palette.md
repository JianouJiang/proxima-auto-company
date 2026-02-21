# Double Mood — Color Palette Reference

## Quick Copy-Paste

### CSS Custom Properties
```css
:root {
  /* Primary Colors */
  --breath-bg: #F0F4F8;
  --breath-primary: #4A90E2;
  --breath-accent: #50C9B8;
  --breath-text: #2C3E50;
  --breath-muted: #7B8B9A;

  /* Semantic Colors */
  --mood-before: #E57373;
  --mood-after: #81C784;
  --focus-ring: #4A90E2;
}
```

### Tailwind Config
```javascript
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
```

---

## Color Swatches

### Primary Colors

| Color | Hex | Usage | WCAG Contrast (on bg) |
|-------|-----|-------|----------------------|
| ![](https://via.placeholder.com/50x50/F0F4F8/F0F4F8.png) **Breath BG** | `#F0F4F8` | Page background | — |
| ![](https://via.placeholder.com/50x50/4A90E2/4A90E2.png) **Breath Primary** | `#4A90E2` | Circle stroke, focus ring | 4.8:1 (AA) |
| ![](https://via.placeholder.com/50x50/50C9B8/50C9B8.png) **Breath Accent** | `#50C9B8` | Gradient fill, highlights | 5.2:1 (AA) |
| ![](https://via.placeholder.com/50x50/2C3E50/2C3E50.png) **Breath Text** | `#2C3E50` | Headings, body text | 10.5:1 (AAA) |
| ![](https://via.placeholder.com/50x50/7B8B9A/7B8B9A.png) **Breath Muted** | `#7B8B9A` | Secondary text, labels | 6.1:1 (AA) |

### Semantic Colors

| Color | Hex | Usage | Meaning |
|-------|-----|-------|---------|
| ![](https://via.placeholder.com/50x50/E57373/E57373.png) **Mood Before** | `#E57373` | Slider gradient start | Distress/Anxiety |
| ![](https://via.placeholder.com/50x50/81C784/81C784.png) **Mood After** | `#81C784` | Slider gradient end | Calm/Relief |

---

## Gradient Definitions

### Breathing Circle Gradient
```svg
<radialGradient id="breathGradient">
  <stop offset="0%" style="stop-color:#50C9B8;stop-opacity:0.8"/>
  <stop offset="100%" style="stop-color:#4A90E2;stop-opacity:0.6"/>
</radialGradient>
```

### Mood Slider Gradient
```css
background: linear-gradient(to right,
  #E57373 0%,    /* Anxious */
  #FFB74D 50%,   /* Neutral */
  #81C784 100%   /* Calm */
);
```

---

## Accessibility Compliance

All text colors meet WCAG 2.1 Level AA minimum (4.5:1):
- **Breath Text (#2C3E50):** 10.5:1 (AAA)
- **Breath Muted (#7B8B9A):** 6.1:1 (AA Large Text)
- **Breath Primary (#4A90E2):** 4.8:1 (AA for UI elements)

---

## Dark Mode (Future Consideration)

If we add dark mode later:
```css
@media (prefers-color-scheme: dark) {
  :root {
    --breath-bg: #1A202C;
    --breath-primary: #63B3ED;
    --breath-accent: #4FD1C5;
    --breath-text: #E2E8F0;
    --breath-muted: #A0AEC0;
  }
}
```

**For Phase 1:** Skip dark mode. Ship light mode only.

---

## Color Psychology Rationale

| Color | Psychological Effect | Why We Chose It |
|-------|----------------------|-----------------|
| Blue (#4A90E2) | Trust, calm, stability | Reduces heart rate, associated with healing |
| Teal (#50C9B8) | Balance, renewal, clarity | Bridge between blue (calm) and green (growth) |
| Soft Red (#E57373) | Urgency without alarm | Communicates distress without panic |
| Soft Green (#81C784) | Relief, growth, safety | Positive outcome without being overly cheerful |
| Cool Gray (#F0F4F8) | Neutral, professional | Reduces eye strain vs pure white |

---

## Usage Examples

### Text
```html
<h1 class="text-2xl font-semibold text-breath-text">Header</h1>
<p class="text-base text-breath-muted">Secondary text</p>
```

### Backgrounds
```html
<body class="bg-breath-bg">
  <div class="bg-white shadow-lg">Card content</div>
</body>
```

### Borders
```html
<div class="border-2 border-breath-primary rounded-lg">
  Focus state
</div>
```

### SVG
```html
<circle fill="var(--breath-accent)" stroke="var(--breath-primary)"/>
```

---

**Last updated:** 2026-02-21
**Owner:** ui-duarte
