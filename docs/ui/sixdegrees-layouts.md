# SixDegrees Layouts & Responsive Design

**Author:** UI Design Director (Matías Duarte)
**Date:** 2026-02-22
**Status:** Complete. Page-by-page layout specifications with responsive breakpoints.

---

## Layout Strategy

**Mobile-First Approach:**
1. Design for 320px width (iPhone SE) as minimum
2. Add breakpoints at 768px (tablet) and 1024px (desktop)
3. All layouts must work bilingual (EN and 中文)
4. Touch targets minimum 44x44px

**Page Hierarchy:**
1. Landing page (index.html) — Static, marketing
2. Intake form (intake.html) — Form, single page, simple
3. Dashboard (dashboard.html) — Complex, tabbed, real-time updates

---

## 1. Landing Page Layout

**File:** `projects/sixdegrees/index.html`

**Purpose:** Explain value proposition. One clear CTA: "Start Your First Connection"

**Structure:**

```
┌─────────────────────────────────────────────────────────┐
│  Header (Fixed or Sticky)                               │
│  ├─ Logo (SixDegrees)                     [EN] [中文]    │
│  └─ Simple nav (if needed) + CTA button                 │
├─────────────────────────────────────────────────────────┤
│  HERO Section                                            │
│  ├─ H1: "AI Agent That Reaches Anyone For You"          │
│  ├─ Subheading: "Get replies from hard-to-reach people" │
│  │           "in 3-7 days through warm intros"          │
│  └─ [Start Your First Connection] (Primary button)      │
├─────────────────────────────────────────────────────────┤
│  Proof Points Section (4 columns on desktop, 1 on mobile)│
│  ├─ 🔍 "Research" — AI analyzes target background       │
│  ├─ 🔗 "Find Path" — Shortest connection through network│
│  ├─ ✉️  "Send" — Personalized emails from YOU (not AI)  │
│  └─ 📊 "Track" — Real-time email status + replies       │
├─────────────────────────────────────────────────────────┤
│  How It Works Section                                    │
│  ├─ Step 1: Tell us who you want to reach               │
│  ├─ Step 2: AI finds the connection path                │
│  ├─ Step 3: Send personalized emails                    │
│  └─ Step 4: Get replies (we guarantee 48h or credits)   │
├─────────────────────────────────────────────────────────┤
│  Social Proof / Trust Section                            │
│  ├─ "Privacy First: We never sell your data"            │
│  ├─ "No Spam: One-time emails, not mass campaigns"      │
│  └─ "Warm Intros: Genuine connections, not cold outreach"│
├─────────────────────────────────────────────────────────┤
│  Pricing Preview Section                                 │
│  ├─ "Free: 1 campaign/month"                            │
│  ├─ "$29/month: 10 campaigns/month"                     │
│  └─ "$99/month: Unlimited + API"                        │
├─────────────────────────────────────────────────────────┤
│  CTA Section (Final push)                                │
│  ├─ H2: "Ready to reach your target?"                   │
│  └─ [Start Your First Connection] (Primary button)      │
├─────────────────────────────────────────────────────────┤
│  Footer                                                  │
│  ├─ Privacy Policy | Terms | Contact                    │
│  └─ Copyright info                                       │
└─────────────────────────────────────────────────────────┘
```

**CSS/HTML Structure:**

