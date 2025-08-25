import requests
import json
import io
import torch
import numpy as np
from PIL import Image

class FormPostRequestNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_url": ("STRING", {"default": "http://127.0.0.1:7788/api/echo"}),
                "image": ("IMAGE",),
                "image_field_name": ("STRING", {"default": "image"}),
            },
            "optional": {
                "form_fields": ("KEY_VALUE",),
                "headers": ("KEY_VALUE",),
            }
        }
 
    RETURN_TYPES = ("STRING", "JSON", "ANY")
    RETURN_NAMES = ("text", "json", "any")
 
    FUNCTION = "make_form_post_request"
 
    CATEGORY = "RequestNode/Post Request"
 
    def make_form_post_request(self, target_url, image, image_field_name, form_fields=None, headers=None):
        files = []
        for i, single_image in enumerate(image):
            # Convert tensor to PIL Image
            img_np = 255. * single_image.cpu().numpy()
            img = Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))
            
            # Save image to a byte buffer
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            files.append((image_field_name, (f'image_{i}.png', buffer, 'image/png')))
        
        data = form_fields if form_fields else {}
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
            
        try:
            response = requests.post(target_url, files=files, data=data, headers=request_headers)
            
            text_output = response.text
            
            try:
                json_output = response.json()
            except json.JSONDecodeError:
                json_output = {"error": "Response is not valid JSON"}
            
            any_output = response.content
            
        except Exception as e:
            error_message = str(e)
            text_output = error_message
            json_output = {"error": error_message}
            any_output = error_message.encode()
        
        return (text_output, json_output, any_output)
 
NODE_CLASS_MAPPINGS = {
    "FormPostRequestNode": FormPostRequestNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "FormPostRequestNode": "Form Post Request Node"
}