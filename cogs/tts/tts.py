"""
TTS cog - converts text messages to speech in voice channels
"""
import re
import discord
from discord.ext import commands
from config import config
from gtts import gTTS


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_queue = {}

    def clean_message(self, message: discord.Message):
        content = message.content

        # Check if there is any text after removing media
        test_content = content
        test_content = re.sub(r'<a?:[a-zA-Z0-9_]+:\d+>', '', test_content)  # Emojis/GIFs
        test_content = re.sub(r'https?://\S+|www\.\S+', '', test_content)  # Links
        test_content = re.sub(r'<[@#&!]\d+>', '', test_content)  # All mentions
        test_content = test_content.strip()
        if not test_content:
            return ""

        # Replace mentions with display names
        for user in message.mentions:
            content = content.replace(str(user.id), user.display_name)

        # Replace role mentions with role names
        for role in message.role_mentions:
            content = content.replace(str(role.id), role.name)

        # Replace channel mentions with channel names
        for channel in message.channel_mentions:
            content = content.replace(str(channel.id), channel.name)

        # Keep only allowed characters (English alphanumeric + basic punctuation)
        cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?\-:;\"\'()]', '', content)

        return cleaned

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content.startswith(config.command_prefix):
            return

        if message.channel.id != config.tts_channel_id:
            return

        text = self.clean_message(message)
        if not text or not text.strip():
            return

        user = message.author
        reply = message.channel.send
        guild = message.guild

        # Check voice connection
        if not user.voice:
            await reply("You must be in a voice channel to use this!")
            return

        # Google TTS
        tts = gTTS(text, lang='en', slow=False)
        tts.save(f'temp.mp3')

        voice_client = guild.voice_client
        voice_channel = user.voice.channel

        if not voice_client:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)

        try:
            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(discord.FFmpegPCMAudio(source="temp.mp3"))
        except Exception as e:
            print(f'{e}')

async def setup(bot):
    await bot.add_cog(TTS(bot))