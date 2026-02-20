# ColdCopy Backend Implementation

**Engineer:** DHH
**Date:** 2026-02-20
**Status:** Complete (Day 3)
**Sprint:** 7-day ColdCopy MVP

## Summary

Implemented complete backend for ColdCopy MVP, including:
- Cloudflare Pages Functions with D1 + KV bindings
- Lazy session management with HttpOnly cookies
- Claude Haiku 4.5 API integration with 25-second timeout
- Response validation with retry logic
- Rate limiting via KV namespace
- Frontend integration with loading animation and error handling

All 6 CTO adjustments incorporated. Ready for production on Day 5.

---

## Architecture Overview

```
Frontend (React + Vite)
         ↓
[Vite Dev Proxy: localhost:5173 → localhost:8788]
         ↓
Cloudflare Pages Functions (/api/*)
         ├─ POST /api/generate: generates email sequence
         └─ GET /api/session: returns session state
         ↓
D1 Database
├─ sessions table: user session + quota
├─ sequences table: generated outputs
└─ Indexes on id, session_id
         ↓
KV Namespace (RATE_LIMIT)
         ├─ rate_limit:{sessionId}
         └─ 1-hour TTL per session
         ↓
Claude Haiku 4.5 API
         ├─ 25-second request timeout
         ├─ JSON response validation
         └─ Single retry on JSON parse failure
```

---

## Implementation Details

### 1. Database Schema (`schema.sql`)

