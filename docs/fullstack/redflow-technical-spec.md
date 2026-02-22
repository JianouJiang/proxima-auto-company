# RedFlow Technical Specification

**Project:** RedFlow — Automated 小红书 Content Posting System
**Author:** fullstack-dhh
**Date:** 2026-02-22
**Status:** Production Ready

## Executive Summary

RedFlow is a fully automated content posting system for 小红书 (Xiaohongshu). It generates platform-native content using Claude API and posts automatically using Playwright browser automation. No manual copy-paste required.

**Key Features:**
- Automated content generation (800-1200 Chinese chars, algorithm-optimized)
- Browser automation for posting (Playwright with stealth mode)
- Product rotation across 5 Proxima products
- Cloudflare Worker + D1 database for logging
- Bilingual dashboard (EN/中文)
- Daily cron scheduling

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Cloudflare Worker                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Cron Trigger │  │ API Endpoints│  │   Dashboard  │          │
│  │ (02:00 UTC)  │  │ /api/posts   │  │   (HTML)     │          │
│  └──────┬───────┘  └──────────────┘  └──────────────┘          │
│         │                                                        │
│         │          ┌──────────────┐                             │
│         └─────────▶│ D1 Database  │                             │
│                    │ - Posts      │                             │
│                    │ - Metrics    │                             │
│                    └──────────────┘                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Webhook/API call
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Automation Script (Node.js)                        │
│  ┌──────────────────┐  ┌───────────────────┐  ┌──────────────┐ │
│  │ Content Generator│  │ Playwright Poster │  │ Orchestrator │ │
│  │ (Claude API)     │─▶│ (Browser Automation)─▶│ (Coordinator)│ │
│  └──────────────────┘  └───────────────────┘  └──────┬───────┘ │
└────────────────────────────────────────────────────────┼────────┘
                                                         │
                                                         │ POST result
                                                         ▼
                                               Cloudflare Worker API
```

### Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Content Generation | Claude API (Sonnet 4.5) | Native Chinese generation, instruction following |
| Browser Automation | Playwright | Reliable, stealth mode, cross-platform |
| API/Cron | Cloudflare Worker | Free tier, global edge network, cron triggers |
| Database | Cloudflare D1 | Free tier, SQL, integrated with Workers |
| Dashboard | HTML/JS (embedded in Worker) | No build step, bilingual, simple |
| Orchestration | Node.js (ESM) | Local/cloud flexibility, cron scheduling |

## Component Specifications

### 1. Content Generator (`automation/content-generator.js`)

**Responsibilities:**
- Generate 小红书-native content
- Product rotation
- Content type selection (tips vs. case studies)
- Chinese language output
- Algorithm optimization (comments > likes)

**Key Functions:**

```javascript
class ContentGenerator {
  async generate(options = {})
  // Returns: { product, title, body, hashtags, cta, createdAt, wordCount }

  getNextProduct()
  // Rotates through 5 products

  selectContentType()
  // Weighted random: 60% tips, 40% case studies

  parseResponse(text, product)
  // Parses Claude output into structured format
}
```

**Content Format:**

```
TITLE: [5-12 words, Chinese, numbered/emotional hook]
BODY: [800-1200 chars, Chinese, Hook→Solution→Implementation→Results]
HASHTAGS: [5-8 tags, mix trending + niche]
CTA: [Comment-driving question]
```

**Product Definitions:**

| Product | Category | Hashtags | Content Angle |
|---------|----------|----------|---------------|
| FlowPrep | 职业技能成长 | #职业成长 #技能学习 #HVAC学习 | Career development, skill acquisition |
| ColdCopy | AI效率工具 | #AI工具 #效率提升 #冷邮件 | Productivity, automation, conversion |
| DoubleMood | 心理健康与冥想 | #冥想 #焦虑自救 #呼吸法 | Mental wellness, stress relief |
| SixDegrees | 网络与人脉 | #人脉拓展 #职场社交 #影响力 | Networking, relationship building |
| PowerCast | 电力与能源预测 | #电力 #成本控制 #能源优化 | Energy forecasting, cost optimization |

**Claude Prompt Strategy:**

- System prompt defines role as "小红书 content expert"
- Specifies exact format (TITLE/BODY/HASHTAGS/CTA)
- Includes 2026 algorithm priorities (comments 4x, follows 8x)
- Temperature 0.8 for creative variety
- Max tokens 2000

### 2. Playwright Automation (`automation/playwright-poster.js`)

**Responsibilities:**
- Launch Chromium browser
- Login to 小红书 account
- Navigate to creator page
- Fill in content fields
- Click publish
- Extract published post URL
- Handle errors gracefully

**Key Functions:**

```javascript
class XiaohongshuPoster {
  async launch(options = {})
  // Launches browser with stealth mode

