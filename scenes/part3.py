from manim import *
from config.style import VGText

class Part3(Scene):
    def construct(self):
        text = VGText("This is Part 3")
        self.play(Write(text))
        self.wait(2)
