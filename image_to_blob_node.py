import io
import torch
import numpy as np
from PIL import Image

class ImageToBlobNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("BYTES",)
    FUNCTION = "convert_image_to_blob"
    CATEGORY = "RequestNode/Converters"

    def convert_image_to_blob(self, image):
        # Convert tensor to PIL Image
        i = 255. * image.cpu().numpy().squeeze()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # Save image to a byte buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        
        return (buffer.getvalue(),)

NODE_CLASS_MAPPINGS = {
    "ImageToBlobNode": ImageToBlobNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToBlobNode": "Image to Blob Node"
}