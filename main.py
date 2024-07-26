import os

import discord
from cogs import bot, news, summarization, stocks, subscriptions
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]

GUILD = discord.Object(1263144988938735726)


class MyApplication(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="CodeJam 2024",
            ),
            **kwargs,
        )

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """Event that fires pretty much before all other events."""
        await bot.setup(self)
        await news.setup(self)
        await summarization.setup(self)
        await stocks.setup(self)
        await subscriptions.setup(self)

        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

    async def on_ready(self) -> None:
        """Event that is called when the bot is ready."""
        print(f"Successfully logged in as {self.user}\nFound in {len(self.guilds)} guilds")


app = MyApplication()

if __name__ == "__main__":
    app.run(TOKEN)
