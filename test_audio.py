import os
from scenes.part1.scene_1_1 import _get_audio_duration

current_dir = os.path.join(os.getcwd(), "scenes", "part1")
voice_path = os.path.join(current_dir, "voice", "1_1.mp3")

print("Checking path:", voice_path)
print("Exists?", os.path.exists(voice_path))
duration = _get_audio_duration(voice_path)
print("Duration:", duration)
