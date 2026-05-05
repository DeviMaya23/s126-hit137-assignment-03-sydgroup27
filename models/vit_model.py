# will contains all the vit model classes
from transformers import pipeline
from .base_model import BaseModel

# Use a pipeline as a high-level helper
class ViTModel(BaseModel):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.pipeline = pipeline("image-classification", model=model_name)

    def predict(self, image_path: str):
        return self.pipeline(image_path)