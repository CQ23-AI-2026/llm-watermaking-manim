

# LLM Watermarking Manim

LLM Watermarking Manim is a mathematical animation project visualizing watermarking algorithms for Large Language Models (LLMs). Using the Manim framework and inspired by 3Blue1Brown, it dynamically simulates embedding mechanisms (Green-Red, Gumbel) into probability distributions and statistical frameworks for AI text detection.

# Minimal Manim Project Structure

## Structure

- `config/` — Shared style (font size, color, font family, weight, slant)
- `scenes/` — Main animation scenes (each part = 1 file)

## How to create a new part

1. In `scenes/`, create a new file (e.g. `part4.py`).
2. Import style from `config/style.py`:
   from config.style import VGText, VG_GREEN, VG_RED, VG_BLUE, VG_ORANGE, VG_PURPLE, VG_GRAY, LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT
3. Use VGText and the config variables for all text (do not hardcode style).
4. Import your new scene class into `main.py` if you want to render it via main.py:
   from scenes.part4 import Part4

## How to run


1. Install manim:
    ```
    pip install manim
    ```
2. Render a part (example):
    - **macOS/Linux:**
       ```
       PYTHONPATH=. manim -pql scenes/part1.py Part1
       ```
    - **Windows (PowerShell):**
       ```
       $env:PYTHONPATH="."; manim -pql scenes/part1.py Part1
       ```

### Render in 1080p or 2K

To render in higher resolution, use one of the following commands:

- **1080p (high quality):**
   - macOS/Linux:
      ```
      PYTHONPATH=. manim -pqh scenes/part1.py Part1
      ```
   - Windows (PowerShell):
      ```
      $env:PYTHONPATH="."; manim -pqh scenes/part1.py Part1
      ```

- **2K (2560x1440):**
   - macOS/Linux:
      ```
      PYTHONPATH=. manim --resolution=2560,1440 scenes/part1.py Part1
      ```
   - Windows (PowerShell):
      ```
      $env:PYTHONPATH="."; manim --resolution=2560,1440 scenes/part1.py Part1
      ```

Output videos will be in `media/videos/` by default.
