"""
Main bot entry point. Loads each cog and starts the bot
"""

import discord
from discord.ext import commands
from config import config

class OmnixBot(commands.Bot):
    async def setup_hook(self):
        cogs = []
        if config.persistence_cog_enabled:
            cogs.append("cogs.persistence.persistence")

        if config.soundboard_cog_enabled:
            cogs.append("cogs.soundboard.soundboard")

        # Load each cog
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f'Loaded {cog}')
            except Exception as e:
                print(f'Failed to load extension {cog}: {e}')

    async def on_ready(self):
        print(f'Logged in as {self.user}')


def main():
    # Required permissions
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    client = OmnixBot(command_prefix=config.command_prefix, intents=intents)

    # Start the bot
    try:
        client.run(config.discord_token)
    except Exception as e:
        print(f'Failed to connect to Discord API: {e}.')


if __name__ == "__main__":
    main()