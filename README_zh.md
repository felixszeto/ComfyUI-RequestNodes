# ComfyUI-RequestNodes

[English Version](README.md)

## 簡介

ComfyUI-RequestNodes 是一個 ComfyUI 的自定義節點插件，提供用於發送 HTTP 請求的功能。目前包含以下節點：

*   **Get Node**: 發送 GET 請求並獲取響應。
*   **Post Node**: 發送 POST 請求並獲取響應。

## 安裝

要安裝 ComfyUI-RequestNodes，請按照以下步驟操作：

1.  **打開 ComfyUI custom_nodes 目錄。**
    *   在你的 ComfyUI 安裝目錄下，找到 `custom_nodes` 文件夾。

2.  **克隆 ComfyUI-RequestNodes 倉庫。**
    *   在 `custom_nodes` 目錄中打開終端或命令提示符。
    *   運行以下命令來克隆倉庫：

    ```bash
    git clone https://github.com/felixszeto/ComfyUI-RequestNodes.git
    ```

3.  **重啟 ComfyUI。**
    *   關閉並重新啟動 ComfyUI，以加載新安裝的節點。

## 使用方法

安裝完成後，你可以在 ComfyUI 的節點列表中找到 "Request Nodes" 類別下的 "Get Node" 和 "Post Node" 節點。

*   **Get Node**:
    *   **url**: 輸入你要請求的 URL 地址。
    *   **param**: 輸入Param信息key/value。
    *   **output_format**: 選擇響應的輸出格式，例如 "text" 或 "json"。
    *   **response**: 輸出響應內容。

*   **Post Node**:
    *   **url**: 輸入你要請求的 URL 地址。
    *   **data**: 輸入 POST 請求的數據，JSON 格式。
    *   **output_format**: 選擇響應的輸出格式，例如 "text" 或 "json"。
    *   **response**: 輸出響應內容。

## 貢獻

歡迎提交 issue 和 pull request 來改進 ComfyUI-RequestNodes!

---

**注意:**

*   請確保你的 ComfyUI 環境已正確安裝 Git。
*   如果你的 ComfyUI 安裝目錄不在默認位置，請根據你的實際情況調整路徑。
*   如果遇到任何問題，請查看 GitHub 倉庫的 issue 頁面或提交新的 issue。
