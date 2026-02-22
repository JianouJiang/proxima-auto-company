# RedFlow Operations Runbook

**System:** RedFlow (Automated 小红书 content posting)
**Infrastructure:** Cloudflare (Workers + D1)
**Status:** Production
**Uptime SLA:** Best effort (free tier)
**On-Call:** Self-hosted automation

---

## System Overview

RedFlow automates daily posting to 小红书 (Xiaohongshu) across multiple product accounts using:

- **Cloudflare Worker:** Dashboard + API for post tracking
- **D1 Database:** Post history and metrics storage
- **Playwright:** Browser automation for 小红书 login + posting
- **Claude API:** AI-powered content generation

**Daily Workflow:**
1. Automation script (local or cloud-hosted) runs at 10am Beijing time
2. Generates content using Claude API
3. Launches browser, logs into 小红书
4. Fills in title, body, hashtags
5. Clicks publish button
6. Stores post URL and metadata in D1
7. Posts visible on dashboard

---

## Infrastructure

### Cloudflare Resources

**Database:**
```
Name:         redflow-db
ID:           58655867-1c20-417f-aa88-acef901dcdf9
Region:       WEUR (Europe)
Tables:       redflow_posts, redflow_metrics
Backups:      Automatic (Cloudflare managed)
```

**Worker:**
```
Name:         redflow-worker
URL:          https://redflow-worker.jianou-works.workers.dev
Version:      2a9d2b40-ac35-4eee-a3d6-85d1f2e0bff3
Cron:         0 2 * * * (daily 02:00 UTC = 10:00 AM Beijing)
Bindings:     DB (D1 database)
```

**API Endpoints:**
- `GET /` — Dashboard (HTML)
- `GET /api/posts` — List all posts (JSON)
- `GET /api/metrics` — Aggregate metrics (JSON)

---

## Daily Monitoring

### 1. Check Dashboard (Manual)

```bash
open https://redflow-worker.jianou-works.workers.dev
```

**What to verify:**
- Stats show correct total post count
- Recent posts table updated today
- No failed posts (red status)
- Bilingual toggle working

### 2. Check API (Programmatic)

```bash
# Get recent posts
curl https://redflow-worker.jianou-works.workers.dev/api/posts | jq '.posts[-1]'

# Check metrics
curl https://redflow-worker.jianou-works.workers.dev/api/metrics | jq '.summary'
```

**Expected:**
```json
{
  "summary": {
    "total_posts": 1,
    "published": 1,
    "failed": null,
    "pending": null
  }
}
```

### 3. Check 小红书 Account

Go to your creator profile:
1. Navigate to https://xiaohongshu.com
2. Check profile for today's post
3. Verify post is public and visible

### 4. Monitor Logs (If Cloud Hosting)

**Railway:**
```bash
railway logs -f
```

**Fly.io:**
```bash
fly logs -f
```

**Local Cron:**
Check terminal output where `npm run auto cron` is running.

---

## Alerting & Troubleshooting

### Problem: Dashboard shows no posts today

**Check list:**

```bash
# 1. Verify Worker is running
curl -I https://redflow-worker.jianou-works.workers.dev
# Should return HTTP 200

# 2. Check database has data
curl https://redflow-worker.jianou-works.workers.dev/api/posts | jq '.posts | length'
# Should be > 0

# 3. Check Worker logs
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow/worker
wrangler tail redflow-worker

# 4. Check if automation is running
# - For local cron: Check terminal
# - For Railway: Check railway logs
# - For Fly.io: Check fly logs
```

### Problem: Automation failed to post

**Check logs for:**
- `❌ Login failed` → Username/password incorrect or account locked
- `❌ Publish failed` → 小红书 UI changed, need selector update
- `❌ CAPTCHA` → Manual login needed, then retry
- `❌ Timeout` → Network issue, retry later

**Recovery steps:**

