# FlowPrep AI Landing Page — Interaction Design

**Designer:** interaction-cooper
**Date:** 2026-02-21
**Product:** FlowPrep AI — Automated CFD Preprocessing for HVAC Engineers
**Deploy Target:** Cloudflare Pages, Single HTML File

---

## Primary Persona

**Name:** David Chen
**Role:** Senior HVAC Engineer at mid-size MEP consultancy
**Age:** 32-45
**Experience:** 8-15 years in building services design

**Goals:**
- **End Goal:** Deliver CFD analysis reports to clients faster without sacrificing quality
- **Experience Goal:** Spend less time on tedious preprocessing, more time interpreting results and design optimization
- **Life Goal:** Be recognized as a technical expert who delivers projects on time

**Context:**
- Runs 3-5 CFD simulations per week (data centers, cleanrooms, laboratories)
- Uses OpenFOAM/ANSYS Fluent — knows the pain of manual meshing
- Skeptical of "AI magic" — needs to see the technical approach
- Budget authority for tools under £100/month
- Time-constrained — will only read if the value proposition is immediate and credible

**Mental Model:**
- "I know CFD preprocessing is painful, but I don't trust automation I don't understand"
- "Show me it works for MY type of geometry (HVAC, not aerospace)"
- "I'll pay if it saves me even 5 hours per month"

**Friction Points:**
- Won't sign up without understanding the technical approach
- Won't pay without seeing proof it works for HVAC geometries
- Won't trust generic claims — needs domain-specific credibility

---

## User Journey Map

### Discovery → Evaluation → Conversion

| Stage | User Goal | User Questions | Design Response |
|-------|-----------|----------------|-----------------|
| **Entry (Hero)** | Understand value in 5 seconds | "What is this? Is this for me?" | Hero headline mentions HVAC + time savings + role (engineer, not manager) |
| **Interest (Problem)** | Validate the pain | "Do they understand my problem?" | Before/after workflow comparison — show the exact steps David wastes time on |
| **Evaluation (How)** | Understand the approach | "Is this real or snake oil?" | Technical "How it Works" with mesh algorithm details, boundary condition logic |
| **Credibility (Trust)** | Assess creator competence | "Who built this? Can I trust them?" | PhD credential + sample output visualization + CFD-specific terminology (Reynolds number, y+ values, etc.) |
| **Trial (Demo)** | See it working | "Does it work for MY geometry?" | Interactive demo or embedded visualization of HVAC-specific case (server room, lab, cleanroom) |
| **Decision (Pricing)** | Evaluate ROI | "Is this worth £39/month?" | ROI math: "4 hours saved × £50/hour = £200/month value for £39" |
| **Action (Signup)** | Commit with low friction | "Can I start immediately?" | Direct Stripe payment link → immediate access (no multi-step funnel) |

---

## Content Structure & User Flow

### Navigation Pattern: **Single-Scroll Linear Narrative**

No traditional navigation menu. User scrolls through a story:
Hero → Problem → Solution → How It Works → Proof → Pricing → CTA

Rationale (Cooper principle):
- David's goal is "evaluate quickly" — navigation adds decisions, slows evaluation
- Linear scroll = one story, one flow, optimized for Primary Persona
- Anchor links waste attention for a page this focused

---

## Section-by-Section Design

### 1. Hero Section (Above-the-Fold, ~100vh)

**User Goal:** Understand value in 5 seconds
**Design Pattern:** Value proposition + visual proof + instant CTA

**Content Blocks:**

```
┌─────────────────────────────────────────────┐
│  [FlowPrep AI Logo]                         │
│                                             │
│  CFD Preprocessing for HVAC Engineers       │
│  From 8 Hours to 15 Minutes                │
│                                             │
│  Automated meshing + boundary conditions    │
│  for OpenFOAM & ANSYS Fluent               │
│                                             │
│  [Visual: Split-screen wireframe vs mesh]  │
│  Left: CAD geometry (gray wireframe)       │
│  Right: Colored CFD mesh (blue/green hex)  │
│                                             │
│  [CTA Button: "Start Free Trial — £39/mo"] │
│  ↓ Scroll to see how it works               │
└─────────────────────────────────────────────┘
```

**Interaction Details:**
- CTA button = primary action (Stripe payment link)
- No email gate here — trust is not yet established
- Visual must show HVAC geometry (ductwork, room, grilles) NOT aerospace
- Scroll hint (animated arrow or text) to guide David down

