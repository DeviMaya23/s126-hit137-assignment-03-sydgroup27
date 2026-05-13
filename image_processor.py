"""A class to represent the image processor used by the game."""

from image_processor_alteration import (
    Alteration,
    ColourShift,
    BlurEffect,
    BrightnessChange,
    SaturationShift,
)
import cv2 as cv
import random
import numpy as np
from PIL import Image
from constants import ALTERED_REGION_COUNT, CANVAS_WIDTH, CANVAS_HEIGHT


# Minimum pixel gap between altered regions so they never sit on top of each
# other and each difference is independently discoverable.
_MIN_REGION_GAP = 10


class ImageProcessor:
    """Loads an image, applies subtle random alterations, and exposes both
    the original and the altered version for use by the game.

    Attributes:
        original_image (np.ndarray): BGR image as loaded (and resized).
        processed_image (np.ndarray): Copy of the original with alterations.
        altered_regions (list[tuple[int,int,int,int]]): (x, y, w, h) for
            every region that was changed — used to draw hint overlays.
    """

    altered_regions: list[tuple[int, int, int, int]]
    alterations: list[Alteration]

    def __init__(self):
        """Sets up the pool of available alteration strategies."""
        self.altered_regions = []
        self.alterations = [
            ColourShift(),
            BlurEffect(),
            BrightnessChange(),
            SaturationShift(),
        ]

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def load_image(self, image_path: str) -> None:
        """Loads, resizes, and alters the image.

        Supports any format that OpenCV can decode (JPEG, PNG, BMP, TIFF,
        WebP, …).  The file name may contain non-ASCII characters.

        Args:
            image_path: Path to the source image file.

        Raises:
            ValueError: If the file cannot be read or decoded.
        """
        self.original_image = self._cv_imread(image_path)

        # Scale down to fit the canvas while keeping the aspect ratio.
        h, w = self.original_image.shape[:2]
        scale = min(CANVAS_WIDTH / w, CANVAS_HEIGHT / h)
        new_w, new_h = int(w * scale), int(h * scale)
        self.original_image = cv.resize(self.original_image, (new_w, new_h))

        self.processed_image = self.original_image.copy()
        self.altered_regions = []

        self._apply_random_alterations(ALTERED_REGION_COUNT)

    def get_original_image(self) -> Image.Image:
        """Returns the unmodified image as an RGB PIL Image."""
        return Image.fromarray(cv.cvtColor(self.original_image, cv.COLOR_BGR2RGB))

    def get_processed_image(self) -> Image.Image:
        """Returns the altered image as an RGB PIL Image."""
        return Image.fromarray(cv.cvtColor(self.processed_image, cv.COLOR_BGR2RGB))

    def get_altered_regions(self) -> list[tuple[int, int, int, int]]:
        """Returns the list of altered (x, y, width, height) regions."""
        return self.altered_regions

    def resize_to_fit(self, img: Image.Image, max_w: int, max_h: int) -> Image.Image:
        """Resizes a PIL image to fit within (max_w, max_h), preserving ratio."""
        img = img.copy()
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        return img

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _apply_random_alterations(self, num_alterations: int) -> None:
        """Places *num_alterations* non-overlapping altered regions randomly.

        Region size is kept moderate (50–90 px) so the alteration covers
        enough pixels to be detectable without dominating the image.

        Alteration type is chosen at random from self.alterations for each
        region, so a single game round may contain a mix of blur, colour
        shift, brightness change, and saturation shift.

        Args:
            num_alterations: How many distinct regions to alter.
        """
        img_h, img_w = self.processed_image.shape[:2]

        # Region dimensions — wide enough to spot, small enough to hunt for.
        MIN_SIZE, MAX_SIZE = 50, 90

        placed: list[tuple[int, int, int, int]] = []
        max_attempts = 200          # safety valve to avoid infinite loops
        attempts = 0

        while len(placed) < num_alterations and attempts < max_attempts:
            attempts += 1

            rw = random.randint(MIN_SIZE, MAX_SIZE)
            rh = random.randint(MIN_SIZE, MAX_SIZE)

            # Guard against images smaller than a single region.
            if img_w <= rw or img_h <= rh:
                continue

            x = random.randint(0, img_w - rw)
            y = random.randint(0, img_h - rh)
            candidate = (x, y, rw, rh)

            if self._overlaps_any(candidate, placed, gap=_MIN_REGION_GAP):
                continue

            placed.append(candidate)

            alteration = random.choice(self.alterations)
            self.processed_image = alteration.apply(self.processed_image, candidate)

        # Record whatever we managed to place (may be < num_alterations on
        # very small images, but this is handled gracefully by the game).
        self.altered_regions = placed

    @staticmethod
    def _overlaps_any(
        candidate: tuple[int, int, int, int],
        placed: list[tuple[int, int, int, int]],
        gap: int,
    ) -> bool:
        """Returns True if *candidate* overlaps (or is too close to) any
        already-placed region.

        Args:
            candidate: (x, y, w, h) region being considered.
            placed: Regions already accepted.
            gap: Minimum pixel clearance between regions.
        """
        cx, cy, cw, ch = candidate
        for px, py, pw, ph in placed:
            # Expand each existing region by *gap* on all sides before testing
            # for intersection.
            if (
                cx < px + pw + gap
                and cx + cw > px - gap
                and cy < py + ph + gap
                and cy + ch > py - gap
            ):
                return True
        return False

    def _cv_imread(self, path: str) -> np.ndarray:
        """Reads an image robustly, handling non-ASCII file paths.

        Args:
            path: File system path to the image.

        Returns:
            BGR image array.

        Raises:
            ValueError: If the file cannot be decoded.
        """
        stream = np.fromfile(path, dtype=np.uint8)
        img = cv.imdecode(stream, cv.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Could not load image from path: {path}")
        return img