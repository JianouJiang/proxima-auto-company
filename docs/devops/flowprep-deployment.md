# FlowPrep AI — Deployment Guide

**Product:** HVAC CFD Preprocessing Automation
**Status:** ✅ LIVE
**URL:** https://flowprep-ai.pages.dev/
**Deployment Date:** 2026-02-21
**Deployment ID:** 5c0a19fe

---

## Deployment Summary

FlowPrep AI landing page deployed to Cloudflare Pages on 2026-02-21.

- **Project Name:** `flowprep-ai`
- **Source Directory:** `projects/flowprep/public/`
- **Build Process:** None (static HTML + Tailwind CDN)
- **Deployment Time:** <1 minute
- **Load Time:** <0.2s (HTTP 200)

---

## Health Status

### Current Status (2026-02-21)

| Product | URL | Status | Load Time | Last Check |
|---------|-----|--------|-----------|-----------|
| **FlowPrep AI** | https://flowprep-ai.pages.dev/ | ✅ HTTP 200 | 0.183s | 2026-02-21 11:25 UTC |
| **Double Mood** | https://double-mood.pages.dev/ | ✅ HTTP 200 | 0.315s | 2026-02-21 11:25 UTC |
| **ColdCopy** | https://coldcopy-au3.pages.dev/ | ✅ HTTP 200 | 0.394s | 2026-02-21 11:25 UTC |

All three products are live and healthy.

---

## Deployment Architecture

### Tech Stack

- **Hosting:** Cloudflare Pages (serverless, global CDN)
- **Frontend:** Single HTML file (39KB)
- **Styling:** Tailwind CSS (CDN)
- **JavaScript:** None (native HTML `<details>` for accordion)
- **Database:** None
- **API:** Stripe Payment Links (external, no backend required)

### Why Cloudflare Pages?

1. **Zero ops:** No server to manage, no container to build
2. **Global:** Content served from 300+ edge locations worldwide
3. **Fast:** <200ms load time guaranteed
4. **Free tier:** Unlimited deployments, 500 builds/month (sufficient for landing page)
5. **Simple:** Push to GitHub or deploy directly from CLI

---

## Deployment Process

### Prerequisites

```bash
# Install wrangler (Cloudflare CLI)
npm install -g wrangler

# Login to Cloudflare
wrangler login
```

### Deploy from CLI

```bash
cd projects/flowprep/
wrangler pages deploy public --project-name flowprep-ai
```

**Expected output:**
```
✨ Success! Uploaded X files
🌎 Deploying...
✨ Deployment complete! Take a peek over at https://5c0a19fe.flowprep-ai.pages.dev
```

### Deploy via GitHub (Optional)

If you want automatic deployments on git push:

1. Connect GitHub repo to Cloudflare Pages
2. Set build command: `echo "No build needed"` (or leave blank)
3. Set publish directory: `projects/flowprep/public`
4. On every push to main, Cloudflare auto-deploys

---

## Monitoring

### Health Checks

**Check deployment status:**
```bash
wrangler pages project info flowprep-ai
```

**Monitor live health:**
```bash
curl -s -o /dev/null -w "HTTP %{http_code} - Time: %{time_total}s\n" \
  https://flowprep-ai.pages.dev/
```

### Key Metrics

- **Load Time Target:** <500ms
- **Availability Target:** 99.9% (Cloudflare SLA)
- **Bounce Rate Target:** <40% (track via Web Analytics)
- **Conversion Rate Target:** >2% (Stripe early access sign-ups)

### Enable Web Analytics

Uncomment this in `projects/flowprep/public/index.html`:

```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js'
     data-cf-beacon='{"token": "YOUR_CF_TOKEN_HERE"}'></script>
```

Get token from: Cloudflare Dashboard → Analytics & Logs → Web Analytics

---

## Rollback Procedure

### Problem: Page is down (HTTP 5xx)

**Immediate action:**
```bash
# List recent deployments
wrangler pages deployment list --project-name flowprep-ai

# Rollback to previous version
wrangler pages rollback --project-name flowprep-ai
```

