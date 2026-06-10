from manim import Scene

from scenes.part3.introduction import IntroductionScene, play_part3_intro
from scenes.part3.threats import ThreatsScene, play_part3_threats
from scenes.part3.core_concept import CoreConceptScene, play_part3_core_concept
from scenes.part3.extraction_defense import ExtractionDefenseScene, play_part3_extraction_defense
from scenes.part3.fingerprinting import FingerprintingScene, play_part3_fingerprinting

__all__ = [
    "IntroductionScene", "ThreatsScene", "CoreConceptScene", "ExtractionDefenseScene", "FingerprintingScene", "Part3",
    "play_part3_intro", "play_part3_threats", "play_part3_core_concept", "play_part3_extraction_defense", "play_part3_fingerprinting"
]

class Part3(Scene):
    def construct(self):
        play_part3_intro(self)
        play_part3_threats(self)
        play_part3_core_concept(self)
        play_part3_extraction_defense(self)
        play_part3_fingerprinting(self)
