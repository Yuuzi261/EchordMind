# EchordMind

<!-- [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blue)](https://discordpy.readthedocs.io/en/stable/) -->

EchordMind 是一個利用 AI 在 Discord 上進行智慧、具上下文感知對話的機器人。它會記住過去的互動，提供個人化的體驗，讓每次對話都像與一個學習成長的夥伴交流。

上面那一段是 AI 寫的，簡單來說就是你可以自己做一個你最好的損友、女朋友、一個只會蛤的羊駝或是戰鬥直升機... 然後在 Discord 上跟他聊天👀。

> [!NOTE]
> 現在 EchordMind 還在早期開發階段，README 中的內容可能會過時或有誤，如果您有任何建議或問題，歡迎隨時在 [Issue](https://github.com/Yuuzi261/EchordMind/issues) 提出。

> [!NOTE]
> EchordMind是一個暫定的名字，如果你有更好的點子，歡迎提出

## 功能

- **對話處理**：在私訊中與用戶進行具上下文感知的回應。
- **記憶系統**：使用短期和長期記憶來維持對話連貫性。
- **AI 整合**：透過 LLMs API 實現自然語言理解與生成。
- **可配置設置**：透過 YAML 文件自訂機器人的個性、語言和行為。
- **模組化架構**：設計具擴展性，便於添加新功能或整合。

## 安裝

### Discord 設定部分

1. 先到 [Discord Developer Portal](https://discord.com/developers/applications) 創建一個新的應用程式。

2. 到 Installation 頁面，確保 `User Install` 已選擇。

3. 到 Bot 頁面，將特權意圖中的 `Message Content Intent` 勾選並保存。

4. 到 OAuth2 頁面，將 `applications.commands` 勾選。Integration Type 的部分改選 `User Install`，並複製產生的 URL。

5. 用任何方式點開 URL 後，同意授權。

### 程式運行部分

1. **複製儲存庫**
    ```bash
    git clone https://github.com/Yuuzi261/EchordMind.git
    cd EchordMind
    ```

2. **設置虛擬環境**
    ```bash
    python -m venv venv
    source venv/bin/activate  # 在 Windows 上：venv\Scripts\activate
    ```

3. **安裝依賴套件**
    ```bash
    pip install -r requirements.txt
    ```

4. **配置環境變數**
    在根目錄中創建一個 `.env` 文件：
    ```env'
    USER_ID=你的_discord_用戶ID
    LOG_LEVEL=INFO
    DISCORD_BOT_TOKEN=你的_discord_機器人令牌
    GEMINI_API_KEY=你的_gemini_api_密鑰
   ```
   > **注意**：`USER_ID` 目前用於在機器人啟動時發送測試訊息。此為臨時功能，未來版本可能會移除。~~不過必須承認這個方法挺有用，至少對個人使用來說...~~

5. **配置 YAML 文件**
   複製範例配置文件並進行自訂：
   ```bash
   cp configs/base_setting_sample.yaml configs/base_setting.yaml
   cp configs/exception_message_sample.yaml configs/exception_message.yaml
   cp configs/personality_sample.yaml configs/personality.yaml
   cp configs/role_settings_sample.yaml configs/role_settings.yaml
   ```

6. **運行機器人**
   ```bash
   python bot.py
   ```

## 使用方法

向機器人發送私訊以開始對話。機器人將根據其配置的個性和過去的互動進行回應。

**示例對話**：

**用戶**：嗨，我在計劃去日本旅行。  
**機器人**：聽起來真有趣！日本文化很豐富。你有沒有特定的目的地？  
**用戶**：東京和京都。  
**機器人**：很棒的選擇！東京很熱鬧，京都充滿歷史。需要活動建議嗎？  
*(稍後)*  
**用戶**：我之前提過日本，現在想加大阪。  
**機器人**：是的，我記得東京和京都！大阪是個很棒的補充，以美食聞名。想聽些菜餚建議嗎？

> [!NOTE]
> 此例子僅供參考，未來等開發比較完整後會在這裡附上真實的對話。

## 配置

機器人的行為可透過 `configs/` 目錄中的 YAML 文件進行自訂：

- **`base_setting.yaml`**：通用設置，如語言 (`lang`)、時間戳提示和天氣提示。
- **`exception_message.yaml`**：各種場景的自訂錯誤訊息（例如 API 失敗）。
- **`personality.yaml`**：透過 `system_prompt` 和摘要設置定義機器人個性。
- **`role_settings.yaml`**：指定對話追蹤的角色（例如 `user`、`model`）。

## 工作原理

EchordMind 結合短期和長期記憶來維持對話上下文：

- **短期記憶**：將最近的對話回合儲存在記憶中。
- **中期記憶**：尚未實作，以後可能會有，類似長期記憶，但比較近期。
- **長期記憶**：在向量數據庫中摘要並儲存重要對話內容，以便後續檢索。

當用戶發送訊息時：
1. 機器人使用向量搜索檢索相關的長期記憶。
2. 將其與短期對話歷史相結合。
3. LLMs 根據此上下文生成回應。
4. 回應發送給用戶，對話內容更新至記憶中。

此系統使機器人能在多次互動中保持連貫、具上下文感知的對話。

## 貢獻

歡迎貢獻！請閱讀 [貢獻指南](https://github.com/Yuuzi261/EchordMind/blob/main/docs/CONTRIBUTING.md) 以了解如何貢獻，包括編碼標準和工作流程。
~~_不過在這之前可能要先有人幫我寫好這個檔案，因為我還沒想好 CONTRIBUTING.md 的內容應該怎麼寫。_~~

## 許可證

此項目採用 [MIT 許可證](https://github.com/Yuuzi261/EchordMind/blob/main/LICENSE)。

---

欲了解更多詳細資訊，請參閱 [項目 wiki](https://github.com/Yuuzi261/EchordMind/wiki)。