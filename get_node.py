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
                "headers": ("DICT", {"default": None}),
                "json_array": ("LIST", {"default": []}),
            }
        }
 
    RETURN_TYPES = ("STRING", "BYTES", "JSON", "ANY")
    RETURN_NAMES = ("text", "file", "json", "any")
 
    FUNCTION = "make_get_request"
 
    CATEGORY = "RequestNode/Get Request"
 
    def make_get_request(self, target_url, headers=None, json_array=None):
        # 構建參數字典
        params = {}
        
        # 合併json_array中的所有JSON
        if json_array:
            for json_obj in json_array:
                if isinstance(json_obj, dict):
                    params.update(json_obj)
        
        # 設置默認headers
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)
        

        try:
            # 使用構建的參數發送 GET 請求
            response = requests.get(target_url, params=params, headers=request_headers)
            
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
