import discord
from discord.ext import commands
from discord.ext import tasks
import random
import os

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@client.event
async def on_ready():
    reminder.start()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Old (better) Top Gear")) 
    print("The bot is ready")

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit = amount)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
  await member.send(f"You have been kicked from TMGS, Because:"+reason)
  await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason = "No reason provided"):
  await ctx.send(f"Banned {member.mention}")
  await member.ban(reason=reason)

@client.command(aliases = ['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")

  for ban_entry in banned_users:
    user = ban_entry.user

    if(user.name, user.discriminator)==(member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"Unbanned {user.mention}")
      return

@client.event  
async def on_member_join(member):
    id = client.get_guild(705786268340191262)
    general = client.get_channel(795686321883578369)
    await general.send(member.mention + ' has joined the server B)')

@client.event 
async def on_member_remove(member):
    id = client.get_guild(705786268340191262)
    welcome = client.get_channel(795686321883578369)
    await welcome.send(member.mention + " has left the server B(")

@client.command()
async def tutor(ctx, *, command):
    math_helper = discord.utils.get(ctx.guild.roles, id=739500218479018066)
    await ctx.send(f"{math_helper.mention} please help {ctx.author.mention} with ```{command}```")

@client.command()
async def suggest(ctx,*,message):
    imgembed= discord.Embed(title="Suggestion", description=f"{message}")
    imgembed.set_footer(text=f"From {ctx.author}", icon_url=ctx.author.avatar_url)
# imgembed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    try:
        image = ctx.message.attachments[0].url
        imgembed.set_image(url=image)
    except IndexError:
        image = None
    message = await ctx.send(embed=imgembed)
    await ctx.message.delete()
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@client.event
async def on_member_join(member):
    mbed = discord.Embed(colour=discord.Colour.green(), title="**Welcome Message**", description="Welcome to Top Gear Maths Shed! We hope you enjoy your stay :D")
    mbed.add_field(name="**Name**", value=member.name, inline=True)
    mbed.set_thumbnail(url = member.avatar_url)
    await member.send(embed=mbed)

@tasks.loop(hours = 2)
async def reminder():
  bump = client.get_channel(722434817773404192)
  await bump.send("REMINDER TO BUMP THIS SERVER")

client.run("token not gonna be revealed :)")
