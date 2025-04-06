import json

class HeaderNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "json_array": ("LIST", {"default": []}),
            }
        }
 
    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("headers",)
 
    FUNCTION = "create_headers"
 
    CATEGORY = "RequestNode/Header"
 
    def create_headers(self, json_array=None):
        headers = {}
        
        # 合併json_array中的所有JSON
        if json_array:
            for json_obj in json_array:
                if isinstance(json_obj, dict):
                    headers.update(json_obj)
            
        return (headers,)

NODE_CLASS_MAPPINGS = {
    "HeaderNode": HeaderNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "HeaderNode": "Header Node"
}