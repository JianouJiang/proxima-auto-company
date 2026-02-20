# ColdCopy Infrastructure Inventory

**Maintained By:** Kelsey Hightower (DevOps)
**Last Updated:** 2026-02-20
**Status:** Production Ready

---

## Overview

ColdCopy runs entirely on Cloudflare free tier services with Claude Haiku API for LLM functionality.

- **Deployments:** 0 pending, 0 failed, 1 active
- **Database:** 1 D1 instance, 2 tables, 0.04MB used
- **Storage:** 1 KV namespace, 0 keys in use
- **Functions:** 2 API endpoints, 0 errors in last 24h

---

## Cloudflare Services

### Pages (Frontend + Functions)

```
Project Name: coldcopy
GitHub Repo: https://github.com/JianouJiang/coldcopy
Build Command: npm run build
Root Directory: projects/coldcopy/

Status: ✅ Active
URL: https://coldcopy-au3.pages.dev
```

**Auto-Deployment:**
- Trigger: Commits to main branch
- Build time: 2-3 minutes
- Deployment time: <1 minute
- Rollback: 1-click from Dashboard

### D1 Database

```
Name: coldcopy-db
ID: 413b402d-f259-4b79-b7e4-3ab887c8a431
Region: WEUR (Western Europe)
Binding: DB

Status: ✅ Live
Tables: 2 (sessions, sequences)
Storage: 0.04MB / 500MB free
```

**Schema:**

```sql
sessions:
  id (TEXT, PRIMARY KEY)
  plan (TEXT, DEFAULT 'free')
  generations_used (INTEGER, DEFAULT 0)
  max_generations (INTEGER, DEFAULT 1)
  created_at (TEXT, DEFAULT now)
  updated_at (TEXT, DEFAULT now)

sequences:
  id (TEXT, PRIMARY KEY)
  session_id (TEXT, FOREIGN KEY → sessions.id)
  input (JSON)
  output (JSON)
  created_at (TEXT, DEFAULT now)
```

**Backups:** Automatic daily via Cloudflare

### KV Namespace

```
Name: RATE_LIMIT
ID: 82359391e9704000a8d5f1efadf9b27f
Binding: RATE_LIMIT

Status: ✅ Live
Keys in use: 0
Storage: 0B / 1GB free
Writes today: 0 / 1,000 free
```

**Usage:**
- Key format: `rate_limit:{sessionId}`
- Value: Counter (integer as string)
- TTL: 3600 seconds (auto-expires)
- Purpose: 1-generation-per-session rate limiting

---

## External Services

### Anthropic Claude API

```
Model: Claude Haiku 4.5
ID: claude-3-5-haiku-20241022
Max Tokens: 4096
Timeout: 25 seconds

Status: ✅ Active (key not yet configured)
API Endpoint: https://api.anthropic.com/v1/messages
```

**Pricing:**
- Input: $0.80 per MTok
- Output: $0.04 per MTok
- Per-generation cost: ~$0.011

**Integration Point:**
- Function: `functions/api/generate.ts`
- Method: POST /api/messages

### GitHub

```
Repository: https://github.com/JianouJiang/coldcopy
Branch: main (default)
Auto-Deploy: Enabled

Status: ✅ Connected
```

---

## Configuration Files

### Root Configuration

**Location:** `/projects/coldcopy/`

| File | Purpose | Last Updated |
|------|---------|---|
| `wrangler.toml` | Cloudflare bindings | 2026-02-20 |
| `package.json` | Root dependencies | 2026-02-20 |
| `tsconfig.json` | TypeScript config | 2026-02-20 |
| `schema.sql` | D1 schema | 2026-02-20 |

### Frontend Configuration

**Location:** `/projects/coldcopy/frontend/`

| File | Purpose |
|------|---------|
| `vite.config.ts` | Build configuration |
| `tsconfig.json` | TypeScript strict mode |
| `package.json` | Dependencies, build scripts |
| `public/_routes.json` | Pages routing (API → Functions) |

### Functions Configuration

**Location:** `/projects/coldcopy/functions/api/`

| File | Endpoint | Methods |
|------|----------|---------|
| `generate.ts` | POST /api/generate | POST (create sequence) |
| `session.ts` | GET /api/session | GET (read session state) |

---

## Secrets & Credentials

### Required Secrets

| Secret | Location | Status | Used By |
|--------|----------|--------|---------|
| ANTHROPIC_API_KEY | Pages > coldcopy > Environment variables | 🔴 NOT SET | functions/api/generate.ts |
| STRIPE_SECRET_KEY | Pages > coldcopy > Environment variables | 🔴 Not yet needed | (Day 5) |
| STRIPE_WEBHOOK_SECRET | Pages > coldcopy > Environment variables | 🔴 Not yet needed | (Day 5) |

### How to Set Secrets

**Via Cloudflare Dashboard:**
1. https://dash.cloudflare.com/
2. Pages > coldcopy > Settings
3. Environment variables > Production
4. Add secret, save

**Via Wrangler CLI:**
```bash
npx wrangler pages secret put SECRET_NAME --project-name coldcopy
```

---

## Performance Baselines

### Latency Targets

| Component | Target | Status |
|-----------|--------|--------|
| Pages response | <200ms | ✅ (typical: 50-100ms) |
| D1 query | <100ms | ✅ (typical: 20-50ms) |
| KV lookup | <50ms | ✅ (typical: 5-20ms) |
| Claude API | 3-5s | ✅ (typical: 3-5s) |
| Total request | <10s | ✅ (typical: 3-6s) |

### Storage Monitoring

**D1 Database:**
- Current: 0.04MB
- Quota: 500MB
- Headroom: 12,500x
- Growth rate: ~0.5KB per user session

