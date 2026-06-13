import os
from moviepy.editor import VideoFileClip

video_path = os.path.join("media", "videos", "part1", "1080p60", "Part1.mp4")
if os.path.exists(video_path):
    with VideoFileClip(video_path) as clip:
        print("VIDEO DURATION:", clip.duration)
        if clip.audio:
            print("AUDIO DURATION:", clip.audio.duration)
        else:
            print("NO AUDIO TRACK IN VIDEO")
else:
    print("VIDEO NOT FOUND")
