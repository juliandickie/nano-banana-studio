# Reverse Prompt Engineering Reference

> Load this when the user runs `/banana reverse` or asks to analyze an image
> and extract a prompt that would recreate it.

## Overview

Reverse prompt engineering takes an existing image and decomposes it into a
structured prompt using the 5-Component Formula. This teaches prompt engineering
by example and enables style recreation across multiple generations.

## How to Analyze an Image

When the user provides an image (file path or upload), analyze it systematically:

### Step 1: Identify the Domain Mode

Look at the image and determine which domain mode best describes it:
Cinema, Product, Portrait, Editorial, UI/Web, Logo, Landscape, Abstract,
Infographic, or Presentation.

### Step 2: Decompose Using the 5-Component Formula

Extract each component from what you observe:

| Component | What to Extract | Weight |
|-----------|----------------|--------|
| **Subject** (30%) | Who/what is the primary focus? Age, appearance, material, species, physical details. | Most important — be specific |
| **Action** (10%) | What is the subject doing? Pose, gesture, movement, state. | Use present-tense verbs |
| **Location** (15%) | Where is the scene? Time of day, weather, atmosphere, environmental details. | Include mood-setting details |
| **Composition** (10%) | Camera perspective, framing, angle, focal length, depth of field. | Estimate the lens and f-stop |
| **Style** (25%) | Visual register, medium, lighting setup, color grading, publication-level reference. | Include prestigious context anchor |

### Step 3: Identify Technical Details

- **Camera/lens estimate:** "Looks like an 85mm f/1.4 based on the depth of field and compression"
- **Lighting setup:** "Key light from upper-left, soft fill from right, rim light behind"
- **Color grading:** "Warm tones, slightly desaturated, lifted shadows"
- **Aspect ratio:** Measure or estimate (16:9, 4:5, 1:1, etc.)

### Step 4: Construct the Prompt

Write the prompt as natural narrative prose following the 5-Component Formula.
Include a prestigious context anchor if appropriate ("Vanity Fair editorial,"
"National Geographic cover," "Apple product photography").

Apply the same rules as regular prompt construction:
- NEVER use banned keywords ("8K", "masterpiece", "ultra-realistic")
- Use specific camera names and lens specs
- Include micro-details (textures, reflections, atmospheric elements)
- Describe what you SEE, not what it MEANS

## Output Format

Present the analysis to the user as:

```
## Reverse Prompt Analysis

**Domain Mode:** [mode]
**Estimated Aspect Ratio:** [ratio]
**Estimated Resolution:** [resolution recommendation]

### 5-Component Breakdown

| Component | Extracted |
|-----------|----------|
| **Subject** | [detailed description] |
| **Action** | [pose/state] |
| **Location** | [setting/context] |
| **Composition** | [camera/framing] |
| **Style** | [lighting/aesthetic/anchor] |

### Reconstructed Prompt

[The full prompt as a single narrative paragraph, ready to copy and use]

### Settings

- **Aspect ratio:** [ratio]
- **Resolution:** [recommendation]
- **Model:** gemini-3.1-flash-image-preview
- **Domain mode:** [mode]
```

## Tips

- **Be more specific than the original** — the model needs detail to recreate,
  even if the original was generated from a simpler prompt
- **Estimate camera specs confidently** — "Shot on Canon EOS R5, 85mm f/1.4"
  gives the model concrete depth-of-field information even if you're guessing
- **Include a prestigious anchor** — "Vanity Fair editorial portrait" or
  "Bon Appetit food photography" actively improves output quality
- **For illustrated/stylized images** — describe the art style, line weight,
  color palette, and shading technique rather than camera specs
- **The reconstructed prompt should be longer than the original** — good
  reverse engineering adds detail the original prompt may have omitted
