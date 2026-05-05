# will contains all the model factory classes

from .vit_model import ViTModel
from .vit_model import ViTModel as DeiTModel  # reuse same pipeline class
from config.settings import AVAILABLE_MODELS

def get_model(model_key: str):
    if model_key == "vit":
        return ViTModel(AVAILABLE_MODELS["vit"])
    elif model_key == "deit":
        return DeiTModel(AVAILABLE_MODELS["deit"])
    else:
        raise ValueError(f"Unknown model key: {model_key}")