# 05 — UI/UX Design Document (Visual & Interaction Design Specification)

| Field | Value |
|---|---|
| Document Name | UI/UX Design Specification |
| Version | 1.0 |
| Status | Baseline for visual design and front-end build; validated by EXP-09 |
| Date | 2026-09-27 |
| Owner | UX/Design Lead |
| Purpose | Defines design philosophy, design system, and interaction design for the web app and capture app, with emphasis on the review interface, AI explanation and confidence UX, accessibility, Bangla typography and mobile use. |
| Source Research | S11/S11a (review console, keyboard-first, colour-coded evidence), S08 (automation bias, evidence-first), S09 (masking, reason capture), S03 (trust failures, moments of truth); VF-11 (devices); EV-08, EV-10, EV-22 |
| Dependencies | `04-wireframes.md` (structure), `01-PRD.md` (PP-1..8, FR-REV), `07` (HITL rules) |

---

## 1. Design Philosophy

> **Teacher efficiency + clarity + trust + auditability.** The interface should feel like a well-organised marking desk: calm, paper-first, and fast. It should not look like an "AI product".

| Principle | Design consequence |
|---|---|
| **The student's writing is the hero** | The answer image gets the most space and the highest visual priority. AI output is secondary, annotated onto or next to the image, never replacing it. |
| **Evidence before verdict** | Criteria and highlighted evidence render before the suggested total. Totals are typographically quieter than criteria (DEC-33). |
| **Honest AI** | Every AI element carries its level (Suggests / Evidence only / Manual) and plain reasons. There are no confidence percentages, no "AI score" hero numbers, no sparkle icons, no anthropomorphic assistant. |
| **One decision per screen, one tap to decide** | Review cards need no scrolling on desktop and minimal scrolling on phones. Confirm is always in the same place (thumb zone on phones). |
| **Speed without rubber-stamping** | Auto-advance, prefetch and shortcuts make it fast. Masked items, forced-open samples and dwell monitoring keep attention (not punitive). |
| **Bangla-first dignity** | Bangla is a first-class UI language with proper shaping, spacing and terminology, not a translation layer. |
| **Everything is reversible until locked, and nothing is silent after** | Undo is visible. Every change leaves an audit trail the teacher can see ("Changed by you, 14:05"). |
| **Calm under stress** | Exam season is stressful. Show progress, deadlines and what is blocking in plain words. No alarm colours for routine states. |

---

## 2. Information Architecture and Navigation

Structure and navigation are specified in `04` §1.

| Rule | Detail |
|---|---|
| Role-aware home | Each role lands on its next action (`04` SCR-02) |
| Exam as the workspace | All exam work lives in tabs of one exam workspace (Paper · Rubrics · Covers · Capture · Processing · Review · Moderation · Results). A state chip in the header shows where the exam is in its lifecycle. |
| Breadcrumbs | Desktop only: School › Exams › Physics 9 H-Y › Review › Q2 (গ) |
| Deep links | Notifications open the exact item or queue |
| Language toggle | Always visible (top bar / More menu). The choice is persisted per user. |

---

## 3. Layout

| Breakpoint | Grid | Key layouts |
|---|---|---|
| Phone 360–767 | 4 columns, 16 px gutters, 16 px margins | Bottom tabs; single-column cards; review card stacked (image → criteria → actions) |
| Tablet 768–1279 | 8 columns, 20 px gutters | Review card 55/45 split in landscape, stacked in portrait |
| Desktop ≥1280 | 12 columns, 24 px gutters, max content 1600 px | Left rail 232 px (collapsible to 64); review card 60/40 split |

- **Density modes:** "Comfortable" (default) and "Compact" (desktop tables and ledgers).
- **Review screen special rule:** no page-level scroll on desktop. The image pane scrolls and zooms independently, and the rubric pane scrolls only if criteria exceed the viewport.

---

## 4. Design System

### 4.1 Design tokens

| Token group | Values (initial; to be tuned in visual design) |
|---|---|
| Spacing | 4-pt scale: 4, 8, 12, 16, 24, 32, 48 |
| Radius | 6 (controls), 10 (cards), 16 (sheets) |
| Elevation | 0 (flat, default), 1 (cards on hover), 2 (menus), 3 (dialogs). Minimal shadows. |
| Motion | 120 ms (micro), 200 ms (panels). Auto-advance transition ≤150 ms. Respect `prefers-reduced-motion`. |
| Focus | 2 px outline, offset 2 px, high-contrast colour; never removed |

### 4.2 Typography

