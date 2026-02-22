# Double Mood Phase 2 — User Flow Design

**Designer:** Alan Cooper (interaction-cooper)
**Date:** 2026-02-21
**Status:** Shipped — Ready for implementation

---

## Primary Persona

**Name:** Emma (艾玛)
**Age:** 28, Product Manager
**Context:** Experiences multiple emotional states throughout the day — not just "anxiety," but a spectrum from burnout to rage to numbness to relief. She knows *something* is wrong but struggles to name it.

**Goals:**
1. **Name the emotion** — "I feel... what? Burnt out? Anxious? Both?"
2. **Track intensity** — "Is this 3/10 mild unease or 8/10 chest-tightness panic?"
3. **Understand triggers** — "Why do I feel this way? What happened?"
4. **Regulate quickly** — "I need relief now, not in 30 minutes"
5. **See patterns over time** — "Do I always feel this way on Mondays?"

**Current Pain Points (Phase 1):**
- 4 moods are too limiting — her emotions don't fit neatly into "anxious/sad/frustrated/overwhelmed"
- No way to track intensity — 3/10 anxiety ≠ 9/10 anxiety
- No context capture — she forgets what triggered emotions
- Only one regulation method (breathing) — sometimes she needs something different

---

## Goal-Directed Flow Design

### Design Principle
**Users don't come to Double Mood to "use an app." They come to feel better.** Every interaction must serve that goal. No unnecessary steps, no cognitive load, no tech jargon.

### Core User Journey
```
I feel bad → I name it → I track it → I release it → I feel better → I understand my patterns
```

---

## Phase 2 User Flow (Complete)

### Screen 1: Weather Category Selection (4 Main Weather)

**User Goal:** Quickly identify the "climate" of my emotion without thinking too hard.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│  How does it feel right now?       │
│  现在感觉像什么天气？                │
├─────────────────────────────────────┤
│                                     │
│  ┌──────┐  ┌──────┐  ┌──────┐     │
│  │  ☀️  │  │  ☁️  │  │  🌫️  │     │
│  │Sunny │  │Cloudy│  │ Foggy│     │
│  │ 晴朗  │  │ 多云  │  │ 迷雾  │     │
│  └──────┘  └──────┘  └──────┘     │
│                                     │
│  ┌──────┐                          │
│  │  ⛈️  │                          │
│  │Stormy│                          │
│  │ 风暴  │                          │
│  └──────┘                          │
│                                     │
│  [Not sure? Skip to describe →]    │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Large touch targets** — 80px × 80px minimum per weather card
- **Weather icons** — Animated on hover/tap (subtle breeze, cloud drift, rain fall, lightning flash)
- **Color-coded borders** — Each weather has a distinct color gradient
  - Sunny: Warm yellows/oranges `#FFD700` → `#FFA500`
  - Cloudy: Cool grays `#B0B0B0` → `#808080`
  - Foggy: Soft blues/greens `#A8DADC` → `#457B9D`
  - Stormy: Deep purples/reds `#5A189A` → `#C1121F`
- **Selected state** — Gentle glow + scale up 1.1x
- **No scrolling** — All 4 weather cards visible on screen (2×2 grid on mobile)

**Accessibility:**
- `aria-label`: "Select Sunny weather for positive emotions"
- Screen reader announces: "4 weather categories available. Use arrow keys to navigate."

**Navigation:**
- **Tap weather** → Auto-advance to Screen 2 (sub-emotion selection)
- **Tap "Not sure?"** → Jump to Screen 4 (trigger text field) for free-form emotion description

---

### Screen 2: Sub-Emotion Selection (16 Total)

**User Goal:** Precisely name the specific emotion within the chosen weather category.

