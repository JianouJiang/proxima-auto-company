# FlowPrep AI Landing Page Deployment

## Status

**LIVE** - FlowPrep AI landing page deployed to Cloudflare Pages.

## Deployment Details

### Live URL

**Primary URL:** https://flowprep-ai.pages.dev/

**Custom Domain:** To enable custom domain (flowprep.ai), create CNAME record in DNS:
```
flowprep.ai CNAME flowprep-ai.pages.dev
```

### Cloudflare Pages Project

- **Project Name:** `flowprep-ai`
- **Account:** jianou.works@gmail.com
- **Account ID:** 68ec8b1ccccb48e1a7cf898d2228c713
- **Build Type:** Static (no build step required)
- **Root Directory:** `public/`
- **Production Branch:** main

### Deployment Metadata

- **Deployment Date:** 2026-02-21 11:04 UTC
- **Deployment ID:** 01ebc1f3
- **Status:** Success
- **Files Deployed:** 1 (index.html)
- **Size:** 0.74 sec upload time
- **Deployment URL:** https://01ebc1f3.flowprep-ai.pages.dev/

## Architecture

FlowPrep AI landing page is a **100% static site** deployed on Cloudflare Pages with the following stack:

- **Hosting:** Cloudflare Pages (CDN + edge caching)
- **HTML:** Single-page static HTML with embedded Tailwind CSS
- **Styling:** Tailwind CSS v4 (CDN)
- **Interactivity:** Vanilla JavaScript (native HTML `<details>` elements for FAQs)
- **Payment Integration:** Stripe Payment Links (external, no backend required)
- **Analytics:** Cloudflare Web Analytics (to be configured)

## Performance

- **Latency:** Global CDN edge servers
- **Caching:** Automatic Cache-Control headers on .pages.dev domain
- **Minification:** Automatic on Cloudflare
- **SSL/TLS:** Automatic, A+ rating

## Web Analytics Setup

Cloudflare Web Analytics provides privacy-respecting analytics without third-party cookies.

### How to Enable

1. **Get Beacon Token:**
   - Go to Cloudflare Dashboard → Analytics & Logs → Web Analytics
   - Click "Create Site" → select domain: `flowprep-ai.pages.dev`
   - Copy the beacon token (format: `abc123def456`)

2. **Update index.html:**
   ```html
   <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "YOUR_BEACON_TOKEN_HERE"}'></script>
   ```
   Replace `YOUR_BEACON_TOKEN_HERE` with actual token from step 1.

3. **Redeploy:**
   ```bash
   cd projects/flowprep
   npx wrangler pages deploy public --project-name=flowprep-ai
   ```

### Metrics Available

Once enabled, Web Analytics tracks:
- **Page Views** - Unique and total
- **Visits** - Session counts
- **Bounce Rate** - Single-page sessions
- **Core Web Vitals** - LCP, FID, CLS
- **Device Type** - Mobile/Desktop/Tablet
- **Country** - Geo-location
- **Referrer** - Traffic source
- **Exit Pages** - Where users leave

### Data Retention

- Free tier: 30 days
- No sampling on Cloudflare Pages

## Stripe Integration

### Payment Link

The landing page links to a Stripe Payment Link for early access:
```
https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05
```

**Features:**
- £39/month subscription (early access pricing)
- Automatic email confirmation to customer
- Subscription management via customer portal
- No backend infrastructure required

**Status:** Link tested and working

## Rollback Procedure

### Quick Rollback (Last Deployment)

If the current deployment has issues, rollback to previous version:

```bash
npx wrangler pages deployment rollback --project=flowprep-ai
```

### Manual Rollback (to Specific Version)

1. List recent deployments:
   ```bash
   npx wrangler pages deployments list --project=flowprep-ai
   ```

2. Rollback to specific deployment ID:
   ```bash
   npx wrangler pages deployment rollback --project=flowprep-ai --id <deployment-id>
   ```

3. Verify rollback completed:
   ```bash
   npx wrangler pages deployment view --project=flowprep-ai --id <deployment-id>
   ```

## Deployment Commands Reference

### Deploy new version

```bash
cd /home/jianoujiang/Desktop/proxima-auto-company/projects/flowprep
npx wrangler pages deploy public --project-name=flowprep-ai
```

### Check deployment status

```bash
npx wrangler pages deployment list --project=flowprep-ai
```

### View specific deployment

```bash
npx wrangler pages deployment view --project=flowprep-ai --id <deployment-id>
```

### Preview URL

After deployment, a preview URL is generated. Format:
```
https://<deployment-id>.flowprep-ai.pages.dev/
```

## Monitoring & Alerts

### Manual Checks

