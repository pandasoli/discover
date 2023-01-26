from discord.ext import commands

from valid import valid_stuff


@commands.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx: commands.Context, amount = 100):
  valid_status = await valid_stuff(ctx)
  if not valid_status: return

  await ctx.channel.purge(limit = amount)
