# ColdCopy Production Runbook

**Date:** 2026-02-20
**DevOps Lead:** Kelsey Hightower
**On-Call Contact:** DevOps Slack #operations

---

## Quick Links

- **Live App:** https://coldcopy-au3.pages.dev
- **GitHub Repo:** https://github.com/JianouJiang/coldcopy
- **Cloudflare Dashboard:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages
- **D1 Database:** ID `413b402d-f259-4b79-b7e4-3ab887c8a431`
- **KV Namespace:** ID `82359391e9704000a8d5f1efadf9b27f`

---

## Common Tasks

### Check Deployment Status

```bash
# View recent deployments
npx wrangler pages deployment list --project-name coldcopy

# View deployment logs
# Go to: https://dash.cloudflare.com/.../pages/view/coldcopy
# Click latest deployment > View Build Log
```

### Deploy New Code

```bash
git push  # Auto-deploys to production

# Or manual deploy:
cd projects/coldcopy
npx wrangler pages deploy --project-name coldcopy
```

### Rollback to Previous Version

```bash
# Option 1: Revert last commit
git revert HEAD
git push

# Option 2: Deploy specific commit
git checkout <commit-hash> -- .
git commit -m "rollback: revert to <commit-hash>"
git push
```

### Check D1 Database

```bash
# List tables
npx wrangler d1 execute coldcopy-db --command "SELECT name FROM sqlite_master WHERE type='table';"

# Query sessions
npx wrangler d1 execute coldcopy-db --command "SELECT * FROM sessions LIMIT 10;"

# Query sequences
npx wrangler d1 execute coldcopy-db --command "SELECT COUNT(*) as total FROM sequences;"

# Check database size
npx wrangler d1 execute coldcopy-db --command "SELECT page_count * page_size / 1024 / 1024 as 'Database Size (MB)' FROM pragma_page_count(), pragma_page_size();"
```

### Check KV Namespace

```bash
# List keys
npx wrangler kv key list --binding RATE_LIMIT | head -20

# Get specific key
npx wrangler kv key get "rate_limit:session-id-here" --binding RATE_LIMIT

# Delete key
npx wrangler kv key delete "rate_limit:session-id-here" --binding RATE_LIMIT

# Check KV usage
# Go to: https://dash.cloudflare.com/.../kv/namespaces
```

### Monitor Error Rate

Check Cloudflare Pages dashboard:
https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages

Look for:
- "Analytics" tab: Request latency, response times
- Error rate (should be <1%)
- Response status codes

### View Function Logs

```bash
# Real-time logs (if available)
npx wrangler tail --format json

# Or check dashboard logs:
# https://dash.cloudflare.com/.../pages
# Navigate to: Analytics > Requests > Filter by status:500
```

---

## Troubleshooting

### Users Getting 404 on /api/generate

**Check:**
1. Latest deployment successful? (check Pages Dashboard)
2. _routes.json present in build output?
3. Functions directory exists in repo?

**Fix:**
```bash
# Re-trigger build
git push

# Or manually redeploy
cd projects/coldcopy
npx wrangler pages deploy --project-name coldcopy
```

**Verify:**
```bash
curl -X POST https://coldcopy-au3.pages.dev/api/generate \
  -H "Content-Type: application/json" \
  -d '{"companyName":"Test"}'
# Should get 400 (invalid input) or 402 (rate limit), NOT 404
```

### D1 Connection Errors

**Error:** "Database binding not found" or "DB is not defined"

**Check:**
1. D1 database ID matches `wrangler.toml`:
   ```
   database_id = "413b402d-f259-4b79-b7e4-3ab887c8a431"
   ```
2. Binding name is "DB" in code and config
3. Schema was migrated

**Fix:**
```bash
# Verify schema
npx wrangler d1 execute coldcopy-db --command "SELECT name FROM sqlite_master WHERE type='table';"

# If tables don't exist, re-run migration
npx wrangler d1 execute coldcopy-db --file schema.sql --remote
```

### KV Rate Limiting Not Working

**Symptom:** Users getting second generation instead of 402 error

**Check:**
1. RATE_LIMIT binding correct in `wrangler.toml`:
   ```
   id = "82359391e9704000a8d5f1efadf9b27f"
   ```
2. KV namespace name is "RATE_LIMIT" in code
3. KV storage isn't full (check Dashboard)

**Fix:**
```bash
# Clear old rate limit keys
npx wrangler kv key list --binding RATE_LIMIT | while read key; do
  npx wrangler kv key delete "$key" --binding RATE_LIMIT
done

# Verify: should be empty now
npx wrangler kv key list --binding RATE_LIMIT
```

### Claude API Timing Out

**Symptom:** Users getting 504 Gateway Timeout

**Check:**
1. ANTHROPIC_API_KEY set in Pages secrets?
2. Claude API status: https://status.anthropic.com/
3. Request payload valid? (check functions/api/generate.ts)

**Possible causes:**
- Claude API is down (check status page)
- Invalid ANTHROPIC_API_KEY (test with curl to Claude API)
- Request payload has invalid JSON
- Timeout is too short (currently 25s - should be fine)

