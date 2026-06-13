from manim import *
import os

from scenes.part5.scene_5_1_summary import play_scene_5_1
from scenes.part5.scene_5_2_benchmarks import play_scene_5_2
from scenes.part5.scene_5_3_open_problems import play_scene_5_3
from scenes.part5.scene_5_4_future import play_scene_5_4

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
        
        play_scene_5_4(self)
        self.wait(0.5)
        self.clear()
