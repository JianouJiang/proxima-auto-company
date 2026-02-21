# ConnectPath Deployment Guide

**For devops-hightower: Complete deployment checklist**

## Pre-Deployment Checklist

- [ ] GitHub Personal Access Token created
- [ ] Cloudflare account ready (free tier OK)
- [ ] Gumroad product listing created
- [ ] Domain name decided (if custom domain)

## Step-by-Step Deployment

### 1. Create Cloudflare KV Namespace

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/connectpath

# Login to Cloudflare (if not already)
wrangler login

# Create KV namespace for production
wrangler kv:namespace create "CONNECTPATH_KV"

# Note the output: "id = YOUR_KV_NAMESPACE_ID"
# Update wrangler.toml with this ID
```

### 2. Set Environment Variables

#### GitHub Token Setup
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `public_repo`
   - ✅ `read:user`
4. Generate token → Copy it (starts with `ghp_`)

#### Add to Cloudflare
```bash
# Add GitHub token as secret
wrangler secret put GITHUB_TOKEN
# Paste your token when prompted
```

### 3. Deploy to Cloudflare Pages

#### Option A: GitHub Integration (Recommended)

1. **Push to GitHub**:
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company
git add projects/connectpath
git commit -m "Add ConnectPath MVP"
git push origin main
```

2. **Connect to Cloudflare Pages**:
   - Go to Cloudflare Dashboard → Pages
   - Click "Create a project"
   - Choose "Connect to Git"
   - Select your GitHub repo: `proxima-auto-company`
   - **Build settings**:
     - Framework preset: None
     - Build command: (leave empty)
     - Build output directory: `/`
     - Root directory: `projects/connectpath`
   - Click "Save and Deploy"

3. **Add Environment Variables** (in Pages settings):
   - Go to Settings → Environment variables
   - Add `GITHUB_TOKEN` → paste your token
   - Save

4. **Bind KV Namespace**:
   - Go to Settings → Functions
   - Scroll to "KV namespace bindings"
   - Add binding:
     - Variable name: `CONNECTPATH_KV`
     - KV namespace: Select the one you created
   - Save

5. **Redeploy** (to apply KV binding):
   - Go to Deployments → Click latest deployment → Retry deployment

#### Option B: Direct Upload (Faster for MVP)

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/connectpath

# Install dependencies
npm install

# Deploy
wrangler pages deploy . --project-name=connectpath --branch=main
```

**After first deploy, add secrets**:
```bash
# Navigate to your project in Cloudflare Dashboard
# Settings → Environment variables → Add variable
# GITHUB_TOKEN = ghp_your_token_here
```

**Bind KV namespace manually** (via Dashboard):
- Settings → Functions → KV namespace bindings
- Add: `CONNECTPATH_KV` → select your namespace

### 4. Verify Deployment

Visit your deployed URL (e.g., `https://connectpath.pages.dev`)

**Test with real GitHub users**:
1. Person A: `torvalds` (Linus Torvalds)
2. Person B: `tj` (TJ Holowaychuk)

