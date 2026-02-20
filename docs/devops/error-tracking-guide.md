# ColdCopy Error Tracking & Alerting Guide

**Date:** 2026-02-20
**Engineer:** Kelsey Hightower
**Service:** ColdCopy Production

---

## Overview

ColdCopy generates errors in three places:
1. **Cloudflare Pages Functions** (API endpoint execution)
2. **D1 Database** (query failures, schema errors)
3. **Claude API** (request failures, timeouts)

This guide shows how to access logs and set up alert thresholds.

---

## 1. Cloudflare Pages Function Logs

### Where to Check

**Dashboard:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages

1. Go to Pages > coldcopy > Deployments
2. Click on latest deployment
3. View "Function Logs" tab
4. Filter by status: "500" or "error"

### What to Look For

**Common Errors:**

| Error | Cause | Fix |
|-------|-------|-----|
| `504 Timeout` | Claude API took >25s | Increase timeout or use smaller requests |
| `402 Rate Limited` | User exceeded quota | Expected behavior, customer should upgrade |
| `500 JSON Parse Error` | Claude response malformed | Add retry logic (done in code) |
| `500 D1 Connection Error` | Database unreachable | Check binding in wrangler.toml |
| `400 Invalid Input` | Missing required field | Validate form inputs on frontend |

### Manual Log Check

```bash
# Using Cloudflare CLI (wrangler)
# Note: Free tier logs only available via dashboard, not CLI

# Alternative: Check real-time logs via dashboard tail
# https://dash.cloudflare.com/.../pages > coldcopy > Logs
```

### Log Query Syntax

In Cloudflare dashboard search:

```
# All errors
status:500 OR status:502 OR status:504

# Only timeouts
status:504

# Only rate limits
status:402

# Only client errors
status:400 OR status:401

# API endpoint specific
path:/api/generate AND (status:500 OR status:502)

# Last 24 hours
ts >= now-24h
```

---

## 2. D1 Database Error Monitoring

### Check Database Health

```bash
# List databases
npx wrangler d1 list

# Query sessions table (check for orphaned entries)
npx wrangler d1 execute coldcopy-db --command "SELECT COUNT(*) as total FROM sessions"

# Check for schema errors
npx wrangler d1 execute coldcopy-db --command ".schema"
```

### D1 Error Scenarios

| Error | Cause | Fix |
|-------|-------|-----|
| `Database not found` | Binding mismatch | Verify database_id in wrangler.toml |
| `UNIQUE constraint failed` | Duplicate session ID (impossible, UUID) | Check query logic |
| `Column not found` | Schema missing | Run migration: `npx wrangler d1 execute coldcopy-db --file schema.sql --remote` |
| `Query timeout` | Too many sessions | Cleanup old records (future: add index) |

### D1 Cleanup (Maintenance)

```bash
# Delete sessions older than 90 days
npx wrangler d1 execute coldcopy-db --command \
  "DELETE FROM sessions WHERE created_at < datetime('now', '-90 days')"

# Check for orphaned sequences (no parent session)
npx wrangler d1 execute coldcopy-db --command \
  "SELECT COUNT(*) FROM sequences WHERE session_id NOT IN (SELECT id FROM sessions)"
```

---

## 3. Claude API Error Tracking

### Error Indicators

Check Cloudflare function logs for these Claude API errors:

```
# API errors (watch for patterns)
401 Unauthorized        → Invalid API key
429 Rate Limited        → Account quota exceeded
500 Internal Error      → Claude API issue
Timeout (25s+)         → Slow request or network issue
```

### Monitor API Cost

```bash
# Check Anthropic API usage via dashboard
# https://console.anthropic.com/account/usage

# Manual estimation from logs
# Each generation uses ~3K tokens × $0.011 / 1M tokens = ~$0.033 per generation
```

### API Key Validation

```bash
# Test API key without spending credits
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: sk-ant-your-key" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-haiku-20241022",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "test"}]
  }' | jq '.error'

# If error is null → key is valid
# If error is "invalid_request_error" → key is invalid
```

---

## 4. Error Alerting Strategy

### Alert Thresholds (MVP Phase)

