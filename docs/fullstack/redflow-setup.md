# RedFlow Setup Guide

**Project:** RedFlow — Automated 小红书 Content Posting System
**Audience:** DevOps, technical users
**Time:** ~30 minutes
**Date:** 2026-02-22

This guide walks you through setting up RedFlow from scratch to first automated post.

## Prerequisites

- Node.js 18+ installed
- Cloudflare account (free tier)
- 小红书 account with login credentials
- Anthropic API key (Claude)

## Step 1: Clone & Install (5 min)

```bash
# Navigate to project
cd /path/to/proxima-auto-company/projects/redflow

# Install dependencies
npm install

# Install Playwright browsers
npx playwright install chromium
```

**Verify installation:**
```bash
node --version  # Should be 18+
npx playwright --version  # Should show Playwright version
```

## Step 2: Configure Environment Variables (5 min)

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required variables:**

```bash
# Claude API key (get from console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# 小红书 credentials
XIAOHONGSHU_USERNAME=your_phone_number_or_email
XIAOHONGSHU_PASSWORD=your_password

# Worker URL (fill this after deploying Worker in Step 4)
REDFLOW_WORKER_URL=https://redflow-worker.your-subdomain.workers.dev
```

**Security check:**
```bash
# Verify .env is in .gitignore
grep .env .gitignore  # Should show ".env"

# NEVER commit .env to git
git status  # Should NOT show .env file
```

## Step 3: Test Content Generation (5 min)

```bash
# Generate test content
npm run generate
```

**Expected output:**
```
🎨 Generating 小红书 post...

📝 Generated Content:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product: FlowPrep
Title: HVAC新手入门：30天从零到精通的真实路线图

Body (1024 chars):
很多人说HVAC难，其实只是没找到对的学习顺序...
[rest of content]

Hashtags: #职业成长 #技能学习 #HVAC学习 #行业入门 #转行指南
CTA: 你考虑过转行吗？评论告诉我！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Content saved to /tmp/generated-post.json
```

**If it fails:**
- Check ANTHROPIC_API_KEY is valid
- Verify internet connection
- Check Anthropic API status (status.anthropic.com)

## Step 4: Deploy Cloudflare Worker + D1 (10 min)

### 4.1 Create D1 Database

```bash
# Create database
wrangler d1 create redflow-db
```

**Output:**
```
✅ Successfully created DB 'redflow-db'

[[d1_databases]]
binding = "DB"
database_name = "redflow-db"
database_id = "abc123-def456-ghi789"  ← Copy this ID
```

### 4.2 Update Worker Config

```bash
# Edit worker/wrangler.toml
nano worker/wrangler.toml

# Replace PLACEHOLDER_DATABASE_ID with actual ID from above
# Example:
# database_id = "abc123-def456-ghi789"
```

### 4.3 Initialize Database Schema

```bash
# Run SQL schema
wrangler d1 execute redflow-db --file=schema.sql
```

**Expected output:**
```
🌀 Executing on redflow-db (abc123-def456-ghi789):
🌀 To execute on your remote database, add a --remote flag to your wrangler command.
✅ Executed 6 statements in 123ms
```

### 4.4 Deploy Worker

```bash
# Deploy to Cloudflare
cd worker
wrangler deploy
```

**Expected output:**
```
⛅️ wrangler 3.102.0
-------------------
Total Upload: 15.67 KiB / gzip: 4.28 KiB
Uploaded redflow-worker (1.23 sec)
Published redflow-worker (0.45 sec)
  https://redflow-worker.your-subdomain.workers.dev
Current Deployment ID: abc123-def456
```

### 4.5 Update .env with Worker URL

```bash
# Copy Worker URL from output above
# Edit .env
nano .env

# Set REDFLOW_WORKER_URL to your Worker URL
REDFLOW_WORKER_URL=https://redflow-worker.your-subdomain.workers.dev
```

### 4.6 Verify Dashboard

```bash
# Open Worker URL in browser
open https://redflow-worker.your-subdomain.workers.dev
# Or: curl https://redflow-worker.your-subdomain.workers.dev
```

**Expected:** Should see RedFlow Dashboard (bilingual, dark mode)

## Step 5: Test Manual Posting (5 min)

**IMPORTANT:** This will post to your 小红书 account. Use a test account if available.

