import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import Activity, ActivityType
from pypresence import Presence

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='y!')


@client.event
async def on_ready():
  print(f'{client.user.name} is online.')


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  if not reason:
    reason = 'No reason.'
  await member.ban(reason=reason)
  await ctx.send(f'{member.mention} has been banned for: {reason}.')


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  if not reason:
    reason = 'No reason.'
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} has been kicked for: {reason}.')


@client.command()
async def avatar(ctx, member: discord.Member = None):
  if not member:
    member = ctx.author
  if member.is_avatar_animated():
    await ctx.send('I cannot show animated avatars.')
  else:
    await ctx.send(member.avatar_url)


@client.command()
async def userinfo(ctx, member: discord.Member = None):
  if not member:
    member = ctx.author
  embed = discord.Embed(title=f'{member.name}#{member.discriminator}',
                        color=member.color)
  embed.set_thumbnail(url=member.avatar_url)
  embed.add_field(name='ID:', value=member.id)
  embed.add_field(name='Nickname:', value=member.nick, inline=False)
  embed.add_field(name='Date when they joined the server:',
                  value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'),
                  inline=False)
  embed.add_field(name='Date when they joined Discord:',
                  value=member.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                  inline=False)
  await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1000):
  await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  if not reason:
    reason = 'No reason.'
  role = discord.utils.get(ctx.guild.roles, name='Muted')
  if not role:
    role = await ctx.guild.create_role(name='Muted')
    for channel in ctx.guild.channels:
      await channel.set_permissions(role, speak=False, send_messages=False)
  await member.add_roles(role, reason=reason)
  await ctx.send(f'{member.mention} has been muted for: {reason}.')


@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
  if not reason:
    reason = 'No reason.'
  role = discord.utils.get(ctx.guild.roles, name='Muted')
  if role:
    await member.remove_roles(role, reason=reason)
    await ctx.send(f'{member.mention} has been unmuted.')
  else:
    await ctx.send("There's no Muted role.")


client.run(TOKEN)
