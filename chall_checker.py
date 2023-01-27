import requests
import dotenv
import os
import json
from logger import print_info
import discord
from discord.ext import tasks, commands


def get_challenges():
    url = os.getenv("URL") + "/api/v1/challenges"
    cookies = {'session': os.getenv("SESSION")}
    challenges = requests.get(url, cookies=cookies).json()

    if not challenges["success"]:
        print("error")
        return -1

    challenges = challenges["data"]

    with open("challenges.json", "w") as wf:
        json.dump(challenges, wf, indent=4)
    print_info("CHALL", "Challenges fetched")
    return challenges


def get_challenges_from_file():
    with open("challenges.json", "r") as rf:
        challenges = json.load(rf)
    return challenges


def format_cat(category):
    if category == "Crypto":
        return "🔒 " + category
    if category == "Reverse":
        return "🤖 " + category
    if category == "Web":
        return "🕸️ " + category
    if category == "System":
        return "🖥️ " + category
    else:
        return "☄️ " + category


class ChallChecker(commands.Cog):
    def __init__(self, bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.challenges = get_challenges_from_file()
        self.check_challenges.start()

    def cog_unload(self):
        self.check_challenges.cancel()

    @commands.command(name="challenges")
    async def challenges(self, ctx):
        challenges = get_challenges()
        await ctx.send(f"Les {len(challenges)} challenges ont été actualisés.")

    # docs loop: https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
    @tasks.loop(minutes=20.0)
    async def check_challenges(self):
        challenges = get_challenges()
        channel = await self.bot.fetch_channel(os.getenv("CHANNEL_ID"))

        if len(self.challenges) == len(challenges):
            # await channel.send(f"Toujours {len(challenges)} challenges sur le site...")
            return

        print_info("NEW", "New challenge found!")
        new = [x for x in challenges if x not in self.challenges]
        self.challenges = challenges
        print(new)

        em = discord.Embed(
            title="Nouveau challenge disponible !", url=os.getenv("URL") + "/challenges", color=0x009aff)
        for c in new:
            em.add_field(
                name=format_cat(c['category']), value=f"**{c['name']}** ({c['value']} points)", inline=False)
        em.set_footer(
            text=f"{len(self.challenges)} challenges maintenant disponibles.", icon_url="https://cdn-icons-png.flaticon.com/512/2164/2164620.png")

        allowed_mentions = discord.AllowedMentions(everyone=True)
        await channel.send("@everyone", embed=em, allowed_mentions=allowed_mentions)

    # def setup(bot):
    #    bot.add_cog(ChallChecker(bot))