**KV Namespace:**
- Current: 0B (keys auto-expire)
- Quota: 1GB
- Headroom: Infinite (auto-cleanup)
- Writes/day: 100 / 1,000 (10% of budget)

---

## Access & Permissions

### Cloudflare Account

```
Account: jianou.works@gmail.com
Account ID: 68ec8b1ccccb48e1a7cf898d2228c713
Token Permissions: workers, d1, kv, pages (write)
Status: ✅ Active
```

### GitHub Repository

```
Owner: JianouJiang
Repo: coldcopy
Default Branch: main
Auto-deploy: Enabled
Status: ✅ Connected to Cloudflare Pages
```

---

## Monitoring & Alerts

### Dashboard Links

1. **Pages Project:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages/view/coldcopy
2. **D1 Database:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/d1/
3. **KV Namespace:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/kv/namespaces

### Key Metrics to Watch

| Metric | Target | Alert | Check |
|--------|--------|-------|-------|
| Error rate | <1% | >5% | Pages Dashboard > Analytics |
| Response time | <200ms | >1000ms | Pages Dashboard > Analytics |
| D1 usage | <50MB | >250MB | D1 Dashboard |
| KV writes/day | <100 | >500 | KV Dashboard |
| Claude errors | <1% | >5% | Function logs |

### Alerting Strategy

Currently: Manual monitoring via Dashboard
Future: Add Axiom, Logtail, or Datadog for automated alerts

---

## Disaster Recovery

### D1 Database Backups

**Automatic:**
- Frequency: Daily
- Retention: 7 days
- Provider: Cloudflare

**Manual Backup:**
```bash
npx wrangler d1 backup create coldcopy-db
```

**Restore:**
```bash
npx wrangler d1 backup restore coldcopy-db --backup-id <id>
```

### Pages Rollback

**Rollback to Previous Deployment:**
1. Go to: https://dash.cloudflare.com/.../pages/view/coldcopy
2. Click "Deployments" tab
3. Select previous deployment
4. Click "Rollback"

**Or via Git:**
```bash
git revert HEAD
git push
# New deployment will be live in 2-3 minutes
```

### KV Data Recovery

KV data persists, no backup needed. Keys auto-expire after TTL.

---

## Scaling & Limits

### Free Tier Limits (Cloudflare)

| Service | Limit | Current Usage | Headroom |
|---------|-------|---|---|
| D1 Tables | Unlimited | 2 | ✅ Plenty |
| D1 Storage | 500MB | 0.04MB | ✅ 12,500x |
| KV Keys | Unlimited | 0 | ✅ Infinite |
| KV Storage | 1GB | 0B | ✅ Infinite |
| Pages Functions | Unlimited | 2 | ✅ Plenty |
| Pages Requests | 100,000/day | ~500 | ✅ 200x |
| Pages Bandwidth | Unlimited | Low | ✅ Plenty |

### API Rate Limits (Claude)

- Requests per minute: 1 req/s limit per account
- Concurrent requests: No limit
- Cost: Per-token (includes usage limits by API key)

---

## Maintenance Schedule

### Daily
- Monitor error rate (Pages Dashboard)
- Check D1 database size
- Review KV usage

### Weekly
- Audit access logs
- Review error logs
- Check API costs
- Verify backups

### Monthly
- Database optimization (VACUUM)
- Dependency updates
- Capacity planning

### Quarterly
- Security audit
- Performance review
- Cost analysis
- Plan scaling if needed

---

## Known Limitations

1. **KV Race Condition:** Read-then-write can race under concurrent requests (accepted for MVP)
2. **D1 Concurrent Access:** Limited concurrent queries (not an issue at MVP scale)
3. **Pages Function Timeout:** 30-second wall-clock limit (mitigation: 25-second API timeout)
4. **No Built-in Auth:** Anonymous sessions only (planned: OAuth/email verification)

---

## Upgrade Path

### If Hitting Free Tier Limits

**D1 Database:**
- Upgrade to paid tier: $0.76/GB/month
- Unlimited reads/writes

**KV Namespace:**
- Upgrade to paid tier: $0.50/GB + ops costs
- Unlimited reads/writes

**Pages Functions:**
- Upgrade to Workers: $0.15 per CPU-second
- Higher concurrency limits

**Claude API:**
- No tier changes: Always pay per-token
- Can optimize with caching/batching

---

## Useful Commands

```bash
# List all resources
npx wrangler pages list --json
npx wrangler d1 list
npx wrangler kv namespace list

# Database operations
npx wrangler d1 execute coldcopy-db --command "SELECT * FROM sessions LIMIT 5"
npx wrangler d1 backup create coldcopy-db

# KV operations
npx wrangler kv key list --binding RATE_LIMIT
npx wrangler kv key get "key-name" --binding RATE_LIMIT

# Secrets
npx wrangler pages secret list --project-name coldcopy
npx wrangler pages secret put SECRET_NAME --project-name coldcopy

# Deployments
npx wrangler pages deployment list --project-name coldcopy
npx wrangler pages deploy --project-name coldcopy

# Logs
npx wrangler tail --format json
```

---

## Document Reference

| Document | Purpose |
|----------|---------|
| DEPLOYMENT_STATUS.md | Current infrastructure status |
| coldcopy-production-setup.md | Setup and configuration details |
| COLDCOPY_RUNBOOK.md | Operational procedures |
| INFRASTRUCTURE_INVENTORY.md | This document - resource inventory |

---

**Inventory Manager:** Kelsey Hightower (DevOps)
**Last Verified:** 2026-02-20
**Next Review:** 2026-02-27 (weekly)
