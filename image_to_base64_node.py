import io
import base64
import torch
import numpy as np
from PIL import Image

class ImageToBase64Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert_image_to_base64"
    CATEGORY = "RequestNode/Converters"

    def convert_image_to_base64(self, image):
        # Convert tensor to PIL Image
        i = 255. * image.cpu().numpy().squeeze()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # Save image to a byte buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        
        # Encode the byte buffer to a base64 string
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return (base64_string,)

NODE_CLASS_MAPPINGS = {
    "ImageToBase64Node": ImageToBase64Node
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToBase64Node": "Image to Base64 Node"
}