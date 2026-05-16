# <img src=resources/icon.gif width="64"> OmnixBot
A modular Discord bot designed to serve as a centralized platform for various server utilities, with the flexibility to expand as needs grow.

# Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Contributing](#contributing)
5. [License](#license)

## Features

### User Persistence
Automatically saves and restores nicknames and roles when members leave and rejoin the server.

### Soundboard
Play audio clips in voice channels using commands or an interactive button menu.

### Text-to-Speech (TTS)
Converts text messages from a designated channel (configurable in `config.ini`) and reads the message out loud to the sender's voice channel.
### Commands
Use `{prefix}help` to display all available commands and their detailed information.

*Note: All commands must start with the prefix set in config.ini (Default is ``~``)*

## Prerequisites
- Python 3.14 or above
- FFmpeg installed (must be in path)
- Discord Bot Token: [Discord Developer Portal](https://discord.com/developers/applications)
- [uv](https://github.com/astral-sh/uv)

## Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/MdTanjeemHaider/omnixbot.git 
    cd omnixbot
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the bot:
   ```bash
   uv run bot.py
   ```

   On your first run, the bot will ask for your discord bot token, paste it and press enter. A `config.ini` file will be created for you to change settings as well.

## Contributing
Contributions, forks, and feedback are all welcome! Feel free to contribute to OmnixBot's development, suggest improvements, or report any issues on the GitHub repository.

## License
OmnixBot is released under the GNU General Public License v3, allowing you to freely use, modify, and distribute the bot in accordance with the terms outlined in the license.