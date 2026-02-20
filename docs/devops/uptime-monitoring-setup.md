# ColdCopy Uptime Monitoring Setup

**Date:** 2026-02-20
**Engineer:** Kelsey Hightower
**Service:** ColdCopy Production (https://e0fee18a.coldcopy-au3.pages.dev)

---

## Quick Start

### Option 1: UptimeRobot (Recommended - Free Tier)

UptimeRobot provides 50 free uptime monitors with 5-minute checks and email alerts.

**Setup Steps:**

1. Go to https://uptimerobot.com and sign up (free)
2. Create two monitors:

**Monitor 1: Main Page (HTTP Status)**
- Type: HTTP(s)
- URL: `https://e0fee18a.coldcopy-au3.pages.dev`
- Method: GET
- Frequency: 5 minutes
- Friendly Name: "ColdCopy Production - Main Page"
- Alert Email: [your-email@example.com]
- Save

**Monitor 2: API Health (POST Test)**
- Type: HTTP(s)
- URL: `https://e0fee18a.coldcopy-au3.pages.dev/api/generate`
- Method: POST
- Frequency: 5 minutes
- Friendly Name: "ColdCopy Production - API Endpoint"
- Request Body (raw JSON):
  ```json
  {
    "companyName": "HealthCheck",
    "targetJobTitle": "Test",
    "problemTheyFace": "Monitoring",
    "yourProduct": "ColdCopy",
    "keyBenefit": "Email sequences",
    "callToAction": "Demo",
    "tone": "Professional"
  }
  ```
- Expected HTTP status: 200
- Alert Email: [your-email@example.com]
- Save

3. Dashboard available at: https://uptimerobot.com/dashboard

**Free Tier Limits:**
- 50 monitors
- 5-minute checks
- Email + webhook alerts
- No API

---

### Option 2: Healthchecks.io (Alternative - Free Tier)

If UptimeRobot doesn't work, use Healthchecks.io (https://healthchecks.io).

**Setup:**
1. Sign up (free tier = 20 checks)
2. Create check:
   - Name: "ColdCopy Main Page"
   - Timeout: 60 seconds
   - Grace period: 60 seconds
3. Copy the check URL
4. Test: `curl https://hc-ping.com/[check-uuid]`
5. Set up cron job or GitHub Actions to ping every 5 minutes:

```bash
# GitHub Actions workflow: .github/workflows/health-check.yml
name: Health Check

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check ColdCopy Main
        run: |
          curl -s -o /dev/null -w "Status: %{http_code}\n" \
            https://e0fee18a.coldcopy-au3.pages.dev
      - name: Check ColdCopy API
        run: |
          curl -s -X POST \
            -H "Content-Type: application/json" \
            -d '{"companyName":"Check","targetJobTitle":"Test","problemTheyFace":"Monitor","yourProduct":"ColdCopy","keyBenefit":"Test","callToAction":"Demo","tone":"Professional"}' \
            https://e0fee18a.coldcopy-au3.pages.dev/api/generate \
            -o /dev/null -w "Status: %{http_code}\n"
```

---

## Manual Monitoring Commands

For on-demand checks without external services:

**Check Main Page:**
```bash
curl -s -o /dev/null -w "HTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  https://e0fee18a.coldcopy-au3.pages.dev
```

**Check API Endpoint:**
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Test Corp",
    "targetJobTitle": "VP Marketing",
    "problemTheyFace": "Low conversion",
    "yourProduct": "Analytics tool",
    "keyBenefit": "Real-time insights",
    "callToAction": "Book demo",
    "tone": "Professional"
  }' \
  https://e0fee18a.coldcopy-au3.pages.dev/api/generate \
  -o /dev/null -w "HTTP Status: %{http_code}\nTime: %{time_total}s\n"
```

**Expected Responses:**
- Main page: HTTP 200 (< 500ms typical)
- API endpoint: HTTP 200 with JSON response (3-5s typical)

---

## Monitoring Checklist

Run this checklist daily during MVP phase:

**Monday-Friday:**
- [ ] Check UptimeRobot dashboard (no down alerts)
- [ ] Test main page manually: `curl -I https://e0fee18a.coldcopy-au3.pages.dev`
- [ ] Test API manually: `curl -X POST https://e0fee18a.coldcopy-au3.pages.dev/api/generate ...`
- [ ] Review email alerts (if any)

**Issues Found:**
- If down <5 minutes: Likely Cloudflare transient, check again in 2 min
- If down >5 minutes: Check Cloudflare status page → Logs → GitHub for recent changes
- If API returning errors: Check Cloudflare Functions logs + ANTHROPIC_API_KEY validity

---

## Integration with Runbooks

**Alert Received:** "ColdCopy Down"

1. **Immediate Actions (First 2 minutes):**
   - Confirm with manual check: `curl -I https://e0fee18a.coldcopy-au3.pages.dev`
   - Check Cloudflare Pages status: https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages
   - Check GitHub Actions (build failures): https://github.com/JianouJiang/coldcopy/actions

2. **If Still Down (2-5 minutes):**
   - Check build logs in Cloudflare Pages
   - Check recent commits: `git log --oneline -5`
   - Review function logs in Cloudflare dashboard

3. **If API Specific (200 OK but API errors):**
   - Check ANTHROPIC_API_KEY in Cloudflare secrets
   - Check Claude API status: https://status.anthropic.com
   - Review function execution logs

4. **Recovery:**
   - If code issue: Fix code, `git push` (auto-redeploys)
   - If API key issue: Update secret in Cloudflare dashboard
   - If Cloudflare issue: Check https://www.cloudflarestatus.com

---

## Escalation

- **No response within 30 mins:** Create GitHub issue with timestamp + error details
- **Revenue impact:** Revert latest deployment: `git revert HEAD && git push`

---

## Log Retention

- UptimeRobot: 90 days free
- Healthchecks.io: 30 days free
- Cloudflare Pages logs: 3 days (check immediately, then save to docs)

**Weekly Export:** Save important incidents to `docs/devops/incidents/` with timestamp + root cause

---

**Setup Date:** 2026-02-20
**Monitor Frequency:** Every 5 minutes
**Alert Method:** Email + Slack (if integrated)
**Critical Threshold:** Any downtime = immediate alert
