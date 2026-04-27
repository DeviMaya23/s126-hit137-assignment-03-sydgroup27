"""A class to represent image processor used by the game.
"""
from image_processor_alteration import Alteration, ColourShift
import numpy as np


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

    def __init__(self, image_path: str):
        """Initialises the image processor with both original image and
        processed image, and the list of altered regions.
        Args:
            image_path (str): The file path of the image to be processed.
        """
        self.alterations = [ColourShift()]  # add 2 more

        # TODO: load image path, put image, initialise altered region list
        # TODO: alteration logic here (region to to apply, randomised alteration types)

    def get_original_image(self) -> np.ndarray:
        return self.original_image

    def get_processed_image(self) -> np.ndarray:
        return self.processed_image

    def get_altered_regions(self) -> list[tuple[int, int, int, int]]:
        return self.altered_regions