**Interaction Pattern (Example: User selected ☁️ Cloudy):**
```
┌─────────────────────────────────────┐
│  ☁️ Cloudy — Which kind?            │
│  多云 — 哪一种？                     │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────┐               │
│  │ ☁️ Thin Clouds   │               │
│  │   薄云           │               │
│  │ Bored, numb      │               │
│  └──────────────────┘               │
│                                     │
│  ┌──────────────────┐               │
│  │ 🌥️ Heavy Clouds  │               │
│  │   厚云           │               │
│  │ Exhausted, burnt │               │
│  └──────────────────┘               │
│                                     │
│  ┌──────────────────┐               │
│  │ 🌦️ Cloudy→Rain   │               │
│  │   多云转雨        │               │
│  │ A bit down       │               │
│  └──────────────────┘               │
│                                     │
│  ┌──────────────────┐               │
│  │ 🌪️ Scattered     │               │
│  │   乱云           │               │
│  │ Racing thoughts  │               │
│  └──────────────────┘               │
│                                     │
│  [← Back to weather]                │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Vertical list** — Each sub-emotion is a full-width card (easier thumb reach)
- **Emoji + Name + Feeling descriptor** — 3-line card format
  - Line 1: Emoji (32px) + English name (bold, 18px)
  - Line 2: Chinese name (16px, muted)
  - Line 3: Feeling descriptor (14px, italic, lighter gray)
- **Card hover/tap** — Background color shift to weather-specific tint
- **Transition animation** — Slide-in from right when entering from Screen 1
- **Back button** — Top-left corner, returns to Screen 1

**Accessibility:**
- `aria-label`: "Heavy Clouds — Exhausted, burnt out, no energy"
- Grouped by weather category with `role="group"` and `aria-labelledby`

**Navigation:**
- **Tap sub-emotion** → Auto-advance to Screen 3 (intensity bar)
- **Tap "← Back"** → Return to Screen 1

---

### Screen 3: Intensity Bar (Emotion Strength)

**User Goal:** Communicate how strong this emotion feels right now.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│  🌥️ Heavy Clouds — How strong?     │
│  厚云 — 强度如何？                   │
├─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐
│  │                                 │
│  │    ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░         │
│  │    ◄─────────────────────►      │
│  │           7 / 10                │
│  │                                 │
│  └─────────────────────────────────┘
│
│  Mild          Moderate     Intense
│  轻微            中等          强烈
│
│  You're feeling quite exhausted.
│  你感到非常疲惫。
│
│  [Continue →]
└─────────────────────────────────────┘
```

**Visual Design:**
- **Large draggable slider** — Thumb height 48px (easy to grab)
- **Visual feedback** — Bar color shifts based on intensity
  - 0-3: Light tint of weather color (soft)
  - 4-7: Medium saturation (moderate)
  - 8-10: High saturation + glow effect (intense)
- **Dynamic text** — Changes based on intensity level
  - 0-3: "You're feeling a bit [emotion]." / "你感到有点[emotion]。"
  - 4-7: "You're feeling quite [emotion]." / "你感到相当[emotion]。"
  - 8-10: "You're feeling very [emotion]." / "你感到非常[emotion]。"
- **Haptic feedback** (if mobile) — Gentle vibration at 0, 5, 10 markers
- **Number display** — Large, centered, updates in real-time as user drags

**Accessibility:**
- `aria-valuemin="0"` `aria-valuemax="10"` `aria-valuenow="7"`
- `aria-label`: "Intensity level 7 out of 10"
- Keyboard: Arrow keys adjust by 1, Page Up/Down adjust by 5

**Navigation:**
- **Tap Continue** → Auto-advance to Screen 4 (trigger text)
- **Back button** (hidden by default) — If user wants to change sub-emotion

---

### Screen 4: Trigger Text Field (Optional Context)

**User Goal:** Capture what caused this emotion (optional — no pressure).

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│  What triggered this feeling?       │
│  是什么引起的？(可选)                │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │ e.g., "Didn't hear back      │  │
│  │ from her after texting"      │  │
│  │                              │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                     │
│  This helps you spot patterns later.│
│  这有助于发现情绪模式。              │
│                                     │
│  [Skip →]     [Save & Continue →]   │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Auto-expanding textarea** — Starts at 2 lines, expands to 6 lines max
- **Placeholder text** — Shows relatable example (rotates between 5-6 examples)
  - "She didn't reply to my message"
  - "Boss criticized my work in front of team"
  - "Scrolled social media for 2 hours"
  - "Had an argument with partner"
  - "Deadline is tomorrow, not ready"
- **Character count** — Hidden (no pressure), but soft limit at 200 chars
- **No validation** — User can write anything or nothing
- **Dual CTA** — "Skip" is equally prominent as "Save & Continue" (no dark pattern)

**Accessibility:**
- `aria-label`: "Optional text field to describe what triggered your emotion"
- `aria-required="false"`

**Navigation:**
- **Tap Skip** → Jump to Screen 5 (regulation method choice)
- **Tap Save & Continue** → Store trigger text → Advance to Screen 5
- **Auto-save** — Text is saved to localStorage as user types (no data loss)

---

### Screen 5: Regulation Method Choice (Dual Options)

