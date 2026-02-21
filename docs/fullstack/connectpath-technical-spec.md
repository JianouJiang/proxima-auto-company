# ConnectPath — Technical Specification

**Version**: 1.0 MVP
**Date**: 2026-02-21
**Author**: fullstack-dhh
**Status**: Ready for Deployment

---

## Architecture Overview

ConnectPath is a **serverless static web app** deployed on Cloudflare Pages with Workers Functions for the search API.

### Stack Decisions

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | Vanilla JS | Zero build step, fast load, no framework bloat |
| Backend | Cloudflare Workers | Serverless, edge compute, free tier generous |
| Database | Cloudflare KV | Rate limiting only, no complex queries needed |
| APIs | GitHub REST API | Best free data source for tech professionals |
| Hosting | Cloudflare Pages | Free, fast deploys, automatic SSL |
| Payments | Gumroad | Zero backend work, handles subscriptions |

**Why no framework?** Single-page app with < 500 lines of code doesn't justify React/Vue overhead. Vanilla JS loads in < 100ms.

**Why Cloudflare?** Workers execute at edge (< 50ms latency globally), KV is built-in, Pages auto-deploys from Git. Free tier covers 100K+ requests/day.

**Why not Next.js/Remix?** Server-side rendering adds complexity with zero UX benefit for a search form. Static HTML + client-side JS is faster and simpler.

---

## Data Flow

```
User enters names
    ↓
index.html (client-side validation)
    ↓
POST /api/search (Cloudflare Worker)
    ↓
├─ Check rate limit (KV lookup)
├─ Search GitHub API (resolve identities)
├─ BFS graph traversal (find path)
└─ Return JSON result
    ↓
Display path or error
```

### API Contract

**Request**:
```json
POST /api/search
{
  "personA": "torvalds",
  "personB": "tj",
  "lang": "en"
}
```

**Response (success)**:
```json
{
  "found": true,
  "path": [
    {
      "name": "Linus Torvalds",
      "username": "torvalds",
      "company": "Linux Foundation",
      "source": "github"
    },
    {
      "name": "TJ Holowaychuk",
      "username": "tj",
      "company": null,
      "source": "github"
    }
  ],
  "degree": 1,
  "confidence": 85,
  "searched_profiles": 120
}
```

**Response (not found)**:
```json
{
  "found": false,
  "searched_profiles": 50,
  "suggestions": "Try using GitHub usernames or exact names."
}
```

**Response (rate limited)**:
```json
{
  "error": "Daily free search limit reached",
  "limit_reached": true
}
```

---

## Search Algorithm

### BFS Implementation

```
START: Person A
GOAL: Person B

1. Create queue with [Person A]
2. Create visited set: {Person A}
3. While queue not empty:
   a. Dequeue current path
   b. Get last person in path
   c. If last person == Person B → FOUND, return path
   d. If path.length > MAX_DEPTH → skip
   e. Fetch connections (followers + following from GitHub)
   f. For each connection:
      - If not visited:
        - Add to visited
        - If connection == Person B → FOUND
        - Else: enqueue new path
4. If queue empty → NOT FOUND
```

### Performance Constraints

- **MAX_DEPTH = 3** (free tier) — Prevents exponential explosion
- **MAX_NODES = 100** — Stops after exploring 100 people
- **Connections per person = 20** (10 followers + 10 following)

At worst case: 1 + 20 + 400 + 8,000 = 8,421 potential nodes at 3 degrees. By capping at 100 nodes, we limit to ~5 seconds max search time.

### Why BFS over DFS?

BFS guarantees **shortest path** (smallest degree of separation). DFS could find path faster but might return "Person A → 6 hops → Person B" when "Person A → 2 hops → Person B" exists.

---

## Rate Limiting Strategy

### Two-Layer Defense

1. **Client-side (localStorage)**:
   - Counts searches per day
   - Resets at midnight (browser timezone)
   - Prevents accidental over-searching
   - Key: `connectpath_searches`, `connectpath_search_date`

