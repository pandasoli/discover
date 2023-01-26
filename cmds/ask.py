import discord
from discord import utils
from discord.ui import Button, View

from valid import valid_stuff
from db import db


async def msg_ask(msg: discord.Message, args: list[str]):
  valid_status = await valid_stuff(msg)
  if not valid_status: return

  # Looking if the db has the method passed
  coll = db.collection('ask-cmds')
  found = coll.find_one({
    'server': msg.guild.name,
    'name': args[1]
  })

  if not found:
    return await msg.reply(f'`d?ask {args[1]}` not found')

  # Making life easier
  role = utils.get(msg.guild.roles, id = found['role'])
  text_msg = ' '.join(args[2:])

  mods_chann = utils.get(msg.guild.channels, name = 'moderator-only')

  # Making a message to send at #moderator-only
  view = View()

  async def accept_btn_callback(intr: discord.Interaction):
    member = msg.author

    await member.add_roles(role)

    await msg.channel.send(f"Congratulations {member.mention}. Now you have the {role}' role 🎉")
    await intr.message.delete()

  async def decline_btn_callback(intr: discord.Interaction):
    await intr.message.delete()

  accept_btn = Button(label = 'Accept', style = discord.ButtonStyle.success)
  accept_btn.callback = accept_btn_callback

  decline_btn = Button(label = 'Decline', style = discord.ButtonStyle.danger)
  decline_btn.callback = decline_btn_callback

  view.add_item(accept_btn)
  view.add_item(decline_btn)

  # Sending the message to the mods
  await mods_chann.send(
    f'`{msg.author.name}` asked the role `{role.name}` with this message: ```{text_msg}```',
    view = view
  )

  # Sending reply to the user
  await msg.reply('Your request was sent 🥰! Now, just wait for the staff accept or not.', delete_after = 3)
  await msg.delete(delay = 3)

async def msg_help(msg: discord.Message):
  help_msm = [
    '`d?help`: open this screen',
    '',
    '**For staff**',
    '`d!create`:',
    '    - `ask <name> <role>`: create a way to ask a role',
    '`d!clear <number = 100>`: clear a number of messages of a channel',
    '',
    '**For members**',
    '`d?ask <name> <message...>`: ask a role for the staff',
    '',
    '',
    'Example:',
    '    `d!create ask staff @Staff-Role`',
    '    `d?ask staff Please let be of the staff`'
  ]

  await msg.channel.send('\n'.join(help_msm))

async def ask(msg: discord.Message):
  args = msg.content.split(' ')
  secondary_prefix = 'd?'

  if args[0].startswith(secondary_prefix):
    cmd = args[0][2:]

    if cmd == 'ask':
      await msg_ask(msg, args)
    elif cmd == 'help':
      await msg_help(msg)
