# will contains all the model factory classes
# from resnet_model import ResNetModel
from .vit_model import ViTModel
from config.settings import AVAILABLE_MODELS
from .text2image_model import Text2ImageModel



def get_model(model_key: str):
    if model_key == "vit":
        return ViTModel(AVAILABLE_MODELS["vit"])
    
    # text2image model
    if model_key == "text2image":
        return Text2ImageModel(AVAILABLE_MODELS["text2image"])
    
    
    models = {
        "vit": ViTModel,
    # "resnet": ResNetModel,
        "text2image": Text2ImageModel

    }
    
    # error handling for unknown model key
    if model_key in models:
        raise ValueError(f"UJnknown model key: {model_key} . Available models are: {list(models.keys())}"
    )


    return models[model_key]()