```html
<!-- Landing page, mobile-first -->
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body class="bg-neutral-white text-neutral-dark">

  <!-- Header -->
  <header class="sticky top-0 bg-white shadow-sm z-40 px-4 md:px-6 py-4">
    <div class="flex items-center justify-between max-w-6xl mx-auto">
      <h1 class="text-2xl font-bold text-primary">
        <span data-en="SixDegrees" data-zh="六度人脉">SixDegrees</span>
      </h1>
      <div class="flex items-center gap-4">
        <button id="lang-en" class="text-sm font-semibold text-primary">EN</button>
        <button id="lang-zh" class="text-sm font-semibold text-secondary-light">中文</button>
        <a href="/intake.html" class="px-4 py-2 rounded bg-primary text-white font-semibold text-sm hover:bg-primary-light">
          <span data-en="Start Now" data-zh="开始">Start Now</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="px-4 md:px-6 py-12 md:py-20 bg-primary-surface">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-4xl md:text-5xl font-bold text-neutral-dark mb-4">
        <span data-en="AI Agent That Reaches Anyone For You" data-zh="AI代理为你联系任何人">
          AI Agent That Reaches Anyone For You
        </span>
      </h2>
      <p class="text-lg md:text-xl text-neutral-base mb-8">
        <span data-en="Get replies from hard-to-reach people in 3–7 days through warm intros." data-zh="通过熟人介绍，在3-7天内获得难以接触的人的回复。">
          Get replies from hard-to-reach people in 3–7 days through warm intros.
        </span>
      </p>
      <a href="/intake.html" class="inline-block px-8 py-4 rounded bg-primary text-white font-bold text-lg hover:bg-primary-light transition-colors">
        <span data-en="Start Your First Connection" data-zh="开始你的第一次联系">
          Start Your First Connection
        </span>
      </a>
    </div>
  </section>

  <!-- Proof Points: 4 columns on desktop, 1 on mobile -->
  <section class="px-4 md:px-6 py-12 md:py-16">
    <div class="max-w-6xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8">
        <!-- Point 1 -->
        <div class="text-center">
          <div class="text-4xl mb-4">🔍</div>
          <h3 class="text-lg font-semibold text-neutral-dark mb-2">
            <span data-en="Research" data-zh="研究">Research</span>
          </h3>
          <p class="text-sm text-neutral-base">
            <span data-en="AI analyzes your target's background, interests, and connections." data-zh="AI分析目标人物的背景、兴趣和联系。">
              AI analyzes your target's background, interests, and connections.
            </span>
          </p>
        </div>
        <!-- Point 2 -->
        <div class="text-center">
          <div class="text-4xl mb-4">🔗</div>
          <h3 class="text-lg font-semibold text-neutral-dark mb-2">
            <span data-en="Find Path" data-zh="寻找路径">Find Path</span>
          </h3>
          <p class="text-sm text-neutral-base">
            <span data-en="We find the shortest connection through YOUR network." data-zh="我们通过您的网络找到最短的连接。">
              We find the shortest connection through YOUR network.
            </span>
          </p>
        </div>
        <!-- Point 3 -->
        <div class="text-center">
          <div class="text-4xl mb-4">✉️</div>
          <h3 class="text-lg font-semibold text-neutral-dark mb-2">
            <span data-en="Send" data-zh="发送">Send</span>
          </h3>
          <p class="text-sm text-neutral-base">
            <span data-en="Personalized emails from YOU (not a bot)." data-zh="来自您的个性化电子邮件（不是机器人）。">
              Personalized emails from YOU (not a bot).
            </span>
          </p>
        </div>
        <!-- Point 4 -->
        <div class="text-center">
          <div class="text-4xl mb-4">📊</div>
          <h3 class="text-lg font-semibold text-neutral-dark mb-2">
            <span data-en="Track" data-zh="追踪">Track</span>
          </h3>
          <p class="text-sm text-neutral-base">
            <span data-en="Real-time status, replies, and next steps." data-zh="实时状态、回复和后续步骤。">
              Real-time status, replies, and next steps.
            </span>
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Trust Section -->
  <section class="px-4 md:px-6 py-12 md:py-16 bg-secondary-surface">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-2xl md:text-3xl font-bold text-neutral-dark mb-8">
        <span data-en="Why SixDegrees?" data-zh="为什么选择SixDegrees?">Why SixDegrees?</span>
      </h2>
      <div class="space-y-4 text-neutral-base">
        <p class="text-base">
          <strong data-en="Privacy First" data-zh="隐私优先">Privacy First</strong> —
          <span data-en="We never sell your data or access without permission." data-zh="我们从不在未经许可的情况下出售或访问您的数据。">
            We never sell your data or access without permission.
          </span>
        </p>
        <p class="text-base">
          <strong data-en="No Spam" data-zh="无垃圾邮件">No Spam</strong> —
          <span data-en="Warm introductions only. One email chain per campaign." data-zh="仅限热情介绍。每个活动一个电子邮件链。">
            Warm introductions only. One email chain per campaign.
          </span>
        </p>
        <p class="text-base">
          <strong data-en="Guaranteed Results" data-zh="保证结果">Guaranteed Results</strong> —
          <span data-en="Get a reply in 48 hours or your credits back." data-zh="在48小时内获得回复，否则退回您的积分。">
            Get a reply in 48 hours or your credits back.
          </span>
        </p>
      </div>
    </div>
  </section>

  <!-- Pricing Section -->
  <section class="px-4 md:px-6 py-12 md:py-16">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-2xl md:text-3xl font-bold text-neutral-dark text-center mb-12">
        <span data-en="Transparent Pricing" data-zh="透明定价">Transparent Pricing</span>
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Free Plan -->
        <div class="rounded bg-white shadow-md border border-neutral-light p-6 text-center">
          <h3 class="text-xl font-bold text-neutral-dark mb-4">
            <span data-en="Free" data-zh="免费">Free</span>
          </h3>
          <p class="text-3xl font-bold text-primary mb-4">$0</p>
          <p class="text-sm text-neutral-base mb-6">
            <span data-en="1 campaign/month" data-zh="每月1个活动">1 campaign/month</span>
          </p>
          <button class="w-full px-4 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold hover:bg-secondary-surface">
            <span data-en="Current Plan" data-zh="当前计划">Current Plan</span>
          </button>
        </div>

        <!-- Starter Plan -->
        <div class="rounded bg-white shadow-md border border-primary p-6 text-center ring-2 ring-primary ring-offset-2">
          <h3 class="text-xl font-bold text-neutral-dark mb-4">
            <span data-en="Starter" data-zh="入门">Starter</span>
          </h3>
          <p class="text-3xl font-bold text-primary mb-4">$29<span class="text-lg text-neutral-base">/mo</span></p>
          <p class="text-sm text-neutral-base mb-6">
            <span data-en="10 campaigns/month" data-zh="每月10个活动">10 campaigns/month</span>
          </p>
          <a href="#upgrade" class="w-full block px-4 py-2 rounded bg-primary text-white font-semibold hover:bg-primary-light">
            <span data-en="Upgrade" data-zh="升级">Upgrade</span>
          </a>
        </div>

        <!-- Pro Plan -->
        <div class="rounded bg-white shadow-md border border-neutral-light p-6 text-center">
          <h3 class="text-xl font-bold text-neutral-dark mb-4">
            <span data-en="Pro" data-zh="专业">Pro</span>
          </h3>
          <p class="text-3xl font-bold text-primary mb-4">$99<span class="text-lg text-neutral-base">/mo</span></p>
          <p class="text-sm text-neutral-base mb-6">
            <span data-en="Unlimited + API Access" data-zh="无限+API访问">Unlimited + API Access</span>
          </p>
          <a href="#upgrade" class="w-full block px-4 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold hover:bg-secondary-surface">
            <span data-en="Upgrade" data-zh="升级">Upgrade</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Final CTA -->
  <section class="px-4 md:px-6 py-12 md:py-16 bg-primary-surface">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-3xl md:text-4xl font-bold text-neutral-dark mb-4">
        <span data-en="Ready to reach your target?" data-zh="准备好联系您的目标了吗？">
          Ready to reach your target?
        </span>
      </h2>
      <p class="text-lg text-neutral-base mb-8">
        <span data-en="Your first campaign is free. No credit card required." data-zh="您的第一个活动是免费的。无需信用卡。">
          Your first campaign is free. No credit card required.
        </span>
      </p>
      <a href="/intake.html" class="inline-block px-8 py-4 rounded bg-primary text-white font-bold text-lg hover:bg-primary-light transition-colors">
        <span data-en="Get Started Now" data-zh="立即开始">Get Started Now</span>
      </a>
    </div>
  </section>

  <!-- Footer -->
  <footer class="px-4 md:px-6 py-8 bg-neutral-surface border-t border-neutral-light">
    <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <p class="text-sm text-secondary-light">
        &copy; 2026 SixDegrees. All rights reserved.
      </p>
      <div class="flex gap-6 text-sm text-secondary-light">
        <a href="#privacy" class="hover:text-neutral-dark">Privacy</a>
        <a href="#terms" class="hover:text-neutral-dark">Terms</a>
        <a href="#contact" class="hover:text-neutral-dark">Contact</a>
      </div>
    </div>
  </footer>

  <script>
    // Language toggle
    document.getElementById('lang-en').addEventListener('click', () => {
      document.querySelectorAll('[data-en]').forEach(el => {
        el.textContent = el.getAttribute('data-en');
      });
      document.getElementById('lang-en').classList.add('text-primary');
      document.getElementById('lang-en').classList.remove('text-secondary-light');
      document.getElementById('lang-zh').classList.remove('text-primary');
      document.getElementById('lang-zh').classList.add('text-secondary-light');
      localStorage.setItem('language', 'en');
    });

    document.getElementById('lang-zh').addEventListener('click', () => {
      document.querySelectorAll('[data-zh]').forEach(el => {
        el.textContent = el.getAttribute('data-zh');
      });
      document.getElementById('lang-zh').classList.add('text-primary');
      document.getElementById('lang-zh').classList.remove('text-secondary-light');
      document.getElementById('lang-en').classList.remove('text-primary');
      document.getElementById('lang-en').classList.add('text-secondary-light');
      localStorage.setItem('language', 'zh');
    });

    // Load saved language
    const savedLang = localStorage.getItem('language') || 'en';
    document.getElementById(`lang-${savedLang}`).click();
  </script>

</body>
</html>
```

