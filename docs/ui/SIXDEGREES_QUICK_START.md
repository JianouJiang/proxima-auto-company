# SixDegrees Design System — Quick Start for DHH

**For:** fullstack-dhh (Frontend Implementation)
**From:** UI Design Director (Matías Duarte)
**Date:** 2026-02-22

---

## You Have 3 Documents to Work From

1. **`sixdegrees-design-system.md`** — All colors, typography, spacing, components
2. **`sixdegrees-layouts.md`** — Page structures and HTML layout templates
3. **`sixdegrees-components.md`** — Complex components (6-degree chain, email carousel, etc.)

**Copy-paste every code example directly.** All CSS uses Tailwind v4 + semantic color variables.

---

## Core Color Palette (TL;DR)

```css
--primary: #2563eb          (Blue — CTA, brand, trust)
--success: #16a34a          (Green — emails sent, campaign complete)
--warning: #ca8a04          (Amber — waiting, in progress, needs attention)
--error: #dc2626            (Red — failed, delete action)
--neutral-dark: #1f2937     (Text, headings)
--neutral-base: #374151     (Body text, secondary)
--neutral-light: #d1d5db    (Borders, dividers)
--neutral-surface: #f9fafb  (Card backgrounds)
```

**Usage:** Every visual element uses one of these colors. No custom colors.

---

## Spacing System (8px Grid)

```
4px = spacing-1
8px = spacing-2  ← Base unit
12px = spacing-3
16px = spacing-4
24px = spacing-6
32px = spacing-8
```

**Tailwind classes:** `p-4`, `p-6`, `mb-4`, `gap-4`, etc.

---

## Typography Stack

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
             "Helvetica Neue", sans-serif, "Noto Sans CJK SC", "Noto Sans";
```

Auto-selects CJK font for Chinese characters, Latin for English. Works perfectly.

**Scale:**
- H1: 32px, bold, `text-neutral-dark`
- H2: 24px, bold, `text-neutral-dark`
- H3: 20px, semibold, `text-neutral-dark`
- Body: 16px, regular, `text-neutral-base`
- Small: 14px, regular, `text-secondary-light`

---

## Component Quick Reference

### Buttons

**Primary (CTA):**
```html
<button class="px-6 py-3 rounded bg-primary hover:bg-primary-light
               text-white font-semibold text-base transition-colors
               focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
  Start Campaign
</button>
```

**Secondary:**
```html
<button class="px-6 py-3 rounded bg-neutral-surface border border-neutral-light
               hover:bg-secondary-surface text-neutral-dark font-semibold text-base
               transition-colors focus:outline-none focus:ring-2 focus:ring-primary">
  Edit Target
</button>
```

**Destructive (Red):**
```html
<button class="px-6 py-3 rounded bg-error hover:bg-error-light text-white
               font-semibold text-base transition-colors">
  Delete Account
</button>
```

### Cards

**Elevated (with shadow):**
```html
<div class="rounded bg-white shadow-md border border-transparent hover:shadow-lg
            transition-shadow p-6">
  <!-- content -->
</div>
```

**Flat (no shadow):**
```html
<div class="rounded bg-secondary-surface border border-neutral-light p-4">
  <!-- content -->
</div>
```

### Status Badges

```html
<!-- Sent (Green) -->
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-success-surface text-success font-semibold text-xs">
  ✓ Sent
</span>

<!-- Waiting (Amber) -->
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-warning-surface text-warning font-semibold text-xs">
  ⏳ Waiting
</span>

<!-- Draft (Gray) -->
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full
             bg-secondary-surface text-secondary font-semibold text-xs">
  ✎ Draft
</span>
```

### Form Fields

```html
<label for="target" class="block text-sm font-semibold text-neutral-dark mb-2">
  Who do you want to reach?
</label>
<input id="target" type="text"
       class="w-full px-4 py-2 rounded border border-neutral-light
              focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary
              transition-colors" />
```

### Tabs

```html
<div class="flex border-b border-neutral-light">
  <button class="pb-4 px-4 border-b-2 border-primary text-primary font-semibold">
    Your Campaign
  </button>
  <button class="pb-4 px-4 border-b-2 border-transparent text-secondary-light hover:text-neutral-base">
    Connections
  </button>
</div>
```

---

## Bilingual Implementation (EN / 中文)

**Every text element needs both languages:**

```html
<h1 data-en="Your Campaign" data-zh="你的活动计划">
  Your Campaign
