# SixDegrees Email — 5-Minute Fix (QUICK REFERENCE)

**Problem:** Email API returns 401
**Solution:** Add ONE DNS record
**Time:** 5 minutes

---

## ⚡ THE FIX (Copy & Paste)

Go to your domain registrar (GoDaddy, Namecheap, Cloudflare DNS, etc.)

Add a TXT record:

```
Name:  _mailchannels.jianou.works
Value: v=mc1 t=sixdegrees.pages.dev
```

Save. Done.

Wait 5-10 minutes. Then test:

```
https://sixdegrees.pages.dev/test-email.html
```

Click "Send Email Now" → Email arrives at Prof. Tom Brown's inbox

---

## 🧪 Verify It Works

```bash
curl -X POST https://sixdegrees.pages.dev/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "tom.brown@tu-berlin.de",
    "subject": "Test",
    "body": "Test"
  }'
```

Should return:
```json
{
  "success": true,
  "status": "sent"
}
```

---

## 📧 Expected Result

- Email arrives in Prof. Tom Brown's inbox in ~5-30 seconds
- Subject: PyPSA Contributors Network — Energy-Tesla Bridge Project
- From: noreply@sixdegrees.pages.dev
- Reply-to: jianou.works@gmail.com

---

## ❓ DNS Registrar Locations

- **GoDaddy:** Settings → Manage DNS
- **Namecheap:** Manage Domain → Advanced DNS
- **Cloudflare:** DNS Records → Add Record
- **AWS Route 53:** Hosted Zones → Records
- **Google Domains:** DNS tab → Custom Records

Look for "Add TXT record" or "Add record"

---

## 🆘 If It Doesn't Work

1. **Wait 10 more minutes** — DNS takes time to propagate
2. **Check record was added:** `nslookup -type=TXT _mailchannels.jianou.works`
3. **Check spelling:**
   - Name: `_mailchannels.jianou.works` (exact)
   - Value: `v=mc1 t=sixdegrees.pages.dev` (exact)
4. **Check it's TXT type** (not CNAME or other)

If still broken: See `/docs/devops/SIXDEGREES-EMAIL-FIX.md` for alternatives

---

## ✅ Success Checklist

- [ ] DNS record added
- [ ] 5-10 minutes waited
- [ ] Test page visited: https://sixdegrees.pages.dev/test-email.html
- [ ] Email sent
- [ ] Email received in inbox
- [ ] Deployment complete ✅

---

Done! Email sending now works.

For detailed info: See `/docs/devops/SIXDEGREES-DEPLOYMENT-COMPLETE.md`
