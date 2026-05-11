"""
TO BE DELETED LATER
This is dummy image processor file
Used for Game UI & Controller development before the actual image processor is done
"""
from image_processor_alteration import Alteration, ColourShift
import numpy as np
from PIL import Image, ImageDraw, ImageTk


class DummyImageProcessor:
    altered_regions: list[tuple[int, int, int, int]]
    alterations: list[Alteration]

    def __init__(self, image_path: str):
        """Initialises the image processor with both original image and
        processed image, and the list of altered regions.
        Args:
            image_path (str): The file path of the image to be processed.
        """
        # self.alterations = [ColourShift()]  # add 2 more

        # TODO: load image path, put image, initialise altered region list
        # TODO: alteration logic here (region to to apply, randomised alteration types)

    # def get_original_image(self) -> np.ndarray:
    #     return self.original_image

    # def get_processed_image(self) -> np.ndarray:
    #     return self.processed_image

    # def get_altered_regions(self) -> list[tuple[int, int, int, int]]:
    #     return self.altered_regions

    # this is hardcoded stuff, will replace later
    def is_valid(self, path: str) -> bool:
        return True

    def load_images(self, path: str):
        # return two identical PIL images for now
       
        image = Image.open(path).convert("RGB")
        return image, image.copy()

    def get_altered_regions(self) -> list:
        # hardcoded fake regions for testing
        return [
            (100, 100, 50, 50),
            (200, 150, 50, 50),
            (300, 200, 50, 50),
            (400, 250, 50, 50),
            (150, 300, 50, 50),
        ]

    def draw_circle(self, img, x: int, y: int, color: str):
        draw = ImageDraw.Draw(img)
        draw.ellipse([x-25, y-25, x+25, y+25], outline=color, width=2)
