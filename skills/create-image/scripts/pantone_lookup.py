#!/usr/bin/env python3
"""
Pantone color lookup and conversion utility for brand book generation.

Provides hex/RGB/CMYK conversion and nearest Pantone Coated color matching
via Euclidean distance in RGB space. Stdlib-only, no external dependencies.

Usage:
    python pantone_lookup.py --hex "#C8102E"
    python pantone_lookup.py --hex "#2563EB"
"""

import argparse
import math
import json
import sys

# ---------------------------------------------------------------------------
# Pantone Coated reference palette (~200 colors)
# Format: "Pantone NNN C" -> "#RRGGBB"
# ---------------------------------------------------------------------------

PANTONE_COLORS: dict[str, str] = {
    # ── Reds / Pinks (25) ──────────────────────────────────────────────
    "Pantone 186 C": "#C8102E",
    "Pantone 185 C": "#E4002B",
    "Pantone 199 C": "#D50032",
    "Pantone 200 C": "#BA0C2F",
    "Pantone 201 C": "#9B2335",
    "Pantone 187 C": "#A6192E",
    "Pantone 188 C": "#7C2128",
    "Pantone 1788 C": "#EF3340",
    "Pantone 1795 C": "#D22630",
    "Pantone 1797 C": "#CB333B",
    "Pantone 1807 C": "#A4343A",
    "Pantone 032 C": "#EF3340",
    "Pantone 485 C": "#DA291C",
    "Pantone 484 C": "#9A3324",
    "Pantone 483 C": "#653024",
    "Pantone 7621 C": "#AB2328",
    "Pantone 7627 C": "#893C47",
    "Pantone 7622 C": "#93272C",
    "Pantone 7423 C": "#B52555",
    "Pantone 7424 C": "#D5477B",
    "Pantone 182 C": "#F5A6C8",
    "Pantone 183 C": "#F28EB1",
    "Pantone 184 C": "#F0598E",
    "Pantone 219 C": "#DA1984",
    "Pantone 226 C": "#D0006F",

    # ── Blues (25) ─────────────────────────────────────────────────────
    "Pantone 286 C": "#0032A0",
    "Pantone 287 C": "#003087",
    "Pantone 288 C": "#002D72",
    "Pantone 289 C": "#0C2340",
    "Pantone 072 C": "#10069F",
    "Pantone 285 C": "#0076CE",
    "Pantone 284 C": "#6CACE4",
    "Pantone 283 C": "#92C1E9",
    "Pantone 290 C": "#BDD6E6",
    "Pantone 291 C": "#A4D3EE",
    "Pantone 300 C": "#005EB8",
    "Pantone 301 C": "#004B87",
    "Pantone 302 C": "#003D6B",
    "Pantone 306 C": "#00B5E2",
    "Pantone 3005 C": "#0077C8",
    "Pantone 2925 C": "#009CDE",
    "Pantone 2935 C": "#003DA5",
    "Pantone 2945 C": "#00487C",
    "Pantone 2955 C": "#002E5D",
    "Pantone 7462 C": "#00558C",
    "Pantone 7468 C": "#006298",
    "Pantone 7689 C": "#4298B5",
    "Pantone 7451 C": "#71B2E4",
    "Pantone 542 C": "#6BAADB",
    "Pantone Process Blue C": "#0085CA",

    # ── Greens (22) ────────────────────────────────────────────────────
    "Pantone 348 C": "#00843D",
    "Pantone 349 C": "#006938",
    "Pantone 350 C": "#2C5234",
    "Pantone 347 C": "#009A44",
    "Pantone 346 C": "#71CC98",
    "Pantone 345 C": "#8FDA8D",
    "Pantone 339 C": "#00B388",
    "Pantone 340 C": "#00965E",
    "Pantone 341 C": "#007A53",
    "Pantone 342 C": "#005C3F",
    "Pantone 3435 C": "#003B2C",
    "Pantone 356 C": "#007A33",
    "Pantone 357 C": "#215732",
    "Pantone 355 C": "#009639",
    "Pantone 354 C": "#00B140",
    "Pantone 361 C": "#43B02A",
    "Pantone 360 C": "#6CC24A",
    "Pantone 7737 C": "#6BA539",
    "Pantone 7738 C": "#4C8C2B",
    "Pantone 7739 C": "#3D7D2F",
    "Pantone 375 C": "#97D700",
    "Pantone 376 C": "#7AB800",

    # ── Yellows / Oranges (18) ─────────────────────────────────────────
    "Pantone Yellow C": "#FEDD00",
    "Pantone 107 C": "#FBE122",
    "Pantone 108 C": "#FEDB00",
    "Pantone 109 C": "#FFD100",
    "Pantone 116 C": "#FFCD00",
    "Pantone 123 C": "#FFC72C",
    "Pantone 130 C": "#F2A900",
    "Pantone 137 C": "#FFA300",
    "Pantone 144 C": "#ED8B00",
    "Pantone 151 C": "#FF8200",
    "Pantone 158 C": "#E87722",
    "Pantone 165 C": "#FF671F",
    "Pantone 021 C": "#FE5000",
    "Pantone 1505 C": "#FF6900",
    "Pantone 7408 C": "#F2A900",
    "Pantone 7409 C": "#EEB33B",
    "Pantone 7548 C": "#FFC600",
    "Pantone 7549 C": "#FFB81C",

    # ── Purples / Violets (17) ─────────────────────────────────────────
    "Pantone 2685 C": "#56008A",
    "Pantone 2665 C": "#7F57B8",
    "Pantone 2645 C": "#A788C7",
    "Pantone 2635 C": "#C4A6D1",
    "Pantone 2627 C": "#401E6C",
    "Pantone 267 C": "#5E2D91",
    "Pantone 268 C": "#512D6D",
    "Pantone 269 C": "#442359",
    "Pantone 266 C": "#753BBD",
    "Pantone 265 C": "#9B7DD4",
    "Pantone 2587 C": "#8246AF",
    "Pantone 2592 C": "#9B26B6",
    "Pantone 2603 C": "#702F8A",
    "Pantone 2612 C": "#6B3077",
    "Pantone 2593 C": "#903F97",
    "Pantone 2583 C": "#A15BA5",
    "Pantone 513 C": "#B44D97",

    # ── Neutrals: Grays, Beiges, Browns (25) ───────────────────────────
    "Pantone Warm Gray 1 C": "#D7D2CB",
    "Pantone Warm Gray 2 C": "#CBC4BC",
    "Pantone Warm Gray 3 C": "#BFB8AF",
    "Pantone Warm Gray 4 C": "#B6ADA5",
    "Pantone Warm Gray 5 C": "#ACA39A",
    "Pantone Warm Gray 6 C": "#A59C94",
    "Pantone Warm Gray 7 C": "#968C83",
    "Pantone Warm Gray 8 C": "#8C8279",
    "Pantone Warm Gray 9 C": "#83786F",
    "Pantone Warm Gray 10 C": "#796E65",
    "Pantone Warm Gray 11 C": "#6E6259",
    "Pantone Cool Gray 1 C": "#D9D9D6",
    "Pantone Cool Gray 3 C": "#C8C9C7",
    "Pantone Cool Gray 5 C": "#B1B3B3",
    "Pantone Cool Gray 7 C": "#97999B",
    "Pantone Cool Gray 9 C": "#75787B",
    "Pantone Cool Gray 11 C": "#53565A",
    "Pantone 7527 C": "#D6D2C4",
    "Pantone 7528 C": "#C4B9A4",
    "Pantone 7530 C": "#ADA294",
    "Pantone 7531 C": "#8B7E74",
    "Pantone 4625 C": "#4F2C1D",
    "Pantone 4695 C": "#5E3929",
    "Pantone 7596 C": "#BCA58D",
    "Pantone 476 C": "#4E3524",

    # ── Blacks and Near-Blacks (12) ────────────────────────────────────
    "Pantone Black C": "#2D2926",
    "Pantone Black 2 C": "#332F21",
    "Pantone Black 3 C": "#212721",
    "Pantone Black 4 C": "#31261D",
    "Pantone Black 5 C": "#3E2B2E",
    "Pantone Black 6 C": "#101820",
    "Pantone Black 7 C": "#3D3935",
    "Pantone 419 C": "#212322",
    "Pantone 426 C": "#25282A",
    "Pantone 433 C": "#1D252D",
    "Pantone 532 C": "#1C2541",
    "Pantone 539 C": "#002F47",

    # ── Whites and Near-Whites (12) ────────────────────────────────────
    "Pantone White C": "#FFFFFF",
    "Pantone 7541 C": "#D9E1E2",
    "Pantone 663 C": "#E8D3E1",
    "Pantone 656 C": "#DDE5ED",
    "Pantone 7485 C": "#D2E6C8",
    "Pantone 7527 C (Light)": "#E2DDD5",
    "Pantone 7534 C": "#D5CDB6",
    "Pantone 000 C": "#F7F3E8",
    "Pantone 7499 C": "#F2E6C2",
    "Pantone 7500 C": "#E4D5B7",
    "Pantone 705 C": "#F5E1DB",
    "Pantone 607 C": "#F2EDD7",
}


# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hex color string to an (R, G, B) tuple.

    Accepts formats: '#RRGGBB', 'RRGGBB', '#RGB'.
    """
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    if len(h) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_cmyk(r: int, g: int, b: int) -> tuple[int, int, int, int]:
    """Approximate RGB to CMYK conversion.

    Returns (C, M, Y, K) as integer percentages 0-100.
    """
    if (r, g, b) == (0, 0, 0):
        return (0, 0, 0, 100)

    c = 1.0 - r / 255.0
    m = 1.0 - g / 255.0
    y = 1.0 - b / 255.0
    k = min(c, m, y)

    if k == 1.0:
        return (0, 0, 0, 100)

    c = (c - k) / (1.0 - k)
    m = (m - k) / (1.0 - k)
    y = (y - k) / (1.0 - k)

    return (round(c * 100), round(m * 100), round(y * 100), round(k * 100))


def _color_distance(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> float:
    """Euclidean distance between two RGB colors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))


def hex_to_nearest_pantone(hex_color: str) -> dict:
    """Find the nearest Pantone Coated color by Euclidean RGB distance.

    Returns:
        {"name": "Pantone 186 C", "hex": "#C8102E", "distance": 12.5}
    """
    target = hex_to_rgb(hex_color)
    best_name = ""
    best_hex = ""
    best_dist = float("inf")

    for name, p_hex in PANTONE_COLORS.items():
        p_rgb = hex_to_rgb(p_hex)
        dist = _color_distance(target, p_rgb)
        if dist < best_dist:
            best_dist = dist
            best_name = name
            best_hex = p_hex

    return {
        "name": best_name,
        "hex": best_hex,
        "distance": round(best_dist, 2),
    }


