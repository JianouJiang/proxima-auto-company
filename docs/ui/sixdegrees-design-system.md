# SixDegrees Design System

**Author:** UI Design Director (Matías Duarte)
**Date:** 2026-02-22
**Product:** SixDegrees — AI Agent That Reaches Anyone Through Your Network
**Status:** Complete. Ready for implementation.
**Tech Stack:** Tailwind CSS v4 + shadcn/ui + HTML/Vanilla JS

---

## Design Philosophy

SixDegrees is **an AI agent service, not a tool**. The interface must convey trust, clarity, and inevitability: "The AI will reach this person, and here's exactly how."

Core principles (Matías Duarte style):

1. **Material Metaphor** — Elevation (shadow depth) shows information hierarchy. Each card/section feels like a physical surface. No flat design.
2. **Typography First** — The 6-degree chain is explained through text + visualization. No mystery.
3. **Motion Communicates State** — Email sent = subtle ripple. Status change = fade transition. No random animations.
4. **Purposeful Color** — Primary (blue) = trust/action. Green = success. Red/Orange = requires attention. Color has semantics.
5. **Adaptive for Bilingual** — EN and 中文 have equal visual weight. Typography scales for both languages.

**Design Principles:**
- Credibility over flash (this is B2B networking, not a game)
- Clarity over cleverness (user must understand the 6-degree chain in 5 seconds)
- Consistency over novelty (use components repeatedly, don't reinvent)
- Minimal friction (every click has clear feedback)

---

## 1. Design Foundations

### 1.1 Color Palette

**Semantic Color Architecture:**

```css
/* Base Tailwind configuration + CSS Variables */
/* src/index.css or <style> tag */

:root {
  /* Primary: Trust Blue (action, CTA, primary brand) */
  --primary: #2563eb;           /* Tailwind: blue-600 */
  --primary-light: #3b82f6;     /* blue-500 (hover) */
  --primary-dark: #1d4ed8;      /* blue-700 (active) */
  --primary-surface: #eff6ff;   /* blue-50 (backgrounds) */
  --primary-text: #ffffff;      /* White on blue */

  /* Secondary: Slate (muted, secondary text, disabled) */
  --secondary: #64748b;         /* slate-500 */
  --secondary-light: #94a3b8;   /* slate-400 */
  --secondary-surface: #f1f5f9; /* slate-100 */
  --secondary-text: #1e293b;    /* slate-900 */

  /* Success: Green (emails sent, replies received, campaign complete) */
  --success: #16a34a;           /* green-600 */
  --success-light: #22c55e;     /* green-500 (hover) */
  --success-surface: #f0fdf4;   /* green-50 */
  --success-text: #ffffff;

  /* Warning: Amber (attention needed, waiting, draft status) */
  --warning: #ca8a04;           /* amber-600 */
  --warning-light: #eab308;     /* amber-400 (hover) */
  --warning-surface: #fffbeb;   /* amber-50 */
  --warning-text: #ffffff;

  /* Error: Red (failed, expired, delete action) */
  --error: #dc2626;             /* red-600 */
  --error-light: #ef4444;       /* red-500 (hover) */
  --error-surface: #fef2f2;     /* red-50 */
  --error-text: #ffffff;

  /* Neutral: Grayscale (text, borders, backgrounds) */
  --neutral-dark: #1f2937;      /* gray-800 (text) */
  --neutral-base: #374151;      /* gray-700 (secondary text) */
  --neutral-light: #d1d5db;     /* gray-300 (borders) */
  --neutral-surface: #f9fafb;   /* gray-50 (card background) */
  --neutral-white: #ffffff;

  /* Elevation / Shadows (Material Design style) */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

  /* Radius: 8px base for modern Material feel */
  --radius: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
}

/* Dark mode support (optional for V1, easy to add later) */
.dark {
  --neutral-dark: #f9fafb;
  --neutral-base: #d1d5db;
  --neutral-light: #4b5563;
  --neutral-surface: #1f2937;
  --neutral-white: #0f172a;

  --primary-surface: #001f3f;
  --secondary-surface: #111827;
  --warning-surface: #332200;
  --success-surface: #002600;
  --error-surface: #330000;
}
```

**Color Usage by Component:**

| Component | Primary Use | Secondary Use | Example |
|-----------|------------|---------------|---------|
| Button (CTA) | `bg-primary` text-white | Hover: `bg-primary-light` | [Start Campaign] [Send Email] |
| Button (Secondary) | `bg-neutral-surface` border-neutral-light | Hover: `bg-secondary-surface` | [Edit] [View More] |
| Button (Destructive) | `bg-error` text-white | Hover: `bg-error-light` | [Delete] [Disconnect] |
| Status Badge | Success: green, Warning: amber, Error: red | `bg-{color}-surface` text-{color} | ✓ Sent, ⏳ Waiting, ✗ Failed |
| Card (elevated) | `bg-white shadow-md` border: none | Hover: `shadow-lg` | Campaign card, email preview |
| Card (flat) | `bg-secondary-surface` border-neutral-light | No shadow | Filter buttons, settings panel |
| Text (heading) | `text-neutral-dark` | `font-bold` | "Your Campaign", "6-Degree Chain" |
| Text (body) | `text-neutral-base` | `text-sm` | Email preview text, descriptions |
| Text (muted) | `text-secondary-light` | `text-xs` | Timestamp, status metadata |
| Link | `text-primary underline` | Hover: `text-primary-dark` | "View full email" |

---

### 1.2 Typography Scale

**Font Stack (supports both EN and 中文):**

```css
:root {
  /* Font Family */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
               "Helvetica Neue", sans-serif, "Noto Sans CJK SC", "Noto Sans";
  --font-mono: "Monaco", "Menlo", "Courier New", monospace;
}

body {
  font-family: var(--font-sans);
  line-height: 1.5;
  letter-spacing: -0.01em;
}
```

**Scale & Hierarchy:**

```css
/* Headings (Bold, establish hierarchy) */
.h1, h1 {
  font-size: 2rem;        /* 32px */
  font-weight: 700;       /* bold */
  line-height: 1.2;
  color: var(--neutral-dark);
  margin-bottom: 1.5rem;
  /* Example: "AI Agent That Reaches Anyone For You" */
}

.h2, h2 {
  font-size: 1.5rem;      /* 24px */
  font-weight: 700;
  line-height: 1.3;
  color: var(--neutral-dark);
  margin-bottom: 1rem;
  /* Example: "Your Campaign", "6-Degree Chain" */
}

.h3, h3 {
  font-size: 1.25rem;     /* 20px */
  font-weight: 600;       /* semibold */
  line-height: 1.4;
  color: var(--neutral-dark);
  margin-bottom: 0.75rem;
  /* Example: "Email #1 to Jake", "What's Happening Now" */
}

.h4, h4 {
  font-size: 1rem;        /* 16px */
  font-weight: 600;
  line-height: 1.5;
  color: var(--neutral-dark);
  margin-bottom: 0.5rem;
  /* Example: Tab names, card titles */
}

/* Body Text */
.body-lg {
  font-size: 1.125rem;    /* 18px */
  font-weight: 400;
  line-height: 1.6;
  color: var(--neutral-base);
  /* Example: Introduction text, descriptions */
}

.body-md {
  font-size: 1rem;        /* 16px */
  font-weight: 400;
  line-height: 1.5;
  color: var(--neutral-base);
  /* Example: Form labels, email preview text */
}

.body-sm {
  font-size: 0.875rem;    /* 14px */
  font-weight: 400;
  line-height: 1.5;
  color: var(--neutral-base);
  /* Example: Helper text, campaign status */
}

.body-xs {
  font-size: 0.75rem;     /* 12px */
  font-weight: 400;
  line-height: 1.4;
  color: var(--secondary-light);
  /* Example: Timestamp, metadata, captions */
}

/* Labels (Form fields, badges) */
.label {
  font-size: 0.875rem;    /* 14px */
  font-weight: 600;
  line-height: 1.5;
  color: var(--neutral-dark);
  text-transform: none;
  /* Example: "Who do you want to reach?" */
}

/* Status Text (Badges, inline status) */
.status {
  font-size: 0.75rem;     /* 12px */
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  /* Example: "SENT", "WAITING", "DELIVERED" */
}
```

**Bilingual Considerations:**

- Chinese characters need slightly larger line-height: `1.8` instead of `1.5`
- Font weights: 400 (regular), 600 (semibold), 700 (bold) work well for both EN and 中文
- Use `font-variant-numeric: tabular-nums` for alignment of numbers (dates, times)
- Avoid very small text (< 12px) for Chinese; readability drops faster

---

### 1.3 Spacing System (8px Grid)

Tailwind classes work here, but for clarity:

```css
:root {
  /* 8px base grid */
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */  ← Base unit
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
}
```

**Spacing Rules:**

| Context | Spacing | Example |
|---------|---------|---------|
| Padding inside card | `p-6` (24px) | Campaign card, email preview |
| Margin between sections | `mb-8` (32px) | Between tabs, between emails |
| Gap in flex row | `gap-4` (16px) | Button groups, email carousel |
| Padding in form field | `px-4 py-2` (16px/8px) | Input boxes, textareas |
| Margin between form fields | `mb-4` (16px) | Form field spacing |
| Tab bar padding | `px-6 py-4` (24px/16px) | Tab labels, navigation |

---

### 1.4 Border & Radius

```css
/* Borders */
.border-default {
  border: 1px solid var(--neutral-light);
}

.border-subtle {
  border: 1px solid #f3f4f6;  /* Very light, almost invisible */
}

/* Radius (8px is modern Material) */
.rounded {
  border-radius: var(--radius);         /* 8px */
}

.rounded-lg {
  border-radius: var(--radius-lg);      /* 12px */
}

.rounded-xl {
  border-radius: var(--radius-xl);      /* 16px */
}

/* Buttons should use rounded (8px), cards use rounded (8px) */
```

---

## 2. Component Library

### 2.1 Buttons

**Primary Button (Call-to-Action):**

```html
<button class="px-6 py-3 rounded bg-primary hover:bg-primary-light active:bg-primary-dark
                text-white font-semibold text-base transition-colors duration-200
                focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2
                disabled:opacity-50 disabled:cursor-not-allowed">
  Start Campaign
</button>

<!-- Tailwind Class Summary: -->
<!-- px-6 py-3 = 24px horizontal, 12px vertical padding -->
<!-- rounded = 8px border-radius -->
<!-- bg-primary = #2563eb -->
<!-- hover:bg-primary-light = #3b82f6 on hover -->
<!-- text-white font-semibold = white text, bold -->
<!-- transition-colors = smooth color change -->
<!-- focus:ring = keyboard accessibility (blue outline) -->
```

**Secondary Button (Less Prominent):**

```html
<button class="px-6 py-3 rounded bg-neutral-surface border border-neutral-light
                hover:bg-secondary-surface text-neutral-dark font-semibold text-base
                transition-colors duration-200 focus:outline-none focus:ring-2
                focus:ring-primary focus:ring-offset-2">
  Edit Target
</button>
```

**Destructive Button (Delete, Disconnect):**

```html
<button class="px-6 py-3 rounded bg-error hover:bg-error-light text-white
                font-semibold text-base transition-colors duration-200
                focus:outline-none focus:ring-2 focus:ring-error focus:ring-offset-2">
  Delete Account
</button>
```

**Button Sizes:**

```html
<!-- Large (primary CTA) -->
<button class="px-6 py-3 text-base">...</button>

<!-- Medium (standard) -->
<button class="px-4 py-2 text-sm">...</button>

<!-- Small (inline action) -->
<button class="px-3 py-1 text-xs">...</button>
```

---

### 2.2 Cards (Elevated Surfaces)

**Primary Card (Campaign, Email Preview):**

```html
<div class="rounded bg-white shadow-md border border-transparent hover:shadow-lg
            transition-shadow duration-200 p-6">
  <h3 class="text-xl font-semibold text-neutral-dark mb-4">
    AI Strategy to Reach Elon Musk
  </h3>
  <p class="text-base text-neutral-base mb-6">
    We found 3 connection paths to your target...
  </p>
</div>

<!-- Tailwind: rounded p-6 bg-white shadow-md -->
<!-- Hover effect: shadow-lg (depth increase) -->
```

**Flat Card (Settings, Filters):**

```html
<div class="rounded bg-secondary-surface border border-neutral-light p-4">
  <!-- No shadow; used for grouping related items -->
</div>

<!-- Tailwind: rounded p-4 bg-secondary-surface border border-neutral-light -->
```

---

### 2.3 Tabs (Navigation)

```html
<div class="flex border-b border-neutral-light mb-6">
  <button class="pb-4 px-4 border-b-2 border-primary text-primary font-semibold text-base">
    Your Campaign
  </button>
  <button class="pb-4 px-4 border-b-2 border-transparent text-secondary-light
                 hover:text-neutral-base transition-colors duration-200">
    Connections
  </button>
  <button class="pb-4 px-4 border-b-2 border-transparent text-secondary-light
                 hover:text-neutral-base transition-colors duration-200">
    Credits & Payment
  </button>
  <button class="pb-4 px-4 border-b-2 border-transparent text-secondary-light
                 hover:text-neutral-base transition-colors duration-200">
    Settings
  </button>
</div>

<!-- Active tab: border-b-2 border-primary (blue underline) -->
<!-- Inactive tab: border-b-2 border-transparent (no underline) -->
<!-- Font weight: semibold (600) for active, regular (400) for inactive -->
```

---

### 2.4 Status Badges

**Sent (Green):**

```html
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-success-surface text-success font-semibold text-xs">
  ✓ Sent
</span>
```

**Waiting (Amber):**

```html
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-warning-surface text-warning font-semibold text-xs">
  ⏳ Waiting
</span>
```

**Draft (Secondary):**

```html
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-secondary-surface text-secondary font-semibold text-xs">
  ✎ Draft
</span>
```

**Failed (Red):**

```html
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-error-surface text-error font-semibold text-xs">
  ✗ Failed
</span>
```

---

### 2.5 Form Fields

**Text Input / Textarea:**

```html
<input type="text"
       class="w-full px-4 py-2 rounded border border-neutral-light
              bg-white text-neutral-dark placeholder-secondary-light
              focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary
              transition-colors duration-200"
       placeholder="Elon Musk">

<!-- For textarea, use similar styling + min-h-[120px] -->
<textarea class="w-full px-4 py-3 rounded border border-neutral-light
                 bg-white text-neutral-dark placeholder-secondary-light
                 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary
                 transition-colors duration-200 resize-none
                 min-h-[120px]"
          placeholder="Why do you want to reach them?"></textarea>
```

**Form Label:**

```html
<label class="block text-sm font-semibold text-neutral-dark mb-2">
  Who do you want to reach?
</label>
<input type="text" class="..." />
```

**Form Field Group:**

```html
<div class="mb-6">
  <label class="block text-sm font-semibold text-neutral-dark mb-2">
    Target Name
  </label>
  <input type="text" class="..." />
  <p class="mt-1 text-xs text-secondary-light">
    First and last name
  </p>
</div>
```

---

### 2.6 Loading States

**Spinner (For API calls):**

```html
<div class="inline-block animate-spin">
  <svg class="w-5 h-5 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
</div>

<!-- Or use Tailwind's built-in animate-spin -->
<div class="animate-spin text-primary text-2xl">⟳</div>
```

**Skeleton Screen (For content loading):**

```html
<div class="space-y-4">
  <div class="h-8 bg-neutral-light rounded animate-pulse"></div>
  <div class="h-4 bg-neutral-light rounded animate-pulse"></div>
  <div class="h-4 bg-neutral-light rounded animate-pulse w-5/6"></div>
</div>
```

---

### 2.7 Modal / Dialog (Email Preview)

```html
<!-- Overlay -->
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
  <!-- Modal Card -->
  <div class="bg-white rounded-lg shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
    <!-- Header -->
    <div class="border-b border-neutral-light px-6 py-4 flex justify-between items-center">
      <h2 class="text-xl font-semibold text-neutral-dark">
        Email Preview
      </h2>
      <button class="text-secondary-light hover:text-neutral-dark transition-colors">
        ✕
      </button>
    </div>

    <!-- Content -->
    <div class="px-6 py-6 space-y-4">
      <div>
        <p class="text-xs font-semibold text-secondary-light mb-1">TO</p>
        <p class="text-base text-neutral-dark">Jake Williams (jake@college.com)</p>
      </div>
      <div>
        <p class="text-xs font-semibold text-secondary-light mb-1">SUBJECT</p>
        <p class="text-base text-neutral-dark">Quick intro to Sarah Chen — Tesla energy project</p>
      </div>
      <div class="bg-secondary-surface rounded p-4 text-sm text-neutral-base leading-relaxed">
        <p>Dear Jake,</p>
        <p class="mt-4">Hope you're doing well! I have a quick intro I think could be valuable...</p>
      </div>
    </div>

    <!-- Footer (Actions) -->
    <div class="border-t border-neutral-light px-6 py-4 flex gap-3">
      <button class="flex-1 px-4 py-2 rounded bg-primary text-white font-semibold hover:bg-primary-light transition-colors">
        Send As-Is
      </button>
      <button class="flex-1 px-4 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold hover:bg-secondary-surface transition-colors">
        Edit This Email
      </button>
    </div>
  </div>
</div>
```

---

## 3. Animations & Transitions

**Material Design motion principles:**
- Duration: 200ms for local changes, 300ms for page transitions
- Easing: `ease-in-out` for natural motion (not `linear`)
- Purpose: every animation explains state change or spatial relationship

```css
/* Fade in (page load, modal open) */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 300ms ease-in-out;
}

/* Slide up (dashboard sections, emails appearing) */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up {
  animation: slideUp 300ms ease-in-out;
}

/* Scale in (status badges) */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.scale-in {
  animation: scaleIn 200ms ease-in-out;
}

/* Ripple effect (email sent) */
@keyframes ripple {
  0% {
    opacity: 1;
    transform: scale(0);
  }
  100% {
    opacity: 0;
    transform: scale(4);
  }
}

.ripple::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 12px;
  background: currentColor;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ripple 600ms ease-in-out;
}

/* Tailwind transition classes (built-in) */
.transition-colors { transition-property: color, background-color, border-color; }
.transition-all { transition-property: all; }
.duration-200 { transition-duration: 200ms; }
.duration-300 { transition-duration: 300ms; }
.ease-in-out { transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }
```

**Specific Animations by Feature:**

| Feature | Animation | Duration | Purpose |
|---------|-----------|----------|---------|
| Email sent status change | Fade in `✓ Sent` badge | 200ms | Confirm action |
| Campaign status update | Slide up new timeline event | 300ms | Highlight new info |
| Email preview modal open | Fade in + scale | 200ms | Focus attention |
| Tab switch | Fade in content | 200ms | Smooth navigation |
| Button hover | Bg color + shadow change | 200ms | Interactive feedback |
| Campaign completion | Celebration ripple | 600ms | Celebrate success |

---

## 4. Responsive Design

**Breakpoints (Mobile-First):**

```css
/* Mobile (default, 320px+) */
/* Tablet (768px+) */
/* Desktop (1024px+) */
```

**Key Responsive Rules:**

| Component | Mobile | Tablet | Desktop |
|-----------|--------|--------|---------|
| Card padding | `p-4` | `p-6` | `p-6` |
| Typography | `text-base` | `text-base` | `text-base` |
| Tab bar | Stack vertically, full width | Horizontal, responsive | Horizontal, fixed width |
| Dashboard grid | 1 column | 1 column | 2-column option |
| 6-degree chain | Vertical layout, scroll horizontal | Horizontal, fit width | Horizontal, fit width |
| Email carousel | 1 email visible, swipe | 1.5 emails visible | 2 emails visible |

**Mobile-First CSS Example:**

```html
<!-- Dashboard section -->
<div class="grid gap-6 md:gap-8">
  <!-- Grid: 1 column by default, 2 on tablet+ -->
  <div class="flex flex-col md:flex-row gap-4 md:gap-6">
    <!-- Flex: column on mobile, row on tablet+ -->
  </div>
</div>

<!-- Tab bar (full-width on mobile, horizontal scroll on desktop) -->
<div class="flex overflow-x-auto md:overflow-x-visible gap-0 border-b border-neutral-light">
  <button class="flex-shrink-0 px-4 md:px-6 py-4 border-b-2 whitespace-nowrap">
    Your Campaign
  </button>
  <!-- ... -->
</div>

<!-- Email carousel (1 email on mobile, 2 on desktop) -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
  <div class="...">Email #1</div>
  <div class="hidden lg:block">Email #2</div>
</div>
```

---

## 5. Accessibility (A11y)

All components must meet WCAG 2.1 AA standards:

```html
<!-- Button with proper focus state -->
<button class="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
        aria-label="Start Campaign">
  Start Campaign
</button>

<!-- Form field with associated label -->
<label for="target-name" class="block text-sm font-semibold mb-2">
  Target Name
</label>
<input id="target-name" type="text" />

<!-- Icon with alt text -->
<button aria-label="Close email preview">
  <svg class="w-6 h-6"><!-- icon --></svg>
</button>

<!-- Color contrast: Always WCAG AA (4.5:1 for text) -->
<!-- Example: #2563eb (primary) on white = 5.1:1 ✓ -->

<!-- Focus visible indicator -->
*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

**Key A11y Rules:**

1. All buttons must have visible focus state (blue outline, 2px)
2. All form inputs must have associated labels
3. Color is never the only way to communicate status (use text + icon)
4. Touch targets (buttons, links) must be at least 44x44px
5. Text contrast must be 4.5:1 for body text, 3:1 for headings

---

## 6. Tailwind v4 Quick Reference

**Install & Configure (for reference):**

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Tailwind classes used most frequently in SixDegrees:**

```
Spacing: p-4, p-6, px-4, py-2, mb-4, mb-6, gap-4, gap-6
Text: text-sm, text-base, text-lg, text-xl, font-semibold, font-bold
Colors: bg-primary, text-primary, text-neutral-dark, text-secondary-light
Borders: border, border-neutral-light, rounded, rounded-lg, rounded-full
Layout: flex, grid, grid-cols-1, md:grid-cols-2, gap-6
States: hover:bg-primary-light, focus:ring-2, disabled:opacity-50
Animation: transition-colors, duration-200, ease-in-out, animate-spin
Responsive: md:px-6, md:grid-cols-2, lg:block, lg:flex

Sizing: w-full, h-auto, max-w-2xl, min-h-[120px]
Flex: flex-1, flex-shrink-0, items-center, justify-between
```

---

## 7. Dark Mode (Optional V2)

For future: add `.dark` class to `<html>` root to toggle theme.

```css
.dark {
  --neutral-dark: #f9fafb;
  --neutral-base: #d1d5db;
  --neutral-surface: #1f2937;
  --neutral-white: #0f172a;
  --primary-surface: #001f3f;
  --secondary-surface: #111827;
}

/* Tailwind dark mode class utility: dark:bg-neutral-surface */
```

---

## 8. Component Example: Email Status Card

**Complete, Copy-Paste Ready Component:**

```html
<div class="rounded bg-white shadow-md border border-transparent hover:shadow-lg transition-shadow p-6">
  <!-- Header -->
  <div class="flex items-start justify-between mb-4">
    <div>
      <p class="text-xs font-semibold text-secondary-light mb-1">EMAIL #1</p>
      <h4 class="text-lg font-semibold text-neutral-dark">
        To: Jake Williams
      </h4>
    </div>
    <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
                 bg-success-surface text-success font-semibold text-xs">
      ✓ Sent
    </span>
  </div>

  <!-- Subject -->
  <div class="mb-4">
    <p class="text-xs font-semibold text-secondary-light mb-1">SUBJECT</p>
    <p class="text-base text-neutral-dark">
      Quick intro to Sarah Chen — Tesla energy project
    </p>
  </div>

  <!-- Preview -->
  <div class="bg-secondary-surface rounded p-4 mb-4 text-sm text-neutral-base leading-relaxed">
    <p>Dear Jake,</p>
    <p class="mt-3">Hope you're doing well! I have a quick intro I think could be valuable...</p>
  </div>

  <!-- Metadata -->
  <div class="flex items-center justify-between text-xs text-secondary-light mb-4">
    <span>Sent 3 hours ago</span>
    <span>✓ Delivered</span>
  </div>

  <!-- Actions -->
  <div class="flex gap-3">
    <button class="flex-1 px-4 py-2 rounded bg-primary text-white font-semibold text-sm
                   hover:bg-primary-light transition-colors">
      View Full Email
    </button>
    <button class="flex-1 px-4 py-2 rounded bg-neutral-surface border border-neutral-light
                   text-neutral-dark font-semibold text-sm
                   hover:bg-secondary-surface transition-colors">
      View Reply
    </button>
  </div>
</div>
```

---

## 9. Bilingual Support (EN / 中文)

**Strategy:** Single HTML with language toggle. All text in data attributes.

```html
<!-- Language Toggle (Top-right of every page) -->
<div class="flex gap-2">
  <button id="lang-en" class="px-3 py-1 rounded bg-primary text-white text-xs font-semibold">
    English
  </button>
  <button id="lang-zh" class="px-3 py-1 rounded bg-neutral-surface border border-neutral-light text-neutral-dark text-xs font-semibold">
    中文
  </button>
</div>

<!-- Element with bilingual text -->
<h2 class="text-2xl font-bold text-neutral-dark"
    data-en="Your Campaign"
    data-zh="你的活动计划">
  Your Campaign
</h2>

<!-- JavaScript: On click, switch language, update all data-* attributes -->
<script>
document.getElementById('lang-en').addEventListener('click', () => {
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = el.getAttribute('data-en');
  });
  localStorage.setItem('language', 'en');
});

