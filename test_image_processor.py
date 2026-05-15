"""Unit test for image processor"""


import pytest
import numpy as np

from constants import ALTERED_REGION_COUNT
from image_processor import ImageProcessor


class TestImageProcessor:
    """Test suite for the ImageProcessor class."""
    def test_load_image_invalid_path(self):
        processor = ImageProcessor()
        with pytest.raises(ValueError):
            processor.load_image("non_existent_file.jpg")

    def test_load_image_invalid_image(self):
        processor = ImageProcessor()
        with pytest.raises(ValueError):
            processor.load_image("test_images/actuallytxtfile.jpg")

    def test_load_image_valid_path(self):
        processor = ImageProcessor()
        processor.load_image("test_images/testpng.png")
        assert processor.original_image is not None
        assert processor.processed_image is not None
        assert not np.array_equal(processor.original_image, processor.processed_image)
        assert len(processor.altered_regions) == ALTERED_REGION_COUNT

    def test_get_altered_regions(self):
        processor = ImageProcessor()
        processor.load_image("test_images/testpng.png")
        regions = processor.get_altered_regions()
        assert len(regions) == ALTERED_REGION_COUNT
        for region in regions:
            assert region[0] >= 0 and region[1] >= 0 # x and y must be non-negative
            assert region[2] > 0 and region[3] > 0 # width and height must be positive
            assert region[0] + region[2] <= processor.original_image.shape[1] # x + width must be within image width
            assert region[1] + region[3] <= processor.original_image.shape[0] # y + height must be within image height
