# 為 EchordMind 貢獻

感謝您對 EchordMind 的興趣！無論是報告錯誤、提出新功能、修正程式碼還是補充文件，我們都歡迎各種形式的貢獻。EchordMind 目前處於早期開發階段，您的參與對我們打造一個強大且友好的 Discord 機器人至關重要。

請在提交問題或拉取請求（Pull Request, PR）之前閱讀本文件，以確保我們能獲得所有必要資訊，順利協助您。

切換語言：[English](https://github.com/Yuuzi261/EchordMind/blob/main/docs/CONTRIBUTING.md) | [繁體中文](https://github.com/Yuuzi261/EchordMind/blob/main/docs/zh-tw/CONTRIBUTING_zh.md)

## 貢獻方式

您可以透過以下方式為 EchordMind 做出貢獻：

- **報告錯誤**：如果您在使用機器人時發現問題，請回報。
- **建議功能**：分享新功能或改進的點子。
- **提交程式碼更改**：修復錯誤、實現功能或優化程式碼。
- **更新文件**：改進 README、Wiki 或其他文件。

## 報告錯誤

提交錯誤報告時，請包含以下資訊，以便我們快速診斷和修復問題：

- **描述**：簡明扼要地描述問題。
- **重現步驟**：詳細說明如何重現問題。
- **預期行為**：您期望的結果。
- **實際行為**：實際發生的結果。
- **環境**：
  - Python 版本
  - discord.py 版本
  - 其他相關依賴項
  - Discord 機器人令牌（請勿分享敏感資訊）
- **螢幕截圖或日誌**：如適用，請提供相關截圖或日誌輸出。

請在 GitHub 儲存庫中開啟一個 Issue 來報告錯誤。

## 建議功能

如果您有新功能或改進的建議，請開啟一個 Issue 並包含：

- **描述**：清楚描述您希望實現的內容。
- **使用場景**：解釋為什麼這個功能有價值。
- **建議解決方案**：如果您有實現的想法，請分享。

## 設置開發環境

要貢獻程式碼，您需要先在本地設置專案。請按照以下步驟操作：

1. **Fork 儲存庫**：在 GitHub 上 Fork EchordMind 儲存庫。
2. **複製您的 Fork**：將您的 Fork 複製到本地。
   ```bash
   git clone https://github.com/Yuuzi261/EchordMind.git
   cd EchordMind
   ```
3. **設置虛擬環境**：創建並啟動虛擬環境。
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 上：venv\Scripts\activate
   ```
4. **安裝依賴項**：使用 requirements.txt 安裝所需依賴。
   ```bash
   pip install -r requirements.txt
   ```
5. **配置環境變數**：在根目錄創建 `.env` 文件，填入您的 Discord 機器人令牌和 Gemini API 密鑰。
   ```env
   USER_ID=您的_discord_用戶ID
   LOG_LEVEL=DEBUG                          # 獲得更多除錯資訊
   LANG=zh-tw                               # 目前支援 en-us, zh-tw
   VECTOR_DB_PATH=data/
   DISCORD_BOT_TOKEN=你的_discord_機器人令牌
   GEMINI_API_KEY=你的_gemini_api_密鑰
   GROK_API_KEY=你的_grok_api_密鑰
   ```
6. **配置 YAML 文件**：複製範例配置文件並根據需要修改。
   ```bash
   cp configs/base_setting_sample.yaml configs/base_setting.yaml
   cp configs/exception_message_sample.yaml configs/exception_message.yaml
   cp configs/personality_sample.yaml configs/personality.yaml
   cp configs/role_settings_sample.yaml configs/role_settings.yaml
   ```
7. **運行機器人**：啟動機器人進行測試。
   ```bash
   python bot.py
   ```

**測試注意事項**：
- EchordMind 目前僅支援私訊（DM），您可以透過向自己的機器人發送訊息來測試。
- 確保您的機器人已在 [Discord Developer Portal](https://discord.com/developers/applications) 中啟用了 `Message Content Intent`。

## 提交更改

提交程式碼更改時，請遵循以下步驟：

1. **創建分支**：為每組更改從 `main` 分支創建一個新分支。
   ```bash
   git checkout -b feature/新功能名稱
   ```
2. **實現更改**：進行更改，遵循專案的程式碼風格（_目前沒有，本人很 free 的在寫，如果有推薦的程式碼風格，歡迎提出。如果要規範程式碼風格，請一併將自動格式化程式碼的功能加入_）。
3. **編寫測試**：如適用，請為您的更改添加測試。雖然目前專案尚未有完整的測試套件，但鼓勵添加測試以提高穩定性。
4. **更新文件**：如果更改影響功能或使用方式，請更新相關文件（例如 README 或 Wiki）。
5. **提交並推送**：使用描述性的提交訊息提交更改並推送到您的分支。
   ```bash
   git commit -m "feat：XXX"
   git push origin feature/新功能名稱
   ```
6. **開啟拉取請求**：從您的分支向原始儲存庫的 `main` 分支創建拉取請求。

## 行為準則

本專案遵循 [行為準則](https://github.com/Yuuzi261/EchordMind/blob/main/docs/CODE_OF_CONDUCT.md)。參與本專案即表示您同意遵守其條款。

## 程式碼風格指南

- 遵循 _尚未規範_ 的 Python 程式碼風格。
- 保持程式碼命名和格式的一致性。

## 提問

如果您對專案有疑問或需要幫助，請：
- 在儲存庫中開啟一個 Issue。
- 透過 [電子郵件](mailto:yuuzi261@yuuzi.cc) 聯繫維護者。

## 拉取請求流程

提交拉取請求後，流程如下：

1. **審查**：維護者將審查您的拉取請求。
2. **測試**：確保所有測試通過。如果您的更改沒有測試，請添加。
3. **文件**：確保文件是最新的。
4. **合併**：審查通過後，您的更改將被合併到 `main` 分支。

## 額外注意事項

- **測試**：由於 EchordMind 是一個 Discord 機器人，測試通常涉及本地運行機器人並透過私訊與其互動。目前以手動測試為主，但鼓勵添加自動化測試。
- **配置**：機器人使用 YAML 文件進行配置（例如個性、錯誤訊息）。測試不同配置時，請修改 `configs/` 目錄中的文件。
- **向量儲存**：專案使用 ChromaDB 進行長期記憶儲存，確保依賴項已正確安裝。

感謝您的支持，讓 EchordMind 變得更好！🚀