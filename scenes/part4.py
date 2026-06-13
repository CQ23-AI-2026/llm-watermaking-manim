from manim import Scene

from scenes.part4.scene_4_1_intro import play_scene_4_1
from scenes.part4.scene_4_2_stats import play_scene_4_2
from scenes.part4.scene_4_3_detectgpt import play_scene_4_3
from scenes.part4.scene_4_4_radar import play_scene_4_4
from scenes.part4.scene_4_5_bias import play_scene_4_5


class Part4(Scene):
    def construct(self):
        play_scene_4_1(self)
        self.wait(0.5)
        self.clear()

        play_scene_4_2(self)
        self.wait(0.5)
        self.clear()

        play_scene_4_3(self)
        self.wait(0.5)
        self.clear()

        play_scene_4_4(self)
        self.wait(0.5)
        self.clear()

        play_scene_4_5(self)
        self.wait(0.5)
