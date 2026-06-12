import os

for s in ["1_1", "1_2", "1_3", "1_4"]:
    try:
        mod = __import__(f"scenes.part1.scene_{s}", fromlist=["_get_audio_duration"])
        _get = mod._get_audio_duration
        current_dir = os.path.join(os.getcwd(), "scenes", "part1")
        path = os.path.join(current_dir, "voice", f"{s}.mp3")
        dur = _get(path)
        print(f"{s}: DUR={dur}")
    except Exception as e:
        print(f"{s} ERROR: {e}")