**Copy Tone:**
- Direct, no fluff: "8 Hours to 15 Minutes" (quantified)
- Role-specific: "HVAC Engineers" (not generic "engineers")
- Technical credibility: Mention OpenFOAM/Fluent by name

---

### 2. Problem Section (~60vh)

**User Goal:** Validate the pain
**Design Pattern:** Before/After Workflow Comparison

**Content Blocks:**

```
┌─────────────────────────────────────────────┐
│  The Manual CFD Preprocessing Nightmare     │
│                                             │
│  [Two-Column Comparison Table]              │
│                                             │
│  Manual Workflow (8-12 hours)              │
│  ├─ 1. Clean CAD geometry (2h)             │
│  ├─ 2. Generate volume mesh (3h)           │
│  ├─ 3. Set boundary conditions (2h)        │
│  ├─ 4. Check mesh quality (1h)             │
│  └─ 5. Debug mesh errors (2h)              │
│                                             │
│  FlowPrep Workflow (15 minutes)            │
│  ├─ 1. Upload STEP file                    │
│  ├─ 2. AI detects surfaces (inlets/walls)  │
│  ├─ 3. Auto-mesh with quality checks       │
│  └─ 4. Export to OpenFOAM/Fluent           │
│                                             │
│  ↓ Sound familiar? Here's how we do it     │
└─────────────────────────────────────────────┘
```

**Interaction Details:**
- Table rows appear sequentially on scroll (subtle animation)
- Each row has icon (clock for manual, lightning for FlowPrep)
- No interaction required — pure information

**Copy Tone:**
- Empathetic: "Nightmare" — acknowledges David's pain
- Specific: "Clean CAD geometry" (not "prepare files") — shows domain knowledge
- Quantified: "2h" per step — realistic numbers build trust

---

### 3. How It Works (Technical Credibility) (~120vh)

**User Goal:** Understand the technical approach
**Design Pattern:** 4-Step Process with Technical Details

**Content Blocks:**