**User Goal:** Choose the emotional regulation technique that feels right for this moment.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│  How would you like to release it?  │
│  如何释放这个情绪？                  │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │  🌊 Sedona Method             │  │
│  │  圣多纳释放法                 │  │
│  │                               │  │
│  │  Feel it → Let it go          │  │
│  │  4 gentle questions           │  │
│  │  ⏱ 2-3 minutes                │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  🫁 Breathing Exercise        │  │
│  │  呼吸练习                     │  │
│  │                               │  │
│  │  Follow the circle            │  │
│  │  3 cycles of calm breathing   │  │
│  │  ⏱ 60 seconds                 │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  🌀 Both (Sedona + Breathing) │  │
│  │  两者都试试                   │  │
│  │  ⏱ 4-5 minutes                │  │
│  └──────────────────────────────┘  │
│                                     │
│  [← Back]                           │
└─────────────────────────────────────┘
```

**Visual Design:**
- **3 large cards** — Full-width, stacked vertically
- **Icon + Name + Description + Time estimate** — 4-line card format
- **Visual preview** — Subtle animated icon (wave for Sedona, breathing circle pulse for Breathing)
- **Equal emphasis** — No card is visually "preferred" (user chooses what feels right)
- **Time estimate** — Helps user set expectations ("I only have 1 minute" → Breathing)

**Accessibility:**
- Each card has `role="button"` and full descriptive `aria-label`
- Screen reader: "Sedona Method. Feel it, then let it go. 4 gentle questions. Estimated time: 2 to 3 minutes."

**Navigation:**
- **Tap Sedona Method** → Advance to Screen 6A (Sedona flow)
- **Tap Breathing Exercise** → Jump to Screen 7 (Breathing flow, same as Phase 1)
- **Tap Both** → Advance to Screen 6A (Sedona first) → Then Screen 7 (Breathing) → Then Screen 8 (After rating)
- **Tap ← Back** → Return to Screen 4 (trigger text)

---

### Screen 6A: Sedona Method — Question 1

**User Goal:** Acknowledge the emotion's existence without judgment.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│                                     │
│          🌊                         │
│                                     │
│  Can you feel this emotion          │
│  right now?                         │
│                                     │
│  我能感受到它的存在吗？              │
│                                     │
│                                     │
│  Just notice it. You don't have to  │
│  change it.                         │
│                                     │
│  只需觉察它。不必改变它。            │
│                                     │
│                                     │
│          [Yes, I feel it →]         │
│                                     │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Minimal UI** — Only the question, no distractions
- **Soft background** — Weather-specific gradient (very subtle, 5% opacity)
- **Wave icon** — Gentle animation (slow oscillation, calming)
- **Breathing space** — Lots of whitespace, text is centered, readable (20px font)
- **Single CTA** — "Yes, I feel it" (no "No" option — the point is awareness, not yes/no)
- **No timer** — User proceeds at their own pace

**Accessibility:**
- `aria-live="polite"` region for question text
- Screen reader pauses slightly before reading the question

**Navigation:**
- **Tap "Yes, I feel it"** → Gentle fade transition to Screen 6B (Question 2)
- **Wait 5 seconds** → Auto-advance if user doesn't tap (respects user's pace)

---

### Screen 6B: Sedona Method — Question 2

**User Goal:** Consider the possibility of release without forcing it.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│                                     │
│          🌊                         │
│                                     │
│  Can you let it go?                 │
│                                     │
│  我能放下它吗？                      │
│                                     │
│                                     │
│  Not "should you," but "can you?"   │
│  There's no wrong answer.           │
│                                     │
│  不是"应该吗"，而是"能吗"？          │
│  没有错误的答案。                    │
│                                     │
│                                     │
│     [Yes →]        [Not yet →]      │
│                                     │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Same minimal aesthetic** — Consistency with Question 1
- **Two CTAs** — "Yes" and "Not yet" (both are valid, no judgment)
- **Button styling** — Both buttons are same size, same color (no dark pattern)
- **Instructional text** — Reminds user there's no "right" answer

**Accessibility:**
- Both buttons have equal prominence in tab order
- Screen reader: "Can you let it go? Two options: Yes, or Not yet."

**Navigation:**
- **Tap "Yes"** → Advance to Screen 6C (Question 3)
- **Tap "Not yet"** → Advance to Screen 6C (Question 3) — Both paths proceed (the answer doesn't matter, the inquiry does)

---

### Screen 6C: Sedona Method — Question 3

**User Goal:** Assess willingness to release, separate from ability.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│                                     │
│          🌊                         │
│                                     │
│  Are you willing to let it go?      │
│                                     │
│  我愿意放下它吗？                    │
│                                     │
│                                     │
│  This is about willingness,         │
│  not ability.                       │
│                                     │
│  这是关于意愿，不是能力。            │
│                                     │
│                                     │
│     [Yes →]        [Not yet →]      │
│                                     │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Identical structure to Screen 6B** — Predictable rhythm
- **Same dual CTA** — "Yes" / "Not yet" (both valid)

**Accessibility:**
- Same as Screen 6B

**Navigation:**
- **Tap "Yes"** → Advance to Screen 6D (Question 4)
- **Tap "Not yet"** → Advance to Screen 6D (Question 4)

---

### Screen 6D: Sedona Method — Question 4

**User Goal:** Choose the timing of release (ideally "now").

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│                                     │
│          🌊                         │
│                                     │
│  When?                              │
│                                     │
│  什么时候？                          │
│                                     │
│                                     │
│  When will you let it go?           │
│                                     │
│  你什么时候放下它？                  │
│                                     │
│                                     │
│  [Now →]    [Repeat cycle →]        │
│                                     │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Same minimal UI** — Final question in the sequence
- **Two CTAs** — "Now" (ideal) or "Repeat cycle" (if not ready)
- **"Now" is slightly more prominent** — Gentle nudge, but not forced

**Accessibility:**
- Screen reader: "When will you let it go? Two options: Now, or Repeat the cycle."

**Navigation:**
- **Tap "Now"** → Advance to Screen 8 (After rating) OR Screen 7 (Breathing) if user chose "Both"
- **Tap "Repeat cycle"** → Loop back to Screen 6A (Question 1) — User can cycle 2-3 times if needed

**Transition Animation:**
- **If "Now"** → Gentle dissolve (2 seconds) with expanding wave icon
- **If "Repeat"** → Quick fade-back to Question 1 (no delay)

---

### Screen 7: Breathing Exercise (Unchanged from Phase 1)

**User Goal:** Activate parasympathetic nervous system through rhythmic breathing.

**Interaction Pattern:** (Same as Phase 1 — no changes needed)
```
┌─────────────────────────────────────┐
│  Follow the circle                  │
│  跟着圆圈呼吸                        │
├─────────────────────────────────────┤
│                                     │
│      ● ○ ○ (Cycle indicators)       │
│                                     │
│         ◯ ← Breathing circle        │
│        (expands/contracts)          │
│                                     │
│    Breathe in... 吸气...            │
│                                     │
└─────────────────────────────────────┘
```

**Duration:** 60 seconds (3 cycles × 10 seconds each: 4s inhale, 6s exhale)

**Navigation:**
- **Auto-advance** after 3 cycles → Screen 8 (After rating)

---

### Screen 8: After Rating (Enhanced)

**User Goal:** Report current emotional state to measure improvement.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│  How are you feeling now?           │
│  现在感觉如何？                      │
├─────────────────────────────────────┤
│                                     │
│  Before: 🌥️ Heavy Clouds — 7/10    │
│  之前: 厚云 — 7/10                  │
│                                     │
│  ┌─────────────────────────────────┐│
│  │                                 ││
│  │    ░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓         ││
│  │    ◄─────────────────────►      ││
│  │           3 / 10                ││
│  │                                 ││
│  └─────────────────────────────────┘│
│                                     │
│  Mild          Moderate     Intense │
│  轻微            中等          强烈   │
│                                     │
│  You're feeling much lighter.       │
│  你感到轻松多了。                    │
│                                     │
│  [Complete →]                       │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Before state reminder** — Shows original emotion + intensity (top of screen)
- **Same intensity slider** — Consistent with Screen 3 (muscle memory)
- **Dynamic comparison text** — Changes based on delta
  - If after < before: "You're feeling much lighter." / "你感到轻松多了。"
  - If after ≈ before: "That's okay. Sometimes it takes time." / "没关系。有时需要时间。"
  - If after > before: "Still tough, huh? You're doing your best." / "还是很难吗？你已经尽力了。"
- **No judgment** — Even if user rates higher, the tone is supportive

**Accessibility:**
- Same slider accessibility as Screen 3

**Navigation:**
- **Tap Complete** → Advance to Screen 9 (Success + Improvement feedback)

---

### Screen 9: Success + Improvement Feedback (Enhanced)

**User Goal:** See tangible evidence of improvement and feel validated.

**Interaction Pattern:**
```
┌─────────────────────────────────────┐
│          ✨                         │
│                                     │
│  You did great!                     │
│  你很棒！                            │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Improvement                  │  │
│  │                               │  │
│  │       -4 points               │  │
│  │                               │  │
│  │  🌥️ Heavy Clouds (7/10)       │  │
│  │         ↓                     │  │
│  │  ☁️ Thin Clouds (3/10)        │  │
│  │                               │  │
│  │  You feel much calmer now.    │  │
│  └──────────────────────────────┘  │
│                                     │
│  Take a moment. You deserve it.     │
│  给自己一点时间，你值得。            │
│                                     │
│  [See patterns →]  [Again →]        │
└─────────────────────────────────────┘
```

**Visual Design:**
- **Large improvement delta** — "-4 points" (or "+2" if improvement is positive)
- **Before/After emotion names** — Shows shift between sub-emotions (if intensity change is large enough to cross boundaries)
- **Visual arrow** — Downward arrow for improvement, upward if worse
- **Color-coded** — Green for improvement, yellow for neutral, orange if worse (no red — no shame)
- **Dual CTA** — "See patterns" (new) or "Again" (restart flow)

**Accessibility:**
- Screen reader: "Improvement: You feel 4 points calmer. Before: Heavy Clouds at 7 out of 10. After: Thin Clouds at 3 out of 10."

**Navigation:**
- **Tap "See patterns"** → Jump to Screen 10 (Weekly patterns view — future feature, placeholder for now)
- **Tap "Again"** → Reset to Screen 1 (Weather category selection)

---

### Screen 10: Weekly Patterns (Future — Phase 3)

**User Goal:** Understand emotional patterns over time.

**Placeholder for Phase 2:**
```
┌─────────────────────────────────────┐
│  Your patterns (coming soon)        │
│  你的情绪模式（即将推出）            │
├─────────────────────────────────────┤
│                                     │
│  Track your emotions for a week to  │
│  see patterns like:                 │
│                                     │
│  • Most common emotions             │
│  • Highest intensity moments        │
│  • Common triggers                  │
│  • Best regulation methods          │
│                                     │
│  记录一周情绪后，你将看到：          │
│                                     │
│  • 最常出现的情绪                    │
│  • 最强烈的时刻                      │
│  • 常见触发因素                      │
│  • 最有效的调节方法                  │
│                                     │
│  [Start fresh session →]            │
└─────────────────────────────────────┘
```

**Note:** This is a placeholder screen for Phase 2. Full implementation will be in Phase 3 with data visualization.

---

## Complete Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          DOUBLE MOOD PHASE 2 — USER FLOW                 │
└──────────────────────────────────────────────────────────────────────────┘

Start
  │
  ▼
┌─────────────────────┐
│ Screen 1:           │
│ Weather Category    │  (4 main weather: Sunny, Cloudy, Foggy, Stormy)
│ Selection           │
└─────────────────────┘
  │
  ├─────────────┬─────────────┬─────────────┐
  ▼             ▼             ▼             ▼
☀️ Sunny      ☁️ Cloudy     🌫️ Foggy      ⛈️ Stormy
  │             │             │             │
  └─────────────┴─────────────┴─────────────┘
  │
  ▼
┌─────────────────────┐
│ Screen 2:           │
│ Sub-Emotion         │  (16 total — 4 per weather category)
│ Selection           │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Screen 3:           │
│ Intensity Bar       │  (0-10 scale, visual feedback)
│                     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Screen 4:           │
│ Trigger Text        │  (Optional — Skip or Save)
│ (Optional)          │
└─────────────────────┘
  │
  ├─── Skip ────┐
  │             │
  ▼             │
┌─────────────────────┐
│ Screen 5:           │
│ Regulation Method   │  (Sedona / Breathing / Both)
│ Choice              │
└─────────────────────┘
  │
  ├───────────┬────────────┬──────────────┐
  ▼           ▼            ▼              │
Sedona      Breathing     Both            │
  │           │            │              │
  ▼           │            ▼              │
┌───────┐     │     ┌────────────────┐    │
│Screen │     │     │ Sedona THEN    │    │
│ 6A-6D │     │     │ Breathing      │    │
│Sedona │     │     └────────────────┘    │
│Method │     │            │              │
│4 Qs   │     │            ▼              │
└───────┘     │     ┌───────┐  ┌────────┐ │
  │           │     │Screen │  │Screen  │ │
  │           │     │ 6A-6D │→ │   7    │ │
  │           │     │Sedona │  │Breathe │ │
  │           │     └───────┘  └────────┘ │
  │           │                     │     │
  │           ▼                     │     │
  │     ┌─────────────────┐         │     │
  │     │ Screen 7:       │         │     │
  │     │ Breathing       │◄────────┘     │
  │     │ Exercise        │               │
  │     └─────────────────┘               │
  │           │                           │
  └───────────┴───────────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Screen 8:           │
│ After Rating        │  (Same 0-10 intensity slider)
│                     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Screen 9:           │
│ Success +           │  (Show improvement delta, before/after emotions)
│ Improvement         │
│ Feedback            │
└─────────────────────┘
  │
  ├──── See patterns ────┐
  │                      ▼
  │               ┌─────────────────────┐
  │               │ Screen 10:          │
  │               │ Weekly Patterns     │  (Phase 3 — Placeholder in Phase 2)
  │               │ (Future)            │
  │               └─────────────────────┘
  │
  └──── Again ────► Back to Screen 1 (Restart)
```