| Metric | Threshold | Action | Cooldown |
|--------|-----------|--------|----------|
| 500 errors | >10 in 1 hour | Check logs, assess severity | 1 hour |
| 504 errors | >5 in 1 hour | Investigate Claude timeout | 1 hour |
| API cost | >$10/day | Check for abuse/loops | 24 hours |
| 402 errors | >50 in 1 day | Normal (users hitting free quota) | N/A |
| Database errors | Any | Immediate check (schema issue) | Real-time |

### Manual Alert Check (Daily)

Add to your monitoring checklist:

```bash
#!/bin/bash
# save as: docs/devops/check-errors.sh

echo "=== Last 24h Error Summary ==="

# Check Cloudflare dashboard for 500+ errors
# Navigate to: https://dash.cloudflare.com/.../pages/coldcopy
# Search: "status:500 OR status:502 OR status:504"
# If >10 errors: investigate

# Check D1 connection
npx wrangler d1 execute coldcopy-db --command "SELECT 1" 2>&1 | \
  grep -q "^1$" && echo "✓ D1 Health: OK" || echo "✗ D1 Health: FAIL"

# Estimate API cost (if we have logs)
echo "✓ Claude API: Check https://console.anthropic.com/account/usage"
```

---

## 5. Incident Response Workflow

### Error Detected

1. **Immediate Check (First 2 minutes):**
   ```bash
   # Confirm error is real
   curl -X POST https://e0fee18a.coldcopy-au3.pages.dev/api/generate \
     -H "Content-Type: application/json" \
     -d '{"companyName":"Test","targetJobTitle":"Test","problemTheyFace":"Test","yourProduct":"Test","keyBenefit":"Test","callToAction":"Test","tone":"Test"}'
   ```

2. **Diagnose (Next 5 minutes):**
   - Check Cloudflare dashboard for error logs
   - Determine error type (500 = server, 402 = quota, 504 = timeout, etc.)
   - Check recent git commits (could be new deployment issue)

3. **Resolve:**
   - **If code issue:** Fix + `git push` (auto-redeploys)
   - **If API key issue:** Update Cloudflare secret
   - **If Claude timeout:** May need rate limiting or optimization
   - **If D1 issue:** Run schema migration

4. **Document:**
   - Save error logs to `docs/devops/incidents/YYYY-MM-DD-incident.md`
   - Record: timestamp, error type, root cause, resolution time
   - Update runbook if new pattern discovered

---

## 6. Sample Incident Report

Save to: `docs/devops/incidents/2026-02-20-api-timeout.md`

```markdown
# Incident Report: API Timeout

**Date/Time:** 2026-02-20 14:30 UTC
**Duration:** 15 minutes
**Impact:** 5 failed requests
**Severity:** Low (not affecting paying users)

## Timeline

- 14:30: UptimeRobot alerts: 504 timeout
- 14:32: Check Cloudflare logs, confirm Claude API slow
- 14:35: Check Anthropic status, no issues reported
- 14:45: Error resolved (transient network issue)

## Root Cause

Claude API intermittent slowness (not our code).

## Resolution

None needed (transient). Monitor for patterns.

## Prevention

- Increase timeout to 30s (check if possible on Pages)
- Add retry logic for 504 (already implemented)

## Metrics

- Error rate: 0.2% of requests
- Customer impact: None (free tier user)
- Cost impact: $0.03 (failed request cost)
```

---

## 7. Integration with Monitoring Stack

### GitHub Actions Health Check

Add to `.github/workflows/health-check.yml`:

```yaml
name: Daily Error Check

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM UTC daily

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check API endpoint
        run: |
          curl -s -X POST \
            -H "Content-Type: application/json" \
            -d '{...}' \
            https://e0fee18a.coldcopy-au3.pages.dev/api/generate | jq '.error'

      - name: Report to issue if error
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: 1,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Daily health check failed at ' + new Date().toISOString()
            })
```

---

## Contacts & Escalation

- **Immediate:** Check logs above
- **5+ mins of downtime:** Create GitHub issue
- **30+ mins of downtime:** Review recent commits, consider rollback
- **If API credentials lost:** Rotate in Cloudflare immediately

---

**Status:** Production Monitoring Active
**Last Updated:** 2026-02-20
**Next Review:** Weekly (Fridays)