| Role | Bangla | Latin | Size / line-height (desktop · phone) |
|---|---|---|---|
| UI font | Noto Sans Bengali (fallback Hind Siliguri) | Noto Sans / Inter | — |
| Display (page titles) | 600 | 600 | 24/32 · 22/30 |
| Heading | 600 | 600 | 18/28 · 18/28 |
| Body | 400 | 400 | 15/24 · **16/26** |
| Dense table | 400 | 400 | 14/22 (desktop only) |
| Caption / chips | 500 | 500 | 13/20 (min for Bangla), never below 12 px |
| Numerals in marks | Tabular figures; Bangla digits (০–৯) optional per school setting | | |
| Math | KaTeX fonts, scaled to 1.05× body | | |

- **Bangla line-height ≥1.6×** to accommodate matra, kar and conjunct stacking. Avoid all-caps and letter-spacing on Bangla.
- **Mixed-script strings** (e.g., "বেগ (velocity) = 12.5 m/s") use the same baseline alignment. Test strings are in the QA visual suite.
- **PDF typography:** the same fonts are embedded. HarfBuzz shaping is verified (TR-BE-04).

### 4.3 Colour system

Colour is never the only carrier of meaning: every state also has an icon and a text label.

| Semantic token | Use | Light-mode example | Paired icon/label |
|---|---|---|---|
| `neutral-*` | Surfaces, text | Warm greys (paper-like background `#FAFAF7`, text `#1F2328`) | — |
| `primary` | Primary actions (Confirm) | Deep teal `#0F6E6E` | — |
| `criterion-met` | Criterion satisfied; evidence outline | Green `#2E7D32` | ✓ "met" |
| `criterion-partly` | Partial | Amber `#B26A00` | ◐ "partly" |
| `criterion-not` | Not met | Brick `#B3261E` | ✗ "not met" |
| `criterion-unknown` | Cannot determine | Slate `#5F6B7A` | ? "can't tell" |
| `risk-high` / `risk-medium` / `risk-low` | Risk chip | Brick / amber / slate-green | ● plus text "High / Medium / Low attention" |
| `ai-level` | Level badges | Blue-grey family (never green, to avoid a "correct" connotation) | "AI suggests" / "Evidence only" / "Manual" / "Batch eligible" |
| `info` / `warning` / `danger` banners | Offline, incidents, blocking errors | Blue / amber / red tints | Icon + text |

- **Contrast:** text ≥4.5:1, large text and UI glyphs ≥3:1 (WCAG 2.2 AA).
- **Colour-blind safety:** met/partly/not are distinguishable by icon shape; checked with deuteranopia/protanopia simulation.
- **Evidence highlights on images:** semi-transparent fills (20% alpha) plus a solid 2 px outline in the criterion colour. The criterion number sits in a small tag at the region's top-left. Highlights must not hide the ink: outlines only when zoom is below 100%.
- **Dim mode** (optional, for evening marking): dark chrome around the image with the image kept at natural paper brightness; toggled per user. A full dark theme is not a goal.

### 4.4 Iconography
A simple line icon set (e.g., Lucide/Material Symbols Outlined). No "robot" or "magic sparkle" metaphors for AI; AI items use a small neutral "lens" glyph.

### 4.5 Core components