---

## 2. Intake Form Layout

**File:** `projects/sixdegrees/intake.html`

**Purpose:** Collect target info + user context in 90 seconds. Mobile-first single column.

**Mobile (320px):**
```
┌─────────────────────────────────┐
│ Header + Language Toggle        │
├─────────────────────────────────┤
│ H1: "Tell us who you want..."  │
│                                 │
│ Form:                           │
│ ┌─────────────────────────────┐ │
│ │ Your Email                  │ │
│ │ [input field]               │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Your Name                   │ │
│ │ [input field]               │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Target Name                 │ │
│ │ [input field]               │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Why do you want to reach... │ │
│ │ [textarea, 500 char]        │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Tell us about yourself      │ │
│ │ [textarea, 500 char]        │ │
│ └─────────────────────────────┘ │
│                                 │
│ [Primary Button: Disabled]      │
│                                 │
│ Progress: 0/5 fields filled     │
└─────────────────────────────────┘
```

**HTML Structure:**

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* Include color palette + typography from design-system.md */
  </style>
</head>
<body class="bg-neutral-white text-neutral-dark">

  <!-- Header -->
  <header class="px-4 md:px-6 py-4 border-b border-neutral-light">
    <div class="max-w-2xl mx-auto flex items-center justify-between">
      <h1 class="text-2xl font-bold text-primary">
        <span data-en="SixDegrees" data-zh="六度人脉">SixDegrees</span>
      </h1>
      <div class="flex gap-2">
        <button id="lang-en" class="px-3 py-1 rounded text-xs font-semibold text-primary">EN</button>
        <button id="lang-zh" class="px-3 py-1 rounded text-xs font-semibold text-secondary-light">中文</button>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="px-4 md:px-6 py-8 md:py-12">
    <div class="max-w-2xl mx-auto">
      <!-- Title -->
      <h2 class="text-3xl md:text-4xl font-bold text-neutral-dark mb-2">
        <span data-en="Who do you want to reach?" data-zh="你想联系谁？">
          Who do you want to reach?
        </span>
      </h2>
      <p class="text-lg text-neutral-base mb-8">
        <span data-en="Tell us about your target and we'll find the best path." data-zh="告诉我们您的目标，我们会找到最佳路径。">
          Tell us about your target and we'll find the best path.
        </span>
      </p>

      <!-- Form -->
      <form id="intake-form" class="space-y-6">
        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-semibold text-neutral-dark mb-2">
            <span data-en="Your Email" data-zh="你的邮箱">Your Email</span>
          </label>
          <input id="email" type="email" required
                 class="w-full px-4 py-2 rounded border border-neutral-light bg-white text-neutral-dark
                        placeholder-secondary-light focus:outline-none focus:ring-2 focus:ring-primary
                        focus:border-primary transition-colors duration-200"
                 placeholder="sarah@company.com" />
        </div>

        <!-- Name -->
        <div>
          <label for="name" class="block text-sm font-semibold text-neutral-dark mb-2">
            <span data-en="Your Name" data-zh="你的名字">Your Name</span>
          </label>
          <input id="name" type="text" required
                 class="w-full px-4 py-2 rounded border border-neutral-light bg-white text-neutral-dark
                        placeholder-secondary-light focus:outline-none focus:ring-2 focus:ring-primary
                        focus:border-primary transition-colors duration-200"
                 placeholder="Sarah Chen"
                 maxlength="50" />
          <p class="text-xs text-secondary-light mt-1">
            <span data-en="Max 50 characters" data-zh="最多50个字符">Max 50 characters</span>
          </p>
        </div>

        <!-- Target Name -->
        <div>
          <label for="target-name" class="block text-sm font-semibold text-neutral-dark mb-2">
            <span data-en="Target Person (Name)" data-zh="目标人物（名字）">Target Person (Name)</span>
          </label>
          <input id="target-name" type="text" required
                 class="w-full px-4 py-2 rounded border border-neutral-light bg-white text-neutral-dark
                        placeholder-secondary-light focus:outline-none focus:ring-2 focus:ring-primary
                        focus:border-primary transition-colors duration-200"
                 placeholder="Elon Musk" />
        </div>

        <!-- Target Title/Company -->
        <div>
          <label for="target-company" class="block text-sm font-semibold text-neutral-dark mb-2">
            <span data-en="Title & Company" data-zh="职位和公司">Title & Company</span>
          </label>
          <input id="target-company" type="text" required
                 class="w-full px-4 py-2 rounded border border-neutral-light bg-white text-neutral-dark
                        placeholder-secondary-light focus:outline-none focus:ring-2 focus:ring-primary
                        focus:border-primary transition-colors duration-200"
                 placeholder="CEO, Tesla" />
        </div>

        <!-- Why -->
        <div>
          <label for="target-reason" class="block text-sm font-semibold text-neutral-dark mb-2">
            <span data-en="Why do you want to reach them?" data-zh="你为什么想联系他们？">
              Why do you want to reach them?
            </span>
          </label>
          <textarea id="target-reason" required
                    class="w-full px-4 py-3 rounded border border-neutral-light bg-white text-neutral-dark
                           placeholder-secondary-light focus:outline-none focus:ring-2 focus:ring-primary
                           focus:border-primary transition-colors duration-200 resize-none min-h-[100px]"
                    placeholder="I want to discuss energy storage solutions for electric vehicles..."
                    maxlength="500"></textarea>
          <p class="text-xs text-secondary-light mt-1">
            <span id="reason-count" data-en="0/500 characters" data-zh="0/500个字符">0/500 characters</span>
          </p>
        </div>

        <!-- Background -->
        <div>
          <label for="user-background" class="block text-sm font-semibold text-neutral-dark mb-2">
            <span data-en="Tell us about yourself" data-zh="告诉我们你自己">Tell us about yourself</span>
          </label>
          <textarea id="user-background" required
                    class="w-full px-4 py-3 rounded border border-neutral-light bg-white text-neutral-dark
                           placeholder-secondary-light focus:outline-none focus:ring-2 focus:ring-primary
                           focus:border-primary transition-colors duration-200 resize-none min-h-[100px]"
                    placeholder="I'm founder of X startup. We're solving energy storage..."
                    maxlength="500"></textarea>
          <p class="text-xs text-secondary-light mt-1">
            <span id="bg-count" data-en="0/500 characters" data-zh="0/500个字符">0/500 characters</span>
          </p>
        </div>

        <!-- Submit Button -->
        <button type="submit" id="submit-btn" disabled
                class="w-full px-6 py-3 rounded bg-primary text-white font-semibold text-base
                       hover:bg-primary-light active:bg-primary-dark transition-colors duration-200
                       disabled:opacity-50 disabled:cursor-not-allowed">
          <span data-en="Let AI Research & Plan" data-zh="让AI研究和规划">Let AI Research & Plan</span>
        </button>

        <!-- Progress -->
        <p id="progress" class="text-center text-xs text-secondary-light">
          <span data-en="0/5 fields filled" data-zh="0/5个字段已填写">0/5 fields filled</span>
        </p>
      </form>
    </div>
  </main>

  <script>
    const form = document.getElementById('intake-form');
    const submitBtn = document.getElementById('submit-btn');
    const progressEl = document.getElementById('progress');

    // Track form completion
    function updateFormState() {
      const fields = ['email', 'name', 'target-name', 'target-company', 'target-reason', 'user-background'];
      const filled = fields.filter(id => document.getElementById(id).value.trim()).length;
      const total = fields.length;

      submitBtn.disabled = filled < total;
      progressEl.textContent = `${filled}/${total} fields filled`;

      // Update character counts
      document.getElementById('reason-count').textContent =
        `${document.getElementById('target-reason').value.length}/500 characters`;
      document.getElementById('bg-count').textContent =
        `${document.getElementById('user-background').value.length}/500 characters`;
    }

    // Add input listeners
    ['email', 'name', 'target-name', 'target-company', 'target-reason', 'user-background'].forEach(id => {
      document.getElementById(id).addEventListener('input', updateFormState);
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const data = {
        user_email: document.getElementById('email').value,
        user_name: document.getElementById('name').value,
        target_name: document.getElementById('target-name').value,
        target_company: document.getElementById('target-company').value,
        target_reason: document.getElementById('target-reason').value,
        user_background: document.getElementById('user-background').value,
      };

      // Show loading state
      submitBtn.disabled = true;
      submitBtn.textContent = 'Analyzing your request...';

      // POST to API (backend handles OAuth redirect)
      try {
        const response = await fetch('/api/intake', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });

        const result = await response.json();
        if (result.oauth_redirect_url) {
          window.location.href = result.oauth_redirect_url;
        } else {
          alert('Error. Please try again.');
          submitBtn.disabled = false;
          submitBtn.textContent = 'Let AI Research & Plan';
        }
      } catch (err) {
        alert('Network error. Please try again.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Let AI Research & Plan';
      }
    });

    // Language toggle
    document.getElementById('lang-en').addEventListener('click', () => {
      document.querySelectorAll('[data-en]').forEach(el => {
        el.textContent = el.getAttribute('data-en');
      });
      localStorage.setItem('language', 'en');
    });

    document.getElementById('lang-zh').addEventListener('click', () => {
      document.querySelectorAll('[data-zh]').forEach(el => {
        el.textContent = el.getAttribute('data-zh');
      });
      localStorage.setItem('language', 'zh');
    });

    // Load saved language
    const savedLang = localStorage.getItem('language') || 'en';
    document.getElementById(`lang-${savedLang}`).click();
  </script>

