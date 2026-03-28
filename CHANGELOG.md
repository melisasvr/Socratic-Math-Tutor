# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]
### Added
- Professional repository governance files and contribution templates.
- Mistake Pattern Detection feature with rule-based classification for common learner errors (for example: sign, arithmetic, algebra-step, formula, unit, and fraction/decimal mistakes).

### Changed
- Added a standardized CONTRIBUTING.md while keeping legacy contribute.md.
- Progress persistence now stores per-attempt mistake tags and exposes aggregated `common_mistakes` analytics.
- Sidebar now displays top common mistakes to help learners identify recurring error patterns.

### Tests
- Added unit tests for the mistake detection module.
- Extended progress tests to validate common-mistake aggregation.

### Security
- Added baseline vulnerability reporting guidance.
