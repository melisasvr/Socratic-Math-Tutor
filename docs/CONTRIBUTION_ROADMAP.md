# Contribution Roadmap

This document contains ready-to-create issue drafts with clear scope, acceptance criteria, labels, and rough effort.

## Recommended Implementation Order

1. Unit tests baseline
2. Progress tracker across sessions
3. Multi-language support
4. More math topics
5. UI themes and polish

## Issue 1: Test Baseline for Core Tutor Flow

- Type: enhancement
- Priority: high
- Labels: testing, good first issue, infra
- Estimated effort: 1-2 days

### Goal
Add a reliable unit test baseline so future feature work does not break core behavior.

### Scope
- Set up `pytest` and `pytest-mock`.
- Add tests for helper functions (for example question extraction).
- Add tests for state transitions in the tutoring flow.
- Mock LLM calls in tests to avoid network dependency.

### Acceptance Criteria
- `pytest` runs successfully from project root.
- At least 8 meaningful unit tests are added.
- Tests cover happy-path and at least one error/edge case per tested module.
- No real API calls are made during tests.

### Out of Scope
- Full end-to-end browser testing.
- Snapshot or visual regression testing.

---

## Issue 2: Progress Tracker Across Sessions

- Type: feature
- Priority: high
- Labels: feature, backend, analytics
- Estimated effort: 2-3 days

### Goal
Persist learner progress so users can see improvement over time.

### Scope
- Add storage layer (start with SQLite).
- Save per-session summary: timestamp, topic, solved/not solved, total interactions.
- Show sidebar stats: total solved, current streak, last 7 days activity.
- Add simple topic-wise progress summary.

### Acceptance Criteria
- Progress data remains available after app restart.
- Sidebar shows at least 3 persistent metrics.
- New problem attempts update stats correctly.
- App handles missing or first-run database gracefully.

### Out of Scope
- User authentication and multi-user accounts.
- Cloud database hosting.

---

## Issue 3: Multi-Language Support (i18n)

- Type: feature
- Priority: medium
- Labels: feature, i18n, ui
- Estimated effort: 2-4 days

### Goal
Allow students to use the tutor in multiple languages.

### Scope
- Add language selector in sidebar.
- Create translation dictionary for static UI text.
- Create language-specific system prompts.
- Persist selected language in session state.
- Start with English, Hindi, and Spanish.

### Acceptance Criteria
- User can switch language without app crash.
- Key UI text and tutor system prompts reflect selected language.
- New and existing sessions default predictably (for example English fallback).
- Missing translation keys fall back to English.

### Out of Scope
- Automatic language detection from uploaded image.
- RTL layout support.

---

## Issue 4: Add Topic Packs (Linear Algebra, Statistics, Number Theory)

- Type: feature
- Priority: medium
- Labels: feature, prompts, education
- Estimated effort: 3-5 days

### Goal
Improve tutoring quality by using topic-aware instruction strategies.

### Scope
- Add topic routing with at least 5 categories.
- Add topic-specific guidance prompts for:
  - Linear algebra
  - Statistics
  - Number theory
- Add fallback to generic math tutor prompt when topic is unclear.

### Acceptance Criteria
- Topic selection or detection chooses a prompt strategy consistently.
- Topic prompts keep Socratic behavior (one small question at a time).
- Tutor does not regress on existing algebra/calculus flows.
- README is updated with supported topic list.

### Out of Scope
- OCR-based automatic classification from images.
- Symbolic algebra solver integration.

---

## Issue 5: Theme System and UI Polish

- Type: enhancement
- Priority: medium
- Labels: ui, design, enhancement
- Estimated effort: 2-3 days

### Goal
Improve readability and engagement with selectable themes and clearer visual hierarchy.

### Scope
- Add 3 theme presets (for example Classic, High Contrast, Minimal).
- Add clearer step progress indicator.
- Improve mobile spacing and button sizing.
- Keep existing app flow and controls unchanged.

### Acceptance Criteria
- Theme can be changed from sidebar.
- All major UI components update according to selected theme.
- Layout remains usable on desktop and mobile widths.
- Contrast is readable in all themes.

### Out of Scope
- Full redesign of interaction model.
- Animation-heavy UI effects.

---

## Suggested Milestones

- Milestone 1: Quality Foundation
  - Issue 1
- Milestone 2: Learner Retention
  - Issue 2
- Milestone 3: Accessibility and Reach
  - Issue 3
- Milestone 4: Academic Depth
  - Issue 4
- Milestone 5: Experience Polish
  - Issue 5

## Definition of Done (Common)

- Code follows current project style and structure.
- README/docs updated where behavior changes.
- No new lint/type/syntax errors.
- Manual smoke test completed with at least one sample math problem.
