import os
import subprocess
import shutil

def mix():
    with open("audio_times.txt", "r") as f:
        lines = f.read().splitlines()

    inputs = []
    filter_complex = ""
    for i, line in enumerate(lines):
        if not line.strip(): continue
        path, time_str = line.split("|")
        time_ms = int(float(time_str) * 1000)
        inputs.append(f"-i \"{path}\"")
        filter_complex += f"[{i+1}:a]adelay={time_ms}|{time_ms}[a{i}]; "

    # Combine all delayed audios
    num_inputs = len(inputs)
    filter_complex += "".join([f"[a{i}]" for i in range(num_inputs)])
    # normalize=0 prevents volume dropping when mixing
    filter_complex += f"amix=inputs={num_inputs}:duration=longest:dropout_transition=0:normalize=0[outa]"

    import sys
    part_dir = sys.argv[1] if len(sys.argv) > 1 else "part1"
    resolution = sys.argv[2] if len(sys.argv) > 2 else "1080p60"
    part_name = sys.argv[3] if len(sys.argv) > 3 else "Part1"

    input_video = os.path.join("media", "videos", part_dir, resolution, f"{part_name}.mp4")
    output_video = os.path.join("media", "videos", part_dir, resolution, f"{part_name}_Fixed.mp4")

    cmd = f"ffmpeg -y -i \"{input_video}\" {' '.join(inputs)} -filter_complex \"{filter_complex}\" -map 0:v -map \"[outa]\" -c:v copy -c:a aac -b:a 192k \"{output_video}\""
    
    print("Running FFmpeg...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("Success! Replacing original video...")
        shutil.move(output_video, input_video)
        print("Done!")
    else:
        print("Error:")
        print(res.stderr)

if __name__ == "__main__":
    mix()
