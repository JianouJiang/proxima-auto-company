# Paywall Testing Guide

**For:** QA, DevOps, or anyone testing the payment flow
**Date:** 2026-02-20

## Quick Local Test (5 minutes)

### 1. Start Dev Server

```bash
cd projects/coldcopy/frontend
npm run dev
```

Visit `http://localhost:5173`

### 2. Force Paywall to Appear

**Option A: Modify Code (Temporary)**

Edit `frontend/src/pages/Generate.tsx` line ~142:

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // TESTING: Force paywall
  setShowPaywall(true);
  return;

  // ... rest of handleSubmit
};
```

Fill out form → Click "Generate Sequence" → Paywall appears instantly.

**Option B: Browser DevTools (No Code Change)**

1. Open DevTools (F12)
2. Go to Network tab
3. Fill out form and click "Generate Sequence"
4. Right-click the `/api/generate` request → "Edit and Resend"
5. Change method to `POST`, send
6. Paywall should appear

**Option C: Actually Hit Quota**

If backend is running with ANTHROPIC_API_KEY:
1. Generate 1 sequence (free tier)
2. Try to generate a 2nd sequence
3. Should return 402 → Paywall appears

### 3. Test Paywall UI

**Verify:**
- [ ] Modal appears over page (dark overlay)
- [ ] Two pricing cards visible (Starter + Pro)
- [ ] "Most Popular" badge on Pro card
- [ ] Close button (X) works
- [ ] Clicking outside modal doesn't close it (intentional)
- [ ] Mobile responsive (resize browser to 375px width)

### 4. Test Payment Links

**Verify:**
- [ ] "Get Starter" button opens Stripe checkout
- [ ] "Go Pro" button opens Stripe checkout
- [ ] Links open in new tab (doesn't navigate away)

**Use Stripe Test Cards:**

| Card Number | Result |
|-------------|--------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 9995` | Decline (insufficient funds) |

- Any future expiry date (e.g., 12/34)
- Any 3-digit CVC (e.g., 123)
- Any ZIP code (e.g., 12345)

### 5. Test Success Page

After completing payment on Stripe:

**Verify:**
- [ ] Redirects to `/success` (may need to manually navigate for now)
- [ ] Green check icon appears
- [ ] "Payment Successful" message
- [ ] Next steps (1-4) are clear
- [ ] "Return to ColdCopy" button works

**To test locally without payment:**

Navigate to `http://localhost:5173/success?session_id=test123`

### 6. Test Cancel Page

After clicking back on Stripe checkout:

**Verify:**
- [ ] Redirects to `/cancel` (may need to manually navigate for now)
- [ ] X icon appears
- [ ] "Payment Cancelled" message
- [ ] Friendly tone (no guilt)
- [ ] Both CTAs work ("Back to ColdCopy", "Go to Homepage")

**To test locally:**

Navigate to `http://localhost:5173/cancel`

## Full End-to-End Test (Production)

### Prerequisites
- ColdCopy deployed to Cloudflare Pages
- Backend API live with working `/api/generate` endpoint
- Stripe Payment Links updated with production URLs

### Test Flow

1. **Hit Quota:**
   - Visit https://coldcopy-app.pages.dev
   - Generate 1 free sequence
   - Try to generate 2nd sequence
   - **Expected:** 402 response → Paywall appears

2. **Start Payment:**
   - Click "Go Pro" (or "Get Starter")
   - **Expected:** Stripe checkout loads

3. **Complete Payment:**
   - Fill in test card `4242 4242 4242 4242`
   - **Expected:** Payment succeeds

4. **Success Redirect:**
   - **Expected:** Redirects to `/success?session_id=xxx`
   - Success message appears
   - Transaction ID shown

