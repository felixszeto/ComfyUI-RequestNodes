import requests
import json

class GetRequestNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_url": ("STRING", {"default": "https://example.com/api"}),
            },
            "optional": {
                "key1": ("STRING", {"default": ""}),
                "value1": ("STRING", {"default": ""}),
                "key2": ("STRING", {"default": ""}),
                "value2": ("STRING", {"default": ""}),
                "key3": ("STRING", {"default": ""}),
                "value3": ("STRING", {"default": ""}),
                "key4": ("STRING", {"default": ""}),
                "value4": ("STRING", {"default": ""}),
                "key5": ("STRING", {"default": ""}),
                "value5": ("STRING", {"default": ""}),
            }
        }
 
    RETURN_TYPES = ("STRING", "BYTES", "JSON", "ANY")
    RETURN_NAMES = ("text", "file", "json", "any")
 
    FUNCTION = "make_get_request"
 
    CATEGORY = "RequestNode/Get Request"
 
    def make_get_request(self, target_url, 
                         key1="", value1="", 
                         key2="", value2="", 
                         key3="", value3="", 
                         key4="", value4="", 
                         key5="", value5=""):
        # 構建參數字典
        params = {}
        
        # 只有當 key 和 value 都不為空時才添加到參數中
        if key1 and value1:
            params[key1] = value1
        if key2 and value2:
            params[key2] = value2
        if key3 and value3:
            params[key3] = value3
        if key4 and value4:
            params[key4] = value4
        if key5 and value5:
            params[key5] = value5
        
        try:
            # 使用構建的參數發送 GET 請求
            response = requests.get(target_url, params=params)
            
            # 準備四種不同格式的輸出
            text_output = response.text
            file_output = response.content  # 直接返回字節串
            
            try:
                json_output = response.json()
            except json.JSONDecodeError:
                json_output = {"error": "Response is not valid JSON"}
            
            any_output = response.content
            
        except Exception as e:
            error_message = str(e)
            text_output = error_message
            file_output = error_message.encode()  # 將錯誤消息轉換為字節串
            json_output = {"error": error_message}
            any_output = error_message.encode()
        
        return (text_output, file_output, json_output, any_output)
 
NODE_CLASS_MAPPINGS = {
    "GetRequestNode": GetRequestNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetRequestNode": "GET Request Node"
}