```bash
# Run full automation once (headless=false to see browser)
npm run auto once
```

**Expected flow:**
1. Generates content via Claude API
2. Launches Chrome browser (visible)
3. Navigates to xiaohongshu.com
4. Logs in with your credentials
5. Navigates to creator page
6. Fills in title, body, hashtags
7. Clicks publish
8. Extracts post URL
9. Logs to Worker API
10. Closes browser

**Expected output:**
```
🎬 Starting RedFlow automated posting...

Step 1: Generating content...
✅ Generated post for DoubleMood
   Title: 焦虑发作时的5秒救急呼吸法：医学认证的马上见效
   Length: 987 chars

Step 2: Posting to 小红书...
🚀 Launching browser...
🔐 Logging in to 小红书...
✅ Login successful
📝 Posting content for DoubleMood...
✅ Title filled
✅ Body filled
🚀 Publish button clicked
✅ Post published successfully

Step 3: Logging to database...
✅ Logged to database (ID: 1)

✅ RedFlow run completed successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product: DoubleMood
Status: published
URL: https://www.xiaohongshu.com/explore/abc123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If login fails:**
- Check XIAOHONGSHU_USERNAME and XIAOHONGSHU_PASSWORD
- 小红书 may show CAPTCHA (manual intervention needed)
- Try running with `headless: false` to see what's happening
- Verify account is not locked

**If posting fails:**
- Check screenshots in `/tmp/post-error.png`
- 小红书 UI may have changed (update selectors in playwright-poster.js)
- Account may need verification

## Step 6: Setup Automated Scheduling (5 min)

### Option A: Local Cron (Simplest)

```bash
# Run as cron job (daily 10am Beijing time)
npm run auto cron

# Output:
# ⏰ Setting up cron: 0 10 * * *
#    (Daily at 10:00 AM Beijing time)
# ✅ Cron job scheduled. Press Ctrl+C to stop.
```

**Keep terminal open or use screen/tmux:**
```bash
# Using screen
screen -S redflow
npm run auto cron
# Detach: Ctrl+A then D
# Reattach: screen -r redflow

# Using tmux
tmux new -s redflow
npm run auto cron
# Detach: Ctrl+B then D
# Reattach: tmux attach -t redflow
```

### Option B: Railway (Cloud, Fully Automated)

```bash
# Install Railway CLI
npm i -g railway

# Login
railway login

# Initialize project
railway init
railway add

# Set environment variables in Railway dashboard
# Go to: railway.app → Your Project → Variables
# Add:
# - ANTHROPIC_API_KEY
# - XIAOHONGSHU_USERNAME
# - XIAOHONGSHU_PASSWORD
# - REDFLOW_WORKER_URL

# Create Procfile
echo "worker: node automation/auto-run.js cron" > Procfile

# Deploy
railway up
```

**Verify:**
- Railway dashboard should show "worker" process running
- Check logs for cron schedule confirmation

### Option C: Fly.io (Cloud, Fully Automated)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch
# Follow prompts, choose region

# Set secrets
fly secrets set ANTHROPIC_API_KEY=sk-ant-xxxxx
fly secrets set XIAOHONGSHU_USERNAME=your_username
fly secrets set XIAOHONGSHU_PASSWORD=your_password
fly secrets set REDFLOW_WORKER_URL=https://your-worker.workers.dev

# Create fly.toml
cat > fly.toml <<EOF
app = "redflow"

[processes]
  worker = "node automation/auto-run.js cron"
EOF

# Deploy
fly deploy
```

**Verify:**
```bash
fly logs
# Should show cron schedule confirmation
```

## Step 7: Verify Everything Works (2 min)

### Check Dashboard

```bash
# Open Worker dashboard
open https://redflow-worker.your-subdomain.workers.dev
```

**Expected:**
- Stats showing 1 published post (from Step 5)
- Recent posts table with your test post
- Bilingual toggle working

### Check API

```bash
# Get recent posts
curl https://redflow-worker.your-subdomain.workers.dev/api/posts | jq

# Get metrics
curl https://redflow-worker.your-subdomain.workers.dev/api/metrics | jq
```