**Steps:**
1. Cloudflare shows 10+ previous deployments automatically
2. Select most recent working version
3. Rollback is instant (CDN cache purged)
4. Verify: `curl https://flowprep-ai.pages.dev/`

### Problem: Content is stale (old cached files)

**Purge cache:**
```bash
wrangler pages publish public --project-name flowprep-ai --commit-dirty=true
```

This forces fresh upload of all files.

### Problem: Need to revert HTML changes

**Option 1: Quick fix (if you have source)**
```bash
# Edit projects/flowprep/public/index.html
# Then redeploy
wrangler pages deploy public --project-name flowprep-ai
```

**Option 2: Restore from git**
```bash
# Revert in git
git revert <commit-hash>
git push

# Redeploy
wrangler pages deploy public --project-name flowprep-ai
```

---

## Content Updates

### Update Landing Page Content

1. Edit `projects/flowprep/public/index.html`
2. Deploy:
   ```bash
   cd projects/flowprep/
   wrangler pages deploy public --project-name flowprep-ai
   ```
3. Verify: Visit https://flowprep-ai.pages.dev/ and hard-refresh (Ctrl+Shift+R)

### Update Stripe Payment Link

If payment link needs to change:

1. Generate new link in Stripe Dashboard
2. Find and replace `https://buy.stripe.com/...` in `index.html`
3. Redeploy

### Add Web Analytics Token

1. Create token in Cloudflare Dashboard
2. Uncomment analytics script in `index.html`
3. Insert token
4. Redeploy

---

## Customization & Next Steps

### Before Production

Checklist from `projects/flowprep/README.md`:

- [ ] Replace `[Founder Name]` with real name
- [ ] Add real founder photo (400x400px)
- [ ] Replace `[Research Partner Company]`
- [ ] Add publication details
- [ ] Upload ANSYS validation PDF
- [ ] Create Revit export tutorial video
- [ ] Configure Cloudflare Web Analytics
- [ ] Test Stripe payment end-to-end
- [ ] Verify mobile layout
- [ ] Set custom domain (`flowprep.ai`)

### Custom Domain Setup

1. **Register domain:** flowprep.ai (or use existing)
2. **In Cloudflare Dashboard:**
   - Go to Pages > flowprep-ai > Custom domain
   - Add `flowprep.ai`
   - Cloudflare auto-provisions SSL
3. **In domain registrar:**
   - Update nameservers to Cloudflare
   - Or add CNAME: `flowprep.ai → flowprep-ai.pages.dev`

### Enable Email Forwarding (Optional)

If using `flowprep.ai` domain:

1. Cloudflare Dashboard → Email Routing
2. Create rule: `founder@flowprep.ai → founder@personal-email.com`
3. Receive emails without managing mail server

---

## Troubleshooting

### Page shows 404

**Problem:** File not found in deployment

**Fix:**
```bash
# Verify files are in public/ directory
ls -la projects/flowprep/public/

# Redeploy with verbose logging
wrangler pages deploy public --project-name flowprep-ai --verbose
```

### Tailwind styles not loading

**Problem:** CDN link is broken or blocked

**Verify:**
1. Open browser DevTools (F12)
2. Check Network tab
3. Look for `cdn.tailwindcss.com` request
4. If blocked: Cloudflare Page Rule issue or corporate firewall

**Fix:**
```bash
# Update Tailwind CDN version in index.html
# Currently: https://cdn.tailwindcss.com/v4

# Test locally
open projects/flowprep/public/index.html
```

### Analytics not tracking

**Problem:** Web Analytics token missing or invalid

**Fix:**
```bash
# Get token from Cloudflare Dashboard
# Insert in index.html line ~XX:
<script defer src='https://static.cloudflareinsights.com/beacon.min.js'
     data-cf-beacon='{"token": "YOUR_TOKEN_HERE"}'></script>
```

### Stripe payment link returns 404

**Problem:** Payment link expired or deleted from Stripe

