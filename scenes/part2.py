from manim import Scene

from scenes.part2.scene_2_0 import play_part2_scene_2_0
from scenes.part2.scene_2_1_1 import play_part2_scene_2_1_1
from scenes.part2.scene_2_1_2 import play_part2_scene_2_1_2
from scenes.part2.scene_2_1_3 import play_part2_scene_2_1_3

class Part2(Scene):
    def construct(self):
        play_part2_scene_2_0(self)
        self.wait(0.2)
        self.clear()
        
        play_part2_scene_2_1_1(self)
        self.wait(0.2)
        self.clear()
        
        play_part2_scene_2_1_2(self)
        self.wait(0.2)
        self.clear()
        
        play_part2_scene_2_1_3(self)
        self.wait(0.2)