document.getElementById('lang-zh').addEventListener('click', () => {
  document.querySelectorAll('[data-zh]').forEach(el => {
    el.textContent = el.getAttribute('data-zh');
  });
  localStorage.setItem('language', 'zh');
});

// On load, restore saved language
const savedLang = localStorage.getItem('language') || 'en';
document.getElementById(`lang-${savedLang}`).click();
</script>
```

**Font pairing (EN + 中文):**

The system font stack already includes Noto Sans CJK SC:
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
             "Helvetica Neue", sans-serif, "Noto Sans CJK SC", "Noto Sans";
```

This auto-selects CJK characters for 中文, Latin for English.

---

## 10. Component Checklist for DHH

**Before starting, verify these components exist:**

- [ ] Primary button (blue, CTA)
- [ ] Secondary button (gray, less prominent)
- [ ] Destructive button (red, delete actions)
- [ ] Card with elevation (shadow-md)
- [ ] Tab navigation (border-bottom indicator)
- [ ] Status badge (green/amber/red)
- [ ] Form input + label
- [ ] Modal/dialog (email preview)
- [ ] Spinner (loading state)
- [ ] Language toggle (EN/中文)
- [ ] Focus state on all interactive elements
- [ ] Mobile responsive (tested on 375px width)
- [ ] Bilingual text rendering (test both languages)

