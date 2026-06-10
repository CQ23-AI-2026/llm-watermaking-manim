from manim import Scene

from scenes.part3.introduction import IntroductionScene, play_part3_intro
from scenes.part3.threats import ThreatsScene, play_part3_threats
from scenes.part3.core_concept import CoreConceptScene, play_part3_core_concept
from scenes.part3.drw import DRWScene, play_part3_drw
from scenes.part3.ginsew import GINSEWScene, play_part3_ginsew
from scenes.part3.cater import CATERScene, play_part3_cater
from scenes.part3.probing import ProbingScene, play_part3_probing
from scenes.part3.fingerprinting import FingerprintingScene, play_part3_fingerprinting

__all__ = [
    "IntroductionScene", "ThreatsScene", "CoreConceptScene",
    "DRWScene", "GINSEWScene", "CATERScene", "ProbingScene", "FingerprintingScene", "Part3",
    "play_part3_intro", "play_part3_threats", "play_part3_core_concept",
    "play_part3_drw", "play_part3_ginsew", "play_part3_cater", "play_part3_probing",
    "play_part3_fingerprinting"
]

class Part3(Scene):
    def construct(self):
        play_part3_intro(self)
        play_part3_threats(self)
        play_part3_core_concept(self)
        play_part3_drw(self)
        play_part3_ginsew(self)
        play_part3_cater(self)
        play_part3_probing(self)
        play_part3_fingerprinting(self)
