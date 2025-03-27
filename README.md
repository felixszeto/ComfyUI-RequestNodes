# ComfyUI-RequestNodes

[中文版本](README_zh.md)

---
# ComfyUI-RequestNodes

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

*   **Post Node**:
    *   **url**: Enter the URL address you want to request.
    *   **data**: Enter the data for the POST request, in JSON format.
    *   **output_format**: Select the output format of the response, such as "text" or "json".
    *   **response**: Output response content.

## Contribution

Welcome to submit issues and pull requests to improve ComfyUI-RequestNodes!

---

**Note:**

*   Please ensure that your ComfyUI environment has Git installed correctly.
*   If your ComfyUI installation directory is not in the default location, please adjust the path according to your actual situation.
*   If you encounter any problems, please check the issue page of the GitHub repository or submit a new issue.
