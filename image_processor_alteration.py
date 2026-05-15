"""A module to represent the image processing alterations.

This module contains the parent class Alteration and child classes
that represent different types of alterations that can be applied to an image.

Design principle: alterations should be noticeable upon careful inspection
but not immediately obvious at a glance — appropriate for a spot-the-difference
game.
"""
import numpy as np
import cv2 as cv
import random


class Alteration:
    """Parent class for image alterations."""
    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        raise NotImplementedError


class ColourShift(Alteration):
    """Shifts one colour channel in a region by a randomised amount.

    The channel (R, G, or B) and direction (+/-) are chosen randomly each
    time apply() is called, so repeated uses produce varied results.
    Shift magnitude is kept moderate — enough to spot, not impossible to miss.
    """

    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        """Applies a colour shift to the specified region.

        Args:
            image (np.ndarray): BGR image (from cv.imread / cv.imdecode).
            region (tuple): (x, y, width, height) of the region to alter.

        Returns:
            np.ndarray: Copy of the image with the colour shift applied.
        """
        x, y, width, height = region
        altered = image.copy()
        roi = altered[y:y + height, x:x + width].astype(np.int16)

        # Pick one BGR channel at random (0=B, 1=G, 2=R)
        channel = random.randint(0, 2)
        # Shift amount: moderate — clearly there but requires a second look
        shift = random.choice([-1, 1]) * random.randint(25, 45)

        roi[:, :, channel] = np.clip(roi[:, :, channel] + shift, 0, 255)
        altered[y:y + height, x:x + width] = roi.astype(np.uint8)
        return altered


class BlurEffect(Alteration):
    """Applies a Gaussian blur to a region.

    The kernel is kept moderate — softness is visible on close inspection
    but blends into the surrounding image at a distance.
    """

    # Odd kernel sizes only; larger = more obvious blur
    _KERNEL_SIZES = [7, 9, 11]

    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        """Applies a blur effect to the specified region.

        Args:
            image (np.ndarray): BGR image.
            region (tuple): (x, y, width, height) of the region to alter.

        Returns:
            np.ndarray: Copy of the image with the blur applied.
        """
        x, y, width, height = region
        altered = image.copy()
        roi = altered[y:y + height, x:x + width]

        k = random.choice(self._KERNEL_SIZES)
        blurred = cv.GaussianBlur(roi, (k, k), sigmaX=0)

        altered[y:y + height, x:x + width] = blurred
        return altered


class BrightnessChange(Alteration):
    """Lightens or darkens a region by a moderate amount.

    The direction (lighter vs darker) is chosen randomly, making the
    alteration less predictable for the player.
    """

    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        """Applies a brightness change to the specified region.

        Args:
            image (np.ndarray): BGR image.
            region (tuple): (x, y, width, height) of the region to alter.

        Returns:
            np.ndarray: Copy of the image with the brightness change applied.
        """
        x, y, width, height = region
        altered = image.copy()
        roi = altered[y:y + height, x:x + width]

        # Positive beta = brighter, negative = darker; range keeps it subtle
        beta = random.choice([-1, 1]) * random.randint(28, 50)
        bright = cv.convertScaleAbs(roi, alpha=1.0, beta=beta)

        altered[y:y + height, x:x + width] = bright
        return altered


class SaturationShift(Alteration):
    """Boosts or reduces colour saturation in a region.

    Over-saturated regions look vivid; desaturated regions appear washed out.
    Both are noticeable on a careful look without standing out immediately.
    """

    def apply(self, image: np.ndarray, region: tuple) -> np.ndarray:
        """Applies a saturation shift to the specified region.

        Args:
            image (np.ndarray): BGR image.
            region (tuple): (x, y, width, height) of the region to alter.

        Returns:
            np.ndarray: Copy of the image with the saturation change applied.
        """
        x, y, width, height = region
        altered = image.copy()
        roi = altered[y:y + height, x:x + width]

        # Work in HSV colour space for clean saturation control
        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV).astype(np.int16)

        # Saturation channel is index 1 in HSV
        # Positive = more vivid, negative = more grey
        shift = random.choice([-1, 1]) * random.randint(50, 90)
        hsv_roi[:, :, 1] = np.clip(hsv_roi[:, :, 1] + shift, 0, 255)

        roi_out = cv.cvtColor(hsv_roi.astype(np.uint8), cv.COLOR_HSV2BGR)
        altered[y:y + height, x:x + width] = roi_out
        return altered