# SixDegrees V2 Operations Runbook

**Last Updated:** 2026-02-22
**For:** Production environment
**Team:** DevOps/SRE

---

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Daily Operations](#daily-operations)
3. [Incident Response](#incident-response)
4. [Monitoring & Alerts](#monitoring--alerts)
5. [Database Management](#database-management)
6. [Deployment & Rollback](#deployment--rollback)
7. [Common Issues & Fixes](#common-issues--fixes)
8. [Backup & Disaster Recovery](#backup--disaster-recovery)

---

## System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│ Cloudflare Edge Network (Global CDN)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐  │
│  │  Pages (Static)  │  │  Functions (API) │  │ Workers  │  │
│  ├──────────────────┤  ├──────────────────┤  └──────────┘  │
│  │ index.html       │  │ /api/intake      │                │
│  │ intake.html      │  │ /api/campaign    │                │
│  │ dashboard.html   │  │ /api/send        │                │
│  │ CSS, JS, assets  │  │                  │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │ D1 Database (connectpath-db)                 │          │
│  ├──────────────────────────────────────────────┤          │
│  │ users | campaigns | email_outreach | ...    │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │ KV Storage (Cache layer)                     │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↓                      ↓                    ↓
    ┌────────────┐    ┌──────────────┐    ┌─────────────┐
    │   Gmail    │    │ Anthropic    │    │   Stripe    │
    │   SMTP     │    │   Claude API │    │  Payment    │
    └────────────┘    └──────────────┘    └─────────────┘
```

### Services
- **Frontend:** Cloudflare Pages (static + functions)
- **Database:** Cloudflare D1 (SQLite in zone)
- **Email:** Gmail SMTP (local script for now)
- **AI:** Anthropic Claude API (strategy generation)
- **Payments:** Stripe (payment links)

### Key Metrics
- **RTO (Recovery Time Objective):** < 5 minutes
- **RPO (Recovery Point Objective):** < 1 hour
- **Uptime Target:** 99.9% (daily downtime budget: 86.4 seconds)

---

## Daily Operations

### Morning Checklist (Daily)

```bash
# 1. Check Pages deployment status
wrangler pages deployments list --project-name sixdegrees

# 2. Check D1 database health
wrangler d1 execute connectpath-db --remote --command="SELECT COUNT(*) as user_count FROM users;"

# 3. Check function logs for errors
wrangler tail sixdegrees 2>&1 | grep -i "error\|warning"

# 4. Monitor Cloudflare Analytics
# → https://dash.cloudflare.com → Pages → sixdegrees → Analytics
```

### Weekly Tasks

- [ ] Review error logs (Cloudflare Analytics)
- [ ] Check D1 database size growth
- [ ] Verify backup integrity
- [ ] Update runbook with new findings
- [ ] Test failover procedures

### Monthly Tasks

- [ ] Full disaster recovery drill
- [ ] Performance audit (Lighthouse score)
- [ ] Security audit (secrets rotation)
- [ ] Cost review (Cloudflare usage)
- [ ] Update incident postmortems

---

## Incident Response

### 1. API Endpoint Down

**Symptoms:** Intake form requests return 500 or timeout

**Severity:** Critical (blocks campaign creation)

**Diagnosis:**
```bash
# Check function logs
wrangler tail sixdegrees --env production

# Test API manually
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{"user_email":"test@test.com","user_name":"Test"}'

# Check D1 connection
wrangler d1 execute connectpath-db --remote \
  --command="SELECT COUNT(*) FROM campaigns;"
```

**Common Causes & Fixes:**

| Cause | Fix | Time |
|-------|-----|------|
| D1 binding not configured | Configure in Cloudflare dashboard (Functions → D1) | 2 min |
| Secrets not set | `wrangler pages secret put ANTHROPIC_API_KEY` | 1 min |
| Database offline | Check Cloudflare status page | 5 min |
| Function deployment failed | Redeploy: `wrangler pages deploy public --project-name sixdegrees` | 2 min |

**Resolution Steps:**
1. Identify failing endpoint (intake, campaign, send)
2. Check function logs for error message
3. Verify D1 binding is set (dashboard: Pages → sixdegrees → Settings → Functions → D1)
4. Check secrets are present: `wrangler pages secret list --project-name sixdegrees`
5. Redeploy if needed
6. Test endpoint again

---

### 2. Landing Page or Intake Form Returns 404

**Symptoms:** https://sixdegrees.pages.dev/ or /intake returns blank page

**Severity:** Critical (users can't access service)

**Diagnosis:**
```bash
# Check pages deployment status
wrangler pages deployments list --project-name sixdegrees | head -5

# Test page load
curl -I https://sixdegrees.pages.dev/

# Check build output directory
ls -la projects/sixdegrees/public/
```

**Resolution:**
1. Check if files exist in `public/` directory
2. If missing, rebuild: `wrangler pages deploy public --project-name sixdegrees`
3. If still broken, rollback: Cloudflare dashboard → Pages → sixdegrees → Deployments → Click previous deployment
4. Verify files were uploaded: `wrangler pages files list sixdegrees`

---

### 3. Database Full / Size Exceeded

**Symptoms:** D1 insert operations fail with "database or disk is full"

**Severity:** Critical (blocks new campaigns)

**Diagnosis:**
```bash
# Check database size
wrangler d1 info connectpath-db --remote

# Count records by table
wrangler d1 execute connectpath-db --remote --command="
  SELECT name, (SELECT COUNT(*) FROM sqlite_master
    WHERE type='table' AND name LIKE '%') as size
  FROM sqlite_master WHERE type='table';"

# Check for old/archived campaigns to delete
wrangler d1 execute connectpath-db --remote --command="
  SELECT id, created_at, status FROM campaigns
  WHERE created_at < strftime('%s', 'now') - 86400*90
  ORDER BY created_at DESC LIMIT 10;"
```

**Resolution:**
1. Archive old campaigns (older than 90 days):
   ```bash
   wrangler d1 execute connectpath-db --remote --command="
     DELETE FROM campaigns WHERE created_at <
       strftime('%s', 'now') - 86400*90 AND status = 'completed';"
   ```
2. Delete orphaned email records:
   ```bash
   wrangler d1 execute connectpath-db --remote --command="
     DELETE FROM email_outreach WHERE campaign_id NOT IN
       (SELECT id FROM campaigns);"
   ```
3. Monitor growth and plan upgrade to larger tier

---

### 4. High Latency / Slow API Response

**Symptoms:** Intake form takes > 10 seconds to respond

**Severity:** High (bad user experience)

**Diagnosis:**
```bash
# Measure response time
time curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{"user_email":"test@test.com",...}'

# Check Cloudflare Analytics for latency
# → https://dash.cloudflare.com → Pages → sixdegrees → Analytics

# Check if Claude API is slow
curl -w "@- " -o /dev/null -s https://api.anthropic.com/v1/health
```

**Common Causes:**

1. **Claude API slow** (strategy generation takes 5-10s)
   - Normal for first request. Cache subsequent requests.

2. **Database query slow**
   ```bash
   # Analyze query performance
   wrangler d1 execute connectpath-db --remote --command="
     EXPLAIN QUERY PLAN
     SELECT * FROM campaigns WHERE user_id = 'user_123';"
   ```

3. **Network latency**
   - Check Cloudflare Analytics for geographic latency
   - Verify edge location is correct

**Resolution:**
- Add query caching (KV layer) for frequently accessed data
- Optimize Claude prompt for faster responses
- Add pagination to large queries
- Monitor via Cloudflare Analytics

---

### 5. Email Sending Fails

**Symptoms:** POST /api/send returns success but emails don't send

**Severity:** High (outreach blocked)

**Diagnosis:**
```bash
# Check email queue status
wrangler d1 execute connectpath-db --remote --command="
  SELECT id, status, error_message FROM email_outreach
  WHERE campaign_id = 'camp_123' LIMIT 5;"

# Check if local Gmail script is running
ps aux | grep send-gmail

# Test Gmail SMTP manually
node projects/sixdegrees/send-gmail.js \
  --to "test@example.com" \
  --subject "Test" \
  --body "Hello"
```

**Resolution:**
1. Verify Gmail App Password is set correctly:
   ```bash
   wrangler pages secret list --project-name sixdegrees | grep GMAIL
   ```
2. Check Gmail account isn't blocking SMTP:
   - https://myaccount.google.com/security (turn off "Less secure apps" blocking)
3. Check network allows SMTP (port 587):
   ```bash
   telnet smtp.gmail.com 587
   ```
4. Run email send script manually:
   ```bash
   cd projects/sixdegrees
   node send-gmail.js --campaign-id camp_123
   ```

---

## Monitoring & Alerts

### Cloudflare Analytics Dashboard

**Access:** https://dash.cloudflare.com → Pages → sixdegrees → Analytics

**Key Metrics to Monitor:**
- Requests per minute (should be stable)
- Error rate (should be < 1%)
- Response time (should be < 2s for landing page, < 5s for API)
- Bandwidth (track growth)

### Setting Up UptimeRobot (Recommended)

```bash
# 1. Create monitor for landing page
# URL: https://sixdegrees.pages.dev/
# Check interval: 5 minutes
# HTTP method: GET
# Acceptable status codes: 200

# 2. Create monitor for API
# URL: https://sixdegrees.pages.dev/api/campaign/test
# Check interval: 5 minutes
# Expected response: Should not contain "error"

# 3. Set alerts
# Email on down: devops@proxima-auto-company.com
# SMS on critical: [your phone]
```

### Cloudflare Workers Tail

Monitor production logs in real-time:
```bash
wrangler tail sixdegrees --env production --format pretty
```

Filter by status:
```bash
wrangler tail sixdegrees --status error --status canceled
```

---

## Database Management

### Viewing Data

```bash
# Count users
wrangler d1 execute connectpath-db --remote --command="SELECT COUNT(*) as users FROM users;"

# List recent campaigns
wrangler d1 execute connectpath-db --remote --command="
  SELECT id, email, target_name, status, created_at
  FROM campaigns ORDER BY created_at DESC LIMIT 10;"

# Check email queue
wrangler d1 execute connectpath-db --remote --command="
  SELECT campaign_id, COUNT(*) as emails,
         SUM(CASE WHEN status='sent' THEN 1 ELSE 0 END) as sent,
         SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) as failed
  FROM email_outreach GROUP BY campaign_id;"
```

### Updating Data (Use Caution!)

```bash
# Fix user email (if needed)
wrangler d1 execute connectpath-db --remote --command="
  UPDATE users SET email = 'newemail@example.com'
  WHERE id = 'user_123';"

# Mark campaign as completed
wrangler d1 execute connectpath-db --remote --command="
  UPDATE campaigns SET status = 'completed'
  WHERE id = 'camp_123';"

# Add credits to user
wrangler d1 execute connectpath-db --remote --command="
  UPDATE users SET credits_balance = credits_balance + 5
  WHERE email = 'user@example.com';"
```

### Backing Up

```bash
# Create manual backup
wrangler d1 backup create connectpath-db

# List backups
wrangler d1 backup list connectpath-db

# Restore from backup
wrangler d1 backup restore connectpath-db --backup-id abc123
```

---

## Deployment & Rollback

### Deploying Updates

```bash
# 1. Make changes to code
# 2. Test locally
# 3. Deploy to production
cd projects/sixdegrees
wrangler pages deploy public --project-name sixdegrees --commit-dirty=true

# 4. Verify deployment
curl https://sixdegrees.pages.dev/ | head -20
```

### Rollback Procedure

If a deployment introduces bugs:

**Option A: Rollback via Dashboard (Fastest)**
1. Go to https://dash.cloudflare.com → Pages → sixdegrees → Deployments
2. Find the previous good deployment
3. Click "Rollback to this deployment"
4. Confirm
5. Verify: curl https://sixdegrees.pages.dev/

**Option B: Redeploy Previous Version**
```bash
# Check git history
git log --oneline projects/sixdegrees/ | head -5

# Revert to previous version
git revert HEAD
cd projects/sixdegrees
wrangler pages deploy public --project-name sixdegrees
```

### Testing Before Deploying

```bash
# 1. Run local tests
npm test --prefix projects/sixdegrees/

# 2. Test locally
wrangler pages dev public --project-name sixdegrees
# Visit http://localhost:8788/

# 3. Test API endpoints
curl -X POST http://localhost:8788/api/intake \
  -H "Content-Type: application/json" \
  -d '{"user_email":"test@test.com",...}'
```

---

## Common Issues & Fixes

### Issue: "Cannot read properties of undefined (reading 'prepare')"

**Cause:** D1 binding not configured for Pages Functions

**Fix:**
1. Go to Cloudflare dashboard
2. Pages → sixdegrees → Settings → Functions
3. Click "Add binding" under "D1 Database"
4. Select: Binding name = `DB`, Database = `connectpath-db`
5. Redeploy or wait for next deployment

### Issue: "ANTHROPIC_API_KEY is undefined"

**Cause:** Secret not set in Pages environment

**Fix:**
```bash
wrangler pages secret put ANTHROPIC_API_KEY --project-name sixdegrees
# Paste your API key when prompted
```

### Issue: "Email sent but recipient didn't receive it"

**Cause:** Gmail SMTP local script not running

**Fix:**
```bash
# Set up cron job to send queued emails
crontab -e
# Add: */15 * * * * cd ~/proxima-auto-company/projects/sixdegrees && node send-gmail.js
```

### Issue: Form submission redirects to wrong page

**Cause:** Hardcoded URL in form JavaScript

**Fix:**
1. Check `projects/sixdegrees/public/intake.html` for hardcoded URLs
2. Change from `/campaign.html?id=...` to `/dashboard?campaign=...`
3. Redeploy

### Issue: Language toggle not working

**Cause:** localStorage disabled or data-en/data-zh attributes missing

**Fix:**
1. Check browser localStorage: `localStorage.getItem('language')`
2. Verify HTML elements have `data-en` and `data-zh` attributes
3. Check JavaScript language switching function is loaded

---

## Backup & Disaster Recovery

### Backup Strategy

| Data | Frequency | Method | Retention |
|------|-----------|--------|-----------|
| D1 Database | Daily | `wrangler d1 backup create` | 30 days |
| Source code | Every commit | Git | Forever |
| Secrets | On change | Document in vault | Forever |
| Configuration | On change | Git (wrangler.toml) | Forever |

### Creating Backup

```bash
# Automated daily backup (add to cron)
0 2 * * * wrangler d1 backup create connectpath-db

# Or manually
wrangler d1 backup create connectpath-db
```

### Disaster Recovery Procedure

**Scenario: Entire D1 database deleted**

**Time to Recovery: ~30 minutes**

1. **Notify users** (if data loss is significant)
2. **Restore database**
   ```bash
   # List available backups
   wrangler d1 backup list connectpath-db

   # Restore from most recent backup
   wrangler d1 backup restore connectpath-db --backup-id <backup-id>
   ```
3. **Verify data integrity**
   ```bash
   wrangler d1 execute connectpath-db --remote --command="
     SELECT COUNT(*) FROM users;
     SELECT COUNT(*) FROM campaigns;
     SELECT COUNT(*) FROM email_outreach;"
   ```
4. **Test API endpoints**
   ```bash
   curl https://sixdegrees.pages.dev/api/intake
   ```
5. **Notify users** that service is restored

### Disaster Recovery Test (Monthly)

Schedule monthly DR drill:
1. Create test database clone
2. Restore backup to clone
3. Verify all data present
4. Test API against clone
5. Document time to recovery
6. Update runbook with findings

---

## Performance Tuning

### Database Query Optimization

```bash
# Check slow queries
wrangler d1 execute connectpath-db --remote --command="
  EXPLAIN QUERY PLAN
  SELECT * FROM campaigns WHERE user_id = ? AND status = ?;"
```

**Common Optimizations:**
- Add indexes: `CREATE INDEX idx_campaigns_user_status ON campaigns(user_id, status);`
- Limit result sets: `SELECT ... LIMIT 100`
- Use pagination: `SELECT ... LIMIT 100 OFFSET 0`

### Frontend Performance

Monitor via Cloudflare Analytics:
- First Contentful Paint (target: < 1s)
- Largest Contentful Paint (target: < 2.5s)
- Cumulative Layout Shift (target: < 0.1)

Optimize:
- Compress images (WebP format)
- Minify CSS/JS
- Remove unused Tailwind CSS
- Enable HTTP/2 Server Push

---

## Security Checklist

- [ ] Secrets never logged (check function logs)
- [ ] API keys rotated quarterly
- [ ] CORS headers set correctly (check Access-Control-Allow-Origin)
- [ ] Rate limiting configured (prevent DDoS)
- [ ] SQL injection prevented (parameterized queries used)
- [ ] Environment separation (dev ≠ prod secrets)

---

## Escalation Path

| Issue | Owner | Time | Notes |
|-------|-------|------|-------|
| Function down | devops-hightower | 15 min | Page immediately |
| Database down | devops-hightower + CTO | 30 min | Evaluate restore vs failover |
| Security incident | CEO + DevOps | 5 min | Isolate, assess, notify |
| Data loss | DevOps + CEO | 60 min | Restore from backup, RCA |

**Contact:**
- DevOps: devops-hightower (on-call)
- CTO: cto-vogels (infrastructure decisions)
- CEO: ceo-bezos (stakeholder communication)

---

## Related Documents

- Deployment Report: `docs/devops/sixdegrees-v2-deployment.md`
- Engineering Handoff: `docs/fullstack/SIXDEGREES_V2_HANDOFF.md`
- Technical Spec: `docs/fullstack/sixdegrees-v2-technical-spec.md`
- Test Plan: `projects/sixdegrees/TEST.md`

---

**Last Updated:** 2026-02-22
**Version:** 1.0
**Next Review:** 2026-03-22 (monthly)
