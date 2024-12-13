import os
import discord
from discord.ext import commands

# Fetch tokens and IDs from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('VERIFY_CHANNEL_ID'))
ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID'))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in tas {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f'Welcome {member.mention}! Please type `!verify` in this channel to gain access.')

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and message.content == '!verify':
        role = discord.utils.get(message.guild.roles, id=ROLE_ID)
        if role:
            if role.position < message.guild.me.top_role.position:
                # Add role to the user
                await message.author.add_roles(role)
                await message.channel.send(f'{message.author.mention} has been verified!')

                # Delete all messages in the verification channel
                async for msg in message.channel.history(limit=100):  # Adjust limit as needed
                    await msg.delete()

                # Hide the channel for the verified role, but keep it visible for others
                await message.channel.set_permissions(role, send_messages=False, read_messages=False)
                await message.channel.set_permissions(message.guild.default_role, send_messages=True, read_messages=True)
            else:
                await message.channel.send('I do not have permission to add this role.')
        else:
            await message.channel.send('Verification role not found.')

    # Ensure other commands are processed
    await bot.process_commands(message)

bot.run(TOKEN)
