import discord
import dotenv
import os
from discord.ext import commands
from chall_checker import ChallChecker

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=";", intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over new challenges..."))

    try:
        await bot.add_cog(ChallChecker(bot))
    except Exception as e:
        print('{}: {}'.format(type(e).__name__, e))

    print(f'Logged in as {bot.user.name} on {len(bot.guilds)} servers')


@bot.event
async def on_command_error(ctx, error):
    print(f"ERR - {ctx.command} - {error}")

dotenv.load_dotenv()
bot.run(os.getenv('TOKEN'))
