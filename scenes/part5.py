from manim import *
import os

from scenes.part5.scene_5_1_summary import play_scene_5_1
from scenes.part5.scene_5_2_challenges import play_scene_5_2
from scenes.part5.scene_5_3_future import play_scene_5_3

class Part5(Scene):
    def construct(self):
        play_scene_5_1(self)
        self.wait(0.5)
        self.clear()
        
        play_scene_5_2(self)
        self.wait(0.5)
        self.clear()
        
        play_scene_5_3(self)
        self.wait(0.5)
        self.clear()
