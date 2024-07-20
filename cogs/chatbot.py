import discord
from discord import app_commands
from .utils import chatbot

chatbot = chatbot.MyChatbot()

async def on_message(message: discord.Message):
    if message.author.bot or message.channel.id != 1263602469829611521:
        return
    
    async with message.channel.typing():
        await message.reply(chatbot.send_message(message.author.nick or message.author.name, message.content), mention_author=False)

@app_commands.command(name="ask")
async def ask_command(interaction: discord.Interaction[discord.Client], query: str):
    """Ask the chatbot about anything!"""
    await interaction.response.send_message(chatbot.send_message(interaction.user.nick or interaction.user.name, query))

def setup(app):
    app.tree.add_command(ask_command)
    app.on_message = app.event(on_message)
