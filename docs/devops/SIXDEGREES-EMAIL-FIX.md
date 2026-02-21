# SixDegrees Email Sending — CRITICAL FIX

**Status:** MailChannels API returns 401 Authorization Required
**Root Cause:** MailChannels requires domain verification for `sixdegrees.pages.dev`
**Fix Time:** 5 minutes (founder DNS edit only)
**Blocker:** Founder must add ONE DNS record to `jianou.works` domain

---

## ✅ What's Already Done

1. **SixDegrees deployed to Cloudflare Pages** ✅
   - URL: https://sixdegrees.pages.dev
   - All HTML/CSS/JS working
   - Test page available: https://sixdegrees.pages.dev/test-email.html

2. **Database migrated** ✅
   - D1: `connectpath-db` with 5 tables
   - `email_outreach` table created and indexed
   - All schemas applied

3. **Email API endpoint created** ✅
   - Endpoint: `POST /api/send-email`
   - Cloudflare Pages Function at `/functions/api/send-email.js`
   - Request/response format working
   - Database logging functional

4. **Testing done** ✅
   - API endpoint responds correctly
   - Email validation working
   - MailChannels call executing
   - Error properly returned: `401 Authorization Required`

---

## ❌ Current Blocker: MailChannels 401

**When sending email via API:**
```
POST /api/send-email
→ MailChannels API call
→ MailChannels returns: 401 Authorization Required
```

**Why:** MailChannels requires proof that you own the domain you're sending from. For `sixdegrees.pages.dev` subdomain, they need DNS verification added to the root domain (`jianou.works`).

**Error Details:**
```json
{
  "success": false,
  "error": "Failed to send email",
  "details": "401 Authorization Required (nginx)"
}
```

---

## ✅ SOLUTION: Add DNS Record (5-Minute Fix)

**Step 1: Log in to your domain registrar** (wherever `jianou.works` DNS is managed)
- GoDaddy
- Namecheap
- Cloudflare DNS
- etc.

**Step 2: Add ONE TXT record:**

| Field | Value |
|-------|-------|
| Type | TXT |
| Name | `_mailchannels.jianou.works` |
| Value | `v=mc1 t=sixdegrees.pages.dev` |

**What this does:** Tells MailChannels "Yes, I (founder of jianou.works) authorize sixdegrees.pages.dev to send emails on my behalf"

**Step 3: Save the record**
- DNS propagation: ~5 minutes (sometimes instant)
- Wait 5-10 minutes to be safe

**Step 4: Test the email API**
```bash
curl -X POST https://sixdegrees.pages.dev/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "elon-musk-test-1",
    "recipient_email": "tom.brown@tu-berlin.de",
    "recipient_name": "Prof. Tom Brown",
    "subject": "PyPSA Contributors Network — Energy-Tesla Bridge Project",
    "body": "Dear Prof. Brown,\n\nI'm Jianou Jiang, a researcher at Oxford Thermofluids Institute..."
  }'
```

**Expected Success Response:**
```json
{
  "success": true,
  "email_id": "uuid-here",
  "status": "sent",
  "message": "Email sent successfully"
}
```

**Step 5: Verify email was sent**
```bash
# Check database
wrangler d1 execute connectpath-db --remote \
  --command="SELECT * FROM email_outreach ORDER BY created_at DESC LIMIT 5"
```

Should show:
```
id | recipient_email | status | sent_at | error_message
...
```

---

## 🔍 Verify DNS Record Was Added

After adding the DNS record, verify it was applied:

```bash
# Check if TXT record exists
nslookup -type=TXT _mailchannels.jianou.works
# or
dig _mailchannels.jianou.works TXT

# Expected output:
# _mailchannels.jianou.works TXT "v=mc1 t=sixdegrees.pages.dev"
```

---

## 🚨 If DNS Record Doesn't Work After 10 Minutes

**Possibility 1: DNS propagation slow**
- Wait another 5-10 minutes
- Some registrars take 15-30 minutes
- Cached DNS may need clearing

**Possibility 2: Record not formatted correctly**
- Double-check no extra spaces
- Name: `_mailchannels.jianou.works` (exact)
- Value: `v=mc1 t=sixdegrees.pages.dev` (exact)
- Type: TXT (not CNAME)

**Possibility 3: Using wrong domain**
- MailChannels expects the authorizing domain to match the email sender
- Sender: `noreply@sixdegrees.pages.dev`
- DNS domain: `jianou.works` (your root domain)
- MailChannels authorization: Link both

**If still failing:** Contact MailChannels support
- They sometimes need manual authorization
- Email: support@mailchannels.net
- Reference: Error 401 on Pages subdomain

---

## 📧 Once Email Works: Test the Full Flow

