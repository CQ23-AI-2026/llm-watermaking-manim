import glob

files = glob.glob(r'd:\HK2-3\CSAI\lamvideo\llm-watermaking-manim\scenes\part2\*.py')

old_logic_self = """        elapsed_time = self.renderer.time - start_time
        wait_time = max(0.0, (voice_duration or 0.0) - elapsed_time)
        if wait_time > 0:
            self.wait(wait_time)
        else:
            self.wait(4.0)"""

new_logic_self = """        elapsed_time = self.renderer.time - start_time
        if voice_duration is not None:
            wait_time = max(0.0, voice_duration - elapsed_time)
            if wait_time > 0:
                self.wait(wait_time)
        else:
            self.wait(4.0)"""

old_logic_scene = """    elapsed_time = scene.renderer.time - start_time
    wait_time = max(0.0, (voice_duration or 0.0) - elapsed_time)
    if wait_time > 0:
        scene.wait(wait_time)
    else:
        scene.wait(4.0)"""

new_logic_scene = """    elapsed_time = scene.renderer.time - start_time
    if voice_duration is not None:
        wait_time = max(0.0, voice_duration - elapsed_time)
        if wait_time > 0:
            scene.wait(wait_time)
    else:
        scene.wait(4.0)"""

count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    original_content = content
    if old_logic_self in content:
        content = content.replace(old_logic_self, new_logic_self)
    
    if old_logic_scene in content:
        content = content.replace(old_logic_scene, new_logic_scene)
        
    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print(f"Fixed {f}")
        
print(f"Total fixed: {count}")
