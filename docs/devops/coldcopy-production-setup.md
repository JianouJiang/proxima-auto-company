# ColdCopy Production Setup Guide

**Date:** 2026-02-20
**DevOps Engineer:** Kelsey Hightower
**Status:** Ready for deployment

---

## Architecture Overview

```
User Browser
    ↓
Cloudflare Pages (Frontend + Functions)
    ├─ Frontend: React + Vite (static)
    ├─ Functions: TypeScript handlers
    │  ├─ POST /api/generate (Claude integration)
    │  └─ GET /api/session (session state)
    ├─ D1 Database (SQLite)
    │  ├─ sessions table
    │  └─ sequences table
    └─ KV Namespace (rate limiting)
         └─ rate_limit:{sessionId}
    ↓
Claude Haiku 4.5 API (email generation)
```

---

## Infrastructure IDs (Production)

| Service | ID | Binding | Status |
|---------|----|---------| -------|
| D1 Database | 413b402d-f259-4b79-b7e4-3ab887c8a431 | DB | Live |
| KV Namespace | 82359391e9704000a8d5f1efadf9b27f | RATE_LIMIT | Live |
| Pages Project | coldcopy | - | Live |
| GitHub Repo | JianouJiang/coldcopy | main branch | Live |

---

## Database Schema

### sessions table

```sql
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  plan TEXT DEFAULT 'free' NOT NULL,
  generations_used INTEGER DEFAULT 0 NOT NULL,
  max_generations INTEGER DEFAULT 1 NOT NULL,
  created_at TEXT DEFAULT (datetime('now')) NOT NULL,
  updated_at TEXT DEFAULT (datetime('now')) NOT NULL
);
```

**Purpose:** Track anonymous user sessions and quota usage
**Trigger:** Created on first /api/generate POST
**Lifecycle:** 90 days via HttpOnly cookie

### sequences table

```sql
CREATE TABLE sequences (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  input JSON NOT NULL,
  output JSON NOT NULL,
  created_at TEXT DEFAULT (datetime('now')) NOT NULL,
  FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

**Purpose:** Store generated email sequences
**Input:** { companyName, targetJobTitle, problemTheyFace, yourProduct, keyBenefit, callToAction, tone }
**Output:** { emails: [{ subjectLineA, subjectLineB, body }, ...] }

---

## API Endpoints

### POST /api/generate

Generates a 7-email cold sequence using Claude Haiku 4.5.

**Request:**
```json
{
  "companyName": "Acme Analytics",
  "targetJobTitle": "VP of Marketing",
  "problemTheyFace": "They lose 30-40% of revenue to cart abandonment",
  "yourProduct": "Real-time analytics dashboard for e-commerce",
  "keyBenefit": "Identify why 60% of carts abandon",
  "callToAction": "Book a 15-min demo",
  "tone": "Professional"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "sequenceId": "seq-xyz-123",
  "sequence": {
    "emails": [
      {
        "subjectLineA": "60% of your carts are leaking",
        "subjectLineB": "Cart abandonment analysis in 30 seconds",
        "body": "Hi [FirstName],\n\nMost e-commerce leaders..."
      },
      // ... 6 more emails
    ]
  }
}
```

**Error Responses:**
- 400: Invalid input (missing required field)
- 402: Rate limit exceeded (user must upgrade)
- 504: Claude API timeout (>25 seconds)
- 500: Server error (validation failure, JSON parse error)

**Latency:** 3-5 seconds typical (Claude Haiku)

### GET /api/session

Returns current session state (quota, plan, generation count).

**Success Response (200):**
```json
{
  "plan": "free",
  "generationsUsed": 0,
  "maxGenerations": 1,
  "canGenerate": true
}
```

**Note:** Returns default state if no session cookie (prevents leaking session data).

---

## Session Management

### HttpOnly Cookies

```
Set-Cookie: coldcopy_session={uuid}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=7776000
```

- **HttpOnly:** Prevents JavaScript access (XSS mitigation)
- **Secure:** HTTPS only (production only)
- **SameSite=Lax:** CSRF protection
- **Max-Age=7776000:** 90 days (reasonable for anonymous session)

### Session Lifecycle

1. User visits /generate page → no session created (zero D1 writes)
2. User submits form → /api/generate checks for coldcopy_session cookie
3. If no cookie:
   - Generate UUID v4
   - INSERT into sessions table with plan='free', max_generations=1
   - Set HttpOnly cookie (90 days)
   - Proceed with generation
4. If cookie exists:
   - Look up session in D1
   - Check generations_used < max_generations
   - Continue or reject with 402 (rate limit exceeded)

---

## Rate Limiting

### KV Storage

**Key format:** `rate_limit:{sessionId}`
**Value:** Counter (integer as string)
**TTL:** 3600 seconds (1 hour)

### Rate Limit Logic

```typescript
const key = `rate_limit:${sessionId}`;
const count = await env.RATE_LIMIT.get(key);

