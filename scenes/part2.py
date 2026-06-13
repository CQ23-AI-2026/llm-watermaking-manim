import os
from manim import Scene

from scenes.part2.init import play_part2_init
from scenes.part2.scene_2_0_llm_basics import play_scene_2_0
from scenes.part2.scene_2_1_1_green_red_core import play_scene_2_1_1
from scenes.part2.scene_2_1_2_kgw_vs_unigram import play_scene_2_1_2
from scenes.part2.scene_2_1_3_watermark_detection import play_scene_2_1_3
from scenes.part2.scene_2_1_4_watermark_examples import play_scene_2_1_4
from scenes.part2.scene_2_1_5_watermark_limitations import play_scene_2_1_5
from scenes.part2.scene_2_1_6_transition_questions import play_scene_2_1_6
from scenes.part2.scene_2_2_1_quality_metric import play_scene_2_2_1
from scenes.part2.scene_2_2_2_detectability import play_scene_2_2_2
from scenes.part2.scene_2_2_3_robustness import play_scene_2_2_3
from scenes.part2.scene_2_2_4_security import play_scene_2_2_4
from scenes.part2.scene_2_3_1_pareto_frontier import play_scene_2_3_1
from scenes.part2.scene_2_3_2_gumbel_watermark import play_scene_2_3_2
from scenes.part2.scene_2_3_3_gumbel_detection import play_scene_2_3_3
from scenes.part2.scene_2_3_4_gumbel_evaluation import play_scene_2_3_4
from scenes.part2.scene_2_4_1_evolution_radar_chart import play_scene_2_4_1
from scenes.part2.scene_2_4_2_impossibility_results import play_scene_2_4_2

class Part2(Scene):
    def construct(self):
        # Reset file ghi chú thời gian audio mỗi khi render lại Part2
        if os.path.exists("audio_times.txt"):
            os.remove("audio_times.txt")

        # 2.intro: Tiêu đề Part 2 "Text Watermark"
        play_part2_init(self)
        self.wait(0.5)
        self.clear()

        # 2.0: Language Model sinh văn bản như thế nào?
        play_scene_2_0(self)
        self.wait(0.5)
        self.clear()

        # 2.1.1: Ý tưởng Green-Red Watermark
        play_scene_2_1_1(self)
        self.wait(0.5)
        self.clear()
        
        # 2.1.2: KGW vs Unigram Watermark
        play_scene_2_1_2(self)
        self.wait(0.5)
        self.clear()
        
        # 2.1.3: Watermark Detection (Z-score)
        play_scene_2_1_3(self)
        self.wait(0.5)
        self.clear()
        
        # 2.1.4: Watermark Examples
        play_scene_2_1_4(self)
        self.wait(0.5)
        self.clear()

        # 2.1.5: Watermark Limitations
        play_scene_2_1_5(self)
        self.wait(0.5)
        self.clear()
        
        # 2.1.6: Transition Questions
        play_scene_2_1_6(self)
        self.wait(0.5)
        self.clear()
        
        # 2.2.1: Quality Metric
        play_scene_2_2_1(self)
        self.wait(0.5)
        self.clear()
        
        # 2.2.2: Detectability
        play_scene_2_2_2(self)
        self.wait(0.5)
        self.clear()
        
        # 2.2.3: Robustness
        play_scene_2_2_3(self)
        self.wait(0.5)
        self.clear()
        
        # 2.2.4: Security & Unforgeability
        play_scene_2_2_4(self)
        self.wait(0.5)
        self.clear()
        
        # 2.3.1: Pareto Frontier
        play_scene_2_3_1(self)
        self.wait(0.5)
        self.clear()
        
        # 2.3.2: Gumbel Watermark
        play_scene_2_3_2(self)
        self.wait(0.5)
        self.clear()
        
        # 2.3.3: Gumbel Detection
        play_scene_2_3_3(self)
        self.wait(0.5)
        self.clear()
        
        # 2.3.4: Gumbel Evaluation
        play_scene_2_3_4(self)
        self.wait(0.5)
        self.clear()
        
        # 2.4.1: Evolution Radar Chart
        play_scene_2_4_1(self)
        self.wait(0.5)
        self.clear()
        
        # 2.4.2: Impossibility Results
        play_scene_2_4_2(self)
        self.wait(0.5)
        self.clear()
        
        # ... các scene tiếp theo sẽ được import sau
