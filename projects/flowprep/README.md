# FlowPrep AI — HVAC CFD Preprocessing Landing Page

**Status:** Landing page complete, ready for deployment
**Built:** 2026-02-21
**Built by:** fullstack-dhh

---

## Overview

FlowPrep AI is an automated CFD preprocessing tool for HVAC engineers. This landing page is designed to convert HVAC engineers who currently spend 4-6 hours on manual CFD preprocessing into paying customers.

**Target Audience:** Senior HVAC engineers at MEP consultancies (8-15 years experience)

**Product:** Automated OpenFOAM workflow for office diffuser placement and server room cooling

---

## File Structure

```
flowprep/
├── README.md (this file)
└── public/
    └── index.html (complete landing page)
```

---

## Technical Stack

- **Single HTML file** (33KB, 682 lines)
- **Tailwind CSS v4** via CDN (no build process)
- **No JavaScript** required (static HTML + CSS only)
- **Semantic HTML5** with accessibility features
- **Responsive design** (mobile-first, breakpoints at 768px and 1024px)

---

## Sections Implemented

1. **Hero** — Value proposition + Stripe payment CTA
2. **Before/After Comparison** — Manual workflow (4-6 hours) vs FlowPrep (15 minutes)
3. **How It Works** — 3-step workflow (Upload → Process → Download)
4. **ANSYS Validation** — Trust signal with ±8% velocity accuracy
5. **Founder Bio** — PhD credibility, technical background
6. **Pricing** — £39/month early access with ROI calculator
7. **FAQ** — 5 common objections preempted
8. **Footer** — Contact, Terms, Privacy

---

## Placeholder Content (For Founder to Replace)

The following placeholders need to be replaced before deployment:

| Placeholder | Location | Replacement Action |
|-------------|----------|-------------------|
| `[Founder Name]` | Hero, Trust section | Replace with actual founder name |
| `[Research Partner]` | Trust section | Replace with validation partner name (e.g., "Arup", "WSP") |
| `[Paper Title]` | Trust section | Replace with actual research paper title or remove line |
| `[Founder Photo]` | Trust section | Add `<img src="founder-photo.jpg" alt="Founder Name headshot">` |
| `[founder email]` | FAQ section | Replace with support email address |
| Screenshot placeholders | Demo section | Add 3 actual screenshots (upload UI, processing status, results page) |

---

## Stripe Payment Integration

Payment link is already integrated:
- **URL:** `https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05`
- **Price:** £39/month
- **Location:** Hero CTA (secondary button), Pricing section CTA (primary button)

No additional code required — Stripe handles checkout flow.

---

## Design System

### Colors (Tailwind config embedded)
- **Primary (Teal):** `#0D9488` — Energy efficiency, scientific credibility
- **Accent (Cyan):** `#0891B2` — Data visualization, links
- **Before/Pain (Red):** `#DC2626` — Manual workflow pain points
- **After/Relief (Green):** `#059669` — FlowPrep workflow benefits

### Typography
- **Font stack:** System fonts (fast loading, professional)
- **Headings:** Bold, tight tracking, 48px-60px (H1)
- **Body:** 16px base, 1.7 line height (optimal readability)

### Layout
- **Max width:** 1280px container, centered
- **Spacing:** 8px grid rhythm (Material Design principle)
- **Responsive:** Mobile-first, single column on <768px

---

## SEO & Meta Tags

Implemented:
- ✅ Title: "FlowPrep AI — HVAC Diffuser CFD in 15 Minutes"
- ✅ Meta description (HVAC-specific keywords)
- ✅ Open Graph tags (social sharing)
- ✅ Twitter Card tags
- ✅ Schema.org structured data (SoftwareApplication)

**Missing (for deployment):**
- `og-image.jpg` (1200x630px social media preview image)

---

## Deployment Checklist

Before deploying to Cloudflare Pages:

- [ ] Replace all `[Placeholder]` text with actual content
- [ ] Add founder headshot photo (square 1:1 aspect ratio)
- [ ] Add 3 demo screenshots (drag-drop UI, processing status, results page)
- [ ] Create `og-image.jpg` for social sharing (1200x630px)
- [ ] Generate ANSYS validation PDF (or link to existing paper)
- [ ] Test Stripe payment link in production mode
- [ ] Validate HTML (W3C validator)
- [ ] Test responsive layout on mobile/tablet
- [ ] Test keyboard navigation and screen reader accessibility
- [ ] Run PageSpeed Insights (target: <2.5s LCP)

---

## Deployment Commands

```bash
# From project root
cd projects/flowprep

# Deploy to Cloudflare Pages
wrangler pages deploy public --project-name=flowprep-ai

# Expected URL: https://flowprep-ai.pages.dev
```

---

## Design Rationale

### Why Green/Teal?
1. Energy efficiency signal (HVAC engineers care about sustainability)
2. Scientific visualization heritage (teal is common in CFD color maps)
3. Differentiation (not blue like every SaaS, not purple like startups)

### Why System Fonts?
1. Zero network requests = instant load
2. Familiar to engineers (macOS/Windows/Linux UI fonts)
3. Professional context (ANSYS doesn't use custom fonts, FlowPrep shouldn't either)

### Why No JavaScript?
1. Fast loading on corporate VPNs
2. Works with strict content security policies
3. Engineers distrust "magic" — static HTML = transparent
4. Native browser features (details/summary accordion, smooth scroll)

### Why Honest Disclaimers?
- "FlowPrep is in beta. Always verify critical results..."
- Engineers can lose PE license if results are wrong
- Transparency = trust (fellow engineer would warn, vendor wouldn't)

---

## Performance Targets

- **First Contentful Paint:** <1.5s
- **Largest Contentful Paint:** <2.5s
- **Total File Size:** <500KB (currently 33KB HTML + Tailwind CDN)
- **Accessibility:** WCAG 2.1 AA compliant

---

## Next Steps (Post-Launch)

1. **Add Plausible Analytics** (privacy-friendly, no GDPR banner needed)
2. **A/B test hero CTA** ("See How It Works" vs "Start Free Trial")
3. **Add email capture** for waitlist (if beta capacity limited)
4. **Create tutorial video** (Revit STL export → FlowPrep workflow)
5. **Write SEO blog posts** (e.g., "OpenFOAM meshing best practices for HVAC")

---

## Reference Documents

Design and UX specifications:
- `docs/interaction/flowprep-landing-ux.md` — User journey, content structure
- `docs/ui/flowprep-design-system.md` — Visual design, color palette, typography

---

**File Status:** Production-ready (pending placeholder content replacement)
**Last Updated:** 2026-02-21
