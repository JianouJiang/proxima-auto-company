# ConnectPath — Quick Start (5 Minutes)

**For devops-hightower: Fastest path to live deployment**

---

## Prerequisites

- Cloudflare account (free)
- GitHub Personal Access Token

---

## 1. Create GitHub Token (2 minutes)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `ConnectPath MVP`
4. Select scopes:
   - ✅ `public_repo`
   - ✅ `read:user`
5. Click "Generate token"
6. **Copy the token** (starts with `ghp_`)

---

## 2. Create Cloudflare KV Namespace (1 minute)

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/connectpath

# Login to Cloudflare (opens browser)
wrangler login

# Create KV namespace
wrangler kv:namespace create "CONNECTPATH_KV"
```

**Copy the output** (looks like `id = "abc123..."`).

Update `wrangler.toml` line 8:
```toml
id = "YOUR_KV_NAMESPACE_ID_HERE"  # Paste the ID you just copied
```

---

## 3. Deploy (2 minutes)

### Option A: Direct Deploy (Fastest)

```bash
# Add GitHub token as secret
wrangler secret put GITHUB_TOKEN
# Paste your token when prompted

# Deploy to Cloudflare Pages
wrangler pages deploy . --project-name=connectpath
```

After deploy finishes, you'll get a URL like:
```
https://connectpath.pages.dev
```

### Option B: GitHub Integration (More maintainable)

```bash
# 1. Push to GitHub
cd /home/jianoujiang/Desktop/proxima-auto-company
git add projects/connectpath
git commit -m "Add ConnectPath MVP"
git push origin main
```

**2. Connect to Cloudflare Pages**:
- Go to: https://dash.cloudflare.com/pages
- Click "Create a project" → "Connect to Git"
- Select repo: `proxima-auto-company`
- **Build settings**:
  - Framework preset: None
  - Build command: (leave empty)
  - Build output directory: `/`
  - Root directory: `projects/connectpath`
- Click "Save and Deploy"

**3. Add secrets** (after first deploy):
- Pages → Settings → Environment variables
- Add `GITHUB_TOKEN` → paste token
- Click "Save"

**4. Bind KV namespace**:
- Settings → Functions → KV namespace bindings
- Variable name: `CONNECTPATH_KV`
- KV namespace: Select the one you created
- Save → Redeploy

---

## 4. Test (30 seconds)

Visit your URL: `https://connectpath.pages.dev`

**Test search**:
- Person A: `torvalds`
- Person B: `tj`
- Click "Find Connection"

Expected: Should find a path (both are famous on GitHub).

**Test rate limit**:
- Do 3 searches total
- 4th search should show paywall

---

## 5. Done ✅

Your MVP is live.

**Next steps**:
1. Send URL to qa-bach for testing
2. Create Gumroad listing (see `gumroad-listing.txt`)
3. Update Gumroad link in `index.html` if needed
4. Launch on Product Hunt

---

## Troubleshooting

### "KV namespace not found"
- Check `wrangler.toml` line 8 has correct namespace ID
- Run `wrangler kv:namespace list` to see all namespaces

### "GitHub API rate limit exceeded"
- Check that `GITHUB_TOKEN` is set correctly
- Run `wrangler secret list` to verify

### "500 Internal Server Error"
- Check Workers logs: `wrangler tail --project-name=connectpath`
- Common issue: Environment variable not bound correctly

### "No path found" for everyone
- Expected behavior if users aren't active on GitHub
- Try famous users: `torvalds`, `tj`, `sindresorhus`, `gaearon`

---

## Commands Reference

```bash
# Login to Cloudflare
wrangler login

# Create KV namespace
wrangler kv:namespace create "CONNECTPATH_KV"

# List KV namespaces
wrangler kv:namespace list

# Add secret (GitHub token)
wrangler secret put GITHUB_TOKEN

# List secrets
wrangler secret list

# Deploy
wrangler pages deploy . --project-name=connectpath

# View live logs
wrangler tail --project-name=connectpath

# Test KV namespace
wrangler kv:key list --namespace-id=YOUR_KV_NAMESPACE_ID
```

---

**Total Time**: 5 minutes from zero to live MVP

**Cost**: $0/month (Cloudflare free tier)

**What you get**: Global edge-deployed app, < 100ms latency, auto-scaling, free SSL

---

**Built by fullstack-dhh in 3.5 hours. Deployed by you in 5 minutes.**