5. **Return to App:**
   - Click "Return to ColdCopy"
   - **Expected:** Back to `/generate` page
   - (Note: Quota won't be updated yet — manual process for MVP)

### Test Cancellation

1. Open paywall
2. Click payment link
3. On Stripe page, click browser back button
4. **Expected:** Redirects to `/cancel`
5. Cancel message appears
6. Both CTAs work

## Stripe Dashboard Verification

After test payment:

1. Login to Stripe Dashboard
2. Go to Payments
3. **Verify:**
   - [ ] Payment appears with correct amount ($19 or $39)
   - [ ] Status is "Succeeded"
   - [ ] Customer email captured
   - [ ] Metadata includes correct product (if set)

## Edge Cases to Test

### 1. Paywall Opens Twice

**Test:** Open paywall, close it, trigger 402 again.
**Expected:** Paywall opens again (no issue).

### 2. User Pays But Backend Doesn't Know

**Current behavior:** User pays, backend quota unchanged (manual fulfillment).
**Expected:** Success page tells user "wait 24 hours for quota upgrade".
**Fix needed?** No (for MVP). Document this in success message.

### 3. User Closes Paywall and Leaves

**Test:** Open paywall, close it, navigate away.
**Expected:** User can come back later, paywall will reappear on next 402.

### 4. Multiple Browser Tabs

**Test:** Open 2 tabs, trigger 402 in both.
**Expected:** Both show paywall independently. Paying in one doesn't update the other (until page refresh).

### 5. Mobile Safari

**Test:** Open on iPhone/iPad, trigger paywall.
**Expected:** Modal is full-screen, scrollable, buttons tappable.

## Visual Regression Tests (Optional)

Take screenshots of:
1. Paywall modal (desktop)
2. Paywall modal (mobile)
3. Success page
4. Cancel page

Compare after any CSS changes to ensure no regressions.

## Performance Tests

**Paywall Load Time:**
- Open DevTools Performance tab
- Trigger paywall
- **Expected:** Modal appears in <100ms (it's just state change, no API call)

**Page Weight:**
- Check Network tab
- **Expected:** No additional HTTP requests when paywall opens (all code is bundled)

## Accessibility Tests

**Keyboard Navigation:**
- [ ] Tab to "Close" button
- [ ] Tab to "Get Starter" button
- [ ] Tab to "Go Pro" button
- [ ] Press Enter on buttons (should work)
- [ ] Press Escape (should close modal — not implemented yet, OK for MVP)

**Screen Reader:**
- [ ] Close button has aria-label
- [ ] Pricing cards are readable
- [ ] Success/Cancel pages are readable

## Known Issues (Acceptable for MVP)

1. **Escape key doesn't close modal** — Could add, but not critical.
2. **Clicking outside modal doesn't close** — Intentional (user must decide).
3. **No "Already paid?" link** — User must email support. OK for MVP.
4. **Success URL has dummy session_id in dev** — Need production Stripe config.

## Troubleshooting

**Paywall doesn't appear:**
- Check console for errors
- Verify 402 response is returned from `/api/generate`
- Check `showPaywall` state in React DevTools

**Payment link doesn't open:**
- Check browser console (popup blocked?)
- Verify links are correct in `Paywall.tsx` lines 9-10

**Success page blank:**
- Check route is added in `App.tsx`
- Check URL matches `/success` exactly

**Icons don't render:**
- Verify lucide-react is installed: `npm list lucide-react`
- Check import paths in Success/Cancel pages

## Deployment Checklist

Before deploying:
- [ ] Build succeeds: `npm run build`
- [ ] No TypeScript errors: `npm run type-check` (if script exists)
- [ ] No console errors when paywall opens
- [ ] Payment links are correct (review `Paywall.tsx`)
- [ ] Success/Cancel routes added to `App.tsx`

After deploying:
- [ ] Update Stripe Payment Links with production URLs
- [ ] Test full flow on production
- [ ] Monitor Stripe Dashboard for test payments
- [ ] Document any issues in Slack/GitHub

---

**Testing completed?** Mark this doc as reviewed and hand off to QA/DevOps.