</body>
</html>
```

---

## 3. Dashboard Layout

**File:** `projects/sixdegrees/dashboard.html`

**Purpose:** Show campaign strategy, live status, emails, and manage payments.

**Structure (Desktop, 1024px+):**

```
┌──────────────────────────────────────────────────────────────────────┐
│ Header                                                                │
│ SixDegrees | Campaign: Elon Musk | [Settings] [Logout]              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│ Tab Navigation (Sticky)                                              │
│ [Your Campaign] [Connections] [Credits & Payment] [Settings]        │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  TAB 1: YOUR CAMPAIGN                                                │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Status: In Progress [████░░░░░░] (32% complete)              │ │
│  │ [View Full Plan] [Start Campaign] [Edit Target]              │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ AI Strategy Card:                                             │ │
│  │ "We found 3 paths to reach Elon..."                           │ │
│  │                                                                │ │
│  │ 6-Degree Chain (SVG Visualization):                           │ │
│  │ [You] → [Friend] → [Tesla Emp] → [Elon]                     │ │
│  │   ✓       ✓          ✓           ⏳                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ What's Happening Now (auto-refresh every 30s)                │ │
│  │ ├─ ✓ Email #1 sent to Friend (2 hours ago)                  │ │
│  │ ├─ ✓ Friend replied (1 hour ago)                             │ │
│  │ ├─ ✓ Email #2 sent to Tesla Emp (45 min ago)               │ │
│  │ └─ ⏳ Waiting for reply (48h timeout, 32h remaining)         │ │
│  │                                                                │ │
│  │ [Refresh]                                                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  Email Carousel (horizontal scroll):                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  Email #1    │  │  Email #2    │  │  Email #3    │               │
│  │              │  │              │  │              │               │
│  │ To: Friend   │  │ To: Tesla    │  │ To: Elon     │               │
│  │ ✓ Sent       │  │ ✓ Sent       │  │ ✎ Draft      │               │
│  │ ↩️ Replied   │  │ ⏳ Waiting   │  │              │               │
│  │              │  │              │  │              │               │
│  │ [View Full]  │  │ [View Full]  │  │ [View Draft] │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Mobile (320px):**

