# Contributing to Socratic Math Tutor

Thanks for your interest in contributing.

## Before You Start
- Read the README for setup and project goals.
- Open an issue first for larger changes so we can align on scope.
- Keep changes focused to one feature or fix per pull request.

## Development Setup
1. Fork and clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Start the app locally:
   - `streamlit run app.py`
5. Run tests:
   - `pytest -q`

## Branching and Commits
- Create a branch from main:
  - `feature/short-description` for new features
  - `fix/short-description` for bug fixes
  - `docs/short-description` for documentation updates
- Use clear commit messages in imperative mood.
- Keep commits small and logically grouped.

## Coding Expectations
- Preserve the Socratic tutoring behavior: guide, do not reveal final answers prematurely.
- Add or update tests for behavior changes.
- Update documentation for setup, behavior, or interface changes.
- Avoid unrelated refactoring in feature/fix pull requests.

## Pull Request Checklist
- [ ] I ran tests locally and they pass.
- [ ] I added or updated tests for behavior changes.
- [ ] I updated docs where needed.
- [ ] My pull request is focused on one purpose.
- [ ] I linked related issues.

## Reporting Bugs
Please include:
- Expected behavior
- Actual behavior
- Steps to reproduce
- Logs and screenshots when relevant
- Environment details (OS, Python version)

## Suggesting Features
Please include:
- Problem statement
- Proposed solution
- Alternatives considered
- Impact on current user flow

## Code of Conduct
Participation in this project is governed by the Code of Conduct in CODE_OF_CONDUCT.md.
