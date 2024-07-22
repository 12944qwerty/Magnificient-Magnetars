import discord
from discord import app_commands
import io
import matplotlib.pyplot as plt
import yfinance


@app_commands.command()
async def stock(interaction: discord.Interaction, ticker: str):

    await interaction.response.defer(ephemeral=False, thinking=True)
    ticker = ticker.upper()
    data_stream = io.BytesIO()

    '''Get information about the stock using yfinance'''
    data = yfinance.download(ticker, period='1y')
    data['Close'].plot()
    current_stock = yfinance.Ticker(ticker)
    current_price = current_stock.info.get('currentPrice')

    '''save and close the file'''
    plt.title(f"{ticker} Stock Prices:")
    plt.savefig(data_stream, format='png', bbox_inches="tight", dpi=80)
    plt.close()

    data_stream.seek(0)
    chart = discord.File(data_stream, filename="stock.png")

    em = discord.Embed(title=f'{ticker} stock prices: ', description=f'Currently worth {current_price}')
    em = em.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
    em = em.set_image(url="attachment://stock.png")

    await interaction.followup.send(embed=em, file=chart)



async def setup(app):
    app.tree.add_command(stock)
