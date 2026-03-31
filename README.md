# OmnixBot
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
Play audio sounds in voice channels using commands or an interactive button menu.

#### Soundboard Commands
| Command                                  | Description                                     |
| ---------------------------------------- | ----------------------------------------------- |
| `soundboard` or `sb`                 | Display the interactive soundboard with buttons |
| `soundboard <sound>` or `sb <sound>` | Play a specific sound                           |
| `reload soundboard` or `r sb`        | Refresh the sound list after adding new files   |

*Note: All commands must start with the prefix set in config.ini (Default is ``~``)*

#### Adding Sounds to Soundboard
1. Place MP3 files in `resources/sounds/raw/`
2. Run `reload soundboard` or restart the bot
3. Optional: Add custom display names in `config.ini` under `[SoundboardCustomNames]`:
   ```ini
   [SoundboardCustomNames]
   filename_without_extension = Custom Display Name 😊
   ```

## Prerequisites
- Python 3.14 or above
- FFmpeg installed (must be in path)
- Discord Bot Token: [Discord Developer Portal](https://discord.com/developers/applications)

## Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/MdTanjeemHaider/omnixbot.git 
    cd omnixbot
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   ```

   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

   On your first run, the bot will ask for your discord bot token, paste it and press enter. A `config.ini` file will be created for you to change settings aswell.

## Contributing
Contributions, forks, and feedback are all welcome! Feel free to contribute to OmnixBot's development, suggest improvements, or report any issues on the GitHub repository.

## License
OmnixBot is released under the GNU General Public License v3, allowing you to freely use, modify, and distribute the bot in accordance with the terms outlined in the license.
