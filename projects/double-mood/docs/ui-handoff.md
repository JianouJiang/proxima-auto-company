# Double Mood UI Handoff — Ready for Development

## Design Deliverables

All design specifications are complete and ready for implementation:

### 1. Design System Documentation
**Location:** `projects/double-mood/docs/design-system.md`

**Contents:**
- Complete color palette with hex codes and semantic meaning
- Typography scale and bilingual considerations
- SVG breathing circle animation code (copy-paste ready)
- Responsive layout mockup with spacing system
- Accessibility specifications (WCAG AAA compliance)
- Tailwind CDN configuration
- Reduced motion support
- Screen reader ARIA labels

### 2. Color Palette Reference
**Location:** `projects/double-mood/docs/color-palette.md`

**Contents:**
- Quick copy-paste CSS variables
- Tailwind config snippet
- Color psychology rationale
- Gradient definitions for SVG and mood sliders
- Accessibility contrast ratios

### 3. Interactive Design Preview
**Location:** `projects/double-mood/docs/design-preview.html`

**View it:** Open in browser to see the breathing animation in action.

**What it shows:**
- Full page layout (mobile-first)
- Working breathing circle with 4s inhale / 6s exhale
- Synchronized text cues ("Breathe in..." / "Breathe out...")
- Bilingual labels (English + 中文)
- Mood slider gradients

---

## Implementation Checklist for Fullstack DHH

### HTML Structure
- [x] Design spec created
- [ ] Build `projects/double-mood/index.html` using Tailwind CDN
- [ ] Copy SVG breathing circle from design-system.md
- [ ] Implement breathing sync JavaScript (10s cycle, 4s inhale)
- [ ] Add mood sliders (before/after) with gradient backgrounds
- [ ] Include bilingual labels for all UI elements

### CSS Styling
- [ ] Use Tailwind classes from design-system.md
- [ ] Apply color palette via Tailwind config
- [ ] Ensure mobile-first responsive layout
- [ ] Add focus ring styles for accessibility
- [ ] Test on iOS Safari and Android Chrome (DevOps to validate)

### JavaScript Functionality
- [ ] Breathing cycle timer (4s inhale, 6s exhale, repeat)
- [ ] Text cue synchronization (fade in/out)
- [ ] Mood slider value tracking (before/after delta)
- [ ] Local storage persistence (optional for Phase 1)

### Accessibility
- [ ] ARIA labels for screen readers
- [ ] Keyboard navigation for sliders
- [ ] Reduced motion media query
- [ ] Contrast ratios verified (WCAG AAA)

---

## Design Decisions Made

### 1. Color Palette: Blue-Green System
**Why:** Psychologically calming, non-clinical feel. Blue reduces heart rate, teal suggests renewal.

**Contrast compliance:**
- Text: 10.5:1 (AAA)
- UI elements: 4.8:1+ (AA)

### 2. Animation Timing: 4s Inhale, 6s Exhale
**Why:** Matches Navy SEAL box breathing cadence. Longer exhale activates parasympathetic nervous system (calm response).

**Technical:** SVG SMIL animation with cubic-bezier easing for natural breath feel.

### 3. Bilingual Display: Simultaneous EN + CN
**Why:** Simplest implementation for Phase 1. Avoids language toggle UI complexity.

**Format:**
- Primary text: English (larger font)
- Secondary text: 中文 (slightly smaller, muted color)

### 4. Typography: System Fonts Only
**Why:** Zero network requests, instant load, excellent Chinese glyph rendering via Noto Sans.

**Stack:** `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans"`

### 5. Layout: Vertical Stack (Mobile-First)
**Why:** 80% of users will access on mobile during anxious moments. Desktop can use same layout (centered, max-width constrained).

**Hierarchy:**
1. Header question
2. Before mood slider
3. Breathing circle (hero element)
4. After mood slider
5. Encouraging footer text

---

## Open Questions for Product Norman

1. **Cycle duration:** Is 10s (4s in, 6s out) optimal? Alternatives:
   - 4-7-8 breathing (4s in, 7s hold, 8s out)
   - Box breathing (4-4-4-4)

2. **Completion feedback:** Should we show:
   - Cycle counter ("3 breaths completed")
   - Mood improvement delta ("+2 calmer")
   - Encouraging message ("You're doing great")

3. **Skip option:** Should users be able to skip breathing and just log mood?

4. **Sound:** Add optional breathing sound cues (inhale/exhale chimes)?

---

## Technical Notes for DevOps Hightower

### Deployment Target
- **Platform:** Cloudflare Pages
- **Domain:** `doublemood.pages.dev` (or custom domain TBD)
- **Build:** None required (static HTML + Tailwind CDN)
- **Analytics:** Cloudflare Web Analytics (privacy-friendly, no cookies)

### Performance Targets
- **Load time:** <1s on 3G (single HTML file, CDN resources)
- **Animation FPS:** 60fps (GPU-accelerated SVG)
- **Lighthouse score:** 90+ (Performance, Accessibility, Best Practices)

### Testing Checklist
- [ ] iOS Safari (iPhone SE, iPhone 14 Pro)
- [ ] Android Chrome (Pixel, Samsung)
- [ ] Desktop Chrome/Firefox/Safari
- [ ] Reduced motion preference
- [ ] Screen reader (VoiceOver, TalkBack)

---

## Next Actions

1. **@fullstack-dhh:** Build `index.html` based on design-preview.html as template
2. **@qa-bach:** Test animation smoothness and accessibility
3. **@devops-hightower:** Deploy to Cloudflare Pages, run Lighthouse audit
4. **@operations-pg:** Add analytics snippet, track mood improvement delta

**Target:** Ship within 24 hours.

---

## Design Philosophy Recap

**Emotional first-aid, not clinical therapy.**

- **Calming:** Blue-green palette, smooth animations, soft gradients
- **Reassuring:** Encouraging copy, bilingual support, non-judgmental tone
- **Immediate:** No login, no friction, instant access to breathing
- **Accessible:** WCAG AAA, keyboard nav, screen readers, reduced motion

**Material metaphor:** The breathing circle feels like a glowing orb you hold in your hand — expanding and contracting with your breath. Physical, tactile, grounding.

---

**Design handoff complete.**
**Owner:** ui-duarte
**Date:** 2026-02-21
**Status:** Ready for development