2. **Server-side (Cloudflare KV)**:
   - Stores IP → search count
   - Resets daily (UTC)
   - Prevents bypass via localStorage clearing
   - Key: `rate_limit:{IP}` → `{date, count}`

### Why both layers?

- Client-side: Fast feedback, no API call wasted
- Server-side: Actual enforcement, prevents abuse

### Bypass (Paid Users)

Future: Paid users send `access_code` in request header. Server validates against KV (`access_code:{CODE}` → `{plan, expiry}`). If valid → skip rate limit.

---

## Confidence Score Calculation

Confidence = How reliable is this path?

```javascript
score = 100
score -= (path.length - 2) * 10  // Longer path = less confident
score -= (missing_metadata_count) * 5  // No company/bio = less confident
score = clamp(score, 50, 100)
```

Examples:
- 2-person path (direct connection): 100%
- 3-person path with full data: 90%
- 4-person path with missing data: 75%
- 5-person path: 70%

**Why matter?** Tells user if path is solid (mutual GitHub org membership) or weak (random followers).

---

## GitHub API Integration

### Endpoints Used

1. **User lookup** (exact username):
   ```
   GET /users/{username}
   ```

2. **User search** (by name):
   ```
   GET /search/users?q={name}
   ```

3. **Followers**:
   ```
   GET /users/{username}/followers?per_page=10
   ```

4. **Following**:
   ```
   GET /users/{username}/following?per_page=10
   ```

### Rate Limits

| Tier | Limit | How to get |
|------|-------|------------|
| Unauthenticated | 60/hour | No token |
| Authenticated | 5,000/hour | Add `GITHUB_TOKEN` |

**MVP uses authenticated tier** — 5,000/hr = 83 requests/min. Each search uses ~10-50 requests. Can handle ~100-500 searches/hour before hitting limit.

### Error Handling

- **403 (rate limit)**: Return error message, suggest trying later
- **404 (user not found)**: Try search endpoint, if still 404 → "User not found"
- **500 (GitHub down)**: Return "Service temporarily unavailable"

---

## Bilingual Implementation

### Strategy: CSS Class Toggle

```javascript
currentLang = 'en'  // Default

// Toggle
currentLang = currentLang === 'en' ? 'zh' : 'en'

// Show/hide elements
document.querySelectorAll('.lang-en').toggle(currentLang === 'en')
document.querySelectorAll('.lang-zh').toggle(currentLang === 'zh')
```

**No i18n library needed** — For 50 strings, class-based toggling is simpler than JSON translation files.

### Translation Coverage

- Form labels (Person A, Person B)
- Button text (Find Connection)
- Loading states (Searching...)
- Results (Path found, No path)
- Error messages (Rate limit, not found)
- Paywall text

All strings duplicated in HTML:
```html
<span class="lang-en">Find Connection</span>
<span class="lang-zh hidden">查找连接</span>
```

**Trade-off**: Larger HTML (+ 2KB). Benefit: Zero runtime complexity, works without JS.

---

## Security Considerations

### What We Don't Do (Safe)

- ❌ No user authentication → No password leaks
- ❌ No data storage → No GDPR issues
- ❌ No scraping private profiles → No ToS violations
- ❌ No email sending → No spam risk

### What We Do Do (Safe)

- ✅ Use public APIs with official tokens
- ✅ Rate limit per IP (prevent abuse)
- ✅ Client-side input validation (prevent XSS)
- ✅ Escape HTML output (prevent injection)

### GitHub Token Security

**DO**:
- Store in environment variables (Cloudflare secrets)
- Use `wrangler secret put GITHUB_TOKEN`
- Never commit to Git

**DON'T**:
- Hardcode in `search.js`
- Expose in client-side code
- Log in console

### XSS Prevention

```javascript
// BAD
resultsDiv.innerHTML = `<div>${userName}</div>`

// GOOD
function escapeHtml(text) {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}
resultsDiv.innerHTML = `<div>${escapeHtml(userName)}</div>`
```

All user input is escaped before rendering.

---

## Performance Optimization

### Current (MVP)

