# RedFlow — Post-Deployment Quick Start

**Status:** Worker deployed and live
**Dashboard:** https://redflow-worker.jianou-works.workers.dev
**Time to full automation:** ~30 minutes

---

## What's Already Done

✅ D1 database created and schema initialized
✅ Cloudflare Worker deployed to production
✅ API endpoints responding correctly
✅ Cron schedule configured (daily 10am Beijing time)
✅ Dashboard accessible and functional

**You only need to:**
1. Setup local environment
2. Test content generation
3. Verify posting works
4. Configure automation scheduling

---

## Step 1: Setup Local Environment (5 min)

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow

# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

**Set these variables in `.env`:**

```bash
# Get API key from: https://console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# Your 小红书 account
XIAOHONGSHU_USERNAME=your_phone_or_email
XIAOHONGSHU_PASSWORD=your_password

# Already deployed Worker (keep as-is)
REDFLOW_WORKER_URL=https://redflow-worker.jianou-works.workers.dev
```

**Save the file** (Ctrl+O, Enter, Ctrl+X in nano)

---

## Step 2: Install Dependencies (3 min)

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow

npm install
npx playwright install chromium
```

---

## Step 3: Test Content Generation (2 min)

```bash
npm run generate
```

**Expected output:**
```
🎨 Generating 小红书 post...

📝 Generated Content:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product: [Product Name]
Title: [Generated Title]
Body: [1000+ character content...]
Hashtags: #tag1 #tag2 #tag3
CTA: [Call to action]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Content saved to /tmp/generated-post.json
```

**If it fails:**
- Check `ANTHROPIC_API_KEY` is correct
- Check internet connection
- Try again (API may be temporarily busy)

---

## Step 4: Test Manual Posting (5 min)

**⚠️ WARNING:** This will post to your 小红书 account. Use test account if possible.

```bash
npm run auto once
```

**What it does:**
1. Generates random content
2. Opens Chrome browser (you'll see it)
3. Logs into 小红书
4. Fills in title, body, hashtags
5. Clicks publish button
6. Saves post URL to database
7. Closes browser

**Expected output:**
```
🎬 Starting RedFlow automated posting...

Step 1: Generating content...
✅ Generated post for [Product]
   Title: [Chinese title]
   Length: 987 chars

Step 2: Posting to 小红书...
🚀 Launching browser...
🔐 Logging in to 小红书...
✅ Login successful
📝 Posting content...
✅ Title filled
✅ Body filled
🚀 Publish button clicked
✅ Post published successfully

Step 3: Logging to database...
✅ Logged to database (ID: 1)

✅ RedFlow run completed successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product: [Product Name]
Status: published
URL: https://www.xiaohongshu.com/explore/[POST_ID]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If login fails:**
- Check username/password in `.env`
- 小红书 may show CAPTCHA (manual intervention needed)
- Try again with `headless=false` to debug:
  ```bash
  HEADLESS=false npm run auto once
  ```

**If posting fails:**
- Check screenshot: `open /tmp/post-error.png`
- 小红书 UI may have changed (may need code update)
- Account may need verification

**Verify it worked:**
1. Go to https://xiaohongshu.com
2. Check your creator account
3. You should see the new post

---

## Step 5: Verify in Dashboard

```bash
# Open dashboard in browser
open https://redflow-worker.jianou-works.workers.dev
```

**You should see:**
- Stats showing 1 published post
- Recent posts table with your test post
- Bilingual toggle (English/Chinese)

**Or check via API:**
```bash
curl https://redflow-worker.jianou-works.workers.dev/api/posts | jq
curl https://redflow-worker.jianou-works.workers.dev/api/metrics | jq
```

---

## Step 6: Setup Automated Posting

Choose ONE method:

### Option A: Local Cron (Simplest, Free)

```bash
npm run auto cron
```

Keep the terminal open (it will post daily at 10am Beijing time).

**To background it (recommended):**
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

---

### Option B: Railway (Cloud, Fully Automated)

```bash
npm i -g railway
railway login
railway init
railway add
```

Then:
1. Go to https://railway.app
2. Open your project
3. Go to Variables tab
4. Add:
   - ANTHROPIC_API_KEY
   - XIAOHONGSHU_USERNAME
   - XIAOHONGSHU_PASSWORD
   - REDFLOW_WORKER_URL

Then deploy:
```bash
echo "worker: node automation/auto-run.js cron" > Procfile
railway up
```

---

### Option C: Fly.io (Cloud, Fully Automated)

```bash
curl -L https://fly.io/install.sh | sh
fly auth login
fly launch
# Choose region

fly secrets set ANTHROPIC_API_KEY=sk-ant-xxxxx
fly secrets set XIAOHONGSHU_USERNAME=your_username
fly secrets set XIAOHONGSHU_PASSWORD=your_password
fly secrets set REDFLOW_WORKER_URL=https://redflow-worker.jianou-works.workers.dev

cat > fly.toml <<EOF
app = "redflow"
[processes]
  worker = "node automation/auto-run.js cron"
EOF

fly deploy
```

---

## Monitoring

### Check Dashboard
```bash
open https://redflow-worker.jianou-works.workers.dev
```

### Check logs (if using Railway)
```bash
railway logs
```

### Check logs (if using Fly.io)
```bash
fly logs
```

### Check Worker logs (technical)
```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow/worker
wrangler tail redflow-worker
```

---

## Troubleshooting

### Content generation fails
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Test API directly
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Login fails with CAPTCHA
- 小红书 may detect bot activity
- Try logging in manually once to verify account
- Wait 24 hours before retrying

### Browser not launching
```bash
# Reinstall Playwright
npx playwright install chromium --with-deps

# Test with visible browser
HEADLESS=false npm run auto once
```

### Posts not showing in dashboard
```bash
# Check database has data
curl https://redflow-worker.jianou-works.workers.dev/api/posts | jq '.posts | length'

# Should show 1 or more
```

---

## Common Commands

```bash
# Generate one post
npm run generate

# Post once manually
npm run auto once

# Setup daily posting (background)
npm run auto cron

# Redeploy worker (if code changed)
cd worker && wrangler deploy

# View Worker dashboard
open https://redflow-worker.jianou-works.workers.dev

# View API posts
curl https://redflow-worker.jianou-works.workers.dev/api/posts | jq

# View API metrics
curl https://redflow-worker.jianou-works.workers.dev/api/metrics | jq
```

---

## Timeline

- **Right now:** Setup local `.env` (2 min)
- **Next:** Install deps and test generation (5 min)
- **Next:** Test manual posting (5-10 min, includes browser launch)
- **Next:** Verify in dashboard (1 min)
- **Next:** Choose and setup automation (5-10 min)
- **Done:** Fully automated 小红书 posting 🚀

**Total time:** ~25-35 minutes

---

## Questions?

Check the full deployment report:
`/home/jianoujiang/Desktop/proxima-auto-company/docs/devops/redflow-deployment.md`

---

**Ready? Let's go.**

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow
cp .env.example .env
nano .env  # Add your keys
npm install
npm run generate
```
