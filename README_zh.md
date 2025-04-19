# ComfyUI-RequestNodes

[English Version](README.md)

## 介紹

ComfyUI-RequestNodes 是一個用於 ComfyUI 的自訂節點插件，提供了發送 HTTP 請求及相關實用工具的功能。目前，它包含以下節點：

*   **Get Request Node**: 發送 GET 請求並檢索響應。
*   **Post Request Node**: 發送 POST 請求並檢索響應。
*   **Rest Api Node**: 一個多功能的節點，用於發送各種 HTTP 方法 (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS) 並支援重試設定。
*   **Key/Value Node**: 創建鍵/值對，用於構建請求參數、標頭或其他類似字典的結構。
*   **String Replace Node**: 使用提供的值替換字串中的佔位符。
*   **Retry Settings Node**: 為 Rest Api Node 創建重試設定配置。

## 測試資源

插件包含以下測試資源：
* `base_flask_server.py` - 用於測試的 Python Flask 伺服器
* `get_node.json` - GET 請求工作流程模板
![7da7547075bfc89220dc8bff1f8c62f](https://github.com/user-attachments/assets/ce9e6f04-1618-433a-8d69-4857a280dc61)
![8b717a369b523e69385f50fe176ccf2](https://github.com/user-attachments/assets/b5f1795a-589d-43df-8e82-a1a079262e5f)
* `post_node.json` - POST 請求工作流程模板
![cd28f656ab8ae165db4095d325fa38d](https://github.com/user-attachments/assets/28ad21f5-2949-4c41-8d61-994b9170f37c)
![c7549268846ea3b570462c92acfb16c](https://github.com/user-attachments/assets/12dbd00b-af85-439d-978f-301760536005)

## 安裝

要安裝 ComfyUI-RequestNodes，請按照以下步驟操作：

1.  **打開 ComfyUI 的 custom_nodes 目錄。**
    *   在您的 ComfyUI 安裝目錄中，找到 `custom_nodes` 資料夾。

2.  **克隆 ComfyUI-RequestNodes 儲存庫。**
    *   在 `custom_nodes` 目錄中打開終端或命令提示符。
    *   運行以下命令克隆儲存庫：

    ```bash
    git clone https://github.com/felixszeto/ComfyUI-RequestNodes.git
    ```

3.  **重新啟動 ComfyUI。**
    *   關閉並重新啟動 ComfyUI 以載入新安裝的節點。

## 使用方法

安裝後，您可以在 ComfyUI 節點列表的 "RequestNode" 分類下找到這些節點，並有 "Get Request", "Post Request", "REST API", 和 "Utils" 等子分類。

*   **Get Request Node**:
    *   **分類**: RequestNode/Get Request
    *   **輸入**:
        *   `target_url` (STRING, 必需): 要發送 GET 請求的 URL。
        *   `headers` (KEY_VALUE, 可選): 請求標頭，通常來自 Key/Value Node。
        *   `query_list` (KEY_VALUE, 可選): 查詢參數，通常來自 Key/Value Node。
    *   **輸出**:
        *   `text` (STRING): 響應主體作為文本。
        *   `file` (BYTES): 響應主體作為字節。
        *   `json` (JSON): 響應主體解析為 JSON (如果有效)。
        *   `any` (ANY): 原始響應內容。
    *   ![image](https://github.com/user-attachments/assets/cdb1938f-f8a9-4a4b-a787-90fa4d543523)

*   **Post Request Node**:
    *   **分類**: RequestNode/Post Request
    *   **輸入**:
        *   `target_url` (STRING, 必需): 要發送 POST 請求的 URL。
        *   `request_body` (STRING, 必需, 多行): 請求主體，通常為 JSON 格式。可以使用 `__str0__`, `__str1__`, ..., `__str9__` 等佔位符，它們將被對應的可選字串輸入替換。
        *   `headers` (KEY_VALUE, 可選): 請求標頭，通常來自 Key/Value Node。
        *   `str0` 到 `str9` (STRING, 可選): 用於替換 `request_body` 中佔位符的字串輸入。
    *   **輸出**:
        *   `text` (STRING): 響應主體作為文本。
        *   `file` (BYTES): 響應主體作為字節。
        *   `json` (JSON): 響應主體解析為 JSON (如果有效)。
        *   `any` (ANY): 原始響應內容。
    *   ![image](https://github.com/user-attachments/assets/6eda9fef-48cf-478c-875e-6bd6d850bff2)

*   **Rest Api Node**:
    *   **分類**: RequestNode/REST API
    *   **輸入**:
        *   `target_url` (STRING, 必需): 請求的 URL。
        *   `method` (下拉選單, 必需): 要使用的 HTTP 方法 (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)。
        *   `request_body` (STRING, 必需, 多行): 請求主體 (對於 HEAD, OPTIONS, DELETE 方法會隱藏)。
        *   `headers` (KEY_VALUE, 可選): 請求標頭，通常來自 Key/Value Node。
        *   `RETRY_SETTING` (RETRY_SETTING, 可選): 重試設定，通常來自 Retry Settings Node。
    *   **輸出**:
        *   `text` (STRING): 響應主體作為文本。
        *   `file` (BYTES): 響應主體作為字節。
        *   `json` (JSON): 響應主體解析為 JSON (如果有效)。對於 HEAD 請求，此輸出包含響應標頭。
        *   `headers` (DICT): 響應標頭作為字典。
        *   `status_code` (INT): 響應的 HTTP 狀態碼。
        *   `any` (ANY): 原始響應內容。

*   **Key/Value Node**:
    *   **分類**: RequestNode/KeyValue
    *   **輸入**:
        *   `key` (STRING, 必需): 鍵名。
        *   `value` (STRING, 必需): 鍵值。
        *   `KEY_VALUE` (KEY_VALUE, 可選): 連接其他 Key/Value Node 的輸出以合併鍵值對。
    *   **輸出**:
        *   `KEY_VALUE` (KEY_VALUE): 包含鍵值對的字典。
    *   ![image](https://github.com/user-attachments/assets/dfe7dab0-2b1b-4f99-ac6f-89e01d03b7e0)

*   **String Replace Node**:
    *   **分類**: RequestNode/Utils
    *   **輸入**:
        *   `input_string` (STRING, 必需, 多行): 包含要替換的佔位符的字串。
        *   `placeholders` (KEY_VALUE, 可選): 鍵值對，其中鍵是佔位符 (例如，`__my_placeholder__`)，值是替換字串。
    *   **輸出**:
        *   `output_string` (STRING): 替換佔位符後的字串。

*   **Retry Settings Node**:
    *   **分類**: RequestNode/KeyValue
    *   **輸入**:
        *   `key` (下拉選單, 必需): 重試設定的鍵 (`max_retry`, `retry_interval`, `retry_until_status_code`, `retry_until_not_status_code`)。
        *   `value` (INT, 必需): 重試設定的整數值。
        *   `RETRY_SETTING` (RETRY_SETTING, 可選): 連接其他 Retry Settings Node 的輸出以合併設定。
    *   **輸出**:
        *   `RETRY_SETTING` (RETRY_SETTING): 包含重試設定的字典。

## 貢獻

歡迎提交 issues 和 pull requests 來改進 ComfyUI-RequestNodes！

---

**注意：**

*   請確保您的 ComfyUI 環境已正確安裝 Git。
*   如果您的 ComfyUI 安裝目錄不在默認位置，請根據您的實際情況調整路徑。
*   如果您遇到任何問題，請查看 GitHub 儲存庫的 issue 頁面或提交新的 issue。
