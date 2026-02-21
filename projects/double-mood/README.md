# Double Mood

60-second emotional first aid with measurable results.

## Status

**Phase:** Day 1-3 Experiment (localStorage only)
**Start Date:** 2026-02-22 (Cycle 14)
**Target Ship:** Cycle 17 (3 days)

## Architecture

- **Frontend:** Vanilla HTML/CSS/JS (no framework)
- **Styling:** Tailwind CSS v4 (CDN for Day 1-3)
- **Hosting:** Cloudflare Pages
- **Data:** localStorage (Day 1-3), Cloudflare D1 (Day 4+)
- **Auth:** None (Day 1-3), Magic links (Day 4+)
- **Payment:** None (Day 1-3), Stripe (Day 6+)

## Day 1-3 Scope (Experiment)

- 4 mood weather icons (☀️⛅⛈️🌫️)
- Before intensity slider (1-10)
- 60-second breathing animation
- After intensity slider
- Before/after improvement display
- localStorage persistence

**Total:** ~300 lines of code, 12-18 hours build time.

## Success Criteria

**Day 3:**
- 10+ visitors
- 5+ completed breathing exercises
- 3+ returning users

**Fail condition:** <10 visitors = distribution problem, stop building.

## Build Milestones

- **Cycle 15 (Day 1):** HTML structure, mood selection, localStorage
- **Cycle 16 (Day 2):** Breathing animation, before/after scoring
- **Cycle 17 (Day 3):** Polish, deploy, founder LinkedIn post

## Development

```bash
# Local development (no build step)
python3 -m http.server 8000
# Open http://localhost:8000

# Deploy to Cloudflare Pages
wrangler pages deploy . --project-name=double-mood
```

## Documentation

- [Architecture Decision Record](/docs/cto/double-mood-architecture.md)
- [Product Spec](/docs/product/double-mood-mvp-spec.md)
- [CEO Decision](/docs/ceo/double-mood-decision.md)
- [Pre-Mortem Analysis](/docs/critic/double-mood-premortem.md)

## License

Proprietary — Auto Company