```
┌─────────────────────────────────────────────┐
│  How FlowPrep Works (Not Magic, Just ML)   │
│                                             │
│  [Step 1: Geometry Analysis]               │
│  ┌─────────────────────────────────────┐   │
│  │ [Visual: CAD file → surface detect] │   │
│  │ • Graph neural network classifies    │   │
│  │   surfaces (inlet/outlet/wall)       │   │
│  │ • Trained on 5,000+ HVAC geometries  │   │
│  │ • Detects grilles, diffusers, ducts  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [Step 2: Intelligent Meshing]             │
│  ┌─────────────────────────────────────┐   │
│  │ [Visual: Mesh refinement zones]     │   │
│  │ • Adaptive sizing near boundaries    │   │
│  │ • y+ targeting for turbulence models │   │
│  │ • Quality metrics (skewness < 0.85)  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [Step 3: Boundary Condition Assignment]   │
│  ┌─────────────────────────────────────┐   │
│  │ [Visual: Colored surfaces + labels] │   │
│  │ • Auto-assign physics (velocity/     │   │
│  │   pressure based on surface type)    │   │
│  │ • HVAC-specific templates (VAV, CAV) │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [Step 4: Export & Validate]               │
│  ┌─────────────────────────────────────┐   │
│  │ [Visual: Export dialog]             │   │
│  │ • OpenFOAM dictionary files          │   │
│  │ • ANSYS Fluent .msh + .jou           │   │
│  │ • Mesh quality report (PDF)          │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Interaction Details:**
- Each step = collapsible accordion OR scroll-triggered reveal
- Visuals = annotated screenshots or simplified diagrams (NOT stock photos)
- Technical terms (y+, skewness) hyperlink to tooltips (not external pages)

**Copy Tone:**
- Transparent: "Not Magic, Just ML" — demystify AI
- Technical: "y+ targeting", "skewness < 0.85" — speak David's language
- Specific: "5,000+ HVAC geometries" — domain credibility

**Cooper Principle Applied:**
- David's goal: "Understand if this works for MY domain"
- Most automation tools show aerospace examples → FlowPrep shows HVAC-specific training data
- Don't hide the implementation model — engineers distrust black boxes

---

### 4. Proof Section (Social Proof + Credibility) (~80vh)

**User Goal:** Assess creator competence
**Design Pattern:** Founder Story + Sample Output

**Content Blocks:**

```
┌─────────────────────────────────────────────┐
│  Built by a CFD Engineer Who Felt Your Pain│
│                                             │
│  [Founder Photo]                            │
│  Dr. [Name], PhD in Machine Learning + CFD  │
│  Former: [Consultancy/University]           │
│                                             │
│  "I spent 6 years running CFD for HVAC     │
│   projects. I built FlowPrep because I was  │
│   tired of spending more time meshing than  │
│   analyzing results."                       │
│                                             │
│  [Sample Output Visualization]              │
│  ┌─────────────────────────────────────┐   │
│  │ Interactive 3D mesh viewer           │   │
│  │ (WebGL-based, rotate/zoom)           │   │
│  │ Example: Server room with hot aisle  │   │
│  │ → Shows refined mesh near servers    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Mesh Quality Metrics:                     │
│  • Min orthogonality: 0.92                 │
│  • Max skewness: 0.78                      │
│  • Cell count: 1.2M (optimal for desktop)  │
└─────────────────────────────────────────────┘
```

**Interaction Details:**
- 3D viewer = embedded (THREE.js or Babylon.js) OR static annotated image if file size matters
- Mesh metrics = actual numbers (not "good" or "excellent")
- Founder photo = professional but approachable (NOT stock photo)

**Copy Tone:**
- Personal: First-person quote from founder
- Relatable: "tired of spending more time meshing" — echoes David's pain
- Credible: PhD + former employer name (if recognizable in industry)

**Cooper Principle Applied:**
- David's Experience Goal: "Spend less time on tedious work"
- Founder story creates empathy: "This person has been in my shoes"
- Sample output proves capability: "This mesh meets MY quality standards"

---

### 5. Pricing Section (ROI-Focused) (~60vh)

**User Goal:** Evaluate ROI
**Design Pattern:** Single Plan + ROI Calculator

**Content Blocks:**

```
┌─────────────────────────────────────────────┐
│  Pricing That Pays for Itself               │
│                                             │
│  [Pricing Card]                             │
│  ┌─────────────────────────────────────┐   │
│  │  Early Access                        │   │
│  │  £39/month (or $79/month)           │   │
│  │                                      │   │
│  │  ✓ Unlimited preprocessing jobs      │   │
│  │  ✓ OpenFOAM + ANSYS Fluent export   │   │
│  │  ✓ Priority email support           │   │
│  │  ✓ Early access to new features     │   │
│  │                                      │   │
│  │  [CTA: Start Now — Stripe Payment]  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ROI Calculation:                          │
│  ┌─────────────────────────────────────┐   │
│  │ You run 4 CFD jobs/month             │   │
│  │ FlowPrep saves 6 hours/job           │   │
│  │ = 24 hours saved/month               │   │
│  │                                      │   │
│  │ Your time = £50/hour (conservative) │   │
│  │ Value = £1,200/month                │   │
│  │ Cost = £39/month                    │   │
│  │                                      │   │
│  │ ROI = 30× 🚀                         │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Cancel anytime. No long-term contract.    │
└─────────────────────────────────────────────┘
```

**Interaction Details:**
- CTA button = Stripe payment link (https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05)
- ROI calculator = static OR interactive (slider for "jobs per month")
- Single plan (no choice paralysis)

**Copy Tone:**
- Value-focused: "Pays for Itself" — not "Affordable"
- Quantified: "30× ROI" — speak David's business language
- Risk-reduction: "Cancel anytime" — removes commitment friction

**Cooper Principle Applied:**
- David's End Goal: "Deliver projects faster"
- ROI math = justifies expense to himself AND manager
- No multi-tier pricing → reduces decision fatigue (Primary Persona optimization)

---

### 6. Final CTA Section (Conversion) (~40vh)

**User Goal:** Commit with low friction
**Design Pattern:** Repeated CTA + FAQ Preemption

**Content Blocks:**

```
┌─────────────────────────────────────────────┐
│  Ready to Get 6 Hours Back This Week?      │
│                                             │
│  [CTA Button: Start Now — £39/month]       │
│  ↓ Immediate access after payment           │
│                                             │
│  Quick Answers:                            │
│  Q: What file formats do you support?      │
│  A: STEP, IGES, STL (more coming soon)     │
│                                             │
│  Q: Can I export to other solvers?         │
│  A: OpenFOAM and Fluent now, SU2/CFX soon  │
│                                             │
│  Q: What if the mesh quality isn't good?   │
│  A: Email us — we'll manually review       │
│                                             │
│  Q: Do you store my geometry files?        │
│  A: No. Processed locally, deleted after   │
│                                             │
│  [Footer]                                   │
│  FlowPrep AI © 2026                        │
│  Contact: hello@flowprep.ai                │
│  Terms | Privacy                            │
└─────────────────────────────────────────────┘
```

**Interaction Details:**
- CTA button = same Stripe link (consistency)
- FAQ = expandable OR static (static better for scroll flow)
- No email signup form (reduces friction — payment = signup)

**Copy Tone:**
- Action-oriented: "Get 6 Hours Back" (benefit, not feature)
- Reassuring: FAQ preempts objections
- Transparent: "Processed locally, deleted after" (privacy concern for IP-sensitive geometries)

**Cooper Principle Applied:**
- David's friction: "What if it doesn't work for my files?"
- FAQ removes blockers BEFORE they become objections
- No multi-step signup → payment link = immediate access (respect David's time)

---

## Interaction Patterns & States

### Scroll-Triggered Animations
- Hero: Fade in on load
- Problem section: Table rows appear sequentially
- How It Works: Each step fades in as user scrolls past
- Proof section: 3D viewer loads when in viewport (performance)

**Rationale:** Animations guide attention, but must be subtle (engineers distrust flashy design)

### CTA Button States
- **Default:** "Start Now — £39/month"
- **Hover:** Subtle scale (1.02×) + shadow depth increase
- **Click:** Redirects to Stripe (https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05)
- **Loading:** "Redirecting to payment..." (if Stripe takes >500ms)

**Rationale:** No modal, no multi-step — direct payment link respects David's time

### 3D Mesh Viewer (Proof Section)
- **Interaction:** Click-drag to rotate, scroll to zoom
- **Default View:** Isometric angle showing mesh refinement near key surfaces
- **Annotations:** Labels pointing to "Refined boundary layer", "Hex core", "Surface mesh"

**Rationale:** Interactive > static image (builds confidence in quality)

### Responsive Breakpoints
- **Desktop (>1024px):** Two-column layout for Before/After, side-by-side How It Works steps
- **Tablet (768-1024px):** Single column, larger touch targets for CTA
- **Mobile (<768px):** Stack all content, disable 3D viewer (replace with annotated image)

**Rationale:** Primary Persona uses desktop at work, but may discover via mobile

---

## Content Hierarchy (F-Pattern Optimized)

David scans in an F-pattern (Nielsen research). Critical info must hit the F hotspots:

```
[HERO HEADLINE] ← Top horizontal bar (F-top)
CFD Preprocessing for HVAC Engineers
From 8 Hours to 15 Minutes

