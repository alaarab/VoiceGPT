# Discord Chatbot README

This is a Discord chatbot that utilizes the OpenAI ChatGPT-3.5 Turbo API to generate responses to user questions and read them aloud in a voice channel. It also has custom commands that generate random stories based on specific prompts.

## Features

- Connects to Discord and responds to user messages
- Uses OpenAI's ChatGPT-3.5 Turbo API for generating responses
- Reads generated responses aloud in a voice channel using Google Text-to-Speech (gTTS)
- Has custom commands to generate random stories based on specific prompts

## Requirements

- Python 3.7 or later
- `discord.py` library
- `openai` library
- `gtts` library
- FFmpeg executable (required for playing audio in a voice channel)

## Installation

1. Clone the repository
2. Install the required libraries:

    ```
    pip install discord.py openai gtts
    ```

3. Download and install [FFmpeg](https://www.ffmpeg.org/download.html) executable

## Usage

1. Set your OpenAI API key and Discord bot token in the script (replace the placeholders)
2. Run the script:

    ```
    python chatbot.py
    ```

3. Invite the bot to your server using the link provided by Discord's developer portal
4. Interact with the bot by sending commands in a text channel:

- `!ask [question]`: Ask the bot a question and it will generate a response using ChatGPT-3.5 Turbo

## Important Notes

- The bot will read the responses aloud in a voice channel that the command author is currently connected to
- Make sure you have the proper permissions to invite and manage bots on your server
- The bot may require additional permissions for accessing voice channels and sending messages
- The bot's intents are currently set to allow most features, but you may need to adjust them based on your needs

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes. Your contributions are always welcome.
