from discord import ChannelType, utils
from discord.ext import commands


async def valid_stuff(ctx: commands.Context) -> bool:
  mods_chann = utils.get(ctx.guild.channels, name = 'moderator-only')

  if not mods_chann:
    await ctx.send("`ERROR`: The server doesn't have a #moderator-only channel")
    return False
  elif mods_chann.type != ChannelType.text:
    await ctx.send("`ERROR`: #moderator-only channel is not a text channel")
    return False

  return True
