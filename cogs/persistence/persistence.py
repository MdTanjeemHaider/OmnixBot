"""
Persistence cog - Restores user nicknames and roles when they rejoin a server.
"""

import discord
from discord.ext import commands
from .database import db
from config import config


class Persistence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload:discord.RawMemberRemoveEvent):
        """Save user data when they leave."""
        user = payload.user
        guild_id = payload.guild_id

        role_ids = []
        for role in user.roles:
            if not role.is_default():
                role_ids.append(role.id)

        db.add_user(user.id, guild_id, user.nick, role_ids)


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        """Restore user data when they rejoin."""
        guild = member.guild

        if not db.user_exists(member.id, guild.id):
            return
        
        nickname, role_ids = db.get_user(member.id, guild.id)

        if config.persistent_roles:
            roles = []
            for role_id in role_ids:
                if guild.get_role(role_id):
                    roles.append(guild.get_role(role_id))
            await member.edit(roles=roles)

        if config.persistent_nicknames:
            await member.edit(nick=nickname)

        db.remove_user(member.id, guild.id)


async def setup(bot):
    await bot.add_cog(Persistence(bot))
