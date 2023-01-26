import discord
from discord.ext import commands

from valid import valid_stuff
from db import db


async def create_ask(ctx: commands.Context, name: str, role: discord.Role):
  # Looking if the db has the method passed
  coll = db.collection('ask-cmds')
  found = coll.find_one({
    'server': ctx.guild.name,
    'name': name
  })

  if found:
    return await ctx.reply(f'`d?ask {name}` already was created 🥸', delete_after = 3)

  # Inserting the new method in the db
  coll.insert_one({
    'server': ctx.guild.name,
    'name': name,
    'role': role.id
  })

  # Replying with alright message
  await ctx.message.reply(f'Done. `d?ask {name}` was created 😍', delete_after = 3)
  await ctx.message.delete(delay = 3)

@commands.command()
@commands.has_permissions(manage_roles = True, manage_messages = True)
async def create(ctx: commands.Context, method: str, name: str, role: discord.Role):
  valid_status = await valid_stuff(ctx)
  if not valid_status: return

  if method == 'ask':
    await create_ask(ctx, name, role)
  else:
    await ctx.message.reply(f"Wtf? 🤨 What you mean with `d!create {method}`? Try to run `d?help`")