```
┌─────────────────────────────┐
│ Header                      │
│ SixDegrees [Settings]       │
├─────────────────────────────┤
│ Campaign: Elon Musk         │
│ Status: In Progress [████░░]│
│ [View Plan] [Start]         │
│                             │
│ 6-Degree Chain (Vertical):  │
│ [You]                       │
│   ↓ ✓                       │
│ [Friend]                    │
│   ↓ ✓                       │
│ [Tesla Emp]                 │
│   ↓ ✓                       │
│ [Elon]                      │
│   ↓ ⏳                       │
│                             │
│ What's Happening Now:       │
│ ✓ Email #1 sent (2h ago)   │
│ ✓ Friend replied (1h ago)  │
│ ✓ Email #2 sent (45m ago)  │
│ ⏳ Waiting for reply...     │
│                             │
│ Tab Navigation (scrollable):│
│ [Your Campaign] [Conn...] ... │
│                             │
│ Email Carousel (1 visible): │
│ ┌─────────────┐             │
│ │ Email #1    │ → → →       │
│ │ To: Friend  │             │
│ │ ✓ Sent      │             │
│ │ ↩️ Replied  │             │
│ │ [View]      │             │
│ └─────────────┘             │
│                             │
└─────────────────────────────┘
```

**HTML Structure (Dashboard, Tab 1: Your Campaign):**

