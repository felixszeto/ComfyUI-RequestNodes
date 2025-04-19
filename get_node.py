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
                "headers": ("KEY_VALUE", {"default": None}),
                "query_list": ("KEY_VALUE", {"default": []}),
            }
        }
 
    RETURN_TYPES = ("STRING", "BYTES", "JSON", "ANY")
    RETURN_NAMES = ("text", "file", "json", "any")
 
    FUNCTION = "make_get_request"
 
    CATEGORY = "RequestNode/Get Request"
 
    def make_get_request(self, target_url, headers=None, query_list=None):
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)
        

        try:
            response = requests.get(target_url, params=query_list, headers=request_headers)
            
            text_output = response.text
            file_output = response.content
            
            try:
                json_output = response.json()
            except json.JSONDecodeError:
                json_output = {"error": "Response is not valid JSON"}
            
            any_output = response.content
            
        except Exception as e:
            error_message = str(e)
            text_output = error_message
            file_output = error_message.encode()
            json_output = {"error": error_message}
            any_output = error_message.encode()
        
        return (text_output, file_output, json_output, any_output)
 
NODE_CLASS_MAPPINGS = {
    "GetRequestNode": GetRequestNode
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetRequestNode": "Get Request Node"
}
