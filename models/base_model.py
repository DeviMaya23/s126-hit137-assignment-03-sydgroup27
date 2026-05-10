# will contains all the base model classes
from abc import ABC, abstractmethod


class BaseModel(ABC):
    """Abstract base for image classification models.

    Subclasses must implement `predict` to return a list of predictions,
    each prediction being a dict with `label` and `score` keys, matching
    the Hugging Face transformers pipeline output.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def predict(self, image_path: str):
       raise NotImplementedError