def get_color_specs(hex_color: str) -> dict:
    """Return full color specifications for a hex color.

    Returns:
        {
            "hex": "#C8102E",
            "rgb": (200, 16, 46),
            "cmyk": (0, 92, 77, 22),
            "pantone": "Pantone 186 C"
        }
    """
    r, g, b = hex_to_rgb(hex_color)
    cmyk = rgb_to_cmyk(r, g, b)
    nearest = hex_to_nearest_pantone(hex_color)

    return {
        "hex": hex_color.upper() if hex_color.startswith("#") else f"#{hex_color.upper()}",
        "rgb": (r, g, b),
        "cmyk": cmyk,
        "pantone": nearest["name"],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pantone color lookup and conversion utility.",
    )
    parser.add_argument(
        "--hex",
        required=True,
        help='Hex color to look up, e.g. "#C8102E" or "2563EB".',
    )
    args = parser.parse_args()

    hex_input = args.hex.strip().strip("'\"")
    if not hex_input.startswith("#"):
        hex_input = f"#{hex_input}"

    specs = get_color_specs(hex_input)
    nearest = hex_to_nearest_pantone(hex_input)

    print(f"Color Specifications for {specs['hex']}")
    print(f"  RGB:     {specs['rgb']}")
    print(f"  CMYK:    {specs['cmyk']}")
    print(f"  Pantone: {specs['pantone']}")
    print(f"  Nearest Pantone Distance: {nearest['distance']}")
    print()
    print("JSON output:")
    output = {
        "hex": specs["hex"],
        "rgb": list(specs["rgb"]),
        "cmyk": list(specs["cmyk"]),
        "pantone": {
            "name": nearest["name"],
            "hex": nearest["hex"],
            "distance": nearest["distance"],
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