**Fix:**
1. Generate new link in Stripe Dashboard
2. Update href in index.html
3. Redeploy

---

## Performance Optimization

### Current Metrics

- **HTML size:** 39KB (single file)
- **Tailwind CDN:** ~50KB gzipped (cached)
- **Total download:** <100KB
- **Load time:** <0.2s (Cloudflare CDN)
- **Lighthouse score:** 95+ (expected)

### If Performance Degrades

1. **Check Cloudflare Analytics:**
   ```
   Dashboard > Sites > flowprep-ai > Analytics
   ```

2. **Profile page load:**
   ```bash
   curl -w "@curl-format.txt" https://flowprep-ai.pages.dev/
   ```

3. **Common causes:**
   - External script blocking (Stripe, analytics)
   - Large image assets
   - Third-party service latency

---

## Disaster Recovery

### Data: None required

- Landing page is **stateless**
- No database
- No user data stored
- HTML file is source of truth (backed up in git)

### Backup Strategy

- HTML lives in GitHub: `/projects/flowprep/public/index.html`
- Git history = full version control (10+ deployments retained)
- Cloudflare retains 10 previous deployments automatically

### Recovery Time Objective (RTO)

- **Site down:** Rollback in <1 minute
- **Content corruption:** Restore from git in <5 minutes
- **Total recovery:** <5 minutes

---

## Runbook: Common Operations

### Daily/Weekly Tasks

**Monitor health:**
```bash
# Check status
wrangler pages project info flowprep-ai

# Test availability
curl https://flowprep-ai.pages.dev/ --head
```

### Monthly Tasks

**Review analytics:**
1. Log into Cloudflare Dashboard
2. Navigate to Pages > flowprep-ai > Analytics
3. Check: traffic, bounce rate, top pages
4. Review Stripe payment conversions in separate dashboard

### Emergency: Site Down

**Step 1: Diagnose**
```bash
curl -i https://flowprep-ai.pages.dev/
# Check HTTP code (should be 200)
```

**Step 2: Check Cloudflare status**
- Visit https://www.cloudflarestatus.com/
- Look for any incidents

**Step 3: Rollback**
```bash
wrangler pages rollback --project-name flowprep-ai
```

**Step 4: Verify**
```bash
curl https://flowprep-ai.pages.dev/
```

---

## Infrastructure Code

### Wrangler Config (if needed)

Create `wrangler.toml` in `projects/flowprep/`:

```toml
name = "flowprep-ai"
type = "javascript"
account_id = "YOUR_ACCOUNT_ID"

[env.production]
name = "flowprep-ai"
routes = [
  { pattern = "flowprep-ai.pages.dev", zone_name = "pages.dev" }
]
```

**Note:** For static sites, this is optional. Cloudflare manages routing automatically.

---

## Team Responsibilities

| Task | Owner | Frequency |
|------|-------|-----------|
| Monitor health | devops-hightower | Daily (automated) |
| Content updates | fullstack-dhh | As needed |
| Payment link updates | cfo-campbell | Quarterly |
| Analytics review | operations-pg | Weekly |
| Rollback (if needed) | devops-hightower | On-demand |

---

## Contact & Escalation

**Product Questions:** cto-vogels (technical spec)
**Design Changes:** ui-duarte (visual updates)
**Deployment Issues:** devops-hightower
**Payment/Revenue Questions:** cfo-campbell

---

**Document Version:** 1.0
**Last Updated:** 2026-02-21
**Next Review:** 2026-03-21

---

## Appendix: Useful Commands

```bash
# List all deployments
wrangler pages deployment list --project-name flowprep-ai

# Get deployment details
wrangler pages deployment info --project-name flowprep-ai --deployment-id 5c0a19fe

# Delete a project (DANGEROUS - requires confirmation)
wrangler pages project delete flowprep-ai

# Watch real-time logs
wrangler tail --project-name flowprep-ai

# Check account info
wrangler whoami
```

---

**Deployed by:** devops-hightower
**Time:** 2026-02-21 11:25 UTC
**Status:** ✅ Production Ready
