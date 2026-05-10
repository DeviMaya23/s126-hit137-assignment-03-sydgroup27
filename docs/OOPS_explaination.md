## OOP Design Overview

- **BaseModel (Abstract)**: defines the common interface.
  - `models/base_model.py` provides the abstract class with `predict(image_path)`.
- **Concrete Models**:
  - `models/vit_model.py` implements `ViTModel` using the transformers 
- **Model Factory**:
  - `models/model_factory.py#get_model(model_key)` returns the correct model instance based on a key.
- **Configuration**:
  - `config/settings.py#AVAILABLE_MODELS` maps model keys to pretrained model names.
- **Reusable UI Components**:
  - `ui/components.py` exposes helpers like `create_button`, `create_labeled_frame`, `create_text_box`, and `create_image_canvas` to compose the GUI.
- **Utilities**:
  - `utils/image_utils.py#process_image` loads and resizes an image for preview.
  - `utils/decorators.py#log_action` example decorator for cross-cutting concerns.