</h1>

<button data-en="Start Campaign" data-zh="启动活动">
  Start Campaign
</button>
```

**JavaScript toggle:**

```javascript
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

// On page load, restore saved language
const savedLang = localStorage.getItem('language') || 'en';
document.getElementById(`lang-${savedLang}`).click();
```

---

## Responsive Breakpoints

**Mobile first (default 320px):**

```html
<!-- Single column on mobile, 3 columns on desktop -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <!-- Each email card -->
</div>

<!-- Full width on mobile, max width on desktop -->
<div class="px-4 md:px-6 max-w-7xl mx-auto">
  <!-- Page content -->
</div>

<!-- Stack vertically on mobile, horizontal on desktop -->
<div class="flex flex-col md:flex-row gap-4 md:gap-6">
  <!-- Items -->
</div>
```

**Key breakpoints:**
- `md:` applies at 768px and above (tablets)
- `lg:` applies at 1024px and above (desktops)

---

## Implementation Checklist

### Page 1: Landing Page (`index.html`)

- [ ] Header with logo + language toggle + CTA button
- [ ] Hero section (H1, subheading, primary CTA button)
- [ ] 4 proof points (icons + text, 1 column mobile, 4 column desktop)
- [ ] Trust section (privacy, no spam, guaranteed results)
- [ ] Pricing cards (Free, $29, $99)
- [ ] Final CTA section
- [ ] Footer with links

**Estimated time:** 1-2 hours

### Page 2: Intake Form (`intake.html`)

- [ ] Header + language toggle
- [ ] Form title + description
- [ ] 6 form fields (email, name, target name, target company, target reason, user background)
- [ ] Character counters for textareas (500 max)
- [ ] Progress indicator (0/6 fields filled)
- [ ] Submit button (disabled until all filled)
- [ ] On submit: show "Analyzing..." spinner, POST to `/api/intake`, redirect to OAuth
- [ ] Language toggle support

**Estimated time:** 1-2 hours

### Page 3: Dashboard (`dashboard.html`)

- [ ] Sticky header (logo, campaign name, settings/logout)
- [ ] Sticky tab navigation ([Your Campaign] [Connections] [Credits] [Settings])
- [ ] Tab 1: Your Campaign
  - [ ] Status card (badge, progress bar, action buttons)
  - [ ] 6-degree chain (SVG or HTML, responsive)
  - [ ] "What's happening now" (timeline with icons)
  - [ ] Email carousel (3 cards, horizontal scroll mobile, grid desktop)
- [ ] Tab 2: Connections (placeholder for email history list)
- [ ] Tab 3: Credits (pricing cards with Stripe links)
- [ ] Tab 4: Settings (account + language + danger zone)
- [ ] Auto-refresh dashboard every 30s (fetch from `/api/campaign/:id`)

**Estimated time:** 3-4 hours

### Accessibility & Testing

- [ ] All buttons have visible focus state (blue ring)
- [ ] All form inputs have associated labels
- [ ] Test bilingual rendering (EN and 中文) on each page
- [ ] Test responsive at 320px, 375px, 768px, 1024px widths
- [ ] Color contrast: 4.5:1 minimum (use WebAIM checker)
- [ ] Touch targets: 44x44px minimum

**Estimated time:** 1 hour

---

## Animation & Micro-interactions

**No animations without purpose. All 200-300ms:**

```css
/* Smooth color transition on button hover */
transition-colors duration-200

/* Fade in new content */
animation: fadeIn 300ms ease-in-out

/* Slide up on page load */
animation: slideUp 300ms ease-in-out

/* Pulse icon when waiting */
animate-pulse
```

See `sixdegrees-design-system.md` Section 3 for all animation specs.

---

## Key Rules (Don't Break These)

1. **All colors come from the palette.** No custom hex values.
2. **All spacing uses 8px grid.** No arbitrary spacing.
3. **All text is bilingual.** Every UI string needs `data-en` and `data-zh`.
4. **All buttons have focus rings.** `focus:ring-2 focus:ring-primary focus:ring-offset-2`
5. **Mobile first.** Design for 320px, then add `md:` and `lg:` classes.
6. **Use Tailwind classes.** No custom CSS unless absolutely necessary.
7. **Test on real mobile.** 375px minimum width (iPhone SE).

---

## File Structure

```
projects/sixdegrees/
├── index.html              (Landing page)
├── intake.html             (Intake form)
├── dashboard.html          (Main dashboard)
├── public/                 (Static assets)
│   ├── logo.svg
│   └── favicon.ico
├── functions/              (Cloudflare Worker Functions)
│   ├── api/
│   │   ├── intake.js
│   │   ├── campaign.js
│   │   ├── oauth/callback.js
│   │   └── send.js
│   └── ...
└── wrangler.toml           (Cloudflare config)
```

---

## API Endpoints You'll Call (from Frontend)

```javascript
// 1. Submit intake form
fetch('/api/intake', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_email: '...',
    user_name: '...',
    target_name: '...',
    // ... etc
  })
});

