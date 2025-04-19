class StringReplaceNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "placeholders": ("KEY_VALUE", {"default": None}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_string",)
    
    FUNCTION = "replace_string"
    
    CATEGORY = "RequestNode/Utils"
    
    def replace_string(self, input_string, placeholders=None):
        if not placeholders:
            return (input_string,)
        
        output_string = input_string
        
        for key, value in placeholders.items():
            str_value = str(value)
            output_string = output_string.replace(key, str_value)
        
        return (output_string,)

NODE_CLASS_MAPPINGS = {
    "StringReplaceNode": StringReplaceNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringReplaceNode": "String Replace Node"
}