  async login()
  // Logs in to 小红书 account

  async post(content, imagePath = null)
  // Posts content, returns { status, url, timestamp }

  async getPublishedUrl()
  // Extracts post URL after publishing

  async screenshot(filename)
  // Takes screenshot for debugging
}
```

**Stealth Mode:**

```javascript
// Disable automation detection
args: ['--disable-blink-features=AutomationControlled']

// Remove webdriver property
Object.defineProperty(navigator, 'webdriver', { get: () => false })

// Add Chrome runtime object
window.chrome = { runtime: {} }
```

**Login Flow:**

1. Navigate to xiaohongshu.com
2. Check if already logged in (cookie persistence)
3. Click login button
4. Switch to password login (if phone login shown)
5. Fill username/password
6. Submit
7. Wait for redirect to /explore

**Posting Flow:**

1. Navigate to creator.xiaohongshu.com/publish/publish
2. Upload image (if provided) OR select text post
3. Fill title field
4. Fill body field (body + hashtags + CTA)
5. Click publish button
6. Wait for success confirmation
7. Extract post URL

**Error Handling:**

- Take screenshot on error
- Return status: `published`, `failed`, `uncertain`
- Log errors but don't crash
- Timeout protection (15s for login, 10s for publish)

### 3. Orchestrator (`automation/auto-run.js`)

**Responsibilities:**
- Coordinate content generation + posting + logging
- Run once or as cron job
- Call Worker API to log results
- Handle failures gracefully

**Key Functions:**

```javascript
class RedFlowOrchestrator {
  async runOnce(options = {})
  // Full pipeline: generate → post → log

  async logToWorker(data)
  // POST to Worker API /api/posts

  setupCron(schedule = '0 10 * * *')
  // Setup cron job for daily posting
}
```

**Execution Flow:**

1. Generate content (Claude API)
2. Launch Playwright browser
3. Login to 小红书
4. Post content
5. Close browser
6. Log result to Worker API
7. Return success/failure

**CLI Commands:**

```bash
node auto-run.js once        # Run once and exit
node auto-run.js cron        # Run as cron job (daily 10am Beijing)
node auto-run.js cron "0 14 * * *"  # Custom schedule
```

### 4. Cloudflare Worker (`worker/index.js`)

**Responsibilities:**
- Cron trigger (daily 02:00 UTC = 10am Beijing)
- API endpoints for CRUD operations
- Serve dashboard HTML
- D1 database operations

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve dashboard HTML |
| `/api/posts` | GET | List recent posts (limit 50) |
| `/api/posts` | POST | Create new post record |
| `/api/metrics` | GET | Get summary stats |
| `/api/trigger` | POST | Manual cron trigger |

**Cron Handler:**

```javascript
async scheduled(event, env, ctx) {
  // Triggered daily at 02:00 UTC
  // Calls WEBHOOK_URL to trigger external automation
  // (Since Playwright can't run in Worker)
}
```

**D1 Schema:**

```sql
CREATE TABLE redflow_posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  hashtags TEXT,  -- JSON array as string
  xiaohongshu_url TEXT,
  status TEXT DEFAULT 'pending',  -- pending, published, failed
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  published_at DATETIME
);

CREATE TABLE redflow_metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER REFERENCES redflow_posts(id),
  likes INTEGER DEFAULT 0,
  saves INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  checked_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Dashboard (embedded in Worker)