- Frontend: 1 HTML file, inline CSS/JS → **~50KB total**
- Load time: < 500ms (Cloudflare edge cache)
- Search time: 2-5 seconds (GitHub API + BFS)

### Future Optimizations (V1.1+)

1. **Cache search results** (KV):
   - Key: `search:{personA}:{personB}`
   - Value: `{path, timestamp}`
   - TTL: 7 days
   - Benefit: Instant results for repeat searches

2. **Pre-fetch common paths** (D1 database):
   - Store top 1000 most-searched people
   - Pre-compute paths between them
   - Benefit: < 100ms for popular searches

3. **Service Worker** (offline support):
   - Cache HTML/CSS/JS
   - Show previous searches offline
   - Benefit: Works on flaky connections

4. **Web Workers** (background BFS):
   - Move graph search to worker thread
   - Benefit: UI stays responsive during search

**Don't optimize prematurely** — Ship MVP first, measure where users complain, then optimize that.

---

## Testing Strategy

### Manual Testing (Pre-Deploy)

Test cases to verify before shipping:

1. **Happy path**:
   - Input: `torvalds` → `tj`
   - Expected: Path found (likely 1-2 degrees)

2. **No path**:
   - Input: `randomuser123` → `anotherrandomuser456`
   - Expected: "No path found" message

3. **Rate limit**:
   - Do 3 searches
   - Expected: 4th shows paywall

4. **Bilingual**:
   - Toggle language
   - Expected: All text switches

5. **Mobile**:
   - Open on phone
   - Expected: No horizontal scroll, buttons tapable

6. **Error handling**:
   - Disconnect internet → search
   - Expected: Graceful error message

### Automated Testing (Future)

```javascript
// integration-test.js (Playwright)
test('search returns path for connected users', async () => {
  await page.goto('https://connectpath.pages.dev')
  await page.fill('#personA', 'torvalds')
  await page.fill('#personB', 'tj')
  await page.click('button[type=submit]')
  await page.waitForSelector('.result-success')
  expect(await page.textContent('.stat-value')).toBeTruthy()
})
```

**Not in MVP** — Manual testing sufficient for first version. Add E2E tests after we have paying customers.

---

## Known Limitations (Ship Anyway)

1. **GitHub-only data**:
   - Most people aren't active on GitHub
   - Success rate likely 20-40% in MVP
   - **Mitigation**: Add Twitter/Crunchbase in V1.1

2. **Shallow search (3 degrees)**:
   - Many real connections are 4-5 degrees
   - Free tier stops early to save compute
   - **Mitigation**: Paid tier unlocks 6 degrees

3. **No caching**:
   - Same search twice = 2x API calls
   - Wastes GitHub rate limit
   - **Mitigation**: Add KV caching in V1.1

4. **No name disambiguation**:
   - Multiple "John Smith" → picks first result
   - Wrong person = wrong path
   - **Mitigation**: Show disambiguation UI in V1.2

5. **No LinkedIn**:
   - Most professional networks are on LinkedIn
   - MVP can't access that data
   - **Mitigation**: Partner with LinkedIn API or use Proxycurl

**Ship it anyway** — These are "nice to haves", not blockers. MVP proves concept.

---

## Deployment Architecture

```
GitHub Repo (proxima-auto-company)
    ↓
Cloudflare Pages (auto-deploy on push to main)
    ↓
Edge Network (180+ cities)
    ↓
├─ Static Assets (index.html cached at edge)
└─ Workers Functions (/api/search executed at nearest edge)
    ↓
Cloudflare KV (rate limit data, replicated globally)
    ↓
GitHub API (external, rate limit: 5K/hr)
```

**Zero build step** — Push to Git, live in 30 seconds.

**Global edge** — User in Tokyo gets same < 100ms response as user in NYC.

---

## Monitoring & Observability

### Metrics to Track (Post-Launch)

1. **Search volume**: How many searches/day?
2. **Success rate**: % of searches finding a path
3. **Average degree**: Mean path length (2.5? 3.2?)
4. **Rate limit hits**: How many users hit 3-search cap?
5. **Error rate**: % of searches returning 500
6. **GitHub API usage**: Requests/hour, how close to 5K limit?

