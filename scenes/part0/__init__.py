from manim import Scene

from .init import InitScene, play_part0_init
from .risks import RisksScene, play_part0_risks

__all__ = ["InitScene", "RisksScene", "Part0", "play_part0_init", "play_part0_risks"]


class Part0(Scene):
    def construct(self):
        play_part0_init(self)
        play_part0_risks(self)
