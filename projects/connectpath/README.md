# ConnectPath - AI Agent Connection Service

An AI agent that helps you reach anyone in the world by researching targets, mapping connection chains, and drafting personalized outreach emails.

## What It Does

ConnectPath takes the "6 degrees of separation" concept and automates it with AI:

1. **User inputs**: CV/intro + target person + motivation
2. **AI agent researches**: Target's background, interests, and public presence
3. **AI finds paths**: Potential intermediaries who can bridge the connection
4. **AI drafts emails**: Personalized outreach for each step in the chain
5. **User reviews & sends**: Get the draft emails and send when ready

## Tech Stack

- **Frontend**: HTML + Tailwind CSS + vanilla JS (bilingual EN/中文)
- **Backend**: Cloudflare Workers + D1 Database
- **AI**: Claude Sonnet 4.5 (Anthropic API)
- **Payment**: Gumroad credit packages
- **Infrastructure**: Cloudflare (Workers, D1, KV, Queues)

## Pricing Model

| Plan | Credits | Price |
|------|---------|-------|
| Starter | 10 | £5 |
| Growth | 50 | £20 |
| Pro | 200 | £50 |
| Unlimited | ∞ (1 month) | £99 |

**1 credit = 1 agent search operation** (research target, find intermediary, draft email)

## Setup

### 1. Create D1 Database

```bash
cd projects/connectpath
wrangler d1 create connectpath-db
```

Copy the database ID and update `wrangler.toml`:

```toml
database_id = "YOUR_DATABASE_ID"
```

### 2. Initialize Database Schema

```bash
wrangler d1 execute connectpath-db --file=schema.sql
```

### 3. Create KV Namespace (optional)

```bash
wrangler kv:namespace create "connectpath-kv"
```

Update `wrangler.toml` with the KV namespace ID.

### 4. Set Secrets

```bash
# Anthropic API key for Claude
wrangler secret put ANTHROPIC_API_KEY

# Gumroad webhook secret (if using webhook verification)
wrangler secret put GUMROAD_WEBHOOK_SECRET
```

### 5. Deploy Worker

```bash
wrangler deploy
```

### 6. Setup Gumroad Products

Create 4 products on Gumroad:
- ConnectPath Starter (£5) - custom field: `plan=starter`
- ConnectPath Growth (£20) - custom field: `plan=growth`
- ConnectPath Pro (£50) - custom field: `plan=pro`
- ConnectPath Unlimited (£99) - custom field: `plan=unlimited`

Configure webhook to: `https://YOUR-WORKER.workers.dev/api/webhook/gumroad`

Update `intake.html` with real Gumroad product links.

## Development

### Run locally

```bash
wrangler dev
```

### Test database queries

```bash
wrangler d1 execute connectpath-db --command="SELECT * FROM users"
```

## API Endpoints

### POST /api/campaigns
Create new campaign

**Body**:
```json
{
  "email": "user@example.com",
  "cv": "I'm a software engineer...",
  "target_name": "Elon Musk",
  "target_role": "CEO at Tesla",
  "motivation": "Want to discuss AI safety...",
  "plan": "starter"
}
```

**Response**:
```json
{
  "success": true,
  "campaign_id": "uuid",
  "message": "Campaign created. Complete payment to start AI agent."
}
```

### GET /api/dashboard?email=user@example.com
Get user credits and campaigns

**Response**:
```json
{
  "credits": 50,
  "campaigns": [
    {
      "id": "uuid",
      "target_name": "Elon Musk",
      "status": "completed",
      "credits_used": 3,
      "results": { ... }
    }
  ]
}
```

### POST /api/webhook/gumroad
Gumroad webhook handler (adds credits after purchase)

### GET /api/campaign/:id
Get single campaign details with steps

## Database Schema

### users
- id, email, credits_balance, created_at, updated_at

### campaigns
- id, user_id, email, cv, target_name, target_role, motivation, status, credits_used, results, created_at, updated_at

### campaign_steps
- id, campaign_id, step_type, step_description, credits_cost, result, status, created_at, completed_at

### credit_transactions
- id, user_id, amount, transaction_type, plan, campaign_id, created_at

## AI Agent Logic

The agent runs 3 steps per campaign:

1. **Research Target** (1 credit)
   - Professional background
   - Interests and passions
   - Recent public content
   - Potential connection points

2. **Find Intermediaries** (1 credit)
   - 2-3 potential bridge people
   - Connection strength analysis
   - How to reach them

3. **Draft Emails** (1 credit)
   - Personalized email to each intermediary
   - Direct email to target (backup)
   - Concise, specific, actionable

Total: **3 credits per campaign**

## Future Enhancements (V2+)

- [ ] Actually send emails on user's behalf (with Gmail API)
- [ ] Track email open rates and replies
- [ ] LinkedIn API integration for real mutual connections
- [ ] Success-based pricing (pay when target replies)
- [ ] Multi-language support beyond EN/中文
- [ ] Campaign templates for common use cases
- [ ] Team accounts with shared credits

## Deployment

Deployed to: `https://connectpath.jianoujiang.workers.dev`

## License

Proprietary - Auto Company