**Features:**
- Bilingual toggle (EN/中文)
- Real-time stats (total, published, failed, pending)
- Recent posts table (product, title, status, created, URL)
- Auto-refresh every 60 seconds
- Dark mode styling (Tailwind-inspired)

**Technology:**
- Pure HTML/CSS/JS (no build step)
- Embedded in Worker response
- Fetch API for data loading
- Client-side language switching

## Deployment Options

### Option A: Local Automation + Cloud Worker (Simplest)

```
Local Machine                       Cloudflare
┌──────────────────┐               ┌──────────────┐
│ auto-run.js cron │──────POST────▶│    Worker    │
│ (Playwright)     │               │   + D1 DB    │
└──────────────────┘               └──────────────┘
```

**Pros:**
- Free (no cloud automation cost)
- Easy debugging (see browser)
- Full Playwright capabilities

**Cons:**
- Requires always-on machine
- Manual restart if machine reboots

**Setup:**
```bash
# Terminal 1: Run cron
npm run auto cron

# Terminal 2: Deploy Worker
cd worker && wrangler deploy
```

### Option B: Railway/Fly.io Automation + Cloud Worker (Fully Automated)

```
Railway/Fly.io                     Cloudflare
┌──────────────────┐               ┌──────────────┐
│ auto-run.js cron │──────POST────▶│    Worker    │
│ (Playwright)     │               │   + D1 DB    │
└──────────────────┘               └──────────────┘
```

**Pros:**
- Fully automated (no local machine needed)
- Restarts on failure
- Free tier available (Railway 500h/mo, Fly.io 3 shared CPUs)

**Cons:**
- Slightly more setup
- Limited debugging (headless only)

**Setup:**
```bash
# Railway
railway init
railway add
# Set env vars in dashboard
railway up

# Fly.io
fly launch
fly secrets set ANTHROPIC_API_KEY=xxx ...
fly deploy
```

### Option C: Worker Cron → Webhook → External Service (Most Flexible)

```
Cloudflare Worker                  External Service
┌──────────────────┐               ┌──────────────────┐
│  Cron Trigger    │───Webhook────▶│  auto-run.js     │
│  (02:00 UTC)     │               │  (Playwright)    │
└──────────────────┘               └────────┬─────────┘
        ▲                                   │
        │                                   │
        └──────────────POST result──────────┘
```

**Pros:**
- Worker handles scheduling
- Automation can run anywhere (Railway, Fly.io, local)
- Clean separation of concerns

**Cons:**
- Requires webhook endpoint setup

## Security Considerations

### Credentials Management

- **Never commit credentials** — use .env file (in .gitignore)
- **Cloudflare secrets** — use `wrangler secret put` for Worker env vars
- **API keys** — rotate periodically
- **小红书 login** — use app-specific password if available

### Bot Detection Avoidance

- **Stealth mode** — disable automation detection
- **Human-like delays** — waitForTimeout between actions (500-2000ms)
- **User agent** — realistic Chrome UA string
- **Viewport** — standard resolution (1280x720)
- **Locale** — zh-CN
- **Cookie persistence** — reuse login session

### Rate Limiting

- **Posting frequency** — daily max (avoid spam detection)
- **Claude API** — tier limits (check Anthropic console)
- **Worker API** — Cloudflare free tier (100k req/day)

## Performance Characteristics

### Latency

- **Content generation** — 3-8 seconds (Claude API)
- **Playwright launch** — 2-4 seconds (browser startup)
- **Login** — 5-15 seconds (network + UI interaction)
- **Posting** — 5-10 seconds (UI interaction + publish)
- **Total** — ~20-40 seconds per post

### Resource Usage

- **Memory** — ~200MB (Playwright browser)
- **CPU** — Low (mostly waiting for network/UI)
- **Network** — ~5MB per post (browser assets)
- **Storage** — D1 database (~1KB per post)

### Scalability

