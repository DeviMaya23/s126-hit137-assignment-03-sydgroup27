"""A module to represent the image processing alterations.

This module contains the parent class Alteration and 3 child classes
that represent different types of alterations that can be applied to the image.
"""
import numpy as np
import cv2 as cv


# parent class, to apply inheritance and polymorphism
class Alteration:
    """Parent class for image alterations."""
    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        raise NotImplementedError


class ColourShift(Alteration):
    """Class for colour shift alteration."""

    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        """Applies a subtle colour shift to the specified region.

        Args:
            image (np.ndarray): Input image from cv.imread
            region (tuple): A tuple (x, y, width, height) defining the
                region to alter.

        Returns:
            np.ndarray: The altered image with the colour shift applied.
        """

        x, y, width, height = region

        altered_image = image.copy()

        # Extract region
        roi = altered_image[y:y + height, x:x + width]

        # Small colour shift
        roi[:, :, 1] = np.clip(
            roi[:, :, 1] + 10,
            0,
            255
        )
        altered_image[y:y + height, x:x + width] = roi

        return altered_image


class BlurEffect(Alteration):
    """Class for applying a blur effect."""

    def apply(self, image: np.ndarray,
              region: tuple) -> np.ndarray:
        """Applies a subtle blur effect to the specified region.

        Args:
            image (np.ndarray): Input image from cv.imread
            region (tuple): A tuple (x, y, width, height) defining the
                region to alter.

        Returns:
            np.ndarray: The altered image with the blur effect applied.
        """

        x, y, width, height = region

        altered_image = image.copy()

        roi = altered_image[y:y + height, x:x + width]

        # Apply slight blur
        blurred = cv.GaussianBlur(roi, (5, 5), 0)

        altered_image[y:y + height, x:x + width] = blurred

        return altered_image


class BrightnessChange(Alteration):
    """Class for slightly changing brightness."""

    def apply(self, image: np.ndarray,
              region: tuple) -> np.ndarray:
        """Applies a slight brightness change to the specified region.
        Args:
            image (np.ndarray): Input image from cv.imread
            region (tuple): A tuple (x, y, width, height) defining the
                region to alter.
        Returns:
            np.ndarray: The altered image with the brightness change applied.
        """

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