```html
<!DOCTYPE html>
<html>
<body>

  <!-- Header -->
  <header class="sticky top-0 bg-white shadow-sm px-4 md:px-6 py-4 z-40">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <h1 class="text-2xl font-bold text-primary">
        <span data-en="SixDegrees" data-zh="六度人脉">SixDegrees</span>
      </h1>
      <div class="flex items-center gap-4">
        <span class="text-sm text-neutral-base">
          <span id="campaign-name" data-en="Campaign: Elon Musk" data-zh="活动：埃隆·马斯克">
            Campaign: Elon Musk
          </span>
        </span>
        <a href="/settings.html" class="text-secondary-light hover:text-neutral-dark">
          ⚙️ <span data-en="Settings" data-zh="设置">Settings</span>
        </a>
        <button class="text-secondary-light hover:text-neutral-dark" onclick="logout()">
          <span data-en="Logout" data-zh="登出">Logout</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Tab Navigation -->
  <nav class="sticky top-[60px] bg-white border-b border-neutral-light px-4 md:px-6 z-30">
    <div class="max-w-7xl mx-auto flex gap-0 overflow-x-auto">
      <button class="tab-btn active pb-4 px-4 md:px-6 border-b-2 border-primary text-primary font-semibold text-sm md:text-base whitespace-nowrap"
              data-tab="campaign"
              data-en="Your Campaign" data-zh="你的活动计划">
        Your Campaign
      </button>
      <button class="tab-btn pb-4 px-4 md:px-6 border-b-2 border-transparent text-secondary-light hover:text-neutral-base font-semibold text-sm md:text-base whitespace-nowrap"
              data-tab="connections"
              data-en="Connections" data-zh="连接">
        Connections
      </button>
      <button class="tab-btn pb-4 px-4 md:px-6 border-b-2 border-transparent text-secondary-light hover:text-neutral-base font-semibold text-sm md:text-base whitespace-nowrap"
              data-tab="credits"
              data-en="Credits & Payment" data-zh="积分和付款">
        Credits & Payment
      </button>
      <button class="tab-btn pb-4 px-4 md:px-6 border-b-2 border-transparent text-secondary-light hover:text-neutral-base font-semibold text-sm md:text-base whitespace-nowrap"
              data-tab="settings"
              data-en="Settings" data-zh="设置">
        Settings
      </button>
    </div>
  </nav>

  <!-- Main Content -->
  <main class="px-4 md:px-6 py-8 md:py-12">
    <div class="max-w-7xl mx-auto">

      <!-- TAB 1: Your Campaign -->
      <div id="tab-campaign" class="tab-content space-y-8">

        <!-- Status Card -->
        <div class="rounded bg-white shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-neutral-dark"
                data-en="AI Strategy to Reach Elon Musk" data-zh="到达埃隆·马斯克的AI策略">
              AI Strategy to Reach Elon Musk
            </h2>
            <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-warning-surface text-warning font-semibold text-sm">
              ⏳ <span data-en="In Progress" data-zh="进行中">In Progress</span>
            </span>
          </div>

          <!-- Progress Bar -->
          <div class="mb-6">
            <div class="w-full bg-neutral-light rounded-full h-2">
              <div class="bg-primary h-2 rounded-full" style="width: 32%"></div>
            </div>
            <p class="text-xs text-secondary-light mt-2">
              <span data-en="Email 2 of 3 sent. Waiting for reply." data-zh="已发送3封电子邮件中的2封。等待回复。">
                Email 2 of 3 sent. Waiting for reply.
              </span>
            </p>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col md:flex-row gap-3">
            <button class="px-6 py-2 rounded bg-primary text-white font-semibold hover:bg-primary-light"
                    data-en="View Full Plan" data-zh="查看完整计划">
              View Full Plan
            </button>
            <button class="px-6 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold hover:bg-secondary-surface"
                    data-en="Edit Target" data-zh="编辑目标">
              Edit Target
            </button>
          </div>
        </div>

        <!-- 6-Degree Chain (SVG) -->
        <div class="rounded bg-white shadow-md p-6">
          <h3 class="text-xl font-bold text-neutral-dark mb-6"
              data-en="Connection Path to Elon" data-zh="到达埃隆的连接路径">
            Connection Path to Elon
          </h3>

          <!-- SVG visualization (see sixdegrees-components.md for full SVG) -->
          <svg class="w-full h-auto" viewBox="0 0 1000 100" preserveAspectRatio="xMidYMid meet">
            <!-- Node 1: You (Sender) -->
            <g transform="translate(100, 50)">
              <circle cx="0" cy="0" r="20" fill="#2563eb" stroke="white" stroke-width="2"/>
              <text x="0" y="0" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="12" font-weight="bold">You</text>
            </g>
            <text x="100" y="70" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">✓ Sent</text>

            <!-- Connection 1 -->
            <line x1="120" y1="50" x2="260" y2="50" stroke="#d1d5db" stroke-width="2"/>

            <!-- Node 2: Friend -->
            <g transform="translate(300, 50)">
              <circle cx="0" cy="0" r="20" fill="#2563eb" stroke="white" stroke-width="2"/>
              <text x="0" y="0" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="10">Friend</text>
            </g>
            <text x="300" y="70" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">✓ Replied</text>

            <!-- Connection 2 -->
            <line x1="320" y1="50" x2="460" y2="50" stroke="#d1d5db" stroke-width="2"/>

            <!-- Node 3: Tesla Emp -->
            <g transform="translate(500, 50)">
              <circle cx="0" cy="0" r="20" fill="#2563eb" stroke="white" stroke-width="2"/>
              <text x="0" y="0" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="10">Tesla</text>
            </g>
            <text x="500" y="70" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">✓ Sent</text>

            <!-- Connection 3 -->
            <line x1="520" y1="50" x2="660" y2="50" stroke="#d1d5db" stroke-width="2"/>

            <!-- Node 4: Target (Elon) -->
            <g transform="translate(700, 50)">
              <circle cx="0" cy="0" r="20" fill="#ca8a04" stroke="white" stroke-width="2"/>
              <text x="0" y="0" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="10">Elon</text>
            </g>
            <text x="700" y="70" text-anchor="middle" fill="#ca8a04" font-size="11" font-weight="bold">⏳ Waiting</text>
          </svg>

          <p class="text-sm text-neutral-base mt-4">
            <strong data-en="Path selected:" data-zh="选定路径：">Path selected:</strong>
            <span data-en="You → Friend → Tesla Employee → Elon (3 degrees, 85% confidence)"
                  data-zh="您 → 朋友 → 特斯拉员工 → 埃隆（3度，85%置信度）">
              You → Friend → Tesla Employee → Elon (3 degrees, 85% confidence)
            </span>
          </p>
        </div>

        <!-- What's Happening Now (Live Status) -->
        <div class="rounded bg-white shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-neutral-dark"
                data-en="What's Happening Now" data-zh="现在发生了什么">
              What's Happening Now
            </h3>
            <button class="text-sm text-primary hover:text-primary-dark font-semibold"
                    data-en="Refresh" data-zh="刷新">
              Refresh
            </button>
          </div>

          <!-- Timeline -->
          <div class="space-y-3">
            <!-- Event 1 -->
            <div class="flex gap-4">
              <span class="text-2xl">✓</span>
              <div>
                <p class="text-base text-neutral-dark font-semibold">
                  <span data-en="Email #1 sent to Friend" data-zh="电子邮件#1已发送给朋友">
                    Email #1 sent to Friend
                  </span>
                </p>
                <p class="text-sm text-secondary-light">Today 3:15 PM</p>
              </div>
            </div>

            <!-- Event 2 -->
            <div class="flex gap-4">
              <span class="text-2xl">↩️</span>
              <div>
                <p class="text-base text-neutral-dark font-semibold">
                  <span data-en="Friend replied" data-zh="朋友回复了">
                    Friend replied
                  </span>
                </p>
                <p class="text-sm text-secondary-light">Today 2:40 PM</p>
              </div>
            </div>

            <!-- Event 3 -->
            <div class="flex gap-4">
              <span class="text-2xl">✓</span>
              <div>
                <p class="text-base text-neutral-dark font-semibold">
                  <span data-en="Email #2 sent to Tesla Employee" data-zh="电子邮件#2已发送给特斯拉员工">
                    Email #2 sent to Tesla Employee
                  </span>
                </p>
                <p class="text-sm text-secondary-light">Today 2:45 PM</p>
              </div>
            </div>

            <!-- Current Status -->
            <div class="flex gap-4 pt-4 border-t border-neutral-light">
              <span class="text-2xl">⏳</span>
              <div>
                <p class="text-base text-neutral-dark font-semibold">
                  <span data-en="Waiting for Tesla Employee's reply" data-zh="等待特斯拉员工的回复">
                    Waiting for Tesla Employee's reply
                  </span>
                </p>
                <div class="mt-2">
                  <div class="w-full bg-neutral-light rounded-full h-1">
                    <div class="bg-warning h-1 rounded-full" style="width: 67%"></div>
                  </div>
                  <p class="text-xs text-secondary-light mt-1">
                    <span data-en="32 hours / 48 hours remaining" data-zh="剩余32/48小时">
                      32 hours / 48 hours remaining
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Email Carousel -->
        <div class="rounded bg-white shadow-md p-6">
          <h3 class="text-xl font-bold text-neutral-dark mb-6"
              data-en="Email Sequence" data-zh="电子邮件序列">
            Email Sequence
          </h3>

          <!-- Carousel container (horizontal scroll on mobile, grid on desktop) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- Email Card 1 -->
            <div class="rounded border border-neutral-light p-4 bg-secondary-surface">
              <div class="flex items-center justify-between mb-3">
                <h4 class="text-base font-semibold text-neutral-dark">
                  <span data-en="Email #1" data-zh="电子邮件#1">Email #1</span>
                </h4>
                <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-success-surface text-success font-semibold text-xs">
                  ✓ <span data-en="Sent" data-zh="已发送">Sent</span>
                </span>
              </div>

              <p class="text-xs font-semibold text-secondary-light mb-2">
                <span data-en="To:" data-zh="至：">To:</span> Jake Williams
              </p>

              <p class="text-sm text-neutral-base font-semibold mb-3">
                <span data-en="Subject:" data-zh="主题：">Subject:</span> Quick intro to Sarah...
              </p>

              <p class="text-sm text-neutral-base mb-4">
                <span data-en="Sent 3 hours ago" data-zh="3小时前发送">Sent 3 hours ago</span>
              </p>

              <div class="flex gap-2">
                <button class="flex-1 px-3 py-2 rounded bg-primary text-white font-semibold text-sm hover:bg-primary-light"
                        data-en="View Full" data-zh="查看完整">
                  View Full
                </button>
                <button class="flex-1 px-3 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold text-sm hover:bg-white"
                        data-en="View Reply" data-zh="查看回复">
                  View Reply
                </button>
              </div>
            </div>

            <!-- Email Card 2 (Similar structure) -->
            <div class="rounded border border-neutral-light p-4 bg-secondary-surface">
              <div class="flex items-center justify-between mb-3">
                <h4 class="text-base font-semibold text-neutral-dark">
                  <span data-en="Email #2" data-zh="电子邮件#2">Email #2</span>
                </h4>
                <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-success-surface text-success font-semibold text-xs">
                  ✓ <span data-en="Sent" data-zh="已发送">Sent</span>
                </span>
              </div>

              <p class="text-xs font-semibold text-secondary-light mb-2">
                <span data-en="To:" data-zh="至：">To:</span> Tesla Engineer
              </p>

              <p class="text-sm text-neutral-base font-semibold mb-3">
                <span data-en="Subject:" data-zh="主题：">Subject:</span> Intro from Jake...
              </p>

              <p class="text-sm text-neutral-base mb-4">
                <span data-en="Sent 45 minutes ago" data-zh="45分钟前发送">Sent 45 minutes ago</span>
              </p>

              <div class="flex gap-2">
                <button class="flex-1 px-3 py-2 rounded bg-primary text-white font-semibold text-sm hover:bg-primary-light"
                        data-en="View Full" data-zh="查看完整">
                  View Full
                </button>
                <button class="flex-1 px-3 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold text-sm hover:bg-white disabled:opacity-50"
                        disabled>
                  <span data-en="No reply yet" data-zh="还没有回复">No reply yet</span>
                </button>
              </div>
            </div>

            <!-- Email Card 3 (Draft) -->
            <div class="rounded border border-neutral-light p-4 bg-secondary-surface">
              <div class="flex items-center justify-between mb-3">
                <h4 class="text-base font-semibold text-neutral-dark">
                  <span data-en="Email #3" data-zh="电子邮件#3">Email #3</span>
                </h4>
                <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-warning-surface text-warning font-semibold text-xs">
                  ✎ <span data-en="Draft" data-zh="草稿">Draft</span>
                </span>
              </div>

              <p class="text-xs font-semibold text-secondary-light mb-2">
                <span data-en="To:" data-zh="至：">To:</span> Elon Musk
              </p>

              <p class="text-sm text-neutral-base font-semibold mb-3">
                <span data-en="Subject:" data-zh="主题：">Subject:</span> [Waiting for Email #2 reply]
              </p>

              <p class="text-xs text-secondary-light mb-4">
                <span data-en="Will send after Email #2 gets reply" data-zh="电子邮件#2回复后将发送">
                  Will send after Email #2 gets reply
                </span>
              </p>

              <button class="w-full px-3 py-2 rounded bg-neutral-surface border border-neutral-light text-neutral-dark font-semibold text-sm hover:bg-white"
                      data-en="View Strategy" data-zh="查看策略">
                View Strategy
              </button>
            </div>

          </div>
        </div>

      </div>

      <!-- TAB 2: Connections (Summary for space) -->
      <div id="tab-connections" class="tab-content hidden">
        <p class="text-neutral-base">
          <span data-en="Email history and connection logs go here." data-zh="电子邮件历史记录和连接日志在这里。">
            Email history and connection logs go here.
          </span>
        </p>
      </div>

      <!-- TAB 3: Credits & Payment (Summary for space) -->
      <div id="tab-credits" class="tab-content hidden">
        <p class="text-neutral-base">
          <span data-en="Pricing and payment options go here." data-zh="定价和付款选项在这里。">
            Pricing and payment options go here.
          </span>
        </p>
      </div>

      <!-- TAB 4: Settings (Summary for space) -->
      <div id="tab-settings" class="tab-content hidden">
        <p class="text-neutral-base">
          <span data-en="Account settings and preferences go here." data-zh="帐户设置和首选项在这里。">
            Account settings and preferences go here.
          </span>
        </p>
      </div>

    </div>
  </main>

  <script>
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tabName = e.currentTarget.getAttribute('data-tab');

        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));

        // Show selected tab
        document.getElementById(`tab-${tabName}`).classList.remove('hidden');

        // Update active button
        document.querySelectorAll('.tab-btn').forEach(b => {
          b.classList.remove('border-primary', 'text-primary', 'font-semibold');
          b.classList.add('border-transparent', 'text-secondary-light');
        });
        e.currentTarget.classList.remove('border-transparent', 'text-secondary-light');
        e.currentTarget.classList.add('border-primary', 'text-primary', 'font-semibold');
      });
    });

    // Language toggle (same as before)
    document.getElementById('lang-en')?.addEventListener('click', () => {
      document.querySelectorAll('[data-en]').forEach(el => {
        el.textContent = el.getAttribute('data-en');
      });
      localStorage.setItem('language', 'en');
    });

    document.getElementById('lang-zh')?.addEventListener('click', () => {
      document.querySelectorAll('[data-zh]').forEach(el => {
        el.textContent = el.getAttribute('data-zh');
      });
      localStorage.setItem('language', 'zh');
    });

    // Load saved language
    const savedLang = localStorage.getItem('language') || 'en';
    // document.getElementById(`lang-${savedLang}`).click();

    function logout() {
      localStorage.clear();
      window.location.href = '/';
    }
  </script>

</body>
</html>
```

---

## Responsive Behavior Rules

| Element | 320px (Mobile) | 768px (Tablet) | 1024px (Desktop) |
|---------|----------------|----------------|------------------|
| Header padding | `px-4` | `px-6` | `px-6` |
| Main content max-width | Full width | `max-w-4xl` | `max-w-7xl` |
| Grid columns | 1 | 2 | 3+ |
| Font sizes | Reduced 10-15% | Standard | Standard |
| Tab bar | Full-width scroll | Horizontal, fixed | Horizontal, fixed |
| Email carousel | 1 visible, swipe | 1.5 visible | 3 visible |
| 6-degree chain | Vertical stack | Horizontal (scaled) | Horizontal (full size) |

---

## Summary

All page layouts are mobile-first, responsive, and bilingual-ready. Each layout uses Tailwind v4 classes and the color palette from the design system.

**Key files:**
- `docs/ui/sixdegrees-design-system.md` — Color, typography, components
- `docs/ui/sixdegrees-layouts.md` (this file) — Page structures
- `docs/ui/sixdegrees-components.md` — 6-degree chain SVG, email carousel details

---

**Layout Document Version:** 1.0
**Status:** Ready for HTML implementation
