# Contributing to Creators Studio

Contributions are welcome! Here's how to help.

## How to Contribute

1. **Fork** the repository
2. **Create a branch** for your feature or fix
3. **Make your changes** and test them
4. **Submit a pull request** with a clear description

## What to Contribute

- Bug fixes
- New domain modes
- Improved prompt templates
- Documentation improvements
- Post-processing recipes

## Guidelines

- Keep SKILL.md under 500 lines (currently ~170 as lean orchestrator -- add features as reference files, not inline)
- Ensure consistency across all reference files (rate limits, model names, aspect ratios)
- Test as plugin: `claude --plugin-dir .`
- Follow existing markdown formatting conventions
- **After every feature:** Follow the Feature Completion Checklist in CLAUDE.md (version bump, docs, consistency check, SKILL.md size check)

## Reporting Issues

Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