Expected result: Should find a path (they're both highly connected in OSS community)

**Test rate limiting**:
1. Open in incognito window
2. Do 3 searches
3. 4th search should show paywall

### 5. Custom Domain (Optional)

If you have a custom domain:

1. Go to Cloudflare Pages → Your project → Custom domains
2. Click "Set up a custom domain"
3. Enter: `connectpath.yourdomain.com`
4. Cloudflare auto-configures DNS
5. Wait for SSL certificate (< 5 min)
6. Visit your custom domain

### 6. Gumroad Integration

1. **Create Gumroad product**:
   - Go to https://gumroad.com/products/new
   - Copy content from `gumroad-listing.txt`
   - Price: $9.99/month (recurring)
   - Content: "After purchase, you'll receive an access code via email"
   - Publish

2. **Update frontend link**:
   - Edit `index.html` line 374
   - Replace `https://jiangyingjuner.gumroad.com/l/connectpath-unlimited`
   - With your actual Gumroad product URL

3. **Deploy changes**:
```bash
git add index.html
git commit -m "Update Gumroad link"
git push origin main
# Cloudflare auto-deploys
```

### 7. Setup Gumroad Webhook (Future: V1.1)

For automatic access code delivery:

1. Gumroad → Settings → Advanced → Webhooks
2. Add webhook URL: `https://connectpath.pages.dev/api/gumroad-webhook`
3. Select events: `sale`, `refund`
4. Create webhook function: `functions/api/gumroad-webhook.js`
   - Receives sale notification
   - Generates unique access code
   - Stores in KV: `access_code:CODE` → `{email, expiry, plan}`
   - Sends email with code (via Resend/SendGrid)

**For MVP**: Manual delivery OK. After purchase, founder manually generates code and emails customer.

## Post-Deployment

### Monitoring

**Check these daily (first week)**:

1. **Error rate**:
```bash
# View Workers logs
wrangler tail --project-name=connectpath
```

2. **Rate limiting stats**:
```bash
# List KV keys to see how many IPs hit rate limit
wrangler kv:key list --namespace-id=YOUR_KV_NAMESPACE_ID
```

3. **GitHub API usage**:
   - Check headers in responses: `X-RateLimit-Remaining`
   - Should stay above 4,000/hr if traffic is low

### Analytics Setup (Optional)

Add Cloudflare Web Analytics (free):

1. Dashboard → Web Analytics → Add a site
2. Get snippet code
3. Add to `index.html` before `</head>`
4. Track:
   - Page views
   - Searches initiated (via custom events)
   - Paywall shown

### First Week Checklist

- [ ] Deploy successful (site loads)
- [ ] Test search works (real GitHub users)
- [ ] Rate limiting works (3 searches then paywall)
- [ ] Mobile responsive (test on phone)
- [ ] Gumroad link works
- [ ] Error handling works (try fake usernames)
- [ ] Bilingual toggle works (EN ↔ 中文)

### If Something Breaks

**Frontend not loading**:
- Check Cloudflare Pages → Deployments → View build logs
- Common issue: Root directory wrong (should be `projects/connectpath`)

**API returns 500 errors**:
- Check Workers logs: `wrangler tail`
- Common issues:
  - `GITHUB_TOKEN` not set → Add in environment variables
  - `CONNECTPATH_KV` not bound → Add in Functions settings
  - GitHub API rate limit hit → Wait 1 hour or add token

**Rate limiting not working**:
- Check KV namespace is bound correctly
- Check browser console for errors
- Common issue: KV read/write fails silently → check binding name matches code

**No path found for known connections**:
- Expected behavior — MVP only searches GitHub
- Most people don't follow each other on GitHub
- Solution: Add Twitter/Crunchbase in V1.1

## Rollback Plan

If deployment breaks:

```bash
# Rollback to previous deployment
# Go to Cloudflare Dashboard → Pages → Deployments
# Click on previous working deployment → "Rollback to this deployment"
```

Or:

```bash
# Redeploy previous git commit
git revert HEAD
git push origin main
# Cloudflare auto-deploys the revert
```

## Cost Estimate

**Cloudflare Free Tier**:
- Pages: 500 builds/month (we use ~10/month)
- Workers: 100K requests/day (MVP uses ~100-500/day)
- KV: 100K reads/day, 1K writes/day (MVP uses ~10 writes, ~50 reads/day)
- **Total cost**: $0/month (until we hit 1K+ users)

**Scaling costs** (if we hit 10K searches/day):
- Cloudflare Workers Paid: $5/month + $0.50/million requests
- KV storage: $0.50/GB-month (negligible for rate limit data)
- **Estimated**: ~$10-20/month at 10K searches/day

**GitHub API**:
- Free with token: 5,000 requests/hour
- If we hit limits: GitHub Enterprise $21/user/month (NOT needed for MVP)

## Success Metrics to Track

1. **Deployment uptime**: Target 99.9% (Cloudflare provides this free)
2. **Search success rate**: Track in KV (store search results metadata)
3. **Rate limit hits**: How many users hit 3-search limit?
4. **Error rate**: < 5% of searches fail

---

**Status**: Ready to deploy
**Owner**: devops-hightower
**Estimated time**: 30 minutes (first time), 5 minutes (subsequent deploys)
**Blockers**: None

**Next action**: Create KV namespace → Add GitHub token → Deploy to Pages
