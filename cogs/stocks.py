import discord
from discord import app_commands
import io
import matplotlib.pyplot as plt
import yfinance
import feedparser


@app_commands.command()
@app_commands.choices(time_periods=[
    discord.app_commands.Choice(name='5 days', value='5d'),
    discord.app_commands.Choice(name='1 month', value='1mo'),
    discord.app_commands.Choice(name='3 months', value='3mo'),
    discord.app_commands.Choice(name='6 months', value='6mo'),
    discord.app_commands.Choice(name='1 year', value='1y'),
    discord.app_commands.Choice(name='2 years', value='2y'),
    discord.app_commands.Choice(name='5 years', value='5y'),
    discord.app_commands.Choice(name='10 years', value='10y'),
    discord.app_commands.Choice(name='Max', value='max'),
    discord.app_commands.Choice(name='YTD', value='ytd'),

])
async def stock(interaction: discord.Interaction, ticker: str, time_periods: discord.app_commands.Choice[str]):

    await interaction.response.defer(ephemeral=False, thinking=True)
    ticker = ticker.upper()
    data_stream = io.BytesIO()

    '''Get information about the stock using yfinance'''
    data = yfinance.download(ticker, period=time_periods.value)
    data['Close'].plot()
    current_stock = yfinance.Ticker(ticker)
    current_price = current_stock.info.get('currentPrice')

    '''save and close the file'''
    plt.title(f"{ticker} Stock Prices:")
    plt.savefig(data_stream, format='png', bbox_inches="tight", dpi=1000)
    plt.close()

    data_stream.seek(0)
    chart = discord.File(data_stream, filename="stock.png")

    em = discord.Embed(
        title=f'{ticker} stock prices: \n {time_periods.name}',
        description=f'Currently worth {current_price} \n \n Related news articles:'
    )
    em = em.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
    em = em.set_image(url="attachment://stock.png")

    rss_url = f'https://news.google.com/rss/search?q={ticker}&hl=en-US&gl=US&ceid=US:en'

    feed = feedparser.parse(rss_url)

    x = 0

    if feed.entries:
        for entry in feed.entries:
            # for every news article add a field for it
            title = entry.title
            link = entry.link
            pubdate = entry.published
            if x < 3:
                em = em.add_field(name=title, value=f'{link} \n Published on {pubdate}', inline=True)

            x = x + 1

    await interaction.followup.send(embed=em, file=chart)


async def setup(app):
    app.tree.add_command(stock)
