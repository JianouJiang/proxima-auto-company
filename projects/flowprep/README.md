# FlowPrep AI Landing Page

**Status:** Production-ready, pending founder content
**Live URL:** https://flowprep-ai.pages.dev/
**Deployment:** Cloudflare Pages

---

## Overview

Single-file HTML landing page for FlowPrep AI — automated OpenFOAM preprocessing for HVAC engineers.

**Target Audience:** HVAC design engineers at MEP consultancies
**Stripe Payment Link:** https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05 (£39/month early access)

---

## Deployment Instructions

The landing page is already deployed to Cloudflare Pages. To redeploy after updates:

```bash
cd projects/flowprep
wrangler pages deploy public --project-name flowprep-ai
```

**Custom domain:** Configure in Cloudflare Pages dashboard (flowprep.ai or keep flowprep-ai.pages.dev)

---

## Founder Placeholders to Fill

Search and replace the following placeholders in `public/index.html`:

### 1. Founder Name
- **Search:** `[Founder Name]`
- **Replace with:** Your full name (e.g., "Dr. Sarah Chen")
- **Locations:** Hero section, Trust section bio

### 2. Founder Email
- **Search:** `[Founder Email]` and `[founder email]`
- **Replace with:** Your support email (e.g., "sarah@flowprep.ai")
- **Locations:** FAQ section, Footer

### 3. Research Partner Company
- **Search:** `[Research Partner Company]`
- **Replace with:** Name of company/institution where you validated FlowPrep (e.g., "Arup Group")
- **Locations:** Trust section bio

### 4. Academic Publication
- **Search:** `[Paper Title]`
- **Replace with:** Your published paper title (e.g., "ML-Enhanced Meshing for HVAC CFD")
- **Search:** `[Journal Name]`
- **Replace with:** Journal or conference name (e.g., "Building and Environment")
- **Locations:** Trust section technical background

### 5. Screenshots (Week 2)
Three screenshot placeholders with dashed borders:
1. **Upload interface:** Drag-drop with STL file example
2. **Processing status:** Progress bar showing OpenFOAM running
3. **Results page:** 3 visualization thumbnails (velocity, temperature, PMV)

Replace these divs with actual `<img>` tags:
```html
<!-- Current placeholder: -->
<div class="bg-flow-bg-tertiary rounded-lg mb-4 aspect-video flex items-center justify-center border-2 border-dashed border-flow-border">
  <p class="text-flow-text-light text-center px-4">[Screenshot: ...]</p>
</div>

<!-- Replace with: -->
<img src="screenshot-upload.png" alt="FlowPrep upload interface" class="rounded-lg mb-4 aspect-video w-full object-cover border border-flow-border">
```

### 6. Founder Photo
- **Current:** Gray placeholder box in Trust section
- **Replace with:** Professional headshot (square 1:1 aspect ratio, min 400×400px)
- **Recommended style:** Professional but approachable, solid background or blurred office

Replace this div:
```html
<div class="aspect-square bg-flow-bg-tertiary rounded-lg flex items-center justify-center border border-flow-border">
  <p class="text-flow-text-light text-center px-4 text-sm">[Founder Photo]<br>Professional headshot<br>(to be added)</p>
</div>
```

With:
```html
<img src="founder-photo.jpg" alt="[Your Name] headshot" class="w-full h-full object-cover rounded-lg border border-flow-border">
```

### 7. Validation Study PDF (Week 4)
- **Current:** "Full validation study (PDF) — Available Week 4"
- **Replace with:** Link to actual PDF after completing validation tests
```html
<a href="flowprep-ansys-validation-2026.pdf" class="text-flow-accent hover:underline font-medium inline-flex items-center">
  Download full validation study (PDF)
  <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
  </svg>
</a>
```

---

## Cloudflare Web Analytics

Add the Cloudflare Web Analytics beacon script to the footer (before `</footer>`):

```html
<!-- Cloudflare Web Analytics -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "YOUR_TOKEN_HERE"}'></script>
```

**Get token:** Cloudflare Dashboard → Analytics & Logs → Web Analytics → Add a site

---

## File Structure

```
projects/flowprep/
├── public/
│   ├── index.html          # Single-file landing page (production-ready)
│   ├── (screenshots)       # Add Week 2: upload.png, processing.png, results.png
│   ├── (founder-photo.jpg) # Add before launch
│   └── (validation.pdf)    # Add Week 4
├── README.md               # This file
└── wrangler.toml           # Cloudflare Pages config (already exists)
```

