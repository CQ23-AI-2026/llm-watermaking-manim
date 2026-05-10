from manim import *

class Part3(Scene):
    def construct(self):
        text = Text("This is Part 3")
        self.play(Write(text))
        self.wait(2)