// 2. Get campaign details (polling every 30s)
fetch('/api/campaign/:campaign_id', {
  headers: { 'Authorization': 'Bearer ' + getToken() }
});

// 3. Send an email
fetch('/api/campaign/:campaign_id/send', {
  method: 'POST',
  body: JSON.stringify({ email_id: 'email-1' })
});

// 4. OAuth callback (handled by backend)
// Redirect to: /api/oauth/callback?code=...&state=...
```

See `docs/interaction/SIXDEGREES_HANDOFF.md` for full API specs.

---

## Testing Checklist

**Before shipping to devops-hightower:**

1. [ ] Landing page loads (check all 6 sections)
2. [ ] Language toggle works (EN ↔ 中文) on every page
3. [ ] Form validation works (character counters, submit disabled until complete)
4. [ ] Dashboard tab switching works (click each tab, content changes)
5. [ ] Email carousel scrolls on mobile (manually test on 375px)
6. [ ] 6-degree chain renders correctly (check SVG on desktop and mobile)
7. [ ] Buttons all have hover + focus states
8. [ ] No horizontal scrollbars on mobile (test at 320px width)
9. [ ] Bilingual text doesn't overflow (test with long Chinese text)
10. [ ] All links/buttons have proper color contrast (use WebAIM)

---

## Common Tailwind Classes You'll Use Most

```
Spacing:    p-4, p-6, px-4, py-2, mb-4, mb-6, gap-4, gap-6
Text:       text-sm, text-base, text-lg, text-xl, font-semibold, font-bold
Colors:     bg-primary, text-primary, text-neutral-dark, text-secondary-light
Borders:    border, border-neutral-light, rounded, rounded-lg, rounded-full
Flex:       flex, flex-col, md:flex-row, items-center, justify-between
Grid:       grid, grid-cols-1, md:grid-cols-3, gap-4, gap-6
States:     hover:bg-primary-light, focus:ring-2, disabled:opacity-50, active:bg-primary-dark
Animation:  transition-colors, duration-200, ease-in-out, animate-spin, animate-pulse
Display:    hidden, md:hidden, lg:block, flex, grid, absolute, fixed, sticky, relative
```

---

## Questions? Reference These Sections

- **Colors:** `sixdegrees-design-system.md` Section 1.1
- **Typography:** `sixdegrees-design-system.md` Section 1.2
- **Components:** `sixdegrees-design-system.md` Section 2
- **Animations:** `sixdegrees-design-system.md` Section 3
- **Layouts:** `sixdegrees-layouts.md` (page-by-page)
- **Complex components:** `sixdegrees-components.md` (6-degree chain, carousel, etc.)

---

## Next Steps

1. **Start with landing page** (`index.html`)
   - Copy HTML structure from `sixdegrees-layouts.md` Section 1
   - Apply colors/spacing from `sixdegrees-design-system.md`
   - Test bilingual toggle

2. **Then build intake form** (`intake.html`)
   - Copy form template from `sixdegrees-layouts.md` Section 2
   - Add form validation (check `sixdegrees-layouts.md` for JavaScript)

3. **Finally build dashboard** (`dashboard.html`)
   - Copy main structure from `sixdegrees-layouts.md` Section 3
   - Add complex components from `sixdegrees-components.md`
   - Implement API calls to devops-hightower endpoints

4. **Test everything**
   - Bilingual (EN/中文)
   - Responsive (320px, 375px, 768px, 1024px)
   - Accessibility (focus, contrast, labels)

---

**Good luck! You've got all the specs you need. Just copy-paste and connect to backend.**

---

Version: 1.0
Date: 2026-02-22
Design System Status: ✓ Complete and Ready