if (count === null) {
  // First request this hour
  await env.RATE_LIMIT.put(key, '1', { expirationTtl: 3600 });
  return true; // Allow
} else if (parseInt(count, 10) >= 1) {
  return false; // Rate limit exceeded
} else {
  // Increment and allow
  await env.RATE_LIMIT.put(key, String(parseInt(count, 10) + 1), {
    expirationTtl: 3600,
  });
  return true; // Allow
}
```

### Free Plan Quota

- 1 generation per session
- Resets every hour (via KV TTL)
- Enforced per-session, not per-IP (prevents abuse)

### Known Race Condition

Read-then-write on KV can race under concurrent requests. At MVP scale, might let 1-2 extra requests through per hour. Cost: $0.011 per overage (negligible). Fix requires Durable Objects (paid tier).

---

## Claude API Integration

### Model

- **Name:** Claude Haiku 4.5
- **ID:** claude-3-5-haiku-20241022
- **Max Tokens:** 4096 (typically 2-2.5K output for 7 emails)
- **Cost:** $0.011 per generation

### Timeout

- **Request Timeout:** 25 seconds (CloudFlare Workers free tier = 30-second wall-clock limit)
- **Abort Strategy:** AbortController aborts at 25s, prevents stalled requests

### Prompt Engineering

**System Prompt:**
```
You are an expert cold email copywriter for B2B SaaS products.
Your task is to generate a 7-email cold email sequence that:
- Opens doors (gets meetings, not spam-folder fodder)
- Uses specific SaaS hooks (trial CTAs, demo hooks, technical credibility)
- Is copy-paste ready for tools like Lemlist, Instantly, Apollo
- Includes A/B subject line variants for each email

Generate exactly 7 emails. Each email must have two A/B subject line variants and a body.

IMPORTANT: Respond with ONLY valid JSON, no preamble or explanation.
Do not include markdown code blocks or any text outside the JSON.
```

**User Prompt:** Includes all form inputs in structured format

### Response Validation

1. Strip text before first `{` and after last `}` (preamble/postamble removal)
2. JSON.parse() with error handling
3. Validate structure:
   - emails array exists and non-empty
   - each email has subjectLineA, subjectLineB, body (all strings)
4. Retry once on JSON parse failure
5. Return user error if both attempts fail

---

## Configuration Files

### wrangler.toml

```toml
name = "coldcopy"
pages_build_output_dir = "frontend/dist"
functions_dir = "functions"

[[d1_databases]]
binding = "DB"
database_name = "coldcopy-db"
database_id = "413b402d-f259-4b79-b7e4-3ab887c8a431"

[[kv_namespaces]]
binding = "RATE_LIMIT"
id = "82359391e9704000a8d5f1efadf9b27f"
```

### tsconfig.json (functions)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ES2022",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "allowJs": true
  },
  "include": ["functions/**/*.ts"],
  "exclude": ["node_modules", "frontend"]
}
```

### package.json (root)

```json
{
  "name": "coldcopy",
  "version": "1.0.0",
  "type": "module",
  "description": "ColdCopy - AI-powered cold email sequence generator",
  "scripts": {
    "build": "cd frontend && npm run build",
    "dev": "cd frontend && npm run dev"
  },
  "devDependencies": {
    "typescript": "^5.3.3"
  },
  "dependencies": {
    "uuid": "^9.0.1"
  }
}
```

---

## Secrets (Required for Production)

### ANTHROPIC_API_KEY

**Status:** Must be set before production use

**Location:** Pages > coldcopy > Settings > Environment variables (Production)

**Value:** Your Anthropic API key (starts with sk-ant-)

**How to set via Dashboard:**
1. https://dash.cloudflare.com/
2. Pages > coldcopy > Settings
3. Environment variables > Production
4. Add variable: ANTHROPIC_API_KEY
5. Paste key value
6. Save

**Verification:**
```bash
npx wrangler pages secret list --project-name coldcopy
```

---

## Deployment Pipeline

### Automatic Deployment (GitHub Integration)

1. Push to main branch: `git push`
2. GitHub triggers Cloudflare Pages build
3. Build command: `npm run build` (runs frontend build)
4. Pages Functions are auto-compiled from /functions directory
5. Frontend + Functions deployed to https://coldcopy-au3.pages.dev

### Manual Deployment

```bash
cd projects/coldcopy
npx wrangler pages deploy --project-name coldcopy
```

