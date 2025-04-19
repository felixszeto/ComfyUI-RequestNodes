class RetrySettingNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": (["max_retry", "retry_interval", "retry_until_status_code", "retry_until_not_status_code"], {"default": ""}, {"default": "max_retry"}),
                "value": ("INT", {"default": 3, "min": 0, "max": 99999}),
            },
            "optional": {
                "RETRY_SETTING": ("RETRY_SETTING", {"default": None}),
            }
        }
 
    RETURN_TYPES = ("RETRY_SETTING",)
    RETURN_NAMES = ("RETRY_SETTING",)
 
    FUNCTION = "create_retry_setting"
 
    CATEGORY = "RequestNode/KeyValue"
 
    def create_retry_setting(self, key="", value="", RETRY_SETTING=None):
        output = {}
        
        if RETRY_SETTING is not None:
            output.update(RETRY_SETTING)
            
        if key and value:
            output[key] = value
            
        return (output,)

NODE_CLASS_MAPPINGS = {
    "RetrySettingNode": RetrySettingNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "RetrySettingNode": "Retry Settings Node"
}