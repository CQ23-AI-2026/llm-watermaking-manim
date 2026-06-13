from manim import Scene

from scenes.part3.introduction import IntroductionScene, play_part3_intro
from scenes.part3.threats import ThreatsScene, play_part3_threats
from scenes.part3.core_concept import CoreConceptScene, play_part3_core_concept
from scenes.part3.drw_34 import DRW34Scene, play_part3_drw_34
from scenes.part3.drw_35 import DRW35Scene, play_part3_drw_35
from scenes.part3.ginsew import GINSEWScene, play_part3_ginsew
from scenes.part3.cater import CATERScene, play_part3_cater
from scenes.part3.probing import ProbingScene, play_part3_probing
from scenes.part3.fingerprinting import FingerprintingScene, play_part3_fingerprinting
from scenes.part3.deepjudge import DeepJudgeScene, play_part3_deepjudge
from scenes.part3.model_watermarking_conclusion import ModelWatermarkingConclusionScene, play_part3_model_watermarking_conclusion

__all__ = [
    "IntroductionScene", "ThreatsScene", "CoreConceptScene",
    "DRW34Scene", "DRW35Scene", "GINSEWScene", "CATERScene", "ProbingScene", "FingerprintingScene", "DeepJudgeScene",
    "ModelWatermarkingConclusionScene", "Part3",
    "play_part3_intro", "play_part3_threats", "play_part3_core_concept",
    "play_part3_drw_34", "play_part3_drw_35",
    "play_part3_ginsew", "play_part3_cater", "play_part3_probing",
    "play_part3_fingerprinting", "play_part3_deepjudge", "play_part3_model_watermarking_conclusion"
]

class Part3(Scene):
    def construct(self):
        play_part3_intro(self)
        play_part3_threats(self)
        play_part3_core_concept(self)
        play_part3_drw_34(self)
        play_part3_drw_35(self)
        play_part3_ginsew(self)
        play_part3_cater(self)
        play_part3_probing(self)
        play_part3_fingerprinting(self)
        play_part3_deepjudge(self)
        play_part3_model_watermarking_conclusion(self)