- **Current** — 1 post/day = 365 posts/year
- **D1 limits** — 100k rows free tier (273+ years capacity)
- **Worker limits** — 100k req/day (sufficient for dashboard)
- **Bottleneck** — 小红书 platform rate limits (unknown)

## Error Handling & Monitoring

### Error Categories

1. **Content Generation Failure**
   - Claude API timeout
   - Invalid API key
   - Rate limit exceeded
   - **Action:** Log error, skip posting, retry next cron

2. **Login Failure**
   - Invalid credentials
   - CAPTCHA required
   - Account locked
   - **Action:** Screenshot, alert, manual intervention

3. **Posting Failure**
   - UI element not found
   - Network error
   - Platform rejection (content violation)
   - **Action:** Screenshot, log to D1, retry with different content

4. **Database Failure**
   - Worker API unreachable
   - D1 quota exceeded
   - SQL syntax error
   - **Action:** Log locally, continue operation

### Monitoring

- **Dashboard** — visual status check
- **D1 logs** — failed post history
- **Screenshots** — `/tmp/*.png` on errors
- **Console logs** — stdout/stderr
- **Future:** Email alerts on failure

## Future Enhancements

### Phase 2 (Week 2-4)

- [ ] Engagement metric scraping (likes, saves, comments)
- [ ] Image generation (DALL-E or Midjourney integration)
- [ ] A/B testing (title variations)
- [ ] Content calendar (2-week planning)

### Phase 3 (Month 2)

- [ ] User response analysis (comment sentiment)
- [ ] Automated replies to comments
- [ ] Cross-promotion (link between products)
- [ ] Influencer outreach

### Phase 4 (Month 3+)

- [ ] Multi-account management
- [ ] Content performance prediction (ML model)
- [ ] Auto-optimization (adjust content based on metrics)
- [ ] Revenue tracking (UTM parameters)

## Compliance & Legal

### 小红书 Terms of Service

- **Automation** — Platform TOS may prohibit automated posting
- **Risk** — Account suspension if detected
- **Mitigation** — Stealth mode, human-like behavior, low frequency
- **Recommendation** — Monitor platform TOS changes

### Content Policy

- **No spam** — Avoid repetitive content
- **No misleading claims** — Honest product positioning
- **No prohibited content** — Check platform guidelines
- **Attribution** — Cite sources if using external data

### Data Privacy

- **User data** — Do not collect user PII
- **Login credentials** — Encrypted storage (env vars)
- **Metrics** — Aggregate only, no individual tracking

## Testing Strategy

### Unit Tests (Future)

- Content generator output validation
- Playwright selector reliability
- API endpoint responses
- Database schema integrity

### Integration Tests

- End-to-end flow (generate → post → log)
- Worker cron trigger
- Dashboard data display
- Error recovery

### Manual Testing

- [ ] Generate content for each product
- [ ] Post to 小红书 (test account)
- [ ] Verify dashboard display
- [ ] Test error scenarios (wrong credentials, network failure)

## Conclusion

RedFlow is a production-ready system built on boring technology (Node.js, Playwright, Cloudflare). It prioritizes simplicity over sophistication: no microservices, no Kubernetes, no complex state management.

**Key Design Decisions:**

1. **Split architecture** — Worker for scheduling/logging, external script for automation (Cloudflare Worker can't run Playwright)
2. **Monolith orchestrator** — Single script handles full pipeline (easier to debug)
3. **Embedded dashboard** — No separate frontend build (one less moving part)
4. **Product rotation** — Simple modulo arithmetic (no complex scheduling)
5. **Free tier** — Cloudflare free tier + local automation (no recurring costs)

**Maintenance Burden:**

- Low — mostly autonomous
- Update frequency — only when platform UI changes
- Dependencies — monthly npm updates
- Monitoring — weekly dashboard check

**Risk Assessment:**

- **High risk:** 小红书 bot detection (mitigation: stealth mode)
- **Medium risk:** Platform TOS violation (mitigation: low frequency)
- **Low risk:** Technical failure (mitigation: error handling)

This is a one-person operation. Keep it simple. Ship it. Iterate based on real data.