**Expected:**
```json
{
  "posts": [
    {
      "id": 1,
      "product": "DoubleMood",
      "title": "焦虑发作时的5秒救急呼吸法...",
      "status": "published",
      "xiaohongshu_url": "https://www.xiaohongshu.com/explore/abc123",
      "created_at": "2026-02-22T10:00:00.000Z"
    }
  ]
}
```

### Check 小红书 Account

```bash
# Login to xiaohongshu.com
# Go to your profile
# Verify post is visible
```

## Troubleshooting

### Content generation fails

**Error:** `❌ Missing ANTHROPIC_API_KEY environment variable`

**Fix:**
```bash
# Verify .env file exists
ls -la .env

# Check contents
cat .env | grep ANTHROPIC_API_KEY

# If empty, add key
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" >> .env
```

### Playwright login fails

**Error:** `❌ Login failed: Timeout`

**Debug:**
```bash
# Run with visible browser
node automation/playwright-poster.js

# Check screenshot
open /tmp/login-error.png
```

**Common issues:**
- CAPTCHA required → Manual login once to set cookie
- Wrong credentials → Verify username/password
- Account locked → Contact 小红书 support
- UI changed → Update selectors in code

### Worker deployment fails

**Error:** `Error: Unknown database ID`

**Fix:**
```bash
# List databases
wrangler d1 list

# Copy correct database_id to worker/wrangler.toml
```

### Dashboard shows no posts

**Error:** Empty table

**Possible causes:**
1. Worker API not deployed → Deploy with `wrangler deploy`
2. Database not initialized → Run `wrangler d1 execute redflow-db --file=schema.sql`
3. Automation didn't run → Check cron logs
4. API endpoint error → Check browser console (F12)

**Debug:**
```bash
# Check Worker logs
wrangler tail

# Test API directly
curl https://your-worker.workers.dev/api/posts
```

### Cron not triggering

**For local cron:**
- Check terminal is still running
- Verify cron schedule syntax (use crontab.guru)

**For Railway/Fly.io:**
```bash
# Railway
railway logs

# Fly.io
fly logs
```

## Daily Operations

### Monitor Posts

```bash
# Dashboard (visual)
open https://redflow-worker.your-subdomain.workers.dev

# API (programmatic)
curl https://redflow-worker.your-subdomain.workers.dev/api/metrics | jq '.summary'
```

### Manual Trigger

```bash
# Run once
npm run auto once

# Force specific product
FORCE_PRODUCT=FlowPrep npm run auto once
```

### Check Logs

```bash
# Local cron
# (Check terminal output)

# Railway
railway logs -f

# Fly.io
fly logs -f

# Worker
wrangler tail
```

### Update Content

```bash
# Edit product definitions
nano automation/content-generator.js
# Modify PRODUCTS array

# Test new content
npm run generate

# Deploy changes (if using Railway/Fly.io)
railway up  # or: fly deploy
```

## Maintenance

### Weekly

- [ ] Check dashboard for failed posts
- [ ] Verify cron is still running
- [ ] Review post engagement on 小红书

### Monthly

- [ ] Update npm dependencies (`npm update`)
- [ ] Rotate API keys (if security policy)
- [ ] Review content performance
- [ ] Adjust content strategy based on metrics

### As Needed

- [ ] Update Playwright selectors (if 小红书 UI changes)
- [ ] Fix bot detection (if account flagged)
- [ ] Scale posting frequency (if successful)

## Next Steps

1. ✅ Setup complete
2. Monitor first week of automated posts
3. Analyze engagement metrics
4. Iterate on content strategy
5. Consider adding:
   - Image generation
   - A/B testing
   - Comment automation
   - Multi-account support

## Support

**Documentation:**
- Technical Spec: `docs/fullstack/redflow-technical-spec.md`
- README: `projects/redflow/README.md`
- Research Report: `docs/research/redflow-xiaohongshu-trends.md`

**Common Commands:**
```bash
# Generate content
npm run generate

# Post manually
npm run post

# Full automation (once)
npm run auto once

# Setup cron
npm run auto cron

# Deploy Worker
cd worker && wrangler deploy

# Check Worker logs
wrangler tail
```

**Emergency Stops:**

```bash
# Stop local cron
Ctrl+C in terminal
# Or: pkill -f "auto-run.js cron"

# Stop Railway
railway down

# Stop Fly.io
fly apps destroy redflow
```

Good luck. Ship it. 🚀
