from manim import Scene

from scenes.part1.scene_1_0 import play_part1_scene_1_0
from scenes.part1.scene_1_1 import play_part1_scene_1_1
from scenes.part1.scene_1_2 import play_part1_scene_1_2
from scenes.part1.scene_1_3 import play_part1_scene_1_3
from scenes.part1.scene_1_4 import play_part1_scene_1_4


class Part1(Scene):
	def construct(self):
		play_part1_scene_1_0(self)
		self.wait(0.2)
		self.clear()

		play_part1_scene_1_1(self)
		self.wait(0.2)
		self.clear()

		play_part1_scene_1_2(self)
		self.wait(0.2)
		self.clear()

		play_part1_scene_1_3(self)
		self.wait(0.2)
		self.clear()

		play_part1_scene_1_4(self)
		self.wait(0.2)