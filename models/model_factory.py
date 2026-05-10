# models/model_factory.py

from .vit_model import ViTModel
from .text2image_model import Text2ImageModel

from config.settings import AVAILABLE_MODELS


def get_model(model_key: str):

    models = {

        "vit": lambda: ViTModel(
            AVAILABLE_MODELS["vit"]
        ),

        "text2image": lambda: Text2ImageModel(
            AVAILABLE_MODELS["text2image"]
        ),

    }

    # ERROR HANDLING
    if model_key not in models:

        raise ValueError(
            f"Unknown model key: {model_key}. "
            f"Available models are: {list(models.keys())}"
        )

    # RETURN MODEL
    return models[model_key]()