---

## Interaction Patterns Summary

### 1. Weather + Sub-Emotion Selection
**Pattern:** Progressive Disclosure (Coarse → Fine)
- **Why:** Reduces cognitive load — user doesn't see all 16 emotions at once
- **How:** 4 weather categories first, then 4 sub-emotions within chosen category
- **Visual cue:** Smooth transition (weather card expands into sub-emotion list)

### 2. Intensity Bar
**Pattern:** Continuous Input with Real-Time Feedback
- **Why:** Allows nuance — 3/10 anxiety feels different from 8/10 anxiety
- **How:** Draggable slider (0-10), color gradient shifts based on value
- **Visual cue:** Number display + dynamic text ("You're feeling quite exhausted")

### 3. Trigger Text Field
**Pattern:** Optional Input with Encouragement (No Pressure)
- **Why:** Respects user agency — some people want to journal, others don't
- **How:** Free-text field with relatable placeholder examples
- **Visual cue:** "Skip" and "Save & Continue" buttons are equally prominent

### 4. Regulation Method Choice
**Pattern:** Explicit Choice (No Default)
- **Why:** User knows best what they need in this moment
- **How:** 3 equal-prominence cards (Sedona / Breathing / Both)
- **Visual cue:** No "recommended" tag — all methods are valid

