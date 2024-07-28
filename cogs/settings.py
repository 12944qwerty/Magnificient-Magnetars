import discord
from discord import app_commands
import sqlite3

async def setvalue(client, guild_id, key, value):
    client.cur.execute('SELECT 1 FROM guild_settings WHERE guild_id = ?', (guild_id,))
    row_exists = client.cur.fetchone()
    if row_exists:
        client.cur.execute(f'UPDATE guild_settings SET {key} = ? WHERE guild_id = ?', (value, guild_id))
    else:
        client.cur.execute(f'INSERT INTO guild_settings (guild_id, {key}) VALUES (?, ?)', (guild_id, value))
    client.con.commit()


async def getvalue(client, guild_id, key):
    client.cur.execute(f"SELECT {key} FROM guild_settings WHERE guild_id = ?", (guild_id,))
    value = client.cur.fetchone()
    return value[0] if value else None

@app_commands.guild_only()
class Settings(app_commands.Group):
    """Configurable settings for the bot"""
    async def interaction_check(self, interaction: discord.Interaction[discord.Client]):
        if interaction.user.guild_permissions.administrator:
            return True
        await interaction.response.send_message("You need to be an administrator to use this command.", ephemeral=True)
        return False

@app_commands.command(name="add_channel")
async def add_channel(interaction: discord.Interaction[discord.Client], channel: discord.TextChannel):
    """Add a channel to the activated chatbot channels"""
    activated_channels = await getvalue(interaction.client, interaction.guild.id, "activated_channels")
    if activated_channels:
        activated_channels = activated_channels.split(",")
    else:
        activated_channels = []
    activated_channels.append(str(channel.id))
    await setvalue(interaction.client, interaction.guild.id, "activated_channels", ",".join(activated_channels))
    await interaction.response.send_message(f"Added {channel.mention} to activated channels.")
    
@app_commands.command(name="remove_channel")
async def remove_channel(interaction: discord.Interaction[discord.Client], channel: discord.TextChannel):
    """Remove a channel from the activated chatbot channels"""
    activated_channels = await getvalue(interaction.client, interaction.guild.id, "activated_channels")
    if activated_channels:
        activated_channels = activated_channels.split(",")
    else:
        activated_channels = []
    activated_channels.remove(str(channel.id))
    await setvalue(interaction.client, interaction.guild.id, "activated_channels", ",".join(activated_channels))
    await interaction.response.send_message(f"Removed {channel.mention} from activated channels.")
    
@app_commands.command(name="list_channels")
async def list_channels(interaction: discord.Interaction[discord.Client]):
    """List all activated chatbot channels"""
    activated_channels = await getvalue(interaction.client, interaction.guild.id, "activated_channels")
    if activated_channels:
        activated_channels = activated_channels.split(",")
    else:
        activated_channels = []
    channels = [interaction.guild.get_channel(int(channel_id)) for channel_id in activated_channels]
    await interaction.response.send_message("Activated Channels:\n" + "\n".join([channel.mention for channel in channels]) or "No activated channels.")

async def setup(app):
    app.con = sqlite3.connect("db/settings.db")
    app.cur = app.con.cursor()
    app.cur.execute("""CREATE TABLE IF NOT EXISTS guild_settings(
                        guild_id INTEGER PRIMARY KEY,
                        activated_channels TEXT);""")
    
    settings = Settings()
    settings.add_command(add_channel)
    settings.add_command(remove_channel)
    settings.add_command(list_channels)
    app.tree.add_command(settings)
