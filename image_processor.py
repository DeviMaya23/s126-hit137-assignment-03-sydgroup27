"""A class to represent image processor used by the game.
"""
from image_processor_alteration import Alteration, ColourShift
import numpy as np
import cv2 as cv
import random

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
        #Load the image
        self.original_image = cv.imread(image_path)
       
        if self.original_imange is None:
            raise ValueError(f"Could not load image from path: {image_path}")
        
        #copy original image for processing
        self.processed_image = self.original_image.copy()

        #store altered regions
        self.altered_regions = [] 

 
        self.alterations = [
            ColourShift(), 
            BlurEffect(),
            BrightnessChange()
            ]  

       # Apply 5 random alterations
        self.apply_random_alterations(5)
    
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

            # Extract region
            region = self.processed_image[
                y:y + region_height,
                x:x + region_width
            ]

            # Choose random alteration
            alteration = random.choice(self.alterations)

            # Apply alteration
            altered_region = alteration.apply(region)

            # Put altered region back
            self.processed_image[
                y:y + region_height,
                x:x + region_width
            ] = altered_region
    def get_original_image(self) -> np.ndarray:
        return self.original_image

    def get_processed_image(self) -> np.ndarray:
        return self.processed_image

    def get_altered_regions(self) -> list[tuple[int, int, int, int]]:
        return self.altered_regions
