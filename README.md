# Telegram to Discord Forwarder

This script forwards messages from a Telegram chat or channel to a Discord channel. It can be configured to forward all messages or only those containing specific keywords.

## Prerequisites

- Python 3.7 or higher
- Telegram API credentials (API ID, API Hash, Phone Number)
  - Obtain your API ID and API Hash from the [Telegram API development tools](https://my.telegram.org/auth).
- Discord bot token
  - Obtain your Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications).

## Installation

1. Clone the repository:

   `git clone https://github.com/yourusername/telegram-to-discord-forwarder.git`
   `cd telegram-to-discord-forwarder`

2. Create a virtual environment:

   `python -m venv env`

3. Activate the virtual environment:

   - On Windows:
     `.\env\Scripts\activate`

   - On macOS and Linux:
     `source env/bin/activate`

4. Install the required packages:

   `pip install -r requirements.txt`

## Configuration

1. When you run the `run.py` script for the first time, it will prompt you to enter your API ID, API Hash, Phone Number, and Discord bot token. The script will automatically save these credentials to the `credentials.txt` file.

## Usage

1. Run the script:

   python run.py
