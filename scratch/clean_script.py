import os

file_path = r"d:\Year3_Semester2\CoSoAI\Project Manim\llm-watermaking-manim\scenes\part3\extraction_defense_script.md"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

cleaned_lines = []
for idx, line in enumerate(lines):
    stripped = line.strip()
    if stripped == "":
        # Keep empty lines only if they surround headings (starts with ##) or dividers (starts with ---)
        prev_is_special = False
        next_is_special = False
        
        if idx > 0:
            prev_stripped = lines[idx-1].strip()
            if prev_stripped.startswith("##") or prev_stripped.startswith("---"):
                prev_is_special = True
                
        if idx < len(lines) - 1:
            next_stripped = lines[idx+1].strip()
            if next_stripped.startswith("##") or next_stripped.startswith("---"):
                next_is_special = True
                
        if prev_is_special or next_is_special:
            cleaned_lines.append("\n")
    else:
        cleaned_lines.append(line)

# Join and write back
cleaned_content = "".join(cleaned_lines)

# Remove consecutive blank lines
import re
cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(cleaned_content)

print("Done cleaning extraction_defense_script.md!")
