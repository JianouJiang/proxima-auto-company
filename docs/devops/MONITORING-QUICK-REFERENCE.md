# ColdCopy Monitoring Quick Reference

**Print this. Put on wall. Keep near desk.**

---

## Daily Checks (5 minutes)

```bash
# 1. Is it up?
curl -I https://e0fee18a.coldcopy-au3.pages.dev
# Expected: HTTP/1.1 200 OK

# 2. Is the API working?
curl -X POST https://e0fee18a.coldcopy-au3.pages.dev/api/generate \
  -H "Content-Type: application/json" \
  -d '{"companyName":"Test","targetJobTitle":"Test",...}'
# Expected: HTTP/1.1 200 + JSON with emails array

# 3. Check email alerts
# (UptimeRobot sends alerts automatically if down)
```

---

## Weekly Checks (Friday, 15 minutes)

```bash
# 1. UptimeRobot Dashboard
# Visit: https://uptimerobot.com/dashboard
# Check: Any downtime? Any alerts?

# 2. Cloudflare Usage
# Visit: https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages
# Check: Request count, error rate, response time

# 3. Claude API Cost
# Visit: https://console.anthropic.com/account/usage
# Check: Daily cost trend. Alert if >$5/day

# 4. Database Health
npx wrangler d1 execute coldcopy-db --command "SELECT COUNT(*) FROM sessions"
# Expected: Count should grow slowly (1-5 new sessions/day)

# 5. Fill weekly health report
# Template: docs/devops/weekly-health-report-template.md
# Takes: 10 minutes
# Send to: CEO
```

---

## If Something's Wrong

### Production URL Returns 500 Error

1. Check Cloudflare dashboard → Pages → coldcopy → Logs
2. Search: `status:500`
3. Common causes:
   - `ANTHROPIC_API_KEY` not set → Fix in Cloudflare secrets
   - Database schema missing → Run migration
   - Function code error → Check git logs, rollback if needed

### API Returns 504 (Timeout)

1. Normal if occasional (Claude API slow)
2. If frequent (>5/hour):
   - Check Claude API status: https://status.anthropic.com
   - Check if large requests (lots of context)
   - May need to reduce timeout tolerance

### High API Cost (>$5/day)

1. Check https://console.anthropic.com/account/usage
2. If spiking:
   - Check Cloudflare logs for bot/scraper activity
   - Verify rate limiting is working
   - Check for infinite loops in code
3. If confirmed abuse:
   - Disable endpoint: Comment out Claude call in functions/api/generate.ts
   - Deploy: `git push`
   - Investigate: Check logs for suspicious patterns

### Database Error

1. Check binding name is "DB" in wrangler.toml
2. Verify database ID matches:
   ```bash
   npx wrangler d1 list
   ```
3. If still broken:
   - Schema might be missing
   - Run: `npx wrangler d1 execute coldcopy-db --file schema.sql --remote`

---

## Alert Thresholds

| Alert | Threshold | Action | Who |
|-------|-----------|--------|-----|
| Downtime | Any | Check logs, investigate | DevOps |
| High error rate | >10 errors/hour | Check dashboard | DevOps |
| API slow | >5s average | Monitor, may be transient | DevOps |
| High cost | >$5/day | Investigate usage | DevOps + CEO |
| Critical cost | >$20/day | Kill endpoint, freeze | CEO |

---

## Key Contacts

- **Uptime Down:** Check UptimeRobot alert email
- **Errors:** Check Cloudflare dashboard
- **Cost Spike:** Check Anthropic console
- **Can't figure it out:** Check docs/devops/error-tracking-guide.md

---

## Useful Commands

```bash
# Check main page health
curl -s -o /dev/null -w "HTTP %{http_code} in %{time_total}s\n" \
  https://e0fee18a.coldcopy-au3.pages.dev

# Check API health
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{...}' \
  https://e0fee18a.coldcopy-au3.pages.dev/api/generate | jq '.success'

# Check database size
npx wrangler d1 list

# Count sessions
npx wrangler d1 execute coldcopy-db --command "SELECT COUNT(*) FROM sessions"

# Check cost from Anthropic API (if authenticated)
curl -s https://api.anthropic.com/v1/beta/usage \
  -H "x-api-key: $ANTHROPIC_API_KEY" | jq '.daily_cost'
```

---

## Dashboards to Bookmark

- **UptimeRobot:** https://uptimerobot.com/dashboard
- **Cloudflare:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages
- **Anthropic:** https://console.anthropic.com/account/usage
- **GitHub:** https://github.com/JianouJiang/coldcopy

---

## Documentation

Full runbooks in: `docs/devops/`

- `uptime-monitoring-setup.md` — How to set up monitoring
- `error-tracking-guide.md` — How to find and fix errors
- `cost-monitoring-guide.md` — How to track costs
- `weekly-health-report-template.md` — Weekly check template
- `CYCLE-8-MONITORING-COMPLETE.md` — Setup summary

---

**Last Updated:** 2026-02-20
**Status:** Production monitoring active
**Next Review:** Friday, 2026-02-27