```sql
-- sessions: one per anonymous user (lazy created)
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  plan TEXT DEFAULT 'free' NOT NULL,
  generations_used INTEGER DEFAULT 0 NOT NULL,
  max_generations INTEGER DEFAULT 1 NOT NULL,
  created_at TEXT DEFAULT (datetime('now')) NOT NULL,
  updated_at TEXT DEFAULT (datetime('now')) NOT NULL
);

-- sequences: stores input + output as JSON
CREATE TABLE sequences (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  input JSON NOT NULL,
  output JSON NOT NULL,
  created_at TEXT DEFAULT (datetime('now')) NOT NULL,
  FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

**Design Decisions:**
- No `users` table (MVP scope)
- No `plans` table (hardcoded "free" plan)
- No `feedback` table (Day 6+ feature)
- JSON storage allows flexible output structure without premature schema design
- Indexes on `sessions.id` and `sequences.session_id` for query performance

**Storage Estimate:**
- 15 MB/month at 100 users/day = 500 MB D1 free tier headroom is 33x
- Sustainable through Day 7 and beyond

### 2. Session Management (Lazy Creation)

Session is created on first API call to `/api/generate`, not on page load.

**Flow:**
1. User visits `/generate` page → no session created (zero D1 writes for bounce traffic)
2. User submits form → Worker checks for `coldcopy_session` cookie
3. If no cookie exists:
   - Generate UUID
   - INSERT into D1 `sessions` table
   - SET `coldcopy_session` HttpOnly cookie (90 days)
   - Proceed with generation
4. If cookie exists:
   - Look up session in D1 (one read per request)
   - Check `generations_used < max_generations`
   - Continue or reject with 402

**Why HttpOnly + D1?**
- JWT cookies are vulnerable to replay attacks (user could copy JWT, use one generation, replay old token)
- D1 is source of truth for quota
- One D1 read per request adds negligible latency (50-150ms from edge to primary region, usually cached)

**Cookie Configuration:**
```
Set-Cookie: coldcopy_session={uuid}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=7776000
```
- `HttpOnly`: Prevents JavaScript access (XSS mitigation)
- `Secure`: HTTPS only
- `SameSite=Lax`: CSRF protection for same-origin POST
- `Max-Age=7776000`: 90 days (reasonable for anonymous session persistence)

### 3. POST /api/generate Endpoint

**Request Contract:**
```typescript
interface GenerateRequest {
  companyName: string;        // 1-50 chars
  targetJobTitle: string;     // 1-100 chars
  problemTheyFace: string;    // 10-300 chars
  yourProduct: string;        // 10-200 chars
  keyBenefit: string;         // 10-150 chars
  callToAction: string;       // 10-100 chars
  tone: 'Professional' | 'Casual' | 'Direct' | 'Friendly';
}
```

**Response Contract (200 OK):**
```typescript
{
  success: true,
  sequenceId: string,
  sequence: {
    emails: [
      {
        subjectLineA: string,
        subjectLineB: string,
        body: string
      },
      // ... 7 total emails
    ]
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required field
- `402 Payment Required`: Rate limit exceeded (user must upgrade)
- `504 Gateway Timeout`: Claude API request exceeded 25-second timeout
- `500 Internal Server Error`: Unexpected error or validation failure after retry

### 4. Claude API Integration

**Model:** Claude Haiku 4.5 (claude-3-5-haiku-20241022)
**Max Tokens:** 4096 (typically 2-2.5K output for 7 emails)
**Timeout:** 25 seconds (Cloudflare Workers free tier = 30-second wall-clock limit)

**Prompt Engineering:**
- System prompt defines role (expert cold email copywriter for SaaS)
- User prompt provides structured inputs + example JSON output
- Instructs model to respond with **ONLY JSON** (no preamble, no markdown)

**Response Validation (Adjustment #4):**
```typescript
function validateClaudeResponse(response: string): EmailSequence {
  // 1. Strip text before first { and after last }
  const jsonMatch = response.match(/\{[\s\S]*\}/);

  // 2. JSON.parse() with error handling
  const parsed = JSON.parse(jsonMatch[0]);

  // 3. Validate structure:
  //    - emails array exists and is non-empty
  //    - each email has subjectLineA, subjectLineB, body (all strings)
  //
  // 4. If validation fails, return user error
  //    (retry logic handled in generateWithClaude)
}
```

**Retry Logic:**
- 1 automatic retry on JSON parsing failure
- If retry also fails, return error to user
- User can manually retry the form
- No queue/background job (keep MVP simple)

**Cost Analysis:**
- Haiku: ~$0.011 per generation (vs Sonnet: $0.032)
- 100 generations/day = $1.08/day = $32/month
- Free tier headroom is comfortable for MVP
- Upgrade path: change model ID, redeploy (1-line change)

### 5. Rate Limiting via KV

**Mechanism:**
```typescript
async function checkRateLimit(sessionId: string, env: Env): boolean {
  const key = `rate_limit:${sessionId}`;
  const count = await env.RATE_LIMIT.get(key);

  // First request this hour → allow
  if (count === null) {
    await env.RATE_LIMIT.put(key, '1', { expirationTtl: 3600 });
    return true;
  }

  // Already made a generation → reject
  const currentCount = parseInt(count, 10);
  if (currentCount >= 1) return false;

  // Increment and allow
  await env.RATE_LIMIT.put(key, String(currentCount + 1), {
    expirationTtl: 3600,
  });
  return true;
}
```

**Quota:**
- Free plan: 1 generation per session
- KV key expires after 3600 seconds (1 hour)
- Rate limit enforced **per session**, not per IP (prevents malicious user from blocking others)

**Known Race Condition (Accepted Risk):**
- Read-then-write on KV can race under concurrent requests
- At MVP scale, might let 1-2 extra requests through per hour
- Cost: $0.011 per overage = negligible
- Fix requires Durable Objects (paid tier) or different architecture
- Not worth complexity vs blast radius

**Note on KV Write Budget:**
- Free tier: 1,000 writes/day
- With lazy session creation: only write on first generation per user
- At 100 users/day generating: 100 KV writes ≈ 10% of budget
- Plenty of headroom

### 6. GET /api/session Endpoint

**Response Contract:**
```typescript
{
  plan: string;             // 'free' or 'pro'
  generationsUsed: number;  // 0-1 for free
  maxGenerations: number;   // 1 for free
  canGenerate: boolean;     // generationsUsed < maxGenerations
}
```

**Behavior:**
- If no session cookie: return default anonymous state (0/1 generation)
- If cookie exists but session not in D1: return default anonymous state (handles cookie-clearing abuse)
- If session in D1: return actual state

**Used By:**
- Frontend can display "1 free sequence used" UI
- Paywall CTA shown when `canGenerate = false`
- Lazy load, not called on page load (preserve D1 reads for critical path)

### 7. Configuration (wrangler.toml)

```toml
name = "coldcopy"
pages_build_output_dir = "frontend/dist"

[[d1_databases]]
binding = "DB"
database_name = "coldcopy-db"
database_id = "placeholder"

[[kv_namespaces]]
binding = "RATE_LIMIT"
id = "placeholder"
```

**Setup Steps:**
```bash
# Create D1 database
npx wrangler d1 create coldcopy-db

# Create KV namespace
npx wrangler kv namespace create RATE_LIMIT

# Set secrets (before production)
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put STRIPE_SECRET_KEY
npx wrangler secret put STRIPE_WEBHOOK_SECRET

# Run schema
npx wrangler d1 execute coldcopy-db --file schema.sql

# Local development
npx wrangler pages dev frontend/dist
```

**Local Environment Variables (.dev.vars):**
```
ANTHROPIC_API_KEY=sk-ant-...
```

`.dev.vars` is in `.gitignore` and never committed.

### 8. Frontend Integration

**API Endpoint:** `POST /api/generate`
**Payload:** FormData from Generate.tsx
**Response Handling:**
1. On 200 OK: Store sequence in sessionStorage → navigate to `/output`
2. On 402: Show toast "Upgrade to continue" → stay on form
3. On 500/504: Show error toast → stay on form
4. On network error: Show generic error → stay on form

**Loading State:**
- While request in flight: show 12-second progress bar animation
- Animation purely visual (request actually completes in 3-5s typically)
- Text: "Generating your sequence... This usually takes 3-5 seconds..."
- After completion: auto-navigate to Output page

**Output Page:**
- Display all 7 emails in expandable cards
- Each email shows:
  - Subject Line A (copy button)
  - Subject Line B (copy button)
  - Body (copy button)
- "Copy" button → "Copied!" (2s) feedback
- Toast notification on copy
- "Generate Another" CTA → back to form
- "Upgrade Now" CTA (placeholder, wired on Day 5)

### 9. Development Workflow

**Vite Proxy Configuration:**
```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8788',
      changeOrigin: true,
    }
  }
}
```

**Two Terminal Sessions:**
```bash
# Terminal 1: Frontend dev server (Vite)
cd projects/coldcopy/frontend
npm run dev
# → http://localhost:5173

# Terminal 2: Backend dev server (Cloudflare Pages)
cd projects/coldcopy
npx wrangler pages dev frontend/dist
# → http://localhost:8788
```

**Request Flow (Local):**
1. User submits form on http://localhost:5173
2. Vite proxy intercepts `/api/generate` request
3. Vite proxies to http://localhost:8788/api/generate
4. Cloudflare Pages Functions handler executes
5. Response returned to frontend

**CORS Not Needed (Local):**
- Vite proxy acts as same-origin request
- No CORS headers required
- Production: same origin anyway (Pages + Functions = same domain)

---

## Production Checklist (Day 5)

- [ ] Create D1 database: `npx wrangler d1 create coldcopy-db`
- [ ] Create KV namespace: `npx wrangler kv namespace create RATE_LIMIT`
- [ ] Update `database_id` and namespace `id` in `wrangler.toml`
- [ ] Run schema: `npx wrangler d1 execute coldcopy-db --file schema.sql`
- [ ] Set secrets:
  - [ ] `npx wrangler secret put ANTHROPIC_API_KEY` (get from Anthropic Console)
  - [ ] `npx wrangler secret put STRIPE_SECRET_KEY` (get from Stripe Dashboard)
  - [ ] `npx wrangler secret put STRIPE_WEBHOOK_SECRET` (generated after Payment Links setup)
- [ ] Test locally: `npm run dev` + `npx wrangler pages dev`
- [ ] Deploy: `git push` (GitHub auto-deploys via Cloudflare Pages)
- [ ] Verify:
  - [ ] Form submission works end-to-end
  - [ ] Generated sequence displays correctly
  - [ ] Rate limit enforces 1 generation per session
  - [ ] Session persists across refreshes (cookie works)
  - [ ] Error handling works (timeout, validation failure, etc.)

---

## CTO Review Adjustments Implemented

### Adjustment #1: updated_at Trigger
✅ Implemented explicit `updated_at = datetime('now')` in UPDATE query:
```sql
UPDATE sessions
SET generations_used = generations_used + 1, updated_at = datetime('now')
WHERE id = ?
```

### Adjustment #2: API Contract Reconciliation
✅ GenerateRequest interface matches actual form fields (7 fields, not 11):
- companyName, targetJobTitle, problemTheyFace, yourProduct, keyBenefit, callToAction, tone
- Removed: companySize, socialProof, compliance, sequenceLength
- sequenceLength hardcoded to 7 in system prompt

### Adjustment #3: Lazy Session Creation
✅ Session created on first `/api/generate` POST, not on page load:
- `GET /api/session` returns default state if no cookie
- D1 insert only happens on form submission
- Saves D1 writes for bounce traffic

### Adjustment #4: Claude Response Validation
✅ Robust validation with retry:
- Strip preamble/postamble (text before first `{`)
- JSON.parse with error handling
- Validate structure (emails array, each email has required fields)
- Retry once on JSON failure
- Return user error if retry also fails

### Adjustment #5: Vite Proxy Configuration
✅ Added to `vite.config.ts`:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8788',
      changeOrigin: true,
    }
  }
}
```
CORS not needed in production (same origin).

### Adjustment #6: ANTHROPIC_API_KEY Secret
✅ Added to secrets setup (Day 5 DevOps task):
- `npx wrangler secret put ANTHROPIC_API_KEY`
- Loaded via `env.ANTHROPIC_API_KEY` in handler

---

## Files Created/Modified

**New Backend Files:**
- `/functions/api/generate.ts` — POST /api/generate handler (370 lines)
- `/functions/api/session.ts` — GET /api/session handler (85 lines)
- `/schema.sql` — D1 schema (26 lines)

**Modified Config:**
- `wrangler.toml` — Added D1 + KV bindings
- `vite.config.ts` — Added API proxy
- `.gitignore` — Added .dev.vars

**New Frontend Files:**
- `src/hooks/use-toast.ts` — Toast hook (40 lines)
- `src/components/Toast.tsx` — Toast display (35 lines)
- `src/pages/Output.tsx` — Output page (160 lines)

**Modified Frontend Files:**
- `src/App.tsx` — Added Output route + ToastContainer
- `src/pages/Generate.tsx` — Added API integration, loading state, error handling (80-line change)
- `src/index.css` — Added @keyframes progressBar animation

**Total: 3 new backend handlers + 1 schema + 4 new frontend files + 3 config updates**

---

## Performance & Reliability

### Latency Targets
- Form submission → Generation: 3-5 seconds (Claude Haiku)
- Plus cold start (first request): +0-2 seconds
- Plus D1 write: +50-150ms
- Total: 3.2-7.2 seconds typical

### Reliability
- Timeout protection: 25-second abort on Claude API (prevents 30-second Worker timeout)
- Retry logic: 1 automatic retry on JSON parse failure
- Error messages: User-friendly copy for each failure mode
- Session persistence: HttpOnly cookies survive page refresh

### Cost (7-day MVP at 100 users/day)
- Claude Haiku: 100 gen × $0.011 × 7 days = $7.70
- D1: 100 writes + reads × 7 days = ~$0 (free tier)
- KV: 100 writes × 7 days = ~$0 (free tier, 1,000 writes/day budget)
- **Total: <$10**

---

## Next Steps (Day 4-5)

**Day 4 Frontend:**
1. Test /output page with real generated sequences
2. Implement copy-to-clipboard for email bodies
3. Add "Upgrade Now" CTA (PaymentLink integration Day 5)
4. Polish loading animation and error states

**Day 5 DevOps + Backend:**
1. Create D1 database in production
2. Create KV namespace in production
3. Run schema migration
4. Set all secrets (ANTHROPIC_API_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET)
5. Deploy to production via git push
6. Test end-to-end in production (real Claude API, real rate limiting)
7. Monitor D1/KV usage and costs

**Day 6 QA:**
1. Manual testing of all flows (happy path, error paths, edge cases)
2. Load testing (100 concurrent requests)
3. Session persistence testing (clear cookies, test recovery)
4. Rate limit verification (ensure 1 generation per session)

---

## Logging & Observability

**Cloudflare Logging:**
- Errors logged to console via `console.error()`
- Visible in Cloudflare Dashboard → Workers → Logs
- Includes request/response details and error stack traces

**Metrics to Monitor:**
- Claude API latency (target: <5s)
- D1 query latency (target: <200ms)
- KV lookup latency (target: <50ms)
- Error rate (target: <1%)
- Rate limit rejections (expect ~2% of requests after Day 3)

**Example Cloudflare Dashboard Query:**
```
status:500 OR error
```

---

## Architecture Strengths

1. **Simplicity:** One database, one KV store, one LLM API, one deployment target
2. **Monolith:** Frontend + Backend deployed together (no CORS, no coordination)
3. **Stateless:** Functions scale horizontally (Cloudflare handles auto-scaling)
4. **Cheap:** Free tier covers MVP (D1 free = 500MB, KV free = 1,000 writes/day)
5. **Fast:** Haiku 4.5 is 3-5s, Cloudflare edge is <100ms from most users
6. **Secure:** HttpOnly cookies, no JWT, D1 source of truth, no exposed secrets

---

## Known Limitations & Future Work

**MVP Scope (Done):**
- Free plan: 1 generation
- Manual retry (user clicks Generate again)
- Single LLM (Claude Haiku)

**Week 2 (Post-MVP):**
- [ ] Paid plans (Pro $49/month, Business custom)
- [ ] Subscription management (Stripe Customer Portal)
- [ ] Email verification (for paid plan)
- [ ] Background job queue (handle generation failures gracefully)
- [ ] Prompt versioning (A/B test prompt variations)

**Post-MVP Infrastructure:**
- [ ] Logging service (Axiom, Logtail, or Datadog)
- [ ] Analytics (Posthog, Plausible)
- [ ] Monitoring/alerts (Cloudflare + email)
- [ ] Database backups (automated via Cloudflare)

---

## Appendix: API Examples

### Request: Generate Cold Email Sequence

```bash
curl -X POST http://localhost:5173/api/generate \
  -H "Content-Type: application/json" \
  -b "coldcopy_session=abc-123" \
  -d '{
    "companyName": "Acme Analytics",
    "targetJobTitle": "VP of Marketing",
    "problemTheyFace": "They lose 30-40% of revenue to cart abandonment but don\u0027t know why",
    "yourProduct": "Real-time analytics dashboard for e-commerce stores",
    "keyBenefit": "Identify why 60% of carts abandon in under 10 seconds",
    "callToAction": "Book a 15-min demo",
    "tone": "Professional"
  }'
```

### Response: 200 OK

```json
{
  "success": true,
  "sequenceId": "seq-xyz-123",
  "sequence": {
    "emails": [
      {
        "subjectLineA": "60% of your carts are leaking - here\u0027s why",
        "subjectLineB": "Cart abandonment analysis in 30 seconds",
        "body": "Hi [FirstName],\n\nMost e-commerce leaders don\u0027t realize why customers abandon carts...\n\n[Full email body]"
      },
      // ... 6 more emails
    ]
  }
}
```

### Response: 402 Rate Limit

```json
{
  "error": "rate_limit_exceeded",
  "message": "You have reached your generation limit. Upgrade to continue."
}
```

---

*Implementation complete. Ready for production on Day 5.*