---

## 11. Design System Rules (Red Flags)

**DO:**
- Use Tailwind utility classes (no custom CSS unless absolutely needed)
- Follow the 8px grid for spacing
- Apply semantic colors (green for success, red for error)
- Show visual feedback for every user action
- Test on mobile devices (375px min)

**DON'T:**
- Create new colors outside the palette
- Use colors purely decoratively (every color has meaning)
- Forget focus states on interactive elements
- Ignore bilingual text weight/sizing
- Skip hover states on buttons/links
- Use shadows unless indicating elevation

---

## Summary

This design system provides a cohesive, accessible, bilingual experience for SixDegrees. Every component is copy-paste ready. Use Tailwind v4 classes as primary implementation; CSS variables support dark mode and future themes.

**Key files for implementation:**
- `docs/ui/sixdegrees-design-system.md` (this file) — Color, typography, components
- `docs/ui/sixdegrees-layouts.md` — Page layouts, grid structures
- `docs/ui/sixdegrees-components.md` — Advanced components (6-degree chain, email carousel, etc.)

**Start here:** Pick a page (landing → intake → dashboard), build all components for that page using the classes above, test on mobile and desktop, toggle language.

---

**Design System Version:** 1.0
**Status:** Ready for Engineering
**Next Review:** After MVP launch