### 5. Sedona Method (4 Questions)
**Pattern:** Sequential Inquiry (One Question Per Screen)
- **Why:** Prevents overwhelm, creates breathing space for reflection
- **How:** 4 separate screens, minimal UI, gentle transitions
- **Visual cue:** Wave icon animation (calming rhythm)

### 6. Breathing Exercise
**Pattern:** Ambient Guidance (Passive Follow-Along)
- **Why:** User doesn't need to think, just breathe
- **How:** Expanding/contracting circle + text cues ("Breathe in...")
- **Visual cue:** Synchronized animation (4s expand, 6s contract)

### 7. Before/After Rating
**Pattern:** Comparative Measurement (Anchored to Previous State)
- **Why:** Makes improvement tangible and visible
- **How:** Show "Before" state at top, then ask for "After" rating
- **Visual cue:** Side-by-side comparison or arrow showing shift

---

## Navigation Structure

### Primary Flow (Happy Path)
```
Screen 1 → Screen 2 → Screen 3 → Screen 4 → Screen 5 → (Screen 6 OR 7) → Screen 8 → Screen 9
```

### Escape Hatches (User Control)
- **Skip trigger field** — Screen 4 → Screen 5 (bypass journaling)
- **Back to weather** — Screen 2 → Screen 1 (change category)
- **Repeat Sedona** — Screen 6D → Screen 6A (cycle again if not ready)
- **Restart** — Screen 9 → Screen 1 (new session)

