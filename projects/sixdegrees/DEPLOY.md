# SixDegrees Deployment Guide

Quick deployment checklist for SixDegrees V2.

## Prerequisites

- Wrangler CLI installed and authenticated
- Cloudflare account
- Anthropic API key for Claude
- Gumroad account (for payments)

## Step-by-Step Deployment

### 1. Create D1 Database

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/connectpath
wrangler d1 create connectpath-db
```

Copy the output `database_id` and update `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "connectpath-db"
database_id = "YOUR_DATABASE_ID_HERE"  # Replace this
```

### 2. Initialize Database Schema

```bash
wrangler d1 execute connectpath-db --file=schema.sql
```

Verify tables created:

```bash
wrangler d1 execute connectpath-db --command="SELECT name FROM sqlite_master WHERE type='table'"
```

Should show: users, campaigns, campaign_steps, credit_transactions

### 3. Create KV Namespace (Optional)

```bash
wrangler kv:namespace create "connectpath-kv"
```

Update `wrangler.toml` with the namespace ID if using KV.

### 4. Set Environment Secrets

```bash
# Anthropic API key for Claude
wrangler secret put ANTHROPIC_API_KEY
# Paste your key when prompted

# Gumroad webhook secret (optional, for webhook verification)
wrangler secret put GUMROAD_WEBHOOK_SECRET
# Generate a random secret and paste it
```

### 5. Deploy Worker

```bash
wrangler deploy
```

Note the deployed URL: `https://connectpath.YOUR-SUBDOMAIN.workers.dev`

### 6. Setup Gumroad Products

Create 4 products on [Gumroad](https://gumroad.com):

1. **SixDegrees Starter** - £5
   - Add custom field: `plan` = `starter`
   - Permalink: `connectpath-starter`

2. **SixDegrees Growth** - £20
   - Add custom field: `plan` = `growth`
   - Permalink: `connectpath-growth`

3. **SixDegrees Pro** - £50
   - Add custom field: `plan` = `pro`
   - Permalink: `connectpath-pro`

4. **SixDegrees Unlimited** - £99
   - Add custom field: `plan` = `unlimited`
   - Permalink: `connectpath-unlimited`

### 7. Configure Gumroad Webhook

In each product settings:
- Go to "Advanced" → "Webhooks"
- Add webhook URL: `https://YOUR-WORKER-URL.workers.dev/api/webhook/gumroad`
- Select "Sale" event
- Save

### 8. Update Frontend Links

Edit `intake.html` line ~180, replace Gumroad links:

```javascript
const gumroadLinks = {
    starter: 'https://gumroad.com/l/connectpath-starter',
    growth: 'https://gumroad.com/l/connectpath-growth',
    pro: 'https://gumroad.com/l/connectpath-pro',
    unlimited: 'https://gumroad.com/l/connectpath-unlimited'
};
```

Replace with your actual Gumroad product URLs.

### 9. Test Full Flow

1. Go to `https://YOUR-WORKER-URL.workers.dev/index.html`
2. Click "Start Your First Connection"
3. Fill intake form with test data
4. Submit (will redirect to Gumroad)
5. Complete test purchase (Gumroad test mode)
6. Check database: `wrangler d1 execute connectpath-db --command="SELECT * FROM users"`
7. Verify credits added
8. Check campaign processing

### 10. Enable Queue Processing

If using Cloudflare Queues for async processing:

```bash
wrangler queues create connectpath-queue
```

Update `wrangler.toml` with queue name, then redeploy:

```bash
wrangler deploy
```

## Production Readiness Checklist

- [ ] D1 database created and initialized
- [ ] Anthropic API key set
- [ ] Worker deployed successfully
- [ ] Gumroad products created
- [ ] Gumroad webhooks configured
- [ ] Frontend links updated
- [ ] End-to-end flow tested
- [ ] Error handling tested
- [ ] Claude API integration tested (uncomment in `worker.js`)
- [ ] Database backups configured (D1 auto-backups)

## Monitoring

Check Worker logs:

```bash
wrangler tail
```

View D1 database:

```bash
wrangler d1 execute connectpath-db --command="SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 10"
```

## Troubleshooting

### Worker not receiving webhook
- Check Gumroad webhook URL is correct
- Verify CORS headers in Worker
- Check Worker logs: `wrangler tail`

### Credits not added after purchase
- Verify webhook is hitting `/api/webhook/gumroad`
- Check user exists in database
- Verify `plan` field in Gumroad product

### Campaign stuck in "processing"
- Check Claude API key is set
- Uncomment real Claude API call in `worker.js`
- Check Worker logs for errors

### Database errors
- Verify schema.sql ran successfully
- Check table names match Worker queries
- Run: `wrangler d1 execute connectpath-db --command="PRAGMA table_info(users)"`

## Custom Domain (Optional)

Add custom domain to Worker:

1. Go to Cloudflare Dashboard → Workers & Pages
2. Select `connectpath` Worker
3. Settings → Triggers → Add Custom Domain
4. Enter `connectpath.yourdomain.com`
5. Update DNS records as prompted

## Cost Estimate

- **D1**: ~£0 (generous free tier: 5GB, 25M reads/month)
- **Workers**: ~£0 (100k requests/day free)
- **Queues**: ~£0 (1M operations/month free)
- **Claude API**: ~£0.003 per campaign (3 API calls × ~£0.001 each)

At 1000 campaigns/month:
- D1: £0
- Workers: £0
- Queues: £0
- Claude: £3
- **Total: ~£3/month**

Revenue at 1000 campaigns (avg £20 per):
- **£20,000/month**

Profit margin: **99.985%**

## Security Notes

- **NEVER** commit API keys to git
- Use `wrangler secret` for all secrets
- Verify Gumroad webhook signatures (optional)
- Validate all user inputs in Worker
- Rate limit API endpoints (TODO)
- Add CAPTCHA to intake form (TODO)

## Next Steps After Deployment

1. Test thoroughly with real payments (small amounts)
2. Monitor first 10 campaigns closely
3. Fix any issues in Claude prompts
4. Improve email draft quality based on feedback
5. Add analytics (Cloudflare Web Analytics)
6. Launch marketing campaign

---

**Ready to ship?** Run: `wrangler deploy`