```bash
# Run manual test
npm run auto once

# Watch browser for errors
HEADLESS=false npm run auto once

# Check screenshot
open /tmp/post-error.png
```

### Problem: API returning 500 error

```bash
# Check database connectivity
wrangler d1 list
# Should show redflow-db with status "production"

# Check Worker code
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow/worker
cat index.js | grep -A 5 "GET /api/posts"

# Redeploy if corrupted
wrangler deploy
```

### Problem: Content generation fails

```bash
# Check ANTHROPIC_API_KEY is valid
curl https://api.anthropic.com/v1/messages \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_API_KEY"

# If key invalid, update in:
# - Local .env file
# - Railway/Fly.io secrets dashboard
# - Then retry
```

---

## Maintenance Tasks

### Daily (Automated)

- [x] 10am Beijing time: Automated post via cron
- [x] Store post in database
- [x] Update dashboard metrics

### Weekly

**Monday:**
```bash
# Check content performance
curl https://redflow-worker.jianou-works.workers.dev/api/metrics | jq '.byProduct'

# Review failed posts
curl https://redflow-worker.jianou-works.workers.dev/api/posts | jq '.posts[] | select(.status=="failed")'
```

**Wednesday:**
```bash
# Verify automation still running
# - Check terminal output (local cron)
# - Check railway/fly logs (cloud)
# - Check for posts in past 3 days
```

**Friday:**
```bash
# Backup check (Cloudflare auto-backup)
wrangler d1 backup list redflow-db

# Review week's posts on 小红书
# Check engagement metrics (likes, saves, comments)
```

### Monthly

**1st of month:**
```bash
# Update npm dependencies
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow
npm update

# Test locally
npm run generate
npm run auto once

# Deploy if changes made
cd worker && wrangler deploy
```

**15th of month:**
```bash
# Review content strategy
# Check which products are performing best
curl https://redflow-worker.jianou-works.workers.dev/api/metrics | jq '.byProduct | sort_by(-.count) | .[0:5]'

# Adjust content prompts if needed
nano automation/content-generator.js
```

**End of month:**
```bash
# Create backup
wrangler d1 backup create redflow-db

# Archive metrics
curl https://redflow-worker.jianou-works.workers.dev/api/metrics > /tmp/redflow-metrics-$(date +%Y-%m).json

# Review monthly stats
jq '.summary' /tmp/redflow-metrics-*.json | tail -1
```

---

## Common Commands

### Local Development

```bash
# Generate one post
npm run generate

# Post manually (one-time)
npm run auto once

# Run with visible browser
HEADLESS=false npm run auto once

# Setup daily automation
npm run auto cron

# Stop cron
Ctrl+C  (or: pkill -f "auto-run.js cron")
```

### Deployment

```bash
# Redeploy Worker
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow/worker
wrangler deploy

# Check deployment history
wrangler deployments list

# View Worker logs
wrangler tail redflow-worker

# Check database list
wrangler d1 list
```

### Database

```bash
# List all posts
wrangler d1 execute redflow-db --file=- --remote <<EOF
SELECT id, product, title, status, created_at FROM redflow_posts ORDER BY created_at DESC LIMIT 20;
EOF

# Count posts by product
wrangler d1 execute redflow-db --file=- --remote <<EOF
SELECT product, COUNT(*) as count FROM redflow_posts GROUP BY product ORDER BY count DESC;
EOF

# Find failed posts
wrangler d1 execute redflow-db --file=- --remote <<EOF
SELECT * FROM redflow_posts WHERE status='failed' ORDER BY created_at DESC;
EOF

# Backup database
wrangler d1 backup create redflow-db

# List backups
wrangler d1 backup list redflow-db
```

### Cloud Hosting

```bash
# Railway
railway logs
railway down

# Fly.io
fly logs -f
fly apps destroy redflow
```

---

## Incident Response

### Website Down (Dashboard not loading)

**Time: 2 minutes**