### Navigation Principles
1. **Always forward** — Default action advances user toward completion
2. **Occasional back** — Only when choice needs revision (Screen 2 → Screen 1)
3. **Skip options** — Never force input (trigger text, regulation method choice)
4. **Auto-advance when possible** — If there's only one next step, don't make user tap "Next"

---

## Data Storage (localStorage Schema)

```javascript
{
  "sessions": [
    {
      "id": "uuid-1234",
      "timestamp": "2026-02-21T14:32:00Z",
      "weatherCategory": "cloudy",          // ☁️ Cloudy
      "subEmotion": "heavy-clouds",         // 🌥️ Heavy Clouds
      "intensityBefore": 7,                 // 0-10
      "trigger": "Boss criticized my work", // Optional
      "regulationMethod": "sedona",         // "sedona" | "breathing" | "both"
      "sedonaCycles": 2,                    // Number of times user repeated Sedona
      "intensityAfter": 3,                  // 0-10
      "improvementDelta": -4,               // After - Before (negative = improvement)
      "durationSeconds": 180                // Total session time
    },
    // ... more sessions
  ],
  "preferences": {
    "language": "en",  // "en" | "zh"
    "lastUsed": "2026-02-21T14:35:00Z"
  }
}
```

**Privacy:** All data stored locally in browser. No server upload in Phase 2.

---

## Mobile-First Interaction Details

### Touch Targets
- **Minimum size:** 48×48px (Apple HIG + Material Design standard)
- **Spacing:** 8px between interactive elements (prevent mis-taps)

### Gestures
- **Tap:** All primary interactions (no long-press, no swipe)
- **Drag:** Intensity slider only
- **Scroll:** Sub-emotion list (Screen 2) if screen is too short

### Haptics (iOS/Android)
- **Intensity slider:** Light haptic at 0, 5, 10 markers
- **Button tap:** Medium haptic on primary CTA
- **Transition:** No haptic (too distracting)

### Keyboard Support (Desktop/Tablet)
- **Arrow keys:** Navigate options, adjust slider
- **Enter/Space:** Select highlighted option
- **Esc:** Go back (if back button exists)
- **Tab:** Focus next interactive element

---

## Accessibility (WCAG 2.1 AA Compliance)

### Screen Reader
- All interactive elements have `aria-label`
- Dynamic content changes announced via `aria-live="polite"`
- Semantic HTML (`<button>`, `<input type="range">`, etc.)

### Keyboard Navigation
- Full flow completable without mouse
- Visible focus indicators (2px blue outline)
- Logical tab order (top to bottom, left to right)

### Color Contrast
- Text: Minimum 4.5:1 ratio (7:1 for body text)
- Interactive elements: 3:1 ratio
- Weather gradients: Tested with colorblind simulators

### Motion
- `prefers-reduced-motion` CSS media query disables all animations
- Breathing circle transitions to static pulsing dots

---

## Bilingual (EN + 中文) Strategy

### Layout
- **Stacked bilingual** — English first, Chinese below (smaller font)
- **Example:**
  ```
  How do you feel right now?
  现在感觉如何？
  ```

### Font Sizes
- **English:** 18px (primary), 14px (secondary)
- **Chinese:** 16px (primary), 12px (secondary)
- **Reason:** Chinese characters are denser, slightly smaller feels balanced

