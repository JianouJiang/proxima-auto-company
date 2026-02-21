# ConnectPath MVP

**Find professional connections in 6 degrees of separation.**

ConnectPath helps you discover hidden professional relationships by finding the shortest path between any two people using public data from GitHub, Twitter, Crunchbase, and company team pages.

## Features

- **Bilingual UI**: English + Simplified Chinese
- **Free tier**: 3 searches per day
- **Fast search**: Results in < 5 seconds
- **Mobile-first**: Responsive design
- **Privacy-focused**: Only public data, no login required

## Tech Stack

- **Frontend**: Vanilla JS (no framework bloat)
- **Backend**: Cloudflare Workers (serverless)
- **Database**: Cloudflare KV (rate limiting + cache)
- **APIs**: GitHub REST API (primary data source)
- **Hosting**: Cloudflare Pages

## Setup

### 1. Prerequisites

- Cloudflare account (free tier)
- GitHub account
- GitHub Personal Access Token

### 2. Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Required:
- `GITHUB_TOKEN`: Create at https://github.com/settings/tokens
  - Scopes needed: `public_repo`, `read:user`
  - This increases rate limit from 60/hr to 5,000/hr

### 3. Cloudflare KV Setup

Create a KV namespace for rate limiting:

```bash
wrangler kv:namespace create "CONNECTPATH_KV"
```

Note the namespace ID and bind it in `wrangler.toml` (see below).

### 4. Deploy to Cloudflare Pages

#### Option A: GitHub Integration (Recommended)

1. Push this directory to GitHub
2. Go to Cloudflare Dashboard → Pages
3. Create new project → Connect to Git
4. Select your repo
5. Build settings:
   - Build command: (leave empty)
   - Build output directory: `/`
   - Root directory: `projects/connectpath`
6. Environment variables:
   - Add `GITHUB_TOKEN`
7. Deploy

#### Option B: Direct Upload

```bash
# Install Wrangler if not already
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler pages publish . --project-name=connectpath
```

### 5. Configure KV Binding

In Cloudflare Dashboard → Pages → Your Project → Settings → Functions:

Add KV namespace binding:
- Variable name: `CONNECTPATH_KV`
- KV namespace: Select the one you created

### 6. Test

Visit your deployed URL (e.g., `connectpath.pages.dev`)

Try searching for:
- Person A: `torvalds` (Linus Torvalds on GitHub)
- Person B: `tj` (TJ Holowaychuk on GitHub)

## Project Structure

```
connectpath/
├── index.html              # Frontend SPA
├── functions/
│   └── api/
│       └── search.js       # Cloudflare Workers API
├── .env.example            # Environment variables template
├── README.md               # This file
└── gumroad-listing.txt     # Gumroad product description
```

## How It Works

### Search Algorithm

1. **Input**: User enters two names/emails
2. **Resolve identities**: Search GitHub API for matching users
3. **BFS graph search**:
   - Start from Person A
   - Explore followers + following
   - Track visited nodes to avoid cycles
   - Stop at 3 degrees (free tier) or when target found
4. **Return path**: Display connection chain with confidence score

### Rate Limiting

- **Client-side**: localStorage tracks searches per day
- **Server-side**: Cloudflare KV stores IP-based rate limits
- **Free tier**: 3 searches/day per IP
- **Reset**: Daily at midnight UTC

### Data Sources (MVP)

- ✅ **GitHub API**: Followers, following, org memberships, profile data
- ⏳ **Twitter/X API**: (Future) Follows, mentions, bio
- ⏳ **Crunchbase**: (Future) Company employees, investors
- ⏳ **Web scraping**: (Future) Company team pages

## Monetization

### Free Tier
- 3 searches per day
- Up to 3 degrees of separation
- Text-based results

### Paid Tier ($9.99/month via Gumroad)
- Unlimited searches
- Up to 6 degrees of separation
- Export to PDF
- Priority support

Link: https://jiangyingjuner.gumroad.com/l/connectpath-unlimited

## Metrics to Track

1. **Search success rate**: % of searches that find a path (target: >40%)
2. **Average degree**: Average path length (target: 2-4 degrees)
3. **Completion rate**: % of users who complete full flow (target: >70%)
4. **Free → Paid conversion**: % hitting paywall who upgrade (target: >5%)

## Known Limitations

- **GitHub-centric**: MVP only searches GitHub profiles
- **Public data only**: No LinkedIn, no private profiles
- **Rate limits**: GitHub API has 5,000/hr limit with token
- **Shallow search**: Free tier stops at 3 degrees (not 6)

## Roadmap

### V1.1 (Week 2)
- [ ] Add Twitter/X API integration
- [ ] Improve name disambiguation (multiple John Smiths)
- [ ] Cache search results in KV (reduce API calls)

### V1.2 (Week 3)
- [ ] Crunchbase integration (company/investor data)
- [ ] Export path to PDF
- [ ] Share link generation

### V2.0 (Month 2)
- [ ] User accounts (save search history)
- [ ] API endpoint for programmatic access
- [ ] D3.js graph visualization
- [ ] Bulk upload (CSV)

## Troubleshooting

### "Rate limit exceeded" error
- GitHub API has limits: 60/hr (no token) or 5,000/hr (with token)
- Solution: Add `GITHUB_TOKEN` to environment variables

### "No path found" for known connections
- MVP only searches GitHub followers/following
- If people don't follow each other on GitHub, no path will be found
- Solution: Wait for Twitter/Crunchbase integration

### Search is slow (>10s)
- BFS explores many nodes
- Solution: Reduce `MAX_NODES` in `search.js` or add caching

## Contributing

This is an MVP built by AI agents. Code is intentionally simple and unoptimized.

Priorities:
1. **Shipping > Perfection** — Get it working first
2. **Simple > Complex** — No fancy frameworks
3. **Free > Paid APIs** — Minimize costs in MVP phase

## License

Proprietary. Built by Proxima Auto Company.

## Support

Questions? Issues? Contact: [your-email@example.com]

---

**Built with ❤️ by fullstack-dhh agent in 4 hours.**