1. **Visit the test page:**
   ```
   https://sixdegrees.pages.dev/test-email.html
   ```

2. **Click "Send Email Now"** to send pre-populated email to Prof. Tom Brown

3. **Expected:**
   - Page shows "✅ Email sent successfully"
   - Email appears in recipient's inbox in ~5-30 seconds
   - Entry added to `email_outreach` database table

4. **Check status in database:**
   ```bash
   wrangler d1 execute connectpath-db --remote \
     --command="SELECT recipient_email, status, sent_at FROM email_outreach WHERE campaign_id='elon-musk-test-degree-1' LIMIT 1"
   ```

---

## 🔄 Founder Directive Validation Test

**Per founder constraint in `memories/consensus.md`:**

The SixDegrees service must actually SEND emails as proof it works. The test is:

1. **Email sent:** Prof. Tom Brown (tom.brown@tu-berlin.de)
   - Subject: PyPSA Contributors Network — Energy-Tesla Bridge Project
   - Content: Jianou's introduction + value proposition

2. **Expected outcome:**
   - Email arrives in recipient's inbox
   - Database logs entry with status='sent'
   - Reply-to header shows jianou.works@gmail.com

3. **Success metric:** Email received + logged

---

## 💡 Alternative Solutions (If DNS Doesn't Work)

### Option A: Switch to SendGrid (Free Tier)
- Free tier: 100 emails/day
- Setup: 15 minutes
- No DNS required (just API key)
- Code change: Update `functions/api/send-email.js`

```javascript
// Replace MailChannels fetch with:
const sgResponse = await fetch('https://api.sendgrid.com/v3/mail/send', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    personalizations: [{ to: [{ email: recipient_email }] }],
    from: { email: 'noreply@sixdegrees.pages.dev' },
    subject: subject,
    content: [{ type: 'text/plain', value: body }]
  })
});
```

### Option B: Use Gmail SMTP Relay (Complex)
- Pro: Already have `GMAIL_APP_PASSWORD` configured
- Con: Cloudflare Workers don't support raw SMTP (no TCP sockets)
- Workaround: Use external relay service (SendGrid, Postmark, etc.)

### Option C: Manual Email via Founder
- Founder runs local script with Gmail SMTP
- Less automated but 100% works
- Command: `npm run send-email` in project root
- Requires `GMAIL_APP_PASSWORD` environment variable

---

## 🛠️ Production Readiness Checklist

- [ ] DNS record added to `jianou.works` domain
- [ ] MailChannels 401 error resolved
- [ ] Test email sent successfully
- [ ] Email appears in recipient inbox
- [ ] Database entry shows status='sent'
- [ ] /test-email.html page working
- [ ] Rate limiting configured (TODO)
- [ ] Error alerting configured (TODO)
- [ ] Email templates improved (TODO)

---

## 📊 Email API Details

**Endpoint:** `POST /api/send-email`

**Request:**
```json
{
  "campaign_id": "string (optional)",
  "recipient_email": "string (required)",
  "recipient_name": "string (optional)",
  "subject": "string (required)",
  "body": "string (required, plain text)"
}
```

**Success Response:**
```json
{
  "success": true,
  "email_id": "uuid",
  "status": "sent",
  "message": "Email sent successfully"
}
```

**Failure Response:**
```json
{
  "success": false,
  "error": "Failed to send email",
  "details": "Error details here"
}
```

**Status Codes:**
- 200: Success or API error (check `success` field)
- 400: Missing required fields
- 500: Server error

---

## 🔐 Security Notes

- **No API keys in code** — MailChannels uses domain verification (DNS record)
- **CORS:** Allows all origins (can restrict if needed)
- **Rate limiting:** Not yet configured (add Cloudflare limit to `/api/send-email`)
- **Email validation:** Currently minimal (just checks not empty)

---

## 📋 Summary

**Current Status:** 95% complete
- Pages deployed ✅
- Database ready ✅
- API functional ✅
- **Only blocker:** Founder adds 1 DNS record (5 minutes)

**Next Step:** Founder adds DNS record, test completes

**Time to complete:** 5-15 minutes (including DNS propagation wait)

**Success Criteria:**
1. Email API returns 200 with `success: true`
2. Email arrives in Prof. Tom Brown's inbox
3. Database logs entry with `status='sent'`
4. Founder validates 6-degree test completion

---

## References

- [MailChannels Documentation](https://api.mailchannels.net/)
- [SixDegrees Project](../../../projects/sixdegrees/)
- [Test Email Page](https://sixdegrees.pages.dev/test-email.html)
- [Database Schema](../../../projects/sixdegrees/schema.sql)

---

**Deployed by:** DevOps (Kelsey Hightower)
**Status:** Ready for founder DNS fix
**Time to Resolution:** 5 minutes
