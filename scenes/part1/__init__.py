from manim import Scene

from .scene_1_1 import play_part1_scene_1_1
from .scene_1_2 import play_part1_scene_1_2
from .scene_1_3 import play_part1_scene_1_3
from .scene_1_4 import play_part1_scene_1_4

__all__ = [
    "Part1",
    "play_part1_scene_1_1",
    "play_part1_scene_1_2",
    "play_part1_scene_1_3",
    "play_part1_scene_1_4",
]


class Part1(Scene):
    def construct(self):
        play_part1_scene_1_1(self)
        play_part1_scene_1_2(self)
        play_part1_scene_1_3(self)
        play_part1_scene_1_4(self)