1. Verify Worker status:
   ```bash
   curl -I https://redflow-worker.jianou-works.workers.dev
   ```

2. If not responding, redeploy:
   ```bash
   cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow/worker
   wrangler deploy
   ```

3. Verify dashboard loads after 30 seconds

4. If still failing, check Cloudflare status dashboard

### Database Corrupted

**Time: 5 minutes (data loss possible)**

1. Create backup first:
   ```bash
   wrangler d1 backup create redflow-db
   ```

2. Check if data can be recovered:
   ```bash
   wrangler d1 backup list redflow-db
   ```

3. If data is lost, re-initialize:
   ```bash
   wrangler d1 execute redflow-db --file=schema.sql --remote
   ```

4. Posts will be lost but system continues working

### Automation Stopped

**Time: Detect next day, fix immediately**

1. Check if process is still running:
   ```bash
   # Local cron
   ps aux | grep "auto-run.js"

   # Cloud hosting
   railway logs  # or fly logs
   ```

2. If local cron died, restart:
   ```bash
   cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow
   npm run auto cron
   ```

3. If cloud platform issue:
   ```bash
   railway down && railway up  # or fly deploy
   ```

4. Verify by checking dashboard for new post within 1 hour

---

## Scaling

### Current Capacity

- **Posts/day:** 1 (can increase)
- **Database:** 40KB (grows ~1KB per post)
- **Worker requests:** <100/day (free tier: 100k/day)
- **Budget:** $0/month

### If Scaling Posts (5+ per day)

1. **Local cron limitation:** Terminal must stay open
   - **Solution:** Move to Railway or Fly.io

2. **Playwright timeout:** Browser may get slow
   - **Solution:** Increase timeout in `playwright-poster.js`
   - **Alternative:** Use Cloudflare Browser Rendering API (paid feature)

3. **Database growth:** D1 free tier: 5GB
   - **Solution:** Archive old posts monthly

4. **API rate limits:** Claude API limits
   - **Solution:** Check Anthropic dashboard for usage
   - **Plan:** May hit API costs

### If Adding Features

1. **Image generation:** Use Cloudflare Workers AI (free tier: 10k/day)
2. **Comment automation:** Requires additional Playwright logic
3. **A/B testing:** Add DB columns for variant tracking
4. **Multi-account:** Create separate Workers per account

---

## Disaster Recovery

### Database Backup

Cloudflare automatically backs up D1 databases. To manually create backup:

```bash
wrangler d1 backup create redflow-db
```

To restore from backup:

```bash
# List available backups
wrangler d1 backup list redflow-db

# Restore from specific backup (ask Cloudflare support)
# NOTE: Cannot self-serve restore; contact support if data loss
```

### Code Backup

All code is in GitHub:
```bash
git clone https://github.com/jianoujiang/proxima-auto-company.git
cd proxima-auto-company/projects/redflow
```

### Full System Recovery

If all Cloudflare resources deleted:

```bash
# 1. Redeploy database
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/redflow
wrangler d1 create redflow-db
# Update database_id in worker/wrangler.toml
wrangler d1 execute redflow-db --file=schema.sql --remote

# 2. Redeploy Worker
cd worker && wrangler deploy

# 3. System back online
# (Posts from before disaster are lost unless backed up separately)
```

**Time to recovery:** ~10 minutes

---

## Contact & Escalation

**On-Call:** Self (founder or DevOps if available)
**Escalation:** None (free tier, best effort)
**SLA:** Best effort (Cloudflare free tier, no SLA)

**Resources:**
- Cloudflare Docs: https://developers.cloudflare.com
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler
- D1 Database: https://developers.cloudflare.com/d1

---

## Sign-Off

**Runbook Created:** 2026-02-22
**Last Updated:** 2026-02-22
**Maintained By:** devops-hightower
**Next Review:** 2026-03-22 (monthly)

---

Ready to operate. System is live.
