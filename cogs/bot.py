import discord
from discord import app_commands


@app_commands.command()
async def info(interaction: discord.Interaction[discord.Client]):
    """Info of bot"""
    app_info = await interaction.client.application_info()
    em = discord.Embed(title=f"Info of {interaction.client.user.display_name}", description=app_info.description)

    em.add_field(name="Guild Count", value=len(interaction.client.guilds))
    users = sum(len(guild.members) for guild in interaction.client.guilds)
    em.add_field(name="Serving # of Users", value=users)

    em.set_author(name=interaction.client.user.display_name, icon_url=interaction.client.user.display_avatar)
    await interaction.response.send_message(embed=em)


@app_commands.command()
async def ping(interaction: discord.Interaction[discord.Client]):
    """Gets the latency of bot"""
    em = discord.Embed(title="Pong!:ping_pong:")
    em.add_field(name="Bot Latency", value=f"{round(interaction.client.latency, 5)}")

    await interaction.response.send_message(embed=em)


async def setup(app):
    app.tree.add_command(info)
    app.tree.add_command(ping)
