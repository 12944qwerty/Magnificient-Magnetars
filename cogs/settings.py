import discord
from discord import app_commands
import sqlite3


@app_commands.command()
async def setvalue(interaction: discord.Interaction[discord.Client], value: str):
    """Set value"""
    em = discord.Embed(title="Set Value")
    interaction.client.cur.execute('SELECT 1 FROM guild_settings WHERE guild_id = ?', (interaction.guild_id,))
    row_exists = interaction.client.cur.fetchone()
    if row_exists:
        interaction.client.cur.execute('UPDATE guild_settings SET value = ? WHERE guild_id = ?', (value, interaction.guild_id))
    else:
        interaction.client.cur.execute('INSERT INTO guild_settings (guild_id, value) VALUES (?, ?)', (interaction.guild_id, value))
    interaction.client.con.commit()
    await interaction.response.send_message(embed=em)


@app_commands.command()
async def getvalue(interaction: discord.Interaction[discord.Client]):
    """Get value"""
    em = discord.Embed(title="Get Value")
    interaction.client.cur.execute("SELECT value FROM guild_settings WHERE guild_id = ?", (interaction.guild_id,))
    value = interaction.client.cur.fetchone()
    if (value):
        em.add_field(name="Value", value=f"{value[0]}")
    else:
        em.add_field(name="No value", value="Nothing found")
    await interaction.response.send_message(embed=em)


async def setup(app):
    app.con = sqlite3.connect("db/settings.db")
    app.cur = app.con.cursor()
    app.cur.execute("""CREATE TABLE IF NOT EXISTS guild_settings(
                        guild_id INTEGER PRIMARY KEY,
                        value string);""")
    app.tree.add_command(getvalue)
    app.tree.add_command(setvalue)
