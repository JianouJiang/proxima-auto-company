# Double Mood Phase 2 — Founder Vision

**Date:** 2026-02-22
**Source:** Founder direct input
**Status:** APPROVED — Build when loop starts

---

## 1. 16 Sub-Emotions (Weather System)

Replace the current 4 mood options with a 2-tier weather metaphor system: 4 main weather categories, each with 4 sub-emotions.

### ☀️ Sunny (Positive Emotions)
| Emoji | Name (CN) | Name (EN) | Feelings |
|-------|-----------|-----------|----------|
| 🌞 | 晴日当空 | Bright Sun | Joy, excitement, achievement |
| 🌸 | 晴暖微风 | Warm Breeze | Tenderness, contentment, feeling loved |
| 🌤️ | 晴转多云 | Partly Cloudy | A bit happy but also tired |
| 🌈 | 雨后初晴 | Rainbow | Relief, liberation, renewed hope |

### ☁️ Cloudy (Neutral / Fatigued Emotions)
| Emoji | Name (CN) | Name (EN) | Feelings |
|-------|-----------|-----------|----------|
| ☁️ | 薄云 | Thin Clouds | Bored, bland, numb |
| 🌥️ | 厚云 | Heavy Clouds | Exhausted, burnt out, no energy |
| 🌦️ | 多云转雨 | Cloudy to Rain | A bit down, want to cry but can't |
| 🌪️ | 乱云 | Scattered Clouds | Racing thoughts, can't focus |

### 🌫️ Foggy (Anxiety / Confusion Emotions)
| Emoji | Name (CN) | Name (EN) | Feelings |
|-------|-----------|-----------|----------|
| 🌫️ | 轻雾 | Light Fog | Mild anxiety, subtle unease |
| 🌫️ | 浓雾 | Dense Fog | Strong anxiety, chest tightness, can't breathe |
| 🌫️ | 晨雾 | Morning Fog | Lost, don't know what to do next |
| 🌫️ | 夜雾 | Night Fog | Lonely, empty, self-doubt |

### ⛈️ Stormy (Intense Negative Emotions)
| Emoji | Name (CN) | Name (EN) | Feelings |
|-------|-----------|-----------|----------|
| 🌩️ | 闪电 | Lightning | Rage, explosive anger |
| 🌧️ | 暴雨 | Downpour | Breakdown crying, emotional flood |
| 🌪️ | 龙卷风 | Tornado | Loss of control, hysteria |
| 🌋 | 火山 | Volcano | Suppressed to the limit, about to erupt |

---

## 2. Emotion Intensity Bar (血条)

Two-step interaction:
1. **Select weather** — pick from 4 categories or 16 sub-emotions
2. **Drag intensity bar** — 0-10 scale representing emotion strength

Examples:
- ⛈️ Stormy + 8/10 = Rage out of control
- 🌫️ Light Fog + 3/10 = Mild anxiety

This data becomes valuable in weekly reports:
> "You had 3 stormy episodes this week, all above 7/10, all after work meetings."

---

## 3. Trigger Mechanism

After selecting emotion + intensity, user can optionally write **what triggered** the emotion.

Example: "She didn't reply to my message"

This free-text field:
- Optional (not required, reduces friction)
- Stored in localStorage / future database
- Used in weekly reports for pattern detection
- Helps user connect emotions to causes over time

---

## 4. Multiple Regulation Methods

Current: Only breathing exercise (too limited).

### Add: Sedona Method (圣多纳释放法)

A guided self-inquiry process with 4 questions, shown one at a time:

1. **"Can I feel this emotion right now?"** (我能感受到它的存在吗？)
   - User sits with the feeling
   - Tap to proceed

2. **"Can I let it go?"** (我能放下它吗？)
   - Yes / No response
   - Either answer is fine — the point is awareness

3. **"Am I willing to let it go?"** (我愿意放下它吗？)
   - Yes / No response
   - No judgment on the answer

4. **"When?"** (什么时候？)
   - "Now" is the ideal answer
   - Can repeat the cycle if not ready

Design direction:
- Calm, minimal UI — one question per screen
- Gentle transitions between questions
- Can repeat the cycle multiple times
- Works for ALL 16 emotion types (not just anxiety)
- Designer has creative freedom on visual presentation

### Keep: Breathing Exercise
- Still available as an option
- User chooses: Breathing OR Sedona Method (or both)

### Future regulation methods (not Phase 2):
- Body scan
- Journaling prompts
- Grounding techniques (5-4-3-2-1)

---

## 5. Weekly Reports (Enhanced)

With richer data (16 emotions + intensity + triggers), weekly reports become powerful:

- Emotion weather map of the week
- Most frequent emotion category
- Highest intensity moments + their triggers
- Patterns: "Your anxiety spikes happen on Monday mornings"
- Improvement tracking: before/after delta trends

---

## Implementation Priority

1. **16 sub-emotions with weather UI** (replace current 4 moods)
2. **Intensity bar** (0-10, combined with weather selection)
3. **Trigger text field** (optional free text)
4. **Sedona Method** (4-question guided release)
5. **Keep breathing** as alternative regulation method
6. **Enhanced localStorage** to store all new data fields

---

## Design Notes from Founder

- Bilingual throughout (EN + 中文)
- Weather metaphor makes emotions less intimidating
- The 16 sub-emotions help users NAME what they feel (therapeutic value)
- Sedona Method is simple but powerful — design should feel calm and spacious
- Designer has creative freedom on Sedona Method visual presentation
