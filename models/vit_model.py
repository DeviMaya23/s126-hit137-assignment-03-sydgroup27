# will contains all the vit model classes
from transformers import AutoImageProcessor, AutoModelForImageClassification
from .base_model import BaseModel

from PIL import Image
import torch

# Use a pipeline as a high-level helper
class ViTModel(BaseModel):
    def __init__(self, model_name):
        super().__init__(model_name)
        # explicitly use slow image processor
        self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=False)
        self.model = AutoModelForImageClassification.from_pretrained(model_name)


    def predict(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)[0]

        id2label = self.model.config.id2label
        scores, indices = torch.topk(probs, k=min(5, probs.shape[0]))
        results = []
        for score, idx in zip(scores.tolist(), indices.tolist()):
            results.append({"label": id2label[idx], "score": float(score)})
        return results