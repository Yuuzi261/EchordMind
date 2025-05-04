# Contributing to EchordMind

Thank you for your interest in EchordMind! We welcome all forms of contributions, whether it’s reporting bugs, suggesting new features, fixing code, or enhancing documentation. EchordMind is currently in its early development phase, and your involvement is vital in helping us create a robust and friendly Discord bot.

Please read this document before submitting issues or pull requests (PRs) to ensure we have all the necessary details to assist you effectively.

## Ways to Contribute

You can contribute to EchordMind in the following ways:

- **Report Bugs**: If you encounter issues while using the bot, let us know.
- **Suggest Features**: Share ideas for new features or improvements.
- **Submit Code Changes**: Fix bugs, implement features, or optimize code.
- **Update Documentation**: Enhance the README, Wiki, or other documentation.

## Reporting Bugs

When submitting a bug report, please include the following details to help us quickly identify and resolve the issue:

- **Description**: A brief summary of the problem.
- **Steps to Reproduce**: Detailed steps to recreate the issue.
- **Expected Behavior**: What you expected to happen.
- **Actual Behavior**: What actually occurred.
- **Environment**: 
  - Python version
  - discord.py version
  - Other relevant dependencies
  - Discord bot token (do not share sensitive information)
- **Screenshots or Logs**: If applicable, include relevant screenshots or log outputs.

Please open an issue in the GitHub repository to report bugs.

## Suggesting Features

If you have ideas for new features or enhancements, please open an issue and include:

- **Description**: A clear explanation of what you’d like to see implemented.
- **Use Case**: Why this feature would be valuable.
- **Proposed Solution**: If you have thoughts on how to implement it, feel free to share.

## Setting Up the Development Environment

To contribute code, you’ll need to set up the project locally. Follow these steps:

1. **Fork the Repository**: Fork the EchordMind repository on GitHub.
2. **Clone Your Fork**: Clone your fork to your local machine.
   ```bash
   git clone https://github.com/Yuuzi261/EchordMind.git
   cd EchordMind
   ```
3. **Set Up Virtual Environment**: Create and activate a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies**: Install the required dependencies using requirements.txt.
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure Environment Variables**: Create a `.env` file in the root directory and add your Discord bot token and Gemini API key.
   ```env
   USER_ID=your_discord_user_id
   LOG_LEVEL=DEBUG                          # For more debugging info
   DISCORD_BOT_TOKEN=your_discord_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   ```
6. **Configure YAML Files**: Copy the sample configuration files and modify them as needed.
   ```bash
   cp configs/base_setting_sample.yaml configs/base_setting.yaml
   cp configs/exception_message_sample.yaml configs/exception_message.yaml
   cp configs/personality_sample.yaml configs/personality.yaml
   cp configs/role_settings_sample.yaml configs/role_settings.yaml
   ```
7. **Run the Bot**: Start the bot for testing.
   ```bash
   python bot.py
   ```

**Testing Notes**: 
- EchordMind currently supports only direct messages (DMs). Test by sending messages to your bot.
- Ensure the `Message Content Intent` is enabled for your bot in the [Discord Developer Portal](https://discord.com/developers/applications).

## Submitting Changes

When submitting code changes, please follow these steps:

1. **Create a Branch**: Create a new branch from `main` for each set of changes.
   ```bash
   git checkout -b feature/new-feature-name
   ```
2. **Implement Changes**: Make your changes, adhering to the project’s code style (_currently undefined; I code freely. If you have code style suggestions, feel free to propose them. If you want to enforce a style, please include automated formatting tools._).
3. **Write Tests**: If applicable, add tests for your changes. While the project lacks a full test suite, we encourage adding tests for stability.
4. **Update Documentation**: If your changes impact functionality or usage, update the relevant documentation (e.g., README or Wiki).
5. **Commit and Push**: Commit your changes with a descriptive message and push to your branch.
   ```bash
   git commit -m "feat: XXX"
   git push origin feature/new-feature-name
   ```
6. **Open a Pull Request**: Create a pull request from your branch to the `main` branch of the original repository.

## Code of Conduct

This project adheres to the [Code of Conduct](https://github.com/Yuuzi261/EchordMind/blob/main/docs/CODE_OF_CONDUCT.md). By participating, you agree to follow its terms.

## Code Style Guide

- Follow the _yet-to-be-defined_ Python code style.
- Maintain consistency in naming and formatting.

## Asking Questions

If you have questions about the project or need assistance, please:
- Open an issue in the repository.
- Contact the maintainer via [email](mailto:yuuzi261@yuuzi.cc).

## Pull Request Process

After submitting a pull request, the process is as follows:

1. **Review**: The maintainer will review your pull request.
2. **Testing**: Ensure all tests pass. If your changes lack tests, please add them.
3. **Documentation**: Confirm that documentation is up to date.
4. **Merge**: Once approved, your changes will be merged into the `main` branch.

## Additional Notes

- **Testing**: As a Discord bot, EchordMind is typically tested locally by running it and interacting via DMs. Manual testing is the current standard, but automated tests are encouraged.
- **Configuration**: The bot uses YAML files for settings (e.g., personality, error messages). Modify files in the `configs/` directory to test different configurations.
- **Vector Storage**: The project uses ChromaDB for long-term memory storage. Ensure dependencies are properly installed.

Thank you for helping make EchordMind better! 🚀