[PROBLEM SECTION] ← Left vertical bar (F-stem)
Manual Workflow (8-12 hours)
├─ Clean CAD geometry (2h)
├─ Generate volume mesh (3h)
...

[HOW IT WORKS] ← Second horizontal bar (F-middle)
Step 1: Geometry Analysis
Step 2: Intelligent Meshing
...

[CTA BUTTON] ← Bottom hotspot
Start Now — £39/month
```

**Design Implication:**
- Headlines left-aligned (not centered)
- Key numbers in left column of tables
- CTA buttons left-aligned OR center (if full-width section)

---

## Copywriting Principles (Applied)

### 1. Specificity Over Generality
- ❌ "Save time on CFD"
- ✅ "From 8 hours to 15 minutes"

### 2. Role-Specific Language
- ❌ "For engineers"
- ✅ "For HVAC engineers at MEP consultancies"

### 3. Technical Credibility Markers
- Mention solver names (OpenFOAM, Fluent)
- Use domain terms (y+, skewness, boundary layer)
- Show actual metrics (not "high quality")

### 4. Benefit-Oriented Headlines
- ❌ "Automated Meshing"
- ✅ "Get 6 Hours Back This Week"

### 5. Friction Reduction
- ❌ "Sign up for free trial" → "Enter credit card" → "Confirm email" → ...
- ✅ "Start Now" → Stripe payment → Immediate access

---

## Error States & Edge Cases

### Stripe Payment Link Fails
- **Scenario:** User clicks CTA, Stripe is unreachable
- **Fallback:** Show inline message: "Payment system temporarily down. Email hello@flowprep.ai to start manually."

### 3D Viewer Won't Load (WebGL Issue)
- **Scenario:** Old browser, no WebGL support
- **Fallback:** Display static annotated image with message: "Interactive viewer requires a modern browser. Here's a preview:"

### Mobile User Tries to Signup
- **Scenario:** David browses on phone, wants to pay
- **Behavior:** Stripe payment link works on mobile → David can signup, but remind: "Desktop recommended for using FlowPrep"

---

## A/B Test Hypotheses (For Future)

After launch, test these variations:

| Element | Variation A (Default) | Variation B | Hypothesis |
|---------|----------------------|-------------|------------|
| Hero CTA | "Start Now — £39/month" | "See Demo First" | Engineers want proof before payment |
| Pricing Display | £39/month | £39/month (first month) then £59 | Lower entry price increases conversion |
| How It Works | 4-step linear | Interactive demo | Interactive engagement increases trust |
| Founder Story | Text + photo | Video (30sec) | Video builds more credibility |

---

## Success Metrics (Defined)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to First Scroll** | <3 seconds | Analytics: Scroll depth event |
| **Scroll Completion Rate** | >60% reach pricing | Analytics: Section visibility |
| **CTA Click Rate** | >8% of visitors | Analytics: Button click event |
| **Payment Completion** | >40% of CTA clicks | Stripe: Payment success rate |
| **Bounce Rate** | <50% | Analytics: Single-page sessions |

---

## Technical Implementation Notes

### Single HTML File Structure
```html
<!DOCTYPE html>
<html>
<head>
  <title>FlowPrep AI - CFD Preprocessing for HVAC Engineers</title>
  <style>
    /* Inline CSS - Tailwind v4 */
  </style>
