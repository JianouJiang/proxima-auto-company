# Double Mood Phase 1 — Deployment Guide

**Target:** Cloudflare Pages (free tier, auto-deploy from git)
**Build time:** 5 minutes
**Live time:** Immediately after deploy
**Rollback:** 1 minute (revert commit + redeploy)

## Prerequisites

- Cloudflare account (create at https://dash.cloudflare.com)
- Wrangler CLI installed (`npm install -g wrangler`)
- GitHub repo connected to Cloudflare Pages (or manual upload)
- Domain (optional for Phase 1 — use `double-mood.pages.dev`)

## Option 1: Deploy via Wrangler CLI (Fastest)

```bash
# Navigate to project root
cd projects/double-mood

# Deploy public/ directory to Cloudflare Pages
wrangler pages deploy public --project-name=double-mood
```

**Output:**
```
Deploying to project: double-mood
Deployment successful! URL: https://double-mood.pages.dev
```

**Time:** ~30 seconds

## Option 2: Deploy via GitHub (Recommended for Auto Company)

1. **Push code to GitHub:**
   ```bash
   cd projects/double-mood
   git add public/index.html
   git commit -m "feat: Double Mood Phase 1 MVP — breathing exercise app"
   git push origin main
   ```

2. **Connect to Cloudflare Pages:**
   - Go to https://dash.cloudflare.com
   - Navigate to Pages
   - Click "Create a project"
   - Select GitHub repo: `proxima-auto-company`
   - Select branch: `main`
   - Build settings:
     - **Framework:** None
     - **Build directory:** `projects/double-mood/public`
     - **Build command:** (leave empty)
   - Deploy

3. **Auto-deploy on future commits:**
   - Any push to `main` auto-deploys to Cloudflare Pages
   - Previous deployments archived (easy rollback via dashboard)

**Time:** 2-3 minutes

## Verification Steps

### 1. Site Loads
```bash
curl -I https://double-mood.pages.dev
```
Expected: `HTTP/1.1 200 OK`

### 2. App Renders
Open https://double-mood.pages.dev in browser:
- [ ] Page loads in <1 second
- [ ] "How do you feel right now?" header visible
- [ ] 4 mood buttons visible (emojis + text)
- [ ] No errors in console (`F12` → Console tab)

### 3. Core Functionality
- [ ] Click a mood button → progresses to before slider
- [ ] Adjust slider → value updates
- [ ] Click "Start Breathing" → breathing animation runs
- [ ] Wait 30 seconds → advances to after slider
- [ ] Adjust after slider → shows improvement
- [ ] Click "Complete" → success screen shows
- [ ] Refresh page → success screen still there (localStorage works)

### 4. Bilingual UI
- [ ] Chinese text appears below English
- [ ] Both languages render without overlap
- [ ] Emoji renders correctly

### 5. Mobile (iPhone/Android)
- [ ] Open on phone
- [ ] Fits screen without scrolling
- [ ] Buttons touch-friendly
- [ ] Breathing animation smooth
- [ ] localStorage persists after refresh

## Performance Check

### Lighthouse Score (Optional but Good)
```bash
# Install lighthouse CLI
npm install -g lighthouse

# Run audit
lighthouse https://double-mood.pages.dev --view
```

**Target for Phase 1:**
- Accessibility: >90
- Performance: >85 (Tailwind CDN might impact, that's ok)
- Best Practices: >90

### Real-world 3G Test (DevTools)
1. Open DevTools (F12)
2. Network tab → Throttling dropdown → Slow 3G
3. Hard reload (Cmd+Shift+R)
4. Check load time <2 seconds ✓

## Rollback (If Needed)

### Via Wrangler
```bash
# List previous deployments
wrangler pages deployments list --project=double-mood

# Rollback to previous deployment
wrangler pages rollback --project=double-mood
```

### Via Cloudflare Dashboard
1. Go to https://dash.cloudflare.com → Pages → double-mood
2. Click "Deployments"
3. Find previous working deployment
4. Click "Rollback"

**Time:** <1 minute

## Custom Domain (Optional)

If using `double-mood.com` instead of `double-mood.pages.dev`:

1. **Point DNS to Cloudflare:**
   - Nameservers → Your domain registrar (GoDaddy, Namecheap, etc)
   - Set to Cloudflare nameservers

2. **Add to Cloudflare Pages:**
   - Pages → double-mood → Settings → Domain
   - Add custom domain: `double-mood.com`
   - SSL auto-generated (free)

3. **Verify:**
   - `curl -I https://double-mood.com`

**Note:** For Phase 1, skip custom domain. `double-mood.pages.dev` is fine and free forever.

## Environment Variables (Future)

For Phase 2+ (analytics, API keys):

```bash
# Set via Wrangler
wrangler pages secret add STRIPE_PUBLIC_KEY --project=double-mood

# In code:
const stripeKey = process.env.STRIPE_PUBLIC_KEY;
```

For Phase 1, no env vars needed (localStorage only).

## Monitoring

### Real-time Logs
```bash
wrangler pages project info --project=double-mood
```

### Cloudflare Analytics
- Dashboard → Pages → double-mood → Analytics
- Tracks: Requests, Data transferred, Cache status
- Free tier: 3-month history

### Custom Analytics (Phase 2)
For now, we only track localStorage. No server-side tracking for Phase 1.

## Disaster Recovery

**If deployment fails:**

1. **Error: "Cannot find public/ directory"**
   - Verify: `ls projects/double-mood/public/index.html`
   - Deploy: `wrangler pages deploy projects/double-mood/public --project-name=double-mood`

2. **Error: "Project not found"**
   - Create project first via Cloudflare Dashboard
   - Or use: `wrangler pages project create --name=double-mood`

3. **Site shows 404 or blank**
   - Check build directory setting (should be `projects/double-mood/public`)
   - Verify `index.html` exists in that directory
   - Redeploy

## Post-Deployment Actions

1. **Share link with founder** → https://double-mood.pages.dev
2. **Create QR code** → https://qr-server.com/api/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fdouble-mood.pages.dev
3. **Add to team doc** → Update `memories/consensus.md` with live link
4. **Tweet/LinkedIn post** → "Just shipped Double Mood — a 3-minute breathing exercise to test a hypothesis. Let's see if anyone uses it."

## Cost

- Cloudflare Pages: **FREE** (unlimited requests, 500 deployments/month)
- Custom domain: **$0-15/year** (optional, not needed Phase 1)
- Analytics: **FREE**

Total Phase 1 cost: **$0**

---

**Status:** Ready to deploy ✓
**Last Updated:** 2026-02-21
**Owner:** devops-hightower
