import requests
import json
import io

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
 
    def make_request(self, target_url, method, request_body, headers=None, RETRY_SETTING=None):
        
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
        
        params = {}
        body_data = None
        
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body_data = json.loads(request_body)
            except json.JSONDecodeError:
                body_data = {"error": "Invalid JSON in request_body"}
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
                return requests.post(target_url, json=body_data, headers=request_headers)
            elif method == "PUT":
                return requests.put(target_url, json=body_data, headers=request_headers)
            elif method == "DELETE":
                return requests.delete(target_url, headers=request_headers)
            elif method == "PATCH":
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