</head>
<body>
  <!-- Hero -->
  <!-- Problem -->
  <!-- How It Works -->
  <!-- Proof -->
  <!-- Pricing -->
  <!-- Final CTA -->

  <script>
    // Scroll-triggered animations
    // 3D viewer (THREE.js CDN)
    // Analytics events
  </script>
</body>
</html>
```

### External Dependencies (CDN)
- THREE.js (for 3D mesh viewer) — fallback to static image if CDN fails
- Google Fonts (Geist Sans) — fallback to system fonts
- Analytics (Plausible or Simple Analytics) — privacy-friendly, no GDPR banner needed

### Performance Targets
- **First Contentful Paint:** <1.5s
- **Largest Contentful Paint:** <2.5s
- **Total File Size:** <500KB (excluding 3D model, which lazy-loads)

---

## Deployment Checklist

Before deploying to Cloudflare Pages:

- [ ] Test Stripe payment link (test mode first, then live mode)
- [ ] Verify 3D viewer works in Chrome/Firefox/Safari
- [ ] Test mobile responsive layout (iPhone SE, iPad)
- [ ] Check accessibility (keyboard navigation, screen reader)
- [ ] Validate HTML (W3C validator)
- [ ] Test loading speed (PageSpeed Insights)
- [ ] Set up analytics (Plausible event tracking)
- [ ] Configure Cloudflare Page Rules (cache, redirects)
- [ ] Add custom domain (flowprep.ai or flowprep-ai.pages.dev)
- [ ] Test payment flow end-to-end (test card, then real card)

---

## Next Actions for Implementation

1. **UI Designer (ui-duarte):** Translate this UX structure into visual design (color scheme, typography, spacing)
2. **Fullstack Dev (fullstack-dhh):** Build single HTML file with inline CSS/JS
3. **QA (qa-bach):** Test all interaction states, payment flow, edge cases
4. **DevOps (devops-hightower):** Deploy to Cloudflare Pages, configure analytics

---

## Cooper's Principles Applied — Summary

| Principle | Application in FlowPrep Landing Page |
|-----------|-------------------------------------|
| **Goal-Directed Design** | David's goal = "Evaluate tool quickly" → Linear scroll, no navigation distractions |
| **Primary Persona Optimization** | Single pricing plan (no choice paralysis), HVAC-specific examples (no generic CFD) |
| **Hide Implementation Model** | Show "How It Works" in David's terms (mesh quality, y+), not in ML jargon (tensors, epochs) |
| **Respect User's Time** | Direct payment link (no multi-step signup), ROI calculator (justifies decision fast) |
| **Interaction Etiquette** | Scroll-triggered animations (guide attention gently), FAQ preempts objections (don't make David search) |
| **Elastic User = Bad** | NOT designing for "anyone interested in CFD" — ONLY for David (HVAC engineer, MEP consultancy, 8+ years exp) |

---

**Document Status:** Ready for UI design handoff
**Last Updated:** 2026-02-21
**Next Owner:** ui-duarte (visual design) → fullstack-dhh (implementation)
