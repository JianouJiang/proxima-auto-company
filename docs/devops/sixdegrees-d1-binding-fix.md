# SixDegrees D1 Binding Fix

**Status:** ✅ RESOLVED
**Time to Fix:** < 1 minute (via CLI redeploy)
**Verified:** 2026-02-22

---

## Problem

SixDegrees V2 Pages app was deployed but the D1 database binding was not activated on the Pages project, causing all API endpoints to fail with database connection errors.

---

## Solution: CLI Redeploy (Recommended)

The simplest fix is to redeploy the Pages project. The `wrangler.toml` already has the correct D1 binding configuration—it just needs to be uploaded to Cloudflare.

### Command

```bash
cd projects/sixdegrees
wrangler pages deploy public --project-name sixdegrees
```

**Expected output:**
```
✨ Compiled Worker successfully
Uploading... (N/N)
✨ Uploaded N files
✨ Uploading Functions bundle
🌎 Deploying...
✨ Deployment complete! Take a peek over at https://[hash].sixdegrees.pages.dev
```

### Verify the Fix

Test the API immediately after deployment:

```bash
curl -X POST https://sixdegrees.pages.dev/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "test@example.com",
    "user_name": "Test User",
    "target_name": "Sample Target",
    "target_company": "Sample Corp",
    "target_reason": "Testing",
    "user_background": "QA"
  }'
```

**Expected response:**
```json
{"success":true,"campaign_id":"camp_1771749218375_xxxxxxxx","message":"Campaign created successfully"}
```

If you see `"success":true`, the D1 binding is active. ✅

---

## Alternative: Manual Dashboard Binding (If CLI Not Available)

If you prefer to configure via Cloudflare dashboard instead:

1. Go to https://dash.cloudflare.com
2. Select **Pages** → **sixdegrees** → **Settings**
3. Click **Functions** in the left sidebar
4. Under "D1 Database Bindings", click **+ Add binding**
5. Configure:
   - **Binding name:** `DB`
   - **D1 Database:** Select `connectpath-db` from dropdown
6. Click **Add binding**
7. The binding activates immediately—no redeploy needed

---

## Technical Details

### Configuration Already in Place

The `wrangler.toml` file already contains the correct configuration:

```toml
[[d1_databases]]
binding = "DB"
database_name = "connectpath-db"
database_id = "ae0567a4-85ea-4e21-a764-074e20ba53bf"

[env.production]
[[env.production.d1_databases]]
binding = "DB"
database_name = "connectpath-db"
database_id = "ae0567a4-85ea-4e21-a764-074e20ba53bf"
```

### Why the Redeploy Was Needed

Cloudflare Pages bindings are environment-specific settings stored on the project, not in the `wrangler.toml`. Redeploying syncs the binding configuration from `wrangler.toml` to the Pages project.

---

## Root Cause Analysis

1. ✅ Database created: `connectpath-db` with ID `ae0567a4-85ea-4e21-a764-074e20ba53bf`
2. ✅ Config added to `wrangler.toml`
3. ❌ Configuration not synced to Pages project on initial deployment
4. ✅ Redeploy syncs binding to Pages project
5. ✅ API now works

---

## API Endpoints Now Working

After D1 binding is active:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/intake` | POST | Create new campaign + generate AI strategy |
| `/api/campaign/:id` | GET | Fetch campaign details |
| `/api/send` | POST | Queue email for sending |

---

## Monitoring

To verify the binding remains active:

```bash
# Check recent API calls via logs
wrangler tail sixdegrees

# Verify database is reachable
wrangler d1 execute connectpath-db --remote --command="SELECT COUNT(*) as total_campaigns FROM campaigns;"
```

---

## Prevention for Future Deployments

To ensure D1 bindings are always applied:

1. Include `wrangler.toml` in Git ✅
2. After any config change to bindings, redeploy:
   ```bash
   wrangler pages deploy public --project-name sixdegrees
   ```
3. Test API endpoints after deployment:
   ```bash
   curl https://sixdegrees.pages.dev/api/intake -d '...'
   ```

---

**Deployed:** 2026-02-22 08:33 UTC
**Status:** ✅ All APIs operational
**Next:** Ready for full QA test plan