| Component | Purpose | Key states & rules |
|---|---|---|
| **Answer viewer** | Show crops and pages | Zoom (pinch, scroll, +/−), pan, rotate, full page, context strip; evidence overlay layer; loading skeleton; image error retry |
| **Criterion row** | One rubric criterion with the AI decision and teacher control | Text (BN/EN per UI), marks (x/y), decision chip, evidence link (hover/tap → highlight), reason line; edit states: tap-to-cycle or stepper; teacher-changed marker ("You changed") |
| **Total bar** | Suggested vs chosen total | Shows "AI suggests 2/3" in secondary style; "Your mark 3/3" in primary once changed |
| **Level badge** | AI support level | Four variants; tooltip explains in one sentence |
| **Risk chip + reasons popover** | Why this needs attention | Level text + up to 3 reasons; "More" opens the full list |
| **Verification badges** | Deterministic checks | "Value matches key ✓", "Unit missing ⚠", "Equivalent (CAS) ✓", "Can't verify ?" (neutral, never red) |
| **Reason chips** | One-tap override reasons | Appear only when the teacher's mark ≠ AI; single select; "Other" opens a text field |
| **Action bar** | Confirm and secondary actions | Confirm is always the leftmost primary button (desktop) or full-width at the bottom (phone); secondary in a "More" menu on phone |
| **Queue progress** | Motivation and orientation | "34 left · ~12 min" (estimate from the teacher's own pace) |
| **Banners** | Offline, incidents, masked item, instruction-text detected | Non-blocking except where the decision is blocked |
| **Stepper wizard** | Setup flows | Numbered steps, save-as-draft, back without data loss |
| **Data table** | Rosters, ledgers, audit | Sticky header, column pinning, Bangla collation sort, inline validation cells, export button |
| **Math editor** | Questions, answers | Palette + LaTeX source toggle; live KaTeX preview |
| **Import wizard** | Excel/CSV/PDF | Upload → mapping → preview (Bijoy conversion highlighted) → validation → commit |
| **Toast** | Non-blocking confirmation | "Saved" (1.5 s), "Queued offline" (persistent until synced) |
| **Dialog** | Destructive or scoped actions | Plain-language consequences ("This will update 34 pending suggestions") |

### 4.6 Forms
- Labels above fields; helper text below; inline validation on blur; errors in plain Bangla/English with a fix hint.
- Marks inputs accept Bangla or Latin digits; they validate bounds immediately (e.g., "max 3").
- Bangla input: native keyboards (Avro/Gboard) are supported. Pasting Bijoy text triggers conversion with a toast "Converted from Bijoy".
- Required fields are marked "(required)", not with an asterisk alone.

### 4.7 Tables
- Default row height 44 px (desktop compact 36 px). Zebra striping off; row dividers subtle.
- Numeric columns right-aligned with tabular figures. Absent shows "ABS", never 0.
- Large ledgers use virtualised scrolling. Exports are always available.

### 4.8 Cards and dashboards
- Cards show one state + one action. No decorative charts.
- Charts: horizontal bars for comparisons, lines for trends across exams, small multiples per section. No pies or 3D. Every chart has a table view for accessibility.
- Dashboards lead with **what needs action**, then status, then trends.

---

## 5. Review Interface (the most important screen)

### 5.1 Anatomy
The structure is in `04` SCR-17. The visual order on desktop follows the prompt's required sequence:

`Student answer (left, dominant) → AI interpretation (transcript under the image) → Rubric criteria (right) → AI suggestion per criterion → Evidence (highlight on hover/tap) → Confidence (risk chip + reasons at the top of the right pane) → Reason (one line per criterion) → Teacher decision (criterion controls + action bar)`

### 5.2 Interaction model

| Interaction | Desktop | Phone |
|---|---|---|
| Confirm & next | `Enter` or `Space` | Big bottom button; swipe left = next (only after a decision) |
| Set a criterion | Click chip / number keys 1–9 select criterion, `←/→` change the decision | Tap to cycle |
| Set total directly | `0–9` then `Enter` (applies as total override with reason) | Stepper in "Edit" |
| Edit mode | `E` | "Edit" button |
| Manual mode | `M` | More → Manual |
| Re-evaluate | `R` | More |
| Clarify / alternative | `C` / `A` | More |
| Flag to HoD | `F` | More |
| Undo | `U` / `Ctrl+Z` | Undo toast (5 s) + history |
| Zoom | `+/−`, scroll with modifier | Pinch |
| Toggle transcript | `T` | "Text" tab |
| Previous item | `←` (when no criterion focused) | Swipe right |

- **Auto-advance** after Confirm (≤150 ms). The next item is prefetched (NFR-PERF-01).
- **Undo** is always available for the last 20 actions until the item is locked.

### 5.3 Anti-rubber-stamping design (DEC-33)

| Mechanism | Design |
|---|---|
| Criteria-first reveal | The total bar is rendered in the secondary style and placed below the criteria. On phones, the total appears only after the criteria are scrolled into view (they fit on screen by design). |
| Masked items (5%) | Distinct banner in neutral blue: "Quality check: score this one first." Criteria have no AI chips until submission, then a reveal with "Keep mine" / "Use AI's" and the difference highlighted. |
| Batch confirm (L3 only) | Grid of ≤20 thumbnails with suggested marks. 1 in 10 is forced open. The confirm button activates after all thumbnails have been visible for ≥1 s each (scroll-through). |
| Dwell awareness | If the median active time is <3 s over 50 consecutive items, a gentle nudge appears: "You're moving fast. Remember, you can open the whole page (W)." Never shown to others. |
| High-risk items | No one-key confirm for high risk: `Enter` first expands the reasons panel, a second `Enter` confirms (a two-step pattern on desktop). On phones the confirm button reads "Confirm after checking ⚠". |
| Instruction text detected | Confirm is disabled until the teacher opens the flagged region (it auto-scrolls to it) |

### 5.4 Fatigue and flow
- Progress with an estimate from the teacher's own pace. A break suggestion after 45 minutes of continuous marking (dismissible, off by default per user).
- Session resume: returning users land on the exact next item.
- "Finish later" keeps the lease released and the position stored.

### 5.5 Performance budgets (UX-critical)
- Next item paint ≤1.0 s p95 (4G), ≤2.5 s (3G-class).
- Criterion toggle feedback ≤50 ms.
- Evidence highlight on hover ≤100 ms.
- Image zoom at 60 fps on mid-range Android (tested on the reference device).

---

## 6. AI Explainability Interface

**Goal:** the teacher understands in ≤5 seconds *what* the AI thinks, *where* it looked, and *why*.

| Element | Specification | Never |
|---|---|---|
| Criterion decision | One of four states with marks: "✓ Formula — 1/1" | A single unexplained total |
| Evidence | Tap or hover highlights region(s). The quote appears under the criterion ("“v = u + at” — line 1"). | Evidence not visible on the image |
| Reason | ≤25 words, rubric language, in the UI language: "Correct value 12.5 but no unit; rubric requires unit." | Generic praise ("Good attempt!"), hedging essays, model self-talk |
| Verification badges | Deterministic facts shown separately from AI judgement | Labelling CAS results as "AI" |
| Provenance (on demand) | "Details" drawer: rubric version, clarifications applied, model/pipeline version label (e.g., "Pipeline 2027.05-b"), time | Vendor or model marketing names in the main UI |
| Transcript | Shown with dotted underline on uncertain spans; the original image is always adjacent | Transcript without the image |

**Explanation example** (Physics গ, 3 marks):
> Criterion 1: 1/1. The student writes *v = u + at* (line 1).
> Criterion 2: 1/1. Substitutes u = 2, a = 1.5, t = 7 (line 2).
> Criterion 3: 0/1. The value 12.5 matches the key but the unit is missing. The rubric requires a unit.
> **AI suggests 2/3.**

The explanation is grounded in the student's answer (quotes and regions), the rubric (criteria text), the model answer (key match) and the item's context (marks, cognitive level).

---

## 7. AI Confidence UX

**Decision:** show **attention levels with reasons**, not probabilities (OQ-22 default; 06 §5.3).

| Level | Label (EN / BN) | Visual | Meaning shown to teacher |
|---|---|---|---|
| High | "Check carefully" / "সতর্কভাবে দেখুন" | Brick dot + text | The AI may be wrong here, for the reasons listed |
| Medium | "Worth a look" / "একবার দেখে নিন" | Amber dot + text | Some uncertainty |
| Low | "Looks routine" / "সাধারণ" | Slate-green dot + text | No warning signs found. Still your decision. |

**Reason vocabulary** (fixed set, translated, mapped from risk signals; 06 §5.1):

| Signal | Teacher-facing reason |
|---|---|
| Legibility low / uncertain spans | "Handwriting unclear in part of the answer" |
| Cross-model disagreement | "Two AI readers disagreed" |
| Sample disagreement | "AI was inconsistent on this answer" |
| CAS different / cannot verify | "Maths check found a difference" / "Maths couldn't be checked automatically" |
| Boundary proximity | "Student is near the pass mark / a grade boundary" |
| High item value | "High-mark question" |
| Mapping uncertainty | "Not sure this answer belongs to this question" |
| Crossed-out / multiple attempts | "Crossed-out work nearby" / "More than one attempt" |
| Instruction-like text | "Contains text addressed to the examiner" |
| Unusual method | "Unusual method, not in the rubric's alternatives" |

- **OCR quality:** the legibility class is shown as a small "Handwriting: clear / average / unclear" tag on the answer viewer.
- **Model disagreement:** when two readers disagree, the details drawer shows both criterion decisions side by side ("Reader A: met · Reader B: not met").
- **Low risk ≠ correct:** the tooltip on low risk says "No warning signs found. You are still the marker."

---

## 8. Feedback Interface

| Surface | Design |
|---|---|
| Teacher comment approval (S) | Per student: AI draft comment in an editable box, labelled "Draft — edit or approve". Approve / Edit / Skip. Bulk "Approve all unchanged" is **not** offered. |
| Result slip (PDF/print) | A4 half-page option. Header: school, exam, student, roll. Table: question → sub-parts (ক খ গ ঘ) with marks. Component totals and pass status. Cognitive-level bar ("Knowledge 90% · Comprehension 70% · Application 55% · Higher-order 40%"). Up to 3 teacher comments. Footer: re-check instructions and deadline. |
| Report card | School-branded, bilingual, ledger-consistent. Absent shown as "ABS". |
| Annotated script (S) | Page images with confirmed marks in margin tags and criteria met. No AI wording, only confirmed decisions. |

Tone: constructive and specific. The AI never writes directly to students or parents.

---

## 9. Accessibility

| Area | Requirement |
|---|---|
| Standard | WCAG 2.2 AA (NFR-A11Y-01) |
| Keyboard | Full review without a mouse; visible focus; skip links; logical order |
| Screen readers | Criterion rows announce "Criterion 2, substitutes values, AI: met, 1 of 1 mark"; images have descriptive labels ("Answer image, Question 2 গ, 2 regions"). Note that handwriting images cannot be made fully accessible, so the transcript (when present) is offered. |
| Targets | ≥44×44 px on touch |
| Text scaling | Up to 200% without loss of function; the layout reflows |
| Motion | Respect reduced motion; no flashing |
| Language | `lang="bn"` / `lang="en"` attributes on content for correct voice and shaping |
| Colour | Never colour-only (§4.3) |
| Cognitive | Plain language; consistent placement; confirmation for destructive actions; undo |

---

## 10. Responsive Design and Mobile Considerations

### 10.1 Web on phones (DEC-20)
- The question-wise review card is fully functional on a 360×800 screen (`04` SCR-17m).
- Setup, rubric editing and results are usable on phones but optimised for larger screens. The phone view shows a "Better on a larger screen" hint for rubric authoring and ledgers without blocking.
- Offline review (S): a prefetch indicator ("30 items ready offline").

### 10.2 Capture app (Android)
| Concern | Design |
|---|---|
| One-handed use with a phone stand | Large shutter; auto-capture option; volume-key shutter |
| Feedback without looking at the screen | Haptic + sound cues: success tick, retake buzz; spoken cue optional (Bangla/English) |
| Sunlight/glare | High-contrast capture UI; glare detection message with a hint ("tilt slightly") |
| Low-end devices | ≤150 MB RAM footprint target; no heavy on-device ML beyond barcode + OpenCV checks; storage warning before a session if free space is below the needed capacity (≈ pages × 400 KB × 2) |
| Throughput | Session counter, per-script page count, "next student" flow, optional continuous mode |
| Error recovery | Every capture action is undoable in CAP-03 before upload |
| Privacy | No images in the phone gallery; app PIN; auto-lock |

---

## 11. Content and Microcopy

| Rule | Example |
|---|---|
| Say "AI suggests", never "AI graded" or "AI marked" | "এআই প্রস্তাব: ২/৩" · "AI suggests 2/3" |
| The teacher is the marker | "Your mark" / "আপনার নম্বর" |
| Plain reasons, no jargon | "Two AI readers disagreed", not "ensemble variance high" |
| Consequences before action | "Publishing sends report cards. You can still handle re-checks later." |
| Bangla terminology glossary | Maintained with teacher reviewers: প্রশ্ন (question), উদ্দীপক (stimulus), জ্ঞানমূলক/অনুধাবনমূলক/প্রয়োগমূলক/উচ্চতর দক্ষতা (the four CQ levels), নম্বর (marks), খাতা (script), পুনর্নিরীক্ষণ (re-check), মডারেশন (moderation) |
| Numbers | Marks as "২/৩" or "2/3" per setting; never percentages for single items |
| Errors | What happened + what to do: "Page 4 is blurry. Retake it before moving on." |

---

## 12. UX Metrics and Testing

| Metric | Target (pilot) | Method |
|---|---|---|
| Review time per item (median, L2 items) | Baseline in EXP-05; target ≥30% faster than manual including totalling/entry | Telemetry + time-motion |
| SUS (teachers) | ≥70 | Survey after first exam |
| Task success: create exam + rubric in ≤30 min (first time), ≤10 min (cloned) | ≥90% | Usability test (EXP-09) |
| Capture time per 10-page script | ≤30 s | EXP-04 |
| Override reason entry time | ≤2 s median | Telemetry |
| Masked-item gap | ≤10 points | 06 §6 |
| Trust (post-exam survey: "I felt in control of every mark") | ≥80% agree | Survey |
| Accessibility defects (serious) | 0 | Audit |

**Usability test plan (EXP-09):**
- 12–20 teachers (BM and EV, 2 schools), moderated, in Bangla.
- Tasks: set up an exam from a template; write a rubric for one CQ; review 50 items including masked and high-risk ones; add an alternative; flag an item; complete a script; moderate a sample.
- Measures: time, errors, SUS, trust questions, think-aloud themes.
- Iterate before G1.
