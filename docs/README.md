# EchordMind

<!-- [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blue)](https://discordpy.readthedocs.io/en/stable/) -->

EchordMind is a Discord bot that uses AI to engage in intelligent, context-aware conversations. It remembers past interactions, providing a personalized experience, making each conversation feel like interacting with a learning and growing companion.

The above description was written by AI. Simply put, you can create your best buddy, girlfriend, a llama that only says "hmm", or even a combat helicopter... and chat with them on Discord 👀.

> [!NOTE]
> EchordMind is currently in early development stages. The content in this README may be outdated or incorrect. If you have any suggestions or issues, feel free to raise them in the [Issues](https://github.com/Yuuzi261/EchordMind/issues) section.

> [!NOTE]
> The name "EchordMind" is tentative. If you have a better idea, feel free to suggest one.

Switch Language: [English](https://github.com/Yuuzi261/EchordMind/blob/main/docs/README.md) | [繁體中文](https://github.com/Yuuzi261/EchordMind/blob/main/docs/zh-tw/README_zh.md)

## Features

- **Conversation Handling**: Responds to users in direct messages with context-aware replies.
- **Memory System**: Uses short-term and long-term memory to maintain conversation continuity.
- **AI Integration**: Implements natural language understanding and generation through LLMs API.
- **Configurable Settings**: Customize the bot's personality, language, and behavior via YAML files.
- **Modular Architecture**: Designed for scalability, making it easy to add new features or integrations.

## Installation

### Discord Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. On the **Installation** page, ensure that `User Install` is selected.
3. On the **Bot** page, check the `Message Content Intent` under Privileged Gateway Intents and save.
4. On the **OAuth2** page, check `applications.commands`. For Integration Type, select `User Install`, and copy the generated URL.
5. Open the URL in any way and authorize the bot.

### Program Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Yuuzi261/EchordMind.git
    cd EchordMind
    ```

2. **Set Up Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    USER_ID=your_discord_user_id
    LOG_LEVEL=INFO
    DISCORD_BOT_TOKEN=your_discord_bot_token
    GEMINI_API_KEY=your_gemini_api_key
    ```
    > **Note**: `USER_ID` is currently used to send a test message when the bot starts. This is a temporary feature and may be removed in future versions. ~~Admittedly, this method is quite useful, at least for personal use...~~

5. **Configure YAML Files**
    Copy the sample configuration files and customize them:
    ```bash
    cp configs/base_setting_sample.yaml configs/base_setting.yaml
    cp configs/exception_message_sample.yaml configs/exception_message.yaml
    cp configs/personality_sample.yaml configs/personality.yaml
    cp configs/role_settings_sample.yaml configs/role_settings.yaml
    ```

6. **Run the Bot**
    ```bash
    python bot.py
    ```

## Usage

Send a direct message to the bot to start a conversation. The bot will respond based on its configured personality and past interactions.

**Example Conversation**:

**User**: Hi, I'm planning a trip to Japan.  
**Bot**: That sounds exciting! Japan has a rich culture. Do you have any specific destinations in mind?  
**User**: Tokyo and Kyoto.  
**Bot**: Great choices! Tokyo is vibrant, and Kyoto is full of history. Need any activity suggestions?  
*(Later)*  
**User**: I mentioned Japan earlier, now I want to add Osaka.  
**Bot**: Yes, I remember Tokyo and Kyoto! Osaka is a fantastic addition, famous for its food. Want some dish recommendations?

> [!NOTE]
> This example is for reference only. Once development is more complete, real conversation examples will be provided here.

## Configuration

The bot's behavior can be customized through YAML files in the `configs/` directory:

- **`base_setting.yaml`**: General settings, such as default model temperature, timestamp prompts, and weather prompts.
- **`exception_message.yaml`**: Custom error messages for various scenarios (e.g., API failures).
- **`personality.yaml`**: Defines the bot's personality through `system_prompt` and summarization settings.
- **`role_settings.yaml`**: Specifies roles for conversation tracking (e.g., `user`, `model`).

## How it works

EchordMind combines short-term and long-term memory to maintain conversation context:

- **Short-term Memory**: Stores recent conversation turns in memory.
- **Mid-term Memory**: Not yet implemented, may be added in the future, similar to long-term memory but more recent.
- **Long-term Memory**: Summarizes and stores important conversation content in a vector database for future retrieval.

When a user sends a message:
1. The bot retrieves relevant long-term memories using vector search.
2. Combines them with the short-term conversation history.
3. LLMs generate a response based on this context.
4. The response is sent to the user, and the conversation is updated in memory.

This system enables the bot to maintain coherent, context-aware conversations across multiple interactions.

## Contribution

Contributions are welcome! Please read the [Contribution Guide](https://github.com/Yuuzi261/EchordMind/blob/main/docs/CONTRIBUTING.md) to learn how to contribute, including coding standards and workflow.

## License

This project is licensed under the [MIT License](https://github.com/Yuuzi261/EchordMind/blob/main/LICENSE).

---

For more detailed information, please refer to the [project wiki](https://github.com/Yuuzi261/EchordMind/wiki).