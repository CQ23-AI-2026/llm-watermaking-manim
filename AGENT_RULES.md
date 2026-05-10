# Agent Coding Rules for This Project

1. Always use text style, color, font size, weight, and slant from config/style.py (import VGText, VG_GREEN, etc.).
2. Do not hardcode any color, font size, or font family in scenes; always use config variables.
3. When creating new text, always use VGText instead of Text.
4. If new style attributes are needed, add them to config/style.py first, then use them in scenes.
5. All scenes must be independent Python files in scenes/ and import style from config/.
6. When updating or refactoring, keep style logic centralized in config/style.py.
