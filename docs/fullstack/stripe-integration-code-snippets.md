# Stripe Integration — Code Snippets

Quick reference for key code sections.

## Paywall Component (Core Logic)

```tsx
// frontend/src/components/Paywall.tsx

const STARTER_LINK = 'https://buy.stripe.com/9B6dR9ath4cR30W68S0VO01';
const PRO_LINK = 'https://buy.stripe.com/dRm14n44TgZD7hc2WG0VO02';

export function Paywall({ isOpen, onClose }: PaywallProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      {/* Modal content with two pricing cards */}
      <a href={STARTER_LINK} target="_blank" rel="noopener noreferrer">
        <Button>Get Starter</Button>
      </a>
      <a href={PRO_LINK} target="_blank" rel="noopener noreferrer">
        <Button>Go Pro</Button>
      </a>
    </div>
  );
}
```

## 402 Handler (Generate.tsx)

```tsx
// frontend/src/pages/Generate.tsx

const [showPaywall, setShowPaywall] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // ... validation ...

  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(formData),
  });

  if (response.status === 402) {
    setShowPaywall(true);  // ← Show paywall
    toast({
      message: 'You have reached your generation limit. Upgrade to continue.',
      type: 'error',
    });
    return;
  }

  // ... handle success ...
};

return (
  <>
    <Paywall isOpen={showPaywall} onClose={() => setShowPaywall(false)} />
    {/* Rest of Generate page */}
  </>
);
```

## Routes (App.tsx)

```tsx
// frontend/src/App.tsx

import Success from "./pages/Success";
import Cancel from "./pages/Cancel";

<Routes>
  <Route path="/" element={<Landing />} />
  <Route path="/generate" element={<Generate />} />
  <Route path="/output" element={<Output />} />
  <Route path="/success" element={<Success />} />  {/* ← New */}
  <Route path="/cancel" element={<Cancel />} />    {/* ← New */}
</Routes>
```

## Success Page (Core Structure)

```tsx
// frontend/src/pages/Success.tsx

export default function Success() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <Card>
        <CardContent>
          <CheckCircle className="w-16 h-16 text-primary" />
          <h1>Payment Successful!</h1>
          <p>Your quota will be upgraded within 24 hours</p>
          <Button onClick={() => navigate('/generate')}>
            Return to ColdCopy
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Cancel Page (Core Structure)

```tsx
// frontend/src/pages/Cancel.tsx

export default function Cancel() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <Card>
        <CardContent>
          <XCircle className="w-16 h-16 text-muted-foreground" />
          <h1>Payment Cancelled</h1>
          <p>No worries! You can upgrade anytime.</p>
          <Button onClick={() => navigate('/generate')}>
            Back to ColdCopy
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Testing: Force Paywall (Local Dev)

```tsx
// Temporarily add this to Generate.tsx handleSubmit

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // TESTING: Force paywall to appear
  setShowPaywall(true);
  return;

  // Comment out the rest for testing
};
```

Or use browser DevTools to simulate 402:

```js
// In browser console
fetch('/api/generate', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ /* ... */ })
}).then(r => console.log(r.status))
```

Then manually set response status to 402 using Network tab → "Edit and Resend".

## Stripe Configuration (Post-Deploy)

After deploying to `https://coldcopy-app.pages.dev`:

**Update Payment Links in Stripe Dashboard:**

1. Starter Link: https://buy.stripe.com/9B6dR9ath4cR30W68S0VO01
2. Pro Link: https://buy.stripe.com/dRm14n44TgZD7hc2WG0VO02

**Set Success URL:**
```
https://coldcopy-app.pages.dev/success?session_id={CHECKOUT_SESSION_ID}
```

**Set Cancel URL:**
```
https://coldcopy-app.pages.dev/cancel
```

`{CHECKOUT_SESSION_ID}` is a Stripe variable that gets replaced with actual session ID.

## Build Command

```bash
cd projects/coldcopy/frontend
npm run build
```

Output: `dist/` directory ready to deploy.

## Deploy to Cloudflare Pages

```bash
# Option 1: Use Wrangler CLI
wrangler pages deploy dist --project-name=coldcopy-app

# Option 2: Push to GitHub, auto-deploy via Cloudflare Pages integration
git add .
git commit -m "feat: stripe payment integration"
git push
```

## Environment Variables (Optional)

If you want to make payment links configurable:

```bash
# frontend/.env
VITE_STRIPE_STARTER_LINK=https://buy.stripe.com/9B6dR9ath4cR30W68S0VO01
VITE_STRIPE_PRO_LINK=https://buy.stripe.com/dRm14n44TgZD7hc2WG0VO02
```

Then in code:

```tsx
const STARTER_LINK = import.meta.env.VITE_STRIPE_STARTER_LINK || 'https://buy.stripe.com/...';
```

But for MVP, hardcoded links are fine.

## Analytics Tracking (Optional)

If Google Analytics is set up:

```tsx
// In Success.tsx
useEffect(() => {
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('event', 'purchase', {
      transaction_id: sessionId,
      currency: 'USD',
    });
  }
}, [sessionId]);
```

No additional setup needed. Will silently fail if gtag not present.

## Responsive Breakpoints

Paywall uses Tailwind's `md:` breakpoint:

```tsx
<div className="grid md:grid-cols-2 gap-6">
  {/* 2 columns on desktop, 1 on mobile */}
</div>
```

Breakpoint is 768px.

## Color Scheme

All components use design tokens:

- `bg-background` — Page background
- `text-foreground` — Primary text
- `text-muted-foreground` — Secondary text
- `bg-primary` — Primary button
- `border-border` — Card borders

Defined in Tailwind config. No hardcoded colors.

## Icons

From `lucide-react`:

- `CheckCircle` — Success
- `XCircle` — Cancel
- `X` — Close button

All 16x16 or 24x24, resized with `className="w-16 h-16"`.

## Manual Fulfillment Process

After payment (until webhooks are set up):

1. Check Stripe Dashboard for new payment
2. Find customer email
3. Update backend quota (manual SQL or admin panel)
4. Send welcome email:

```
Subject: Welcome to ColdCopy Pro!

Hi [Name],

Your payment for ColdCopy [Starter/Pro] is confirmed.

Your account has been upgraded. You can now generate [50/unlimited] sequences.

Start here: https://coldcopy-app.pages.dev/generate

Questions? Reply to this email.

Thanks!
ColdCopy Team
```

See `docs/cfo/post-payment-flow.md` for full process.

---

**That's it.** All key code snippets in one place.