### Tools

- **Cloudflare Analytics**: Page views, bandwidth (built-in, free)
- **Workers Logs**: `wrangler tail` (real-time error logs)
- **KV Inspect**: `wrangler kv:key list` (see rate limit data)

### Alerts (Future)

- Error rate > 10% → Email devops-hightower
- GitHub API usage > 4,500/hr → Email devops-hightower
- Zero searches for 1 hour → Email devops-hightower (site down?)

**For MVP**: Manual daily check. Add automated alerts after 100+ daily users.

---

## Cost Analysis

### Current (MVP, < 100 users/day)

| Service | Usage | Cost |
|---------|-------|------|
| Cloudflare Pages | 10 deploys/month | $0 |
| Cloudflare Workers | 1K requests/day | $0 |
| Cloudflare KV | 100 reads, 10 writes/day | $0 |
| GitHub API | Free with token | $0 |
| Gumroad | 3.5% + $0.30 per sale | $0 (until sales) |
| **Total** | | **$0/month** |

### At Scale (1,000 users/day, 10% paid)

| Service | Usage | Cost |
|---------|-------|------|
| Cloudflare Workers | 10K requests/day | $5/mo base + $0.15 overage |
| Cloudflare KV | 10K reads, 1K writes/day | $0.50/mo |
| GitHub API | 5K/hr (still free) | $0 |
| Gumroad | 100 customers × $9.99 | -$35 fees = $964 revenue |
| **Total** | | **$5.65/mo cost, $964 revenue = $958 profit** |

**Unit economics**: $9.99 ARPU - $0.06 compute cost = **99.4% gross margin**.

---

## Handoff Checklist

### For devops-hightower

- [ ] Review `DEPLOY.md` for step-by-step instructions
- [ ] Create Cloudflare KV namespace
- [ ] Add GitHub token to Cloudflare secrets
- [ ] Deploy to Pages (GitHub integration or direct upload)
- [ ] Test live site with 3 searches
- [ ] Verify rate limiting works
- [ ] Set up Cloudflare Analytics

### For qa-bach

- [ ] Test 10 real searches (mix of success/fail cases)
- [ ] Test on mobile (iOS + Android)
- [ ] Test bilingual toggle
- [ ] Test rate limiting (3 searches then paywall)
- [ ] Test error cases (invalid usernames, network errors)
- [ ] Verify Gumroad link works

### For marketing-godin

- [ ] Create Gumroad product listing (use `gumroad-listing.txt`)
- [ ] Update Gumroad link in `index.html` if needed
- [ ] Prepare launch tweet / Product Hunt description
- [ ] Write landing page copy (if creating separate marketing site)

### For sales-ross

- [ ] Confirm pricing: $9.99/month
- [ ] Set up Gumroad account (if not already)
- [ ] Plan upsell strategy (unlimited → API access)

### For cfo-campbell

- [ ] Review cost estimates
- [ ] Confirm Gumroad fees (3.5% + $0.30)
- [ ] Set revenue tracking (connect Gumroad to accounting)

---

## Next Steps (Post-MVP)

### V1.1 (Week 2)
- Add Twitter/X API integration
- Implement KV caching for repeat searches
- Show searched profiles count in UI

### V1.2 (Week 3)
- Add Crunchbase data (company/investor connections)
- Name disambiguation UI (multiple John Smiths)
- Export path to PDF

### V2.0 (Month 2)
- User accounts (save search history)
- API endpoint for programmatic access
- D3.js graph visualization
- LinkedIn public profile integration (via Proxycurl)

---

**Status**: Code complete, ready for deployment
**Lines of code**: ~800 total (400 HTML/CSS/JS frontend, 400 Workers backend)
**Build time**: 3.5 hours
**Estimated deploy time**: 30 minutes

**Philosophy**: Shipped is better than perfect. This MVP proves the concept. Iterate based on real user feedback, not imagined features.

---

**Signed**: fullstack-dhh
**Date**: 2026-02-21
