"""
Soundboard cog - plays audio in voice channels with buttons or commands.
"""

import os
import discord
from discord.ext import commands
from config import config
from .utils import normalize_and_fetch


def split_list(lst, chunk_size):
    """Split list into chunks of specified size."""
    result = []
    for i in range(0, len(lst), chunk_size):
        result.append(lst[i:i + chunk_size])

    return result


class Soundboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.raw_folder = "resources/sounds/raw/"
        self.normalized_folder = "resources/sounds/normalized/"
        self.target_dbfs = config.soundboard_target_dbfs
        self.custom_names = config.soundboard_custom_names

        # Create folders if they don't exist
        os.makedirs(self.raw_folder, exist_ok=True)
        os.makedirs(self.normalized_folder, exist_ok=True)

        self.sounds = normalize_and_fetch(self.raw_folder, self.normalized_folder, self.target_dbfs)

    @commands.group(name="soundboard", aliases=["sb"], case_insensitive=True, invoke_without_command=True)
    async def soundboard(self, context: commands.Context):
        # If incorrect arguments were passed
        if len(context.message.content.split()) > 1:
            await context.send(f"Invalid subcommand! Use {context.prefix}help sb to see available commands.")
            return

        if len(self.sounds) == 0:
            await context.send("No sounds found!")
            return

        await self.show_soundboard(context)

    @soundboard.command(name="play", aliases=["p"])
    async def play_command(self, context: commands.Context, *, sound_name:str):
        if not sound_name:
            await context.send("Sound name is required!")
            return

        sound_path = os.path.join(self.normalized_folder, f"{sound_name.lower()}.mp3")
        if sound_path not in self.sounds:
            await context.send(f"Sound '{sound_name}' not found!")
            return

        await self.play_sound(context, sound_path, is_interaction=False)

    @soundboard.command(name="add")
    async def add_command(self, context: commands.Context):
        # Check permissions
        if not context.author.guild_permissions.administrator and context.author.id not in config.soundboard_whitelist:
            await context.send("You must be administrator (or whitelisted) to add commands!")
            return

        if not context.message.attachments:
            await context.send("Please attach an audio file with the command!")
            return

        failed_files = ""
        success_count = 0
        for attachment in context.message.attachments:
            filename = attachment.filename.lower()
            if not filename.endswith(".mp3"):
                failed_files += f"\n{filename}: Not a mp3!"
                continue

            # Check if file already exists
            raw_path = os.path.join(self.raw_folder, filename)
            if os.path.exists(raw_path):
                failed_files += f"\n{filename}: File already exists!"
                continue

            try:
                await attachment.save(raw_path)
                success_count += 1
            except Exception as e:
                failed_files += f"\n{filename}: {e}"

        self.sounds = normalize_and_fetch(self.raw_folder, self.normalized_folder, self.target_dbfs)

        if success_count > 0:
            await context.send(f"Successfully added {success_count} sounds!")
        if len(failed_files) != 0:
            await context.send(f"Errors:{failed_files}")

    async def play_sound(self, context, sound_path, is_interaction):
        """Connect to voice channel and play the sound."""
        if is_interaction:
            await context.response.defer(ephemeral=True)
            user = context.user
            reply = context.followup.send
            ephemeral = True
        else:
            user = context.author
            reply = context.send
            ephemeral = False
        guild = context.guild

        # Check voice connection
        if not user.voice:
            await reply("You must be in a voice channel to use this!", ephemeral=ephemeral)
            return

        voice_client = guild.voice_client
        voice_channel = user.voice.channel

        if not voice_client:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)

        try:
            if voice_client.is_playing():
                voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(sound_path))
        except Exception as e:
            print(f'Failed to play sound: {e}')

    def create_sound_button(self, sound_path):
        """Create a button for a sound."""
        sound_name = os.path.splitext(os.path.basename(sound_path))[0]
        label = self.custom_names.get(sound_name, sound_name)

        button = discord.ui.Button(label=label, style=discord.ButtonStyle.primary)

        async def callback(interaction, path=sound_path):
            await self.play_sound(interaction, path, is_interaction=True)

        button.callback = callback
        return button

    async def show_soundboard(self, context):
        """Display the soundboard with buttons."""
        sounds_per_view = 30
        sound_views = split_list(self.sounds, sounds_per_view)

        for i, sound_batch in enumerate(sound_views):
            layout_view = discord.ui.LayoutView()
            if i == 0:
                layout_view.add_item(discord.ui.TextDisplay("## 🔊 Soundboard 🔊"))
                layout_view.add_item(discord.ui.Separator())

            action_row = discord.ui.ActionRow()
            button_count = 0

            for sound in sound_batch:
                button = self.create_sound_button(sound)
                action_row.add_item(button)
                button_count += 1

                # Create a new action row every 5 button
                if button_count == 5:
                    layout_view.add_item(action_row)
                    action_row = discord.ui.ActionRow()
                    button_count = 0

            # Remaining action row
            if button_count > 0:
                layout_view.add_item(action_row)

            await context.send(view=layout_view)

    @soundboard.command(name="reload", aliases=["r"])
    async def reload_command(self, context: commands.Context):
        """Reload sounds from the raw folder."""
        self.sounds = normalize_and_fetch(self.raw_folder, self.normalized_folder, self.target_dbfs)
        await context.send("Reloaded sounds!")


async def setup(bot):
    await bot.add_cog(Soundboard(bot))