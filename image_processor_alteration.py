"""A module to represent the image processing alterations.

This module contains the parent class Alteration and 3 child classes
that represent different types of alterations that can be applied to the image.
"""
import numpy as np


# parent class, to apply inheritance and polymorphism
class Alteration:
    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        raise NotImplementedError


class ColourShift(Alteration):
    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        pass

# TODO: add 2 more alteration classes here
