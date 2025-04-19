# ComfyUI-RequestNodes

[中文版本](README_zh.md)

## Introduction

ComfyUI-RequestNodes is a custom node plugin for ComfyUI that provides functionality for sending HTTP requests and related utilities. Currently, it includes the following nodes:

*   **Get Request Node**: Sends GET requests and retrieves responses.
*   **Post Request Node**: Sends POST requests and retrieves responses.
*   **Rest Api Node**: A versatile node for sending various HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS) with retry settings.
*   **Key/Value Node**: Creates key/value pairs for building request parameters, headers, or other dictionary-like structures.
*   **String Replace Node**: Replaces placeholders in a string with provided values.
*   **Retry Settings Node**: Creates retry setting configurations for the Rest Api Node.

## Test Resources

The plugin includes the following test resources:
* `base_flask_server.py` - Python Flask server for testing
* `get_node.json` - GET request workflow template
![7da7547075bfc89220dc8bff1f8c62f](https://github.com/user-attachments/assets/ce9e6f04-1618-433a-8d69-4857a280dc61)
![8b717a369b523e69385f50fe176ccf2](https://github.com/user-attachments/assets/b5f1795a-589d-43df-8e82-a1a079262e5f)
* `post_node.json` - POST request workflow template
![cd28f656ab8ae165db4095d325fa38d](https://github.com/user-attachments/assets/28ad21f5-2949-4c41-8d61-994b9170f37c)
![c7549268846ea3b570462c92acfb16c](https://github.com/user-attachments/assets/12dbd00b-af85-439d-978f-301760536005)

## Installation

To install ComfyUI-RequestNodes, follow these steps:

1.  **Open the ComfyUI custom_nodes directory.**
    *   In your ComfyUI installation directory, find the `custom_nodes` folder.

2.  **Clone the ComfyUI-RequestNodes repository.**
    *   Open a terminal or command prompt in the `custom_nodes` directory.
    *   Run the following command to clone the repository:

    ```bash
    git clone https://github.com/felixszeto/ComfyUI-RequestNodes.git
    ```

3.  **Restart ComfyUI.**
    *   Close and restart ComfyUI to load the newly installed nodes.

## Usage

After installation, you can find the nodes under the "RequestNode" category in the ComfyUI node list, with subcategories like "Get Request", "Post Request", "REST API", and "Utils".

*   **Get Request Node**:
    *   **Category**: RequestNode/Get Request
    *   **Inputs**:
        *   `target_url` (STRING, required): The URL to send the GET request to.
        *   `headers` (KEY_VALUE, optional): Request headers, typically from a Key/Value Node.
        *   `query_list` (KEY_VALUE, optional): Query parameters, typically from a Key/Value Node.
    *   **Outputs**:
        *   `text` (STRING): The response body as text.
        *   `file` (BYTES): The response body as bytes.
        *   `json` (JSON): The response body parsed as JSON (if valid).
        *   `any` (ANY): The raw response content.
    *   ![image](https://github.com/user-attachments/assets/cdb1938f-f8a9-4a4b-a787-90fa4d543523)

*   **Post Request Node**:
    *   **Category**: RequestNode/Post Request
    *   **Inputs**:
        *   `target_url` (STRING, required): The URL to send the POST request to.
        *   `request_body` (STRING, required, multiline): The request body, typically in JSON format. Placeholders like `__str0__`, `__str1__`, ..., `__str9__` can be used and will be replaced by the corresponding optional string inputs.
        *   `headers` (KEY_VALUE, optional): Request headers, typically from a Key/Value Node.
        *   `str0` to `str9` (STRING, optional): String inputs to replace placeholders in `request_body`.
    *   **Outputs**:
        *   `text` (STRING): The response body as text.
        *   `file` (BYTES): The response body as bytes.
        *   `json` (JSON): The response body parsed as JSON (if valid).
        *   `any` (ANY): The raw response content.
    *   ![image](https://github.com/user-attachments/assets/6eda9fef-48cf-478c-875e-6bd6d850bff2)

*   **Rest Api Node**:
    *   **Category**: RequestNode/REST API
    *   **Inputs**:
        *   `target_url` (STRING, required): The URL for the request.
        *   `method` (Dropdown, required): The HTTP method to use (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS).
        *   `request_body` (STRING, required, multiline): The request body (hidden for HEAD, OPTIONS, DELETE methods).
        *   `headers` (KEY_VALUE, optional): Request headers, typically from a Key/Value Node.
        *   `RETRY_SETTING` (RETRY_SETTING, optional): Retry settings, typically from a Retry Settings Node.
    *   **Outputs**:
        *   `text` (STRING): The response body as text.
        *   `file` (BYTES): The response body as bytes.
        *   `json` (JSON): The response body parsed as JSON (if valid). For HEAD requests, this output contains the response headers.
        *   `headers` (DICT): The response headers as a dictionary.
        *   `status_code` (INT): The HTTP status code of the response.
        *   `any` (ANY): The raw response content.

*   **Key/Value Node**:
    *   **Category**: RequestNode/KeyValue
    *   **Inputs**:
        *   `key` (STRING, required): The key name.
        *   `value` (STRING, required): The key value.
        *   `KEY_VALUE` (KEY_VALUE, optional): Connect output from other Key/Value Nodes to merge pairs.
    *   **Outputs**:
        *   `KEY_VALUE` (KEY_VALUE): A dictionary containing the key/value pair(s).
    *   ![image](https://github.com/user-attachments/assets/dfe7dab0-2b1b-4f99-ac6f-89e01d03b7e0)

*   **String Replace Node**:
    *   **Category**: RequestNode/Utils
    *   **Inputs**:
        *   `input_string` (STRING, required, multiline): The string containing placeholders to be replaced.
        *   `placeholders` (KEY_VALUE, optional): Key/Value pairs where keys are placeholders (e.g., `__my_placeholder__`) and values are the replacement strings.
    *   **Outputs**:
        *   `output_string` (STRING): The string with placeholders replaced.

*   **Retry Settings Node**:
    *   **Category**: RequestNode/KeyValue
    *   **Inputs**:
        *   `key` (Dropdown, required): The retry setting key (`max_retry`, `retry_interval`, `retry_until_status_code`, `retry_until_not_status_code`).
        *   `value` (INT, required): The integer value for the retry setting.
        *   `RETRY_SETTING` (RETRY_SETTING, optional): Connect output from other Retry Settings Nodes to merge settings.
    *   **Outputs**:
        *   `RETRY_SETTING` (RETRY_SETTING): A dictionary containing the retry setting(s).

## Contribution

Welcome to submit issues and pull requests to improve ComfyUI-RequestNodes!

---

**Note:**

*   Please ensure that your ComfyUI environment has Git installed correctly.
*   If your ComfyUI installation directory is not in the default location, please adjust the path according to your actual situation.
*   If you encounter any problems, please check the issue page of the GitHub repository or submit a new issue.
