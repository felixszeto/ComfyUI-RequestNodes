import requests
import json
import io
from PIL import Image
import numpy as np
import torch

class RestApiNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_url": ("STRING", {"default": "https://example.com/api", "forceInput":True}),
                "request_body": ("STRING", {"default": "{}", "multiline": True, "forceInput":True}),
                "method": (["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"], {"default": "GET"}),
            },
            "optional": {
                "headers": ("KEY_VALUE", {"default": None}),
                "RETRY_SETTING": ("RETRY_SETTING", {"default": None}),
                "image": ("IMAGE", {"default": None}),
                "mask": ("MASK", {"default": None}),
                "image_field_name": ("STRING", {"default": "image", "tooltip": "Field name for image in the request"}),
                "mask_field_name": ("STRING", {"default": "mask", "tooltip": "Field name for mask in the request"}),
            }
        }
    
    @classmethod
    def HIDE_INPUTS(s, method):
        hide_inputs = {}
        
        if method in ["HEAD", "OPTIONS", "DELETE"]:
            hide_inputs["request_body"] = True
            
        return hide_inputs
 
    RETURN_TYPES = ("STRING", "BYTES", "JSON", "DICT", "INT", "ANY")
    RETURN_NAMES = ("text", "file", "json", "headers", "status_code", "any")
 
    FUNCTION = "make_request"
 
    CATEGORY = "RequestNode/REST API"
 
    def _tensor_to_pil(self, tensor):
        """Convert ComfyUI tensor to PIL Image"""
        # Handle PyTorch tensors
        if hasattr(tensor, 'cpu'):
            # Convert PyTorch tensor to numpy
            tensor = tensor.cpu().numpy()
        
        # ComfyUI tensors are typically in format [batch, height, width, channels]
        if len(tensor.shape) == 4:
            # Take first image from batch
            tensor = tensor[0]
        
        # Convert from [0,1] float to [0,255] uint8
        if tensor.dtype in [np.float32, np.float64]:
            tensor = (tensor * 255).astype(np.uint8)
        elif hasattr(tensor, 'dtype') and 'float' in str(tensor.dtype):
            tensor = (tensor * 255).astype(np.uint8)
        
        # Ensure tensor is numpy array
        if not isinstance(tensor, np.ndarray):
            tensor = np.array(tensor)
        
        # Convert numpy array to PIL Image
        if len(tensor.shape) == 3 and tensor.shape[2] == 3:
            # RGB image
            return Image.fromarray(tensor, 'RGB')
        elif len(tensor.shape) == 3 and tensor.shape[2] == 4:
            # RGBA image
            return Image.fromarray(tensor, 'RGBA')
        elif len(tensor.shape) == 2:
            # Grayscale image
            return Image.fromarray(tensor, 'L')
        else:
            raise ValueError(f"Unsupported tensor shape: {tensor.shape}")
    
    def _pil_to_bytes(self, pil_image, format_name):
        """Convert PIL Image to bytes"""
        buffer = io.BytesIO()
        
        # Handle format conversion
        if format_name.lower() in ['jpg', 'jpeg']:
            # JPEG doesn't support transparency, convert RGBA to RGB
            if pil_image.mode == 'RGBA':
                # Create white background
                background = Image.new('RGB', pil_image.size, (255, 255, 255))
                background.paste(pil_image, mask=pil_image.split()[-1])  # Use alpha channel as mask
                pil_image = background
            pil_image.save(buffer, format='JPEG', quality=95)
        elif format_name.lower() == 'png':
            pil_image.save(buffer, format='PNG')
        elif format_name.lower() == 'webp':
            pil_image.save(buffer, format='WEBP', quality=95)
        else:
            # Default to PNG
            pil_image.save(buffer, format='PNG')
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _mask_to_pil(self, mask_tensor):
        """Convert ComfyUI mask tensor to PIL Image"""
        # Handle PyTorch tensors
        if hasattr(mask_tensor, 'cpu'):
            mask_tensor = mask_tensor.cpu().numpy()
        
        # ComfyUI masks are typically in format [batch, height, width] or [height, width]
        if len(mask_tensor.shape) == 3:
            # Take first mask from batch
            mask_tensor = mask_tensor[0]
        
        # Convert from [0,1] float to [0,255] uint8
        if mask_tensor.dtype in [np.float32, np.float64]:
            mask_tensor = (mask_tensor * 255).astype(np.uint8)
        elif hasattr(mask_tensor, 'dtype') and 'float' in str(mask_tensor.dtype):
            mask_tensor = (mask_tensor * 255).astype(np.uint8)
        
        # Ensure tensor is numpy array
        if not isinstance(mask_tensor, np.ndarray):
            mask_tensor = np.array(mask_tensor)
        
        # Convert to PIL Image (grayscale)
        return Image.fromarray(mask_tensor, 'L')
    
    def _detect_image_format(self, pil_image):
        """Detect the best format for the image based on its properties"""
        if pil_image.mode in ['RGBA', 'LA'] or 'transparency' in pil_image.info:
            return 'png'  # Use PNG for images with transparency
        else:
            return 'jpg'  # Use JPG for opaque images (smaller file size)
    

    def make_request(self, target_url, method, request_body, headers=None, RETRY_SETTING=None, 
                    image=None, mask=None,
                    image_field_name="image", mask_field_name="mask"):
        
        # Trim whitespace from target_url
        target_url = target_url.strip()
        
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)
        
        default_max_retry = 3
        max_retry = default_max_retry
        retry_until_status_code = 0
        retry_until_not_status_code = 0
        retry_interval = 1000
        retry_non_2xx = False

        if RETRY_SETTING is not None:
            if "max_retry" in RETRY_SETTING:
                max_retry = RETRY_SETTING["max_retry"]
            retry_until_status_code = RETRY_SETTING.get("retry_until_status_code", 0)
            retry_until_not_status_code = RETRY_SETTING.get("retry_until_not_status_code", 0)
            retry_interval = RETRY_SETTING.get("retry_interval", 1000)

            if "max_retry" in RETRY_SETTING and not any(key in RETRY_SETTING for key in ["retry_until_status_code", "retry_until_not_status_code"]):
                retry_non_2xx = True
        
        # Check if image and mask are provided
        has_image = image is not None
        has_mask = mask is not None
        
        params = {}
        body_data = None
        files = None
        
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body_data = json.loads(request_body)
            except json.JSONDecodeError:
                body_data = None
            
            # Handle image and mask using multipart/form-data
            if has_image or has_mask:
                files = {}
                
                # When uploading files, put JSON data as form data instead of json parameter
                if isinstance(body_data, dict):
                    # Add JSON data as form fields
                    for key, value in body_data.items():
                        if isinstance(value, (dict, list)):
                            files[key] = (None, json.dumps(value), 'application/json')
                        else:
                            files[key] = (None, str(value))
                
                # Add image as file (detect best format)
                if has_image:
                    pil_image = self._tensor_to_pil(image)
                    format_name = self._detect_image_format(pil_image)
                    image_bytes = self._pil_to_bytes(pil_image, format_name)
                    
                    # Create filename with proper extension
                    ext = format_name if format_name != 'jpg' else 'jpeg'
                    filename = f"{image_field_name}.{ext}"
                    
                    # Determine MIME type
                    mime_type = f"image/{ext}"
                    if ext == 'jpg':
                        mime_type = "image/jpeg"
                    
                    files[image_field_name] = (filename, image_bytes, mime_type)
                
                # Add mask as file (masks are always PNG to preserve transparency)
                if has_mask:
                    pil_mask = self._mask_to_pil(mask)
                    mask_bytes = self._pil_to_bytes(pil_mask, 'png')
                    filename = f"{mask_field_name}.png"
                    files[mask_field_name] = (filename, mask_bytes, "image/png")
                
                # Remove Content-Type header to let requests set it for multipart
                if 'Content-Type' in request_headers:
                    del request_headers['Content-Type']
                
                # Clear body_data since we're using multipart form data
                body_data = None
                
        elif method == "GET":
            try:
                params_data = json.loads(request_body)
                if isinstance(params_data, dict):
                    params = params_data
            except json.JSONDecodeError:
                pass
        
        def send_request():
            if method == "GET":
                return requests.get(target_url, params=params, headers=request_headers)
            elif method == "POST":
                if files:
                    return requests.post(target_url, files=files, headers=request_headers)
                else:
                    return requests.post(target_url, json=body_data, headers=request_headers)
            elif method == "PUT":
                if files:
                    return requests.put(target_url, files=files, headers=request_headers)
                else:
                    return requests.put(target_url, json=body_data, headers=request_headers)
            elif method == "DELETE":
                return requests.delete(target_url, headers=request_headers)
            elif method == "PATCH":
                if files:
                    return requests.patch(target_url, files=files, headers=request_headers)
                else:
                    return requests.patch(target_url, json=body_data, headers=request_headers)
            elif method == "HEAD":
                return requests.head(target_url, headers=request_headers)
            elif method == "OPTIONS":
                return requests.options(target_url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        
        max_attempts = 1
        attempts = 0
        last_exception = None
        
        has_specific_retry_conditions = (retry_until_status_code > 0 or retry_until_not_status_code > 0 or retry_non_2xx)

        if has_specific_retry_conditions and  max_retry == 0:
            import sys
            max_attempts = sys.maxsize
        elif max_retry > 0:
            max_attempts = max_retry + 1
        else:
            max_attempts = 1
        
        try:
            while attempts < max_attempts:
                try:
                    attempts += 1
                    response = send_request()
                    
                    if retry_until_status_code > 0 and response.status_code != retry_until_status_code:
                        if attempts < max_attempts:
                            import time
                            time.sleep(retry_interval / 1000)
                        continue
                    elif retry_until_not_status_code > 0 and response.status_code == retry_until_not_status_code:
                        if attempts < max_attempts:
                            import time
                            time.sleep(retry_interval / 1000)
                        continue
                    elif retry_non_2xx and (response.status_code < 200 or response.status_code >= 300):
                        if attempts < max_attempts:
                            import time
                            time.sleep(retry_interval / 1000)
                        continue
                    
                    break
                    
                except Exception as e:
                    last_exception = e
                    if attempts < max_attempts:
                        import time
                        time.sleep(retry_interval / 1000)
                    else:
                        raise
            
            text_output = response.text
            
            if method == "HEAD":
                file_output = io.BytesIO(b"")
                any_output = b""
            else:
                file_output = io.BytesIO(response.content)
                any_output = response.content
            
            try:
                if method == "HEAD":
                    json_output = dict(response.headers)
                else:
                    json_output = response.json()
            except json.JSONDecodeError:
                if method == "HEAD":
                    json_output = dict(response.headers)
                else:
                    json_output = {"error": "Response is not valid JSON"}
            
            if attempts > 1:
                retry_info = {"retries": attempts - 1}
                if max_retry > 0:
                    retry_info["max_retry"] = max_retry
                if retry_until_status_code > 0:
                    retry_info["retry_until_status_code"] = retry_until_status_code
                if retry_until_not_status_code > 0:
                    retry_info["retry_until_not_status_code"] = retry_until_not_status_code
                if retry_non_2xx:
                    retry_info["retry_non_2xx"] = True
                if isinstance(json_output, dict):
                    json_output["retry_info"] = retry_info
            
        except Exception as e:
            error_message = str(e)
            text_output = error_message
            file_output = io.BytesIO(error_message.encode())
            json_output = {"error": error_message}
            headers_output = {"error": error_message}
            status_code = 0
            any_output = error_message
        else:
            headers_output = dict(response.headers)
            status_code = response.status_code
        
        return (text_output, file_output, json_output, headers_output, status_code, any_output)
 
NODE_CLASS_MAPPINGS = {
    "RestApiNode": RestApiNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "RestApiNode": "Rest Api Node"
}