### Rollback

1. Identify issue from Dashboard logs
2. Fix code locally
3. Commit and push (triggers new deployment)
4. Or revert: `git revert HEAD && git push`

---

## Monitoring

### Cloudflare Dashboard

**URL:** https://dash.cloudflare.com/68ec8b1ccccb48e1a7cf898d2228c713/pages

View:
- Deployments: Status, build logs, previous versions
- Analytics: Request latency, error rate, caching
- Functions: Execution time, errors

### Key Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Pages response time | <200ms | >1000ms |
| D1 query latency | <100ms | >500ms |
| KV lookup latency | <50ms | >200ms |
| Claude API latency | <5s | >20s |
| Error rate | <1% | >5% |

### Error Investigation

Check Pages dashboard logs:
```
status:500 OR error
```

---

## Cost Estimate (7-day MVP)

| Service | Cost | Usage |
|---------|------|-------|
| D1 Database | $0 | 0.04MB / 500MB free |
| KV Namespace | $0 | 100 writes/day / 1,000 free |
| Pages Functions | $0 | 500 requests/day / 100,000 free |
| Claude Haiku | ~$7.70 | 100 gen/day × 7 days × $0.011 |
| **Total** | **~$8** | Free tier + minimal API costs |

---

## Security Checklist

- [x] ANTHROPIC_API_KEY in Pages secrets (not hardcoded)
- [x] HttpOnly cookies (prevents XSS)
- [x] D1 as source of truth (prevents replay attacks)
- [x] Rate limiting per-session (prevents abuse)
- [x] 25-second timeout on Claude API (prevents stalled requests)
- [x] Input validation on form (prevents injection)
- [x] No CORS headers needed (same origin)

---

## Troubleshooting

### Pages Functions returning 404

**Check:**
1. Functions directory exists: `functions/api/`
2. `functions_dir = "functions"` in wrangler.toml
3. Latest deployment successful

**Fix:** `git push` (retrigger deployment)

### D1 Connection Errors

**Check:**
1. Database ID matches wrangler.toml
2. Schema migrated: `npx wrangler d1 execute coldcopy-db --file schema.sql --remote`
3. Binding name is "DB" in code and config

### Rate Limit Not Working

**Check:**
1. KV namespace ID correct
2. Binding name is "RATE_LIMIT"
3. Test: `npx wrangler kv key list --binding RATE_LIMIT`

### Claude API Timeout

**Check:**
1. ANTHROPIC_API_KEY set correctly
2. Request payload is valid JSON
3. Timeout is 25 seconds

---

## Local Development

### Prerequisites

```bash
node --version  # v18+
npm --version
npx --version
```

### Setup

```bash
cd projects/coldcopy

# Install dependencies
npm install
cd frontend && npm install && cd ..

# Create .dev.vars for local secrets
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .dev.vars
```

### Development Servers

**Terminal 1: Frontend (Vite)**
```bash
cd frontend
npm run dev
# → http://localhost:5173
```

**Terminal 2: Backend (Cloudflare Pages)**
```bash
npx wrangler pages dev frontend/dist
# → http://localhost:8788
```

Vite proxy forwards /api/* requests to backend (http://localhost:8788)

### Build

```bash
npm run build
# Outputs: frontend/dist/
```

### Database Commands

```bash
# List databases
npx wrangler d1 list

# Execute query
npx wrangler d1 execute coldcopy-db --command "SELECT * FROM sessions"

# Local database (for testing)
npx wrangler d1 execute coldcopy-db --file schema.sql
```

### KV Commands

```bash
# List keys
npx wrangler kv key list --binding RATE_LIMIT

# Get value
npx wrangler kv key get "rate_limit:session-id" --binding RATE_LIMIT

# Delete key
npx wrangler kv key delete "rate_limit:session-id" --binding RATE_LIMIT
```

---

## Project Structure

```
projects/coldcopy/
├── functions/                 # Pages Functions (TypeScript)
│   └── api/
│       ├── generate.ts       # POST /api/generate
│       └── session.ts        # GET /api/session
├── frontend/                  # React + Vite
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Generate.tsx  # Form page
│   │   │   └── Output.tsx    # Results page
│   │   ├── components/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── dist/                 # Built output
│   ├── package.json
│   └── tsconfig.json
├── schema.sql                # D1 schema
├── wrangler.toml            # Cloudflare configuration
├── tsconfig.json            # Root TypeScript config
├── package.json             # Root package (scripts + uuid)
└── README.md
```

---

**Deployment Manager:** Kelsey Hightower
**Last Updated:** 2026-02-20
**Status:** Ready for production (awaiting API key)
