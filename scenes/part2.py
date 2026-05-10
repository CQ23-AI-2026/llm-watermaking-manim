
from manim import *
from config.style import VGText, VG_BLUE

class Part2(Scene):
    def construct(self):
        from config.style import VG_GREEN, VG_RED, VG_BLUE, VG_ORANGE, VG_PURPLE, VG_GRAY, LARGE_FONT_SIZE, SMALL_FONT_SIZE, BOLD_WEIGHT, ITALIC
        title = VGText("This is Part 2", color=VG_BLUE, font_size=LARGE_FONT_SIZE, weight=BOLD_WEIGHT)
        subtitle = VGText("Demo: Shared style config", color=VG_GREEN)
        highlight = VGText("Font size & color from config!", color=VG_ORANGE, font_size=SMALL_FONT_SIZE, slant="ITALIC")
        extra = VGText("Red text", color=VG_RED).next_to(highlight, DOWN)
        extra2 = VGText("Purple bold", color=VG_PURPLE, weight=BOLD_WEIGHT).next_to(extra, DOWN)
        extra3 = VGText("Gray italic", color=VG_GRAY, slant="ITALIC").next_to(extra2, DOWN)
        subtitle.next_to(title, DOWN)
        highlight.next_to(subtitle, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.play(FadeIn(highlight))
        self.play(FadeIn(extra))
        self.play(FadeIn(extra2))
        self.play(FadeIn(extra3))
        self.wait(2)
