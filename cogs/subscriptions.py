import discord
from discord import app_commands

FEEDS = {
    'google': 'https://news.google.com/rss/search?q={CATEGORY}&hl=en-US&gl=US&ceid=US:en'
    'yahoo': 'https://www.yahoo.com/news/rss/{CATEGORY}',
    'washingtonpost': 'https://feeds.washingtonpost.com/rss/{CATEGORY}'
}
CATEGORIES = {
    'world': 'World', # yahoo: world, google: World, wpost: world
    'sports': 'Sports', # yahoo: sport, google: Sports, wpost: sports
    'tech': 'Technology', # yahoo: tech, google: Technology, wpost: business/technology
    'health': 'Health', # yahoo: health, google: Health, wpost: N/A
    'politics': 'Politics', # yahoo: politics, google: Politics, wpost: politics
    'science': 'Science', # yahoo: science, google: Science, wpost: N/A
    'business': 'Business', # yahoo: business, google: Business, wpost: business
}
active_feed = ''

@app_commands.command()
async def subscribe(interaction: discord.Interaction, query: str):
    pass

def sub_to_google():
    pass

def sub_to_yahoo():
    pass

def sub_to_washingtonpost():
    pass


def setup(app):
    active_feed = sub_to_google()
    app.tree.add_command(subscribe)