---

## Technical Stack

- **Single HTML file** — No build process, ~900 lines
- **Tailwind CSS v4** — CDN (no npm install)
- **Minimal JavaScript** — Only for button transitions and FAQ accordion
- **Semantic HTML5** — Accessibility built-in
- **Responsive design** — Mobile-first, breakpoints at 768px and 1024px

---

## Sections Implemented

1. **Hero** — Value proposition + dual CTAs (See Demo + Early Access)
2. **Before/After** — Manual workflow (4-6 hours) vs FlowPrep (15 minutes)
3. **Demo (How It Works)** — 3-step workflow with screenshot placeholders
4. **ANSYS Validation** — ±8% accuracy callout with beta disclaimer
5. **Trust (Founder Bio)** — PhD credibility, technical background, validation methodology
6. **Pricing** — £39/month with ROI calculator (£1,500 value vs £39 cost)
7. **FAQ** — 7 questions preempting objections
8. **Final CTA** — "Ready to Get 6 Hours Back This Week?"
9. **Footer** — Contact, Terms, Privacy, Cloudflare Analytics placeholder

---

## Design System

**Color Palette:** Green/teal energy theme
- Primary: `#0D9488` (Teal-600) — Energy efficiency signal
- Accent: `#0891B2` (Cyan-600) — Data visualization
- Success: `#10B981` (Emerald-500) — Validation checkmarks
- Before (pain): `#DC2626` (Red-600) — Manual workflow pain
- After (relief): `#059669` (Emerald-600) — FlowPrep benefits

**Typography:** System font stack (no web fonts for fast loading)
**Layout:** Single-scroll linear narrative (no nav menu)

Full design system: `docs/ui/flowprep-design-system.md`
Interaction design: `docs/interaction/flowprep-landing-ux.md`

---

## Content Principles

1. **No fake testimonials** — Only real validation data
2. **No AI fluff** — Technical accuracy over marketing polish
3. **Honest disclaimers** — "FlowPrep is beta, verify results with ANSYS"
4. **Domain-specific** — HVAC examples only (no aerospace/automotive)
5. **Technical credibility** — Use CFD terminology (snappyHexMesh, y+, skewness)

---

## Pre-Launch Checklist

- [ ] Replace all `[Founder Name]` placeholders
- [ ] Replace all `[Founder Email]` placeholders
- [ ] Replace `[Research Partner Company]`
- [ ] Replace `[Paper Title]` and `[Journal Name]`
- [ ] Add 3 screenshots (upload, processing, results)
- [ ] Add founder photo (square, professional)
- [ ] Test Stripe payment link (use test mode first)
- [ ] Add Cloudflare Web Analytics script
- [ ] Validate HTML with W3C validator
- [ ] Test mobile responsive layout (iPhone SE, iPad)
- [ ] Test accessibility (keyboard navigation, screen reader)
- [ ] Test loading speed with PageSpeed Insights
- [ ] Verify all links work (Terms, Privacy, Refund Policy pages TBD)

---

## After Launch (Week 2-4)

- **Week 2:** Add 3 real screenshots from working FlowPrep prototype
- **Week 3:** Record Revit-to-STL tutorial video, update FAQ link
- **Week 4:** Publish ANSYS validation study PDF, update all validation links

---

## SEO & Meta Tags

Implemented:
- Title: "FlowPrep AI — HVAC CFD Preprocessing in 15 Minutes"
- Meta description with HVAC-specific keywords
- Open Graph tags for social sharing
- Twitter Card tags
- Schema.org structured data (SoftwareApplication)

**Missing (optional):**
- `og-image.jpg` (1200×630px social media preview image)

---

## Performance Targets

- **First Contentful Paint:** <1.5s
- **Largest Contentful Paint:** <2.5s
- **Total File Size:** <500KB (HTML + Tailwind CDN)
- **Accessibility:** WCAG 2.1 AA compliant

---

## Support

For technical issues with the landing page, contact the fullstack team.
For content questions, contact the product/marketing team.

**Built by:** fullstack-dhh (Agent)
**Last Updated:** 2026-02-21
**Next Review:** After founder adds content (Week 2)
