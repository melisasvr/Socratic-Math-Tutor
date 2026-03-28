# ARCHITECTURE

This file documents the high-level ARCHITECTURE of Socratic Math Tutor.

## Goal
Provide step-by-step, Socratic math help without directly revealing final answers.

## High-Level Components
- `app.py`: Streamlit entrypoint.
- `src/socratic_tutor/ui.py`: UI rendering and interaction flow.
- `src/socratic_tutor/llm.py`: LLM calls (Groq/OpenAI-compatible).
- `src/socratic_tutor/prompts.py`: Prompt templates and tutoring behavior rules.
- `src/socratic_tutor/topics.py`: Topic detection and topic-specific guidance.
- `src/socratic_tutor/i18n.py`: Multi-language strings.
- `src/socratic_tutor/progress.py`: Session and persistence for learning progress.
- `src/socratic_tutor/themes.py`: UI theme presets and style generation.
- `src/socratic_tutor/helpers.py`: Shared utility functions.
- `src/socratic_tutor/config.py`: Environment and runtime configuration.

## Request/Response Flow
1. Student enters or uploads a problem.
2. App asks confidence/intention (yes/no starting point).
3. Prompt builder creates strict Socratic guidance instructions.
4. LLM generates one-step guidance and a next question.
5. UI collects learner response and repeats until completion.
6. Progress metrics are updated and displayed.

## Design Principles
- Never give away complete answers by default.
- Ask one question at a time.
- Keep responses short, supportive, and actionable.
- Keep state explicit so the tutor remains predictable.

## Testing Strategy
- Unit tests in `tests/` cover helpers, progress logic, and topic behavior.
- `pytest -q` is used for local validation.

## Future Extensions
- More topic modules.
- Better OCR for handwritten uploads.
- Optional teacher dashboard and analytics.
