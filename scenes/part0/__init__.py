from manim import Scene

from scenes.part0.init import InitScene, play_part0_init
from scenes.part0.risks import RisksScene, play_part0_risks
from scenes.part0.detection import DetectionScene, play_part0_detection


__all__ = [
    "InitScene", "RisksScene", "DetectionScene", "Part0",
    "play_part0_init", "play_part0_risks", "play_part0_detection"
]


class Part0(Scene):
    def construct(self):
        play_part0_init(self)
        play_part0_risks(self)
        play_part0_detection(self)

