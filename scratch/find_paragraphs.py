import os

root_dir = r"d:\Year3_Semester2\CoSoAI\Project Manim\llm-watermaking-manim"
scenes_dir = os.path.join(root_dir, "scenes")

results = []

for root, dirs, files in os.walk(scenes_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "Paragraph(" in content:
                    lines = content.splitlines()
                    for idx, line in enumerate(lines):
                        if "Paragraph(" in line:
                            results.append(f"{os.path.relpath(path, root_dir)}:L{idx+1} - {line.strip()}")
            except Exception as e:
                results.append(f"Error reading {path}: {e}")

with open(os.path.join(root_dir, "scratch", "paragraphs.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(results))
print("Done! Found", len(results), "matches.")