### Translation Quality
- All Chinese translations reviewed by native speaker (Founder)
- Avoid direct translation — use culturally resonant phrases
  - "You did great!" → "你很棒！" (not "你做得很好" — too formal)

---

## Phase 2 → Phase 3 Migration Path

### What Phase 2 Sets Up
1. **Rich data collection** — 16 emotions + intensity + triggers = pattern detection ready
2. **localStorage schema** — Designed to scale to server sync later
3. **User habits** — Training users to log emotions consistently

### What Phase 3 Will Add
1. **Weekly reports** — Data visualization (charts, heatmaps)
2. **Pattern detection** — "You feel anxious every Monday at 9am"
3. **Trigger analysis** — "Your top 3 triggers: Work, Relationships, Social media"
4. **Regulation efficacy** — "Sedona works better for you than Breathing (65% vs 45% improvement)"
5. **Cloud sync** — Save data across devices
6. **Notifications** — "Haven't logged today, feeling okay?"

---

## Design Philosophy (Alan Cooper Principles Applied)

### 1. Goal-Directed Design
**User's goal:** Feel better, not "use an app"
- **Applied:** Every screen serves emotional regulation, not feature showcasing
- **Example:** No "About" button, no "Settings" icon — just the flow

### 2. Persona-Driven
**Primary Persona:** Emma (anxious 28yo PM)
- **Applied:** 16 emotions cover her spectrum (not just "anxiety")
- **Example:** "Heavy Clouds — Exhausted, burnt out" speaks to her burnout specifically

### 3. Implementation Model Hidden
**Tech reality:** localStorage, JavaScript state management
- **Applied:** User never sees "Saving to localStorage..." or error codes
- **Example:** Auto-save trigger text as they type (no "Save" button anxiety)

### 4. Interaction Etiquette
**Software as polite assistant**
- **Applied:** No interruptions, no forced inputs, no guilt-tripping
- **Example:** "Skip" button on trigger field is equally prominent as "Save & Continue"

### 5. Elastic User = Enemy
**No designing for "everyone"**
- **Applied:** Optimized for Emma's specific emotional landscape
- **Example:** Secondary Persona (college student with social anxiety) is accommodated but not prioritized

---

## Potential Interaction Pitfalls (Pre-Mortem)

### Pitfall 1: Sub-Emotion Overload
**Risk:** 16 emotions feel overwhelming instead of helpful
**Mitigation:** Progressive disclosure (4 weather → 4 sub-emotions), not all 16 at once

### Pitfall 2: Intensity Bar Confusion
**Risk:** User doesn't understand 0-10 scale (is 0 good or bad?)
**Mitigation:** Visual gradient (red → yellow → green) + descriptive text labels

### Pitfall 3: Sedona Method Too Vague
**Risk:** User doesn't "get it," feels like pseudoscience
**Mitigation:** Instructional text explains intent ("This is about awareness, not yes/no"), gentle tone

### Pitfall 4: Trigger Field Feels Like Homework
**Risk:** User abandons flow because writing feels like a chore
**Mitigation:** "Skip" button, placeholder examples, no character limit pressure

### Pitfall 5: Bilingual Layout Clutter
**Risk:** Chinese text makes UI feel cramped
**Mitigation:** Smaller Chinese font, muted color, generous whitespace

### Pitfall 6: User Forgets What They Rated "Before"
**Risk:** Can't accurately compare after-state to before-state
**Mitigation:** Show "Before: 🌥️ Heavy Clouds — 7/10" at top of Screen 8

---

## Wireframe Examples (Text-Based)

### Screen 1 (Weather Selection) — Mobile Viewport
```
┌──────────────────────────────────┐
│ 📱 (375px × 812px viewport)      │
├──────────────────────────────────┤
│                                  │
│  How does it feel right now?     │
│  现在感觉像什么天气？             │
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │    ☀️      │  │    ☁️      │ │
│  │   Sunny    │  │   Cloudy   │ │
│  │    晴朗     │  │    多云     │ │
│  └────────────┘  └────────────┘ │
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │    🌫️      │  │    ⛈️      │ │
│  │   Foggy    │  │   Stormy   │ │
│  │    迷雾     │  │    风暴     │ │
│  └────────────┘  └────────────┘ │
│                                  │
│  [Not sure? Skip to describe →] │
│                                  │
└──────────────────────────────────┘
```

