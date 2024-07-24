import discord
from discord import app_commands
from enum import Enum


FEEDS = {
    'google': 'https://news.google.com/rss/search?q={CATEGORY}&hl=en-US&gl=US&ceid=US:en',
    'yahoo': 'https://www.yahoo.com/news/rss/{CATEGORY}',
    'w_post': 'https://feeds.washingtonpost.com/rss/{CATEGORY}',
}

class Category(Enum):
    GOOGLE = ('World', 'Sports', 'Technology', 'Health', 'Politics', 'Science', 'Business')
    YAHOO = ('world', 'sport', 'tech', 'health', 'politics', 'science', 'business')
    W_POST = ('world', 'sports', 'business/technology', None, 'politics', None, 'business')

    def __init__(self, world, sports, tech, health, politics, science, business):
        self.world = world
        self.sports = sports
        self.tech = tech
        self.health = health
        self.politics = politics
        self.science = science
        self.business = business


active_feed = ''

@app_commands.command()
async def subscribe(interaction: discord.Interaction, query: str):
    pass

def get_subscription_feed():
    return active_feed

def sub_to_google(requested_category):
    category = getattr(Category.GOOGLE, requested_category)
    return FEEDS['google'].format(CATEGORY=category)

def sub_to_yahoo(requested_category):
    category = getattr(Category.YAHOO, requested_category)
    return FEEDS['yahoo'].format(CATEGORY=category)

def sub_to_washington_post(requested_category):
    category = getattr(Category.W_POST, requested_category)
    return FEEDS['w_post'].format(CATEGORY=category)


def setup(app):
    active_feed = sub_to_google('world')
    app.tree.add_command(subscribe)