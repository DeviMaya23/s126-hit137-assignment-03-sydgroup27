from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

class Text2ImageModel:
    # Text-to-Image generation model using Stable Diffusion
    def __init__(self, model_name: str):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        # Move the model to GPU if available
        if torch.cuda.is_available():
            self.pipe.to("cuda")
    # Generate an image from a text prompt
    def predict(self, prompt: str) -> Image.Image:
        result = self.pipe(prompt, guidance_scale=7.5)
        return result.images[0]