**Fix:**
```bash
# Verify API key works
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: sk-ant-YOUR_KEY_HERE" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-3-5-haiku-20241022",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "hello"}]
  }'
```

### Slow Response Times

**Symptom:** Users report >5 second load times

**Check:**
1. Claude API latency (typically 3-5s, but can spike)
2. D1 query latency (<100ms typical)
3. Network latency to Cloudflare edge

**Optimize:**
- D1 is edge-cached, queries should be fast
- Claude API can't be optimized without changing model
- Consider caching Claude responses for identical inputs (future feature)

**Monitor:**
```bash
# Test from different regions
for region in us eu asia; do
  curl -w "@curl-format.txt" -o /dev/null -s https://coldcopy-au3.pages.dev
done
```

---

## Incident Response

### Process

1. **Detect:** Monitoring alert or user report
2. **Assess:** Check error rate, affected users, root cause
3. **Communicate:** Notify team, update status
4. **Mitigate:** Hot fix or rollback
5. **Resolve:** Deploy permanent fix
6. **Post-mortem:** Document lessons learned

### Common Incidents

#### High Error Rate (>5%)

**Possible causes:**
- Deployment introduced bug
- Claude API is rate-limited
- D1 is overloaded
- Network issue

**Immediate action:**
```bash
# Check latest deployment logs
# https://dash.cloudflare.com/.../pages/view/coldcopy

# If recent deploy caused issue: rollback
git revert HEAD
git push

# Wait 2-3 minutes for Pages redeploy
```

#### Database Locked / Connection Errors

**Symptom:** All requests getting 500 errors

**Cause:** D1 query timeout or concurrent access issue

**Fix:**
```bash
# Check D1 status
npx wrangler d1 list

# If locked, wait 2 minutes and retry
# D1 auto-recovers from transaction locks

# If persistent, contact Cloudflare support
```

#### Rate Limiting Too Strict

**Symptom:** Legitimate users getting 402 errors immediately

**Cause:** Could be:
- KV TTL not working (old keys not expiring)
- Rate limiting logic bug
- Attack (many requests from one session)

**Check:**
```bash
# Inspect a session's rate limit key
npx wrangler kv key get "rate_limit:session-id" --binding RATE_LIMIT

# If old keys stuck, purge:
npx wrangler kv key delete "rate_limit:session-id" --binding RATE_LIMIT
```

---

## Maintenance

### Weekly Checks

- [ ] Check error rate (target: <1%)
- [ ] Review Pages analytics dashboard
- [ ] Check D1 storage usage (should be <50MB)
- [ ] Verify KV operations (writes/reads within budget)
- [ ] Check Claude API costs

### Monthly Tasks

- [ ] Review and analyze error logs
- [ ] Audit database queries for performance
- [ ] Clean up old sessions if DB grows large
- [ ] Update dependencies (`npm audit fix`)
- [ ] Backup D1 database (automated via Cloudflare)

### Quarterly Capacity Planning

- [ ] Estimate storage growth (D1, KV, R2 if used)
- [ ] Project API costs based on usage trends
- [ ] Plan scaling if approaching free tier limits

---

## Escalation

### Need Help?

1. **Pages Functions issue?** → Check Cloudflare Pages docs
2. **D1 database issue?** → Check D1 docs
3. **KV issue?** → Check KV docs
4. **Can't resolve?** → Contact Cloudflare support

**Cloudflare Support:** https://support.cloudflare.com/

---

## Secrets Management

### Setting Secrets

**ANTHROPIC_API_KEY** (required for /api/generate):

Option 1: Via Dashboard
1. https://dash.cloudflare.com/
2. Pages > coldcopy > Settings
3. Environment variables (Production)
4. Add: `ANTHROPIC_API_KEY`
5. Save

Option 2: Via CLI
```bash
npx wrangler pages secret put ANTHROPIC_API_KEY --project-name coldcopy
# Paste key when prompted
```

**Verify:**
```bash
npx wrangler pages secret list --project-name coldcopy
```

### Never Commit Secrets

- ANTHROPIC_API_KEY
- STRIPE_SECRET_KEY (when added)
- JWT secrets (when added)

Always use `.env` (local dev) and Pages Secrets (production).

---

## Useful Commands Cheat Sheet

```bash
# Deployments
npx wrangler pages deployment list --project-name coldcopy
npx wrangler pages deploy --project-name coldcopy

# Database
npx wrangler d1 list
npx wrangler d1 execute coldcopy-db --command "SELECT 1"
npx wrangler d1 execute coldcopy-db --file schema.sql --remote

# KV
npx wrangler kv namespace list
npx wrangler kv key list --binding RATE_LIMIT
npx wrangler kv key get "key-name" --binding RATE_LIMIT

# Secrets
npx wrangler pages secret list --project-name coldcopy
npx wrangler pages secret put SECRET_NAME --project-name coldcopy

# Logs
npx wrangler tail --format json
npx wrangler pages deployment view <deployment-id> --project-name coldcopy

# Local development
npm run build
cd frontend && npm run dev
npx wrangler pages dev frontend/dist
```

---

**Document:** ColdCopy Production Runbook
**Last Updated:** 2026-02-20
**Status:** Active
