"""A class to represent image processor used by the game.
"""


from image_processor_alteration import (
    Alteration,
    ColourShift,
    BlurEffect,
    BrightnessChange)
import cv2 as cv
import random
import numpy as np
from PIL import Image
from constants import ALTERED_REGION_COUNT, CANVAS_WIDTH, CANVAS_HEIGHT


class ImageProcessor:
    """A class to represent the image processor used by the game.
    Attributes:
        original_image (np.ndarray): Image loaded from the file path.
        processed_image (np.ndarray): Image after alteration.
        altered_regions (list[tuple]): A list of tuples representing
            the regions that have been altered.
            The tuple format is (x, y, width, height).
    """
    altered_regions: list[tuple[int, int, int, int]]
    alterations: list[Alteration]

    def __init__(self):
        """Initializes the ImageProcessor with available alterations."""
        self.altered_regions = []
        self.alterations = [
            ColourShift(),
            BlurEffect(),
            BrightnessChange()
            ]

    def load_image(self, image_path: str) -> None:
        """Initialises the image processor with both original image and
        processed image, and the list of altered regions.

        Args:
            image_path (str): The file path of the image to be processed.
        """
        # Load the image
        self.original_image = self._cv_imread(image_path)

        if self.original_image is None:
            raise ValueError(f"Could not load image from path: {image_path}")

        # resize to canvas size
        h, w = self.original_image.shape[:2]
        scale = min(CANVAS_WIDTH / w, CANVAS_HEIGHT / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        self.original_image = cv.resize(self.original_image, (new_w, new_h))

        # copy original image for processing
        self.processed_image = self.original_image.copy()

        # store altered regions
        self.altered_regions = []

        # Apply random alterations
        self.apply_random_alterations(ALTERED_REGION_COUNT)

    def apply_random_alterations(self, num_alterations: int):
        """Applies a specified number of random alterations to the image.

        Args:
            num_alterations (int): The number of random alterations to apply.
        """
        height, width = self.processed_image.shape[:2]
        for _ in range(num_alterations):

            # Random region size
            region_width = random.randint(40, 80)
            region_height = random.randint(40, 80)

            # Random position
            x = random.randint(0, width - region_width)
            y = random.randint(0, height - region_height)

            # Save region
            self.altered_regions.append(
                (x, y, region_width, region_height)
            )

            region = (x, y, region_width, region_height)

            alteration = random.choice(self.alterations)

            self.processed_image = alteration.apply(
                self.processed_image,
                region
                )

    def get_original_image(self) -> Image:
        """Returns the original image as a PIL Image in RGB format.
        """
        return Image.fromarray(cv.cvtColor(self.original_image,
                                           cv.COLOR_BGR2RGB))

    def get_processed_image(self) -> Image:
        """Returns the processed image as a PIL Image in RGB format.
        """
        return Image.fromarray(cv.cvtColor(self.processed_image,
                                           cv.COLOR_BGR2RGB))

    def get_altered_regions(self) -> list[tuple[int, int, int, int]]:
        """Returns the list of altered regions."""
        return self.altered_regions

    def resize_to_fit(self, img: Image.Image, max_w: int,
                      max_h: int) -> Image.Image:
        """Resizes an image to fit within specified dimensions.

        Args:
            img (Image.Image): The image to resize.
            max_w (int): Maximum width in pixels.
            max_h (int): Maximum height in pixels.
        """
        img = img.copy()
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        return img
    
    def _cv_imread(self, path: str) -> np.ndarray:
        """Reads an image from a file path using OpenCV, handling non-ASCII file names."""
        stream = np.fromfile(path, dtype=np.uint8)
        img = cv.imdecode(stream, cv.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Failed to load image: {path}")
        return img
