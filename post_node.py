import requests
import json
import io

class PostRequestNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_url": ("STRING", {"default": "https://example.com/api"}),
                "request_body": ("STRING", {"default": "{}", "multiline": True}),
            },
            "optional": {
                "str0": ("STRING", {"default": ""}),
                "str1": ("STRING", {"default": ""}),
                "str2": ("STRING", {"default": ""}),
                "str3": ("STRING", {"default": ""}),
                "str4": ("STRING", {"default": ""}),
                "str5": ("STRING", {"default": ""}),
                "str6": ("STRING", {"default": ""}),
                "str7": ("STRING", {"default": ""}),
                "str8": ("STRING", {"default": ""}),
                "str9": ("STRING", {"default": ""}),
            }
        }
 
    RETURN_TYPES = ("STRING", "BYTES", "JSON", "ANY")
    RETURN_NAMES = ("text", "file", "json", "any")
 
    FUNCTION = "make_post_request"
 
    CATEGORY = "RequestNode/Post Request"
 
    def make_post_request(self, target_url, request_body, str0="", str1="", str2="", str3="", str4="", str5="", str6="", str7="", str8="", str9=""):
        # 收集所有字符串輸入
        string_inputs = {
            "str0": str0, "str1": str1, "str2": str2, "str3": str3, "str4": str4,
            "str5": str5, "str6": str6, "str7": str7, "str8": str8, "str9": str9
        }
        
        # 替換 request_body 中的佔位符
        for key, value in string_inputs.items():
            placeholder = f"__{key}__"
            if value:  # 只有當值不為空時才進行替換
                request_body = request_body.replace(placeholder, value)
        
        # 嘗試解析 request_body 為 JSON
        try:
            body_data = json.loads(request_body)
        except json.JSONDecodeError:
            body_data = {"error": "Invalid JSON in request_body"}
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(target_url, json=body_data, headers=headers)
            
            # 準備四種不同格式的輸出
            text_output = response.text
            file_output = io.BytesIO(response.content)
            
            try:
                json_output = response.json()
            except json.JSONDecodeError:
                json_output = {"error": "Response is not valid JSON"}
            
            any_output = response.content
            
        except Exception as e:
            error_message = str(e)
            text_output = error_message
            file_output = io.BytesIO(error_message.encode())
            json_output = {"error": error_message}
            any_output = error_message
        
        return (text_output, file_output, json_output, any_output)
 
NODE_CLASS_MAPPINGS = {
    "PostRequestNode": PostRequestNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "PostRequestNode": "POST Request Node"
}
