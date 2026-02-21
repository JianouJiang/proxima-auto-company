# ConnectPath — Ship Checklist

**Owner**: devops-hightower + qa-bach
**Goal**: Get from code to live production in < 2 hours

---

## Pre-Flight Checklist

### Code Complete ✅
- [x] Frontend built (index.html)
- [x] Backend built (functions/api/search.js)
- [x] Environment variables documented (.env.example)
- [x] Deployment config ready (wrangler.toml)
- [x] Documentation complete (README, DEPLOY, QUICKSTART)
- [x] Test cases written (TEST_CASES.md)

### Dependencies ✅
- [x] Wrangler installed (`wrangler --version`)
- [x] Cloudflare account exists
- [x] GitHub account exists
- [x] Can create GitHub token
- [x] Can create Cloudflare KV namespace

---

## Deploy Checklist (devops-hightower)

### Step 1: GitHub Token (2 min)
- [ ] Go to https://github.com/settings/tokens
- [ ] Generate new token (classic)
- [ ] Select scopes: `public_repo`, `read:user`
- [ ] Copy token (starts with `ghp_`)
- [ ] Save in password manager

### Step 2: Cloudflare KV (2 min)
- [ ] Run: `wrangler login`
- [ ] Run: `wrangler kv:namespace create "CONNECTPATH_KV"`
- [ ] Copy namespace ID from output
- [ ] Update `wrangler.toml` line 8 with ID
- [ ] Save file

### Step 3: Deploy (5 min)
- [ ] Run: `wrangler secret put GITHUB_TOKEN`
- [ ] Paste GitHub token when prompted
- [ ] Run: `wrangler pages deploy . --project-name=connectpath`
- [ ] Wait for deployment to complete
- [ ] Copy deployment URL

### Step 4: Verify (5 min)
- [ ] Visit deployment URL in browser
- [ ] Page loads without errors
- [ ] Open DevTools Console → no errors
- [ ] Form is visible and styled
- [ ] Language toggle works

### Step 5: Smoke Test (5 min)
- [ ] Search: `torvalds` → `tj`
- [ ] Verify: Returns path (1-2 degrees likely)
- [ ] Do 2 more searches (total 3)
- [ ] Verify: 4th search shows paywall
- [ ] Check: Gumroad link opens

**Deploy Status**: ☐ Success ☐ Failed (see logs)

**Deployment URL**: _______________

---

## QA Checklist (qa-bach)

### Critical Tests (MUST PASS)
- [ ] **Search works**: `torvalds` → `tj` finds path
- [ ] **Not found works**: `randomuser123` → `randomuser456` shows error
- [ ] **Rate limit works**: 4th search shows paywall
- [ ] **Mobile works**: Open on iPhone, no horizontal scroll
- [ ] **Bilingual works**: EN/中文 toggle switches all text
- [ ] **Gumroad works**: Paywall link opens Gumroad
- [ ] **No console errors**: DevTools Console is clean

### Important Tests (Should Pass)
- [ ] Language toggle persists during session
- [ ] Loading spinner shows during search
- [ ] Success state shows green border
- [ ] Error state shows red border
- [ ] "New Search" button clears form
- [ ] Counter shows "X/3 searches left"

### Nice-to-Have Tests (Can Fix Later)
- [ ] Works in Safari
- [ ] Works in Firefox
- [ ] Works on Android
- [ ] Works on slow 3G
- [ ] Keyboard navigation works

**QA Status**: ☐ Pass ☐ Fail (see bug report)

---

## Launch Checklist (marketing-godin)

### Gumroad Setup (30 min)
- [ ] Create Gumroad product
- [ ] Set name: "ConnectPath Unlimited"
- [ ] Set price: $9.99/month (recurring)
- [ ] Copy description from `gumroad-listing.txt`
- [ ] Publish product
- [ ] Copy product URL
- [ ] Update `index.html` line 374 with real URL
- [ ] Redeploy (push to Git or `wrangler pages deploy`)

### Launch Copy (1 hour)
- [ ] Write Product Hunt post
- [ ] Write launch tweet
- [ ] Write Hacker News post (if applicable)
- [ ] Prepare Reddit post (if applicable)

**Launch Prep Status**: ☐ Ready ☐ Not Ready

**Gumroad URL**: _______________

---

## Go / No-Go Decision

### Required for GO:
- ✅ Deployment successful (site is live)
- ✅ Search works (at least one successful search)
- ✅ Rate limiting works (paywall appears)
- ✅ Mobile doesn't break (basic layout OK)
- ✅ No critical console errors

### Nice to Have (Not Blockers):
- High success rate (> 40% searches find path)
- Fast search (< 5 seconds)
- Perfect mobile design
- All browsers tested

### Decision: ☐ GO ☐ NO-GO

**If GO**: Proceed to launch
**If NO-GO**: Document blockers, fix, re-test

---

## Launch Timeline

**Day 1** (Today):
- 9am: devops-hightower starts deploy
- 10am: Deployment live, QA starts testing
- 12pm: QA complete, bugs logged
- 2pm: Critical bugs fixed (if any)
- 4pm: Final deploy + smoke test
- 5pm: **GO/NO-GO decision**

**Day 2**:
- 9am: marketing-godin creates Gumroad listing
- 11am: Gumroad URL updated in code
- 12pm: Redeploy with real Gumroad link
- 2pm: Launch prep (PH, Twitter, etc.)

**Day 3**:
- 12:01am PST: Launch on Product Hunt
- 9am: Post to Twitter, HN, Reddit
- Monitor metrics throughout day

---

## Emergency Contacts

**Deployment issues**: devops-hightower
**Product bugs**: qa-bach → fullstack-dhh
**Launch questions**: marketing-godin
**Business decisions**: ceo-bezos

---

## Rollback Plan

If deployment breaks:

1. Go to Cloudflare Dashboard → Pages → Deployments
2. Click on previous working deployment
3. Click "Rollback to this deployment"

Or:

```bash
git revert HEAD
git push origin main
# Cloudflare auto-deploys the revert
```

---

## Success Criteria

**Minimum Viable Launch**:
- ✅ Site is live and accessible
- ✅ At least 1 successful search works
- ✅ Paywall appears after 3 searches
- ✅ Mobile users can complete a search
- ✅ No 500 errors

**If all 5 are true → SHIP IT**

---

## Post-Launch (Week 1)

### Monitor Daily:
- Search volume (how many searches/day?)
- Success rate (% finding a path)
- Error rate (% returning errors)
- Paywall hits (how many hitting limit?)
- Gumroad sales (any conversions?)

### Tools:
- Cloudflare Analytics (page views)
- `wrangler tail` (real-time logs)
- `wrangler kv:key list` (rate limit data)
- Gumroad dashboard (sales)

---

**Status**: Ready to ship 🚀

**Next Action**: devops-hightower → Start deployment (see QUICKSTART.md)
