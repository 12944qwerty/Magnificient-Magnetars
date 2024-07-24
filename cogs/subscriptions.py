import discord
from discord import app_commands


FEEDS = {
    'google': 'https://news.google.com/rss/search?q={CATEGORY}&hl=en-US&gl=US&ceid=US:en',
    'yahoo': 'https://www.yahoo.com/news/rss/{CATEGORY}',
    'washington_post': 'https://feeds.washingtonpost.com/rss/{CATEGORY}',
}

CATEGORIES = {
    'google': {
        'world': 'World',
        'sports': 'Sports',
        'tech': 'Technology',
        'health': 'Health',
        'politics': 'Politics',
        'science': 'Science',
        'business': 'Business',
    },
    'yahoo': {
        'world': 'world',
        'sports': 'sport',
        'tech': 'tech',
        'health': 'health',
        'politics': 'politics',
        'science': 'science',
        'business': 'business',
    },
    'washington_post': {
        'world': 'world',
        'sports': 'sports',
        'tech': 'business/technology',
        'health': None,
        'politics': 'politics',
        'science': None,
        'business': 'business',
    },
}

class Subscription:
    
    def __init__(self):
        self.feed = ''
        self.category = ''
        self.active_feed_url = ''

    def sub_to(self, feed, category='world'):
        self.feed = FEEDS[feed]
        self.category = CATEGORIES[feed][category]
        if self.category == None:
            raise Error(f'Category "{category}" doesn\'t exist for feed "{feed}"')

        self.active_feed_url = self.feed.format(CATEGORY=self.category)
    
    def swap_category(self, new_category):
        self.category = CATEGORIES[self.feed][new_category]
        if self.category == None:
            raise Error(f'Category "{category}" doesn\'t exist for feed "{feed}"')
        
        self.active_feed_url = self.feed.format(CATEGORY=self.category)


subscription = Subscription()

@app_commands.command()
async def subscribe(interaction: discord.Interaction, query: str):
    if query in FEEDS.keys():
        subscription.sub_to(query)
        await interaction.response.send_message(f'Subscribed to "{query}"!')
    else:
        await interaction.response.send_message(f'Invalid subscription: "{query}"')

def get_subscription():
    return subscription

def setup(app):
    active_feed = sub_to('google', 'world')
    app.tree.add_command(subscribe)