- **Uptime:** Monitor at https://flowprep-ai.pages.dev/
- **Core Web Vitals:** Test via Google PageSpeed Insights
- **SSL Certificate:** Automatic renewal by Cloudflare
- **DNS Resolution:** Check CNAME target

### Cloudflare Dashboard Alerts

Coming soon: Set up Cloudflare notifications for:
- High error rates
- DDoS attacks
- SSL/TLS certificate renewal

## Git Integration

### Current Setup

- Repository: proxima-auto-company (GitHub)
- Branch: main
- Cloudflare Pages: Manual deployment via `wrangler pages deploy`

### Future: Auto-Deploy on Git Push

To enable automatic deployment on `git push`:

1. Connect GitHub repo to Cloudflare Pages in dashboard
2. Set build command: `(none)` (static site)
3. Build output directory: `public/`
4. Production branch: `main`

Then:
```bash
git push origin main  # Auto-deploys to production
```

Currently using manual deployment to maintain control over deployment timing.

## File Structure

```
projects/flowprep/
├── public/
│   └── index.html          # Single HTML file, 30KB
├── README.md               # Project README
└── wrangler.toml          # (not required for Pages, but can be added)
```

## Security

### Current Status

- **SSL/TLS:** A+ rating (automatic)
- **DDoS Protection:** Cloudflare managed
- **Bot Management:** Cloudflare managed
- **API Keys:** None exposed (no backend)
- **Sensitive Data:** None stored (static site)

### Hardening Recommendations

1. **Enable Authenticated Origin Pulls** (if adding origin later)
2. **Set Security Headers** in Cloudflare:
   ```
   X-Frame-Options: SAMEORIGIN
   X-Content-Type-Options: nosniff
   X-XSS-Protection: 1; mode=block
   ```
3. **Rate Limiting:** If adding API endpoints
4. **WAF Rules:** Cloudflare Web Application Firewall (free tier)

## Cost Analysis

### Monthly Spend Estimate

| Service | Cost | Notes |
|---------|------|-------|
| Cloudflare Pages | $0 | Free tier (100,000 requests/day) |
| Cloudflare Web Analytics | $0 | Free tier (30-day retention) |
| Stripe Payment Links | 2.9% + £0.20 per transaction | Only on completed sales |
| **Total** | **~£0** | Scales with revenue only |

### Bandwidth Usage

- Current: ~1 KB per page view (HTML only)
- Estimated traffic: 1,000 visitors/day = 1 MB/day
- Monthly estimate: ~30 MB
- Free tier: 100 GB/month

### Cost Optimization

- **CDN:** Cloudflare edge caching (automatic)
- **Compression:** Gzip enabled (automatic)
- **Images:** None in current version (text-based design)
- **Third-party scripts:** Only Tailwind CDN + Stripe Links (minimal)

## Troubleshooting

### Issue: 404 Not Found

**Cause:** Cloudflare Pages redirecting to wrong path

**Solution:**
```bash
# Verify index.html exists in public/
ls -la projects/flowprep/public/

# Redeploy with verbose output
npx wrangler pages deploy public --project-name=flowprep-ai --verbose
```

### Issue: Stripe link not working

**Solution:**
- Test link directly: https://buy.stripe.com/dRm5kD0SH8t7ato54O0VO05
- Verify target="_blank" in HTML
- Check Stripe dashboard for payment link status

### Issue: Analytics not firing

**Solution:**
1. Verify beacon token is correct in HTML
2. Check browser DevTools → Network tab for beacon.min.js request
3. Confirm Cloudflare Web Analytics site is created

### Issue: Custom domain not resolving

**Solution:**
1. Verify CNAME record is set correctly:
   ```bash
   nslookup flowprep.ai
   # Should return: flowprep-ai.pages.dev
   ```
2. Wait 24-48 hours for DNS propagation
3. Check Cloudflare DNS settings in dashboard

## Next Steps

1. **Enable Web Analytics:** Get beacon token and update HTML (5 min)
2. **Custom Domain:** Add CNAME record for flowprep.ai (1 hour for DNS)
3. **Monitor Traffic:** Set up Cloudflare alerts
4. **Git Auto-Deploy:** Connect GitHub repo (optional, for CI/CD)

## Links

- **Live Site:** https://flowprep-ai.pages.dev/
- **Cloudflare Dashboard:** https://dash.cloudflare.com/
- **Wrangler Docs:** https://developers.cloudflare.com/workers/wrangler/
- **Pages Docs:** https://developers.cloudflare.com/pages/
- **Web Analytics Docs:** https://developers.cloudflare.com/analytics/web-analytics/

---

**Last Updated:** 2026-02-21 by Kelsey Hightower (DevOps)
**Next Review:** After Web Analytics enabled and traffic incoming
