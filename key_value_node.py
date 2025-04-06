import json

class KeyValueNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": ""}),
                "value": ("STRING", {"default": ""}),
            },
            "optional": {
                "input_json": ("LIST", {"default": None}),
            }
        }
 
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("json_array",)
 
    FUNCTION = "create_key_value"
 
    CATEGORY = "RequestNode/KeyValue"
 
    def create_key_value(self, key="", value="", input_json=None):
        output = {}
        
        # 合并输入JSON (从LIST中取第一个元素)
        if input_json and len(input_json) > 0 and isinstance(input_json[0], dict):
            output.update(input_json[0])
            
        # 添加当前key/value
        if key and value:
            output[key] = value
            
        return ([output],)

NODE_CLASS_MAPPINGS = {
    "KeyValueNode": KeyValueNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "KeyValueNode": "Key/Value Node"
}