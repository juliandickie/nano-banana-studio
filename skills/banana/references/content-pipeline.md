# Content Pipeline Reference

> Load this when the user runs `/banana content` or asks to generate
> a complete content package from a single idea.

## Overview

Orchestrates multiple existing scripts to produce a complete content package from one idea: hero image, social media pack, email headers, format variants, and optionally a slide deck. Uses a two-phase workflow: plan (estimate cost) then generate (execute).

## Usage

```bash
# Create execution plan with cost estimate
python3 ${CLAUDE_SKILL_DIR}/scripts/content_pipeline.py plan --idea "product launch" --outputs hero,social,email,formats --preset tech-saas

# Execute the plan
python3 ${CLAUDE_SKILL_DIR}/scripts/content_pipeline.py generate --plan ~/content_TIMESTAMP/plan.json

# Check status of a running/completed plan
python3 ${CLAUDE_SKILL_DIR}/scripts/content_pipeline.py status --plan ~/content_TIMESTAMP/plan.json
```

## Output Types

| Type | Script Used | API Calls | Description |
|------|-------------|-----------|-------------|
| `hero` | generate.py | 1 | Hero image at 4K, 16:9 |
| `social` | social.py | 3-4 | Top 6 platforms, grouped by ratio |
| `email` | multiformat.py | 0 | Converts from hero (no API call) |
| `formats` | multiformat.py | 0 | PNG/WebP/JPEG at 4K/2K/1K |
| `deck` | slides.py | Variable | Requires separate slide prompts |

## Two-Phase Workflow

### Phase 1: Plan
The `plan` command generates a `plan.json` with:
- Estimated API calls and total cost
- Step-by-step execution order
- Dependencies between steps (email/formats depend on hero)

**Always run plan first** to review cost before committing API calls.

### Phase 2: Generate
The `generate` command executes plan.json step by step:
- Calls existing scripts via subprocess
- Handles dependencies (waits for hero before converting)
- Updates plan.json after each step (can resume from failure)
- Writes manifest.json when complete

## Dependencies

Steps can depend on others:
- `email` and `formats` depend on `hero` (they convert the hero image)
- `social` runs independently (generates its own images)
- If `hero` fails, dependent steps are blocked

## Output Structure

```
~/Documents/nanobanana_generated/content_TIMESTAMP/
    plan.json       # Execution plan with status per step
    manifest.json   # Final manifest of all outputs
    hero/           # Hero image
    social/         # Platform-specific images
    email/          # Email header variants
    formats/        # Multi-format pack
```

## Cost Estimation

The plan shows estimated cost before any API calls are made. Cost is based on the pricing table in `references/cost-tracking.md`.

Example: `hero` (4K) + `social` (4 API calls at 4K) = ~$0.78 total.
`email` and `formats` are free (just format conversion from hero).
