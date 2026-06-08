import os
import unicodedata

root_dir = r"d:\Year3_Semester2\CoSoAI\Project Manim\llm-watermaking-manim"
scenes_dir = os.path.join(root_dir, "scenes")

nfc_so = unicodedata.normalize("NFC", "sở")
nfd_so = unicodedata.normalize("NFD", "sở")

results = []

for root, dirs, files in os.walk(scenes_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                normalized_content = unicodedata.normalize("NFC", content)
                if nfc_so in normalized_content:
                    lines = content.splitlines()
                    for idx, line in enumerate(lines):
                        norm_line = unicodedata.normalize("NFC", line)
                        if nfc_so in norm_line:
                            results.append(f"{os.path.relpath(path, root_dir)}:L{idx+1} - {line.strip()}")
            except Exception as e:
                results.append(f"Error reading {path}: {e}")

with open(os.path.join(root_dir, "scratch", "results.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(results))
print("Done! Found", len(results), "matches.")
