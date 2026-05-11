"""A module to represent the image processing alterations.

This module contains the parent class Alteration and 3 child classes
that represent different types of alterations that can be applied to the image.
"""
import numpy as np
import cv2 as cv


# parent class, to apply inheritance and polymorphism
class Alteration:
    #Base class for alterations
    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        raise NotImplementedError


#child class 1
class ColourShift(Alteration):
    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        
        x,y,width,height = region

        altered_image = image.copy()

        #Extract region
        roi = altered_image[y:y + height, x:x + width]

         # Small colour shift
        roi[:, :, 1] = np.clip(
            roi[:, :, 1] + 10,
            0,
            255
        )
        altered_image[y:y + height, x:x + width] = roi

        return altered_image

#child class 2

class BlurEffect(Alteration):
    """Applies a subtle blur effect."""

    def apply(self, image: np.ndarray,
              region: tuple) -> np.ndarray:

        x, y, width, height = region

        altered_image = image.copy()

        roi = altered_image[y:y + height, x:x + width]

        # Apply slight blur
        blurred = cv.GaussianBlur(roi, (5, 5), 0)

        altered_image[y:y + height, x:x + width] = blurred

        return altered_image

# Child Class 3
class BrightnessChange(Alteration):
    """Slightly changes brightness."""

    def apply(self, image: np.ndarray,
              region: tuple) -> np.ndarray:

        x, y, width, height = region

        altered_image = image.copy()

        roi = altered_image[y:y + height, x:x + width]

        # Increase brightness slightly
        bright = cv.convertScaleAbs(
            roi,
            alpha=1.0,
            beta=12
        )

        altered_image[y:y + height, x:x + width] = bright

        return altered_image