### Screen 3 (Intensity Bar) — Mobile Viewport
```
┌──────────────────────────────────┐
│ 📱                               │
├──────────────────────────────────┤
│                                  │
│  🌥️ Heavy Clouds — How strong?  │
│  厚云 — 强度如何？                │
│                                  │
│  ┌──────────────────────────────┐│
│  │  ▓▓▓▓▓▓▓░░░░░░░░░░░░         ││
│  │  ◄──────────────────────►    ││
│  │         7 / 10               ││
│  └──────────────────────────────┘│
│                                  │
│  Mild      Moderate      Intense │
│  轻微        中等         强烈    │
│                                  │
│  You're feeling quite exhausted. │
│  你感到非常疲惫。                 │
│                                  │
│  ┌──────────────────────────────┐│
│  │      [Continue →]            ││
│  └──────────────────────────────┘│
│                                  │
└──────────────────────────────────┘
```

### Screen 6B (Sedona Question 2) — Mobile Viewport
```
┌──────────────────────────────────┐
│ 📱                               │
├──────────────────────────────────┤
│                                  │
│          🌊                      │
│                                  │
│  Can you let it go?              │
│                                  │
│  我能放下它吗？                   │
│                                  │
│                                  │
│  Not "should you," but "can you?"│
│  There's no wrong answer.        │
│                                  │
│  不是"应该吗"，而是"能吗"？       │
│  没有错误的答案。                 │
│                                  │
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │  Yes →     │  │ Not yet →  │ │
│  └────────────┘  └────────────┘ │
│                                  │
└──────────────────────────────────┘
```

---

## Implementation Checklist (For fullstack-dhh)

### Core Flow
- [ ] Screen 1: Weather category selection (4 cards, touch-friendly)
- [ ] Screen 2: Sub-emotion selection (16 total, grouped by weather)
- [ ] Screen 3: Intensity bar (0-10, draggable slider, color gradient)
- [ ] Screen 4: Trigger text field (optional, auto-expanding textarea)
- [ ] Screen 5: Regulation method choice (Sedona / Breathing / Both)
- [ ] Screen 6A-6D: Sedona Method (4 questions, one per screen)
- [ ] Screen 7: Breathing exercise (reuse Phase 1 implementation)
- [ ] Screen 8: After rating (intensity slider, show before-state)
- [ ] Screen 9: Success + improvement feedback (delta calculation)
- [ ] Screen 10: Weekly patterns placeholder (coming in Phase 3)

### Data & State
- [ ] localStorage schema (sessions array, preferences object)
- [ ] Auto-save trigger text as user types
- [ ] Calculate improvement delta (after - before)
- [ ] Store Sedona cycle count
- [ ] Track total session duration

### Accessibility
- [ ] All buttons have `aria-label`
- [ ] Intensity slider has `aria-valuemin/max/now`
- [ ] Dynamic text changes use `aria-live="polite"`
- [ ] Keyboard navigation (Tab, Enter, Arrow keys)
- [ ] Focus indicators (2px blue outline)
- [ ] `prefers-reduced-motion` media query

### Bilingual
- [ ] All screens have EN + 中文 stacked layout
- [ ] Chinese font 2px smaller than English
- [ ] Culturally resonant Chinese translations (reviewed by Founder)

### Visual Design
- [ ] Weather-specific color gradients (Sunny/Cloudy/Foggy/Stormy)
- [ ] Animated weather icons (subtle, calming)
- [ ] Intensity bar color shifts (red → yellow → green)
- [ ] Sedona wave icon animation (gentle oscillation)
- [ ] Transition animations (fade, slide, dissolve)

### Testing
- [ ] Test on iPhone (Safari)
- [ ] Test on Android (Chrome)
- [ ] Test with screen reader (VoiceOver, TalkBack)
- [ ] Test with keyboard only
- [ ] Test with `prefers-reduced-motion` enabled

---

## Ship Criteria

This design is ready for implementation when:
1. ✅ All 10 screens are wireframed (text-based is fine)
2. ✅ Interaction patterns are defined (tap/drag/swipe)
3. ✅ Navigation flow is clear (happy path + escape hatches)
4. ✅ Data storage schema is specified
5. ✅ Accessibility requirements are documented
6. ✅ Bilingual strategy is defined

**Status:** ✅ Shipped — This document is complete and ready for `fullstack-dhh` to implement.

---

## Next Actions (For Other Agents)

### For `fullstack-dhh` (Developer)
- Read this flow document
- Implement Screens 1-10 in HTML/CSS/JS
- Use existing Phase 1 codebase as foundation
- Test on mobile devices + screen readers

### For `ui-duarte` (Visual Designer)
- Design weather-specific color palettes (Sunny/Cloudy/Foggy/Stormy)
- Create animated weather icons (SVG, Lottie, or CSS)
- Design Sedona wave icon animation
- Provide visual mockups for Screens 3, 6A-6D (highest visual priority)

### For `qa-bach` (QA)
- Create test plan for 10-screen flow
- Test keyboard navigation + screen reader
- Test localStorage persistence (refresh page, close/reopen browser)
- Test edge cases (user rates "after" higher than "before")

### For `devops-hightower` (DevOps)
- No changes needed — Phase 2 is still static site (no backend)
- Verify Cloudflare Pages deployment works with new screens

---

**End of Document**
