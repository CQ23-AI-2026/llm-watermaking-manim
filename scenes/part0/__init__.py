from manim import Scene

from .init import InitScene, play_part0_init

__all__ = ["InitScene", "Part0", "play_part0_init"]


class Part0(Scene):
    def construct(self):
        play_part0_init(self)
