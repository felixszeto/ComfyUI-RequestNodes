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
                "KEY_VALUE": ("KEY_VALUE", {"default": None}),
            }
        }
 
    RETURN_TYPES = ("KEY_VALUE",)
    RETURN_NAMES = ("KEY_VALUE",)
 
    FUNCTION = "create_key_value"
 
    CATEGORY = "RequestNode/KeyValue"
 
    def create_key_value(self, key="", value="", KEY_VALUE=None):
        output = {}
        
        if KEY_VALUE is not None:
            output.update(KEY_VALUE)
            
        if key and value:
            output[key] = value
            
        return (output,)

NODE_CLASS_MAPPINGS = {
    "KeyValueNode": KeyValueNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "KeyValueNode": "Key/Value Node"
}