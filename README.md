# ComfyUI-RequestNodes

[中文版本](README_zh.md)

## Introduction

ComfyUI-RequestNodes is a custom node plugin for ComfyUI that provides functionality for sending HTTP requests. Currently, it includes the following nodes:

*   **Get Node**: Sends GET requests and retrieves responses.
*   **Post Node**: Sends POST requests and retrieves responses.

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

After installation, you can find the "Get Node" and "Post Node" nodes under the "Request Nodes" category in the ComfyUI node list.

*   **Get Node**:
    *   **url**: Enter the URL address you want to request.
    *   **param**: Enter Param information key/value.
    *   **output_format**: Select the output format of the response, such as "text" or "json".
    *   **response**: Output response content.
    *   ![2051bd17154dbb9ab4b203f955c873a](https://github.com/user-attachments/assets/f1774cfe-66d9-4da6-b77d-35c51247d1f2)



*   **Post Node**:
    *   **url**: Enter the URL address you want to request.
    *   **data**: Enter the data for the POST request, in JSON format.
        *   In the `data` field, you can use placeholders like `__str1__`, `__str2__`, etc. in your JSON request body.
        *   These placeholders will be replaced by the values of input strings `str1`, `str2`, etc. respectively.
        *   For example, if you have an input string named `str1` with the value "example", and your JSON data is `{"key": "__str1__"}`, the actual request body will be `{"key": "example"}`.
    *   **output_format**: Select the output format of the response, such as "text" or "json".
    *   **response**: Output response content.
    *   ![62c32f115bc6aaf8bdf454755275695](https://github.com/user-attachments/assets/1d1e090d-1c4e-4891-9c5e-d1ddcabd06da)

   
## Contribution

Welcome to submit issues and pull requests to improve ComfyUI-RequestNodes!

---

**Note:**

*   Please ensure that your ComfyUI environment has Git installed correctly.
*   If your ComfyUI installation directory is not in the default location, please adjust the path according to your actual situation.
*   If you encounter any problems, please check the issue page of the GitHub repository or submit a new issue.
