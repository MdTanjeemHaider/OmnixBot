"""
Configuration loader for the bot. Reads from config.ini or creates from defaults.ini
"""

import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option # Preserve case sensitivity

        # Create a new config.ini if it does not exist
        if not os.path.isfile("config.ini"):
            print("No config.ini found, creating config.ini")
            self.create_config()

        self.config.read("config.ini", encoding="utf-8")

        try:
            # General discord settings
            self.discord_token = self.config.get("Discord", "token")
            self.command_prefix = self.config.get("Discord", "prefix", fallback="~")

            # Persistence cog settings
            self.persistence_cog_enabled = self.config.getboolean("Persistence", "enabled", fallback=True)
            self.persistent_nicknames = self.config.getboolean("Persistence", "nicknames", fallback=True)
            self.persistent_roles = self.config.getboolean("Persistence", "roles", fallback=True)

            # Soundboard cog settings
            self.soundboard_cog_enabled = self.config.getboolean("Soundboard", "enabled", fallback=True)
            self.soundboard_target_dbfs = self.config.getint("Soundboard", "target_dbfs", fallback=-36)
            self.soundboard_max_idle_time = self.config.getint("Soundboard", "max_idle_time", fallback=20)
            self.soundboard_whitelist = []
            whitelist = self.config.get("Soundboard", "whitelist", fallback="")
            if whitelist != "":
                whitelist = whitelist.replace(" ", "")
                whitelist = whitelist.split(",")

                for user_id in whitelist:
                    self.soundboard_whitelist.append(int(user_id))
            self.soundboard_custom_names = {}
            for key, value in self.config.items("SoundboardCustomNames"):
                self.soundboard_custom_names[key] = value

        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}") from e


    def create_config(self):
        """Create config.ini from defaults.ini template."""
        with open("defaults.ini", "r", encoding="utf-8") as file:
            defaults = file.read()

        discord_token = input("Please enter your discord token: ")
        defaults = defaults.replace("YOUR_DISCORD_TOKEN_HERE",  discord_token)

        with open("config.ini", "w", encoding="utf-8") as file:
            file.write(defaults)

        print("Config file created with default values")


config = Config()