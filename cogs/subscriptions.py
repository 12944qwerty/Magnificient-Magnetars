import discord
from discord import app_commands, Interaction


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
        self.feed_name = 'google'
        self.category = ''
        self.active_feed_url = ''

    def sub_to(self, feed, category='world'):
        self.feed_name = feed
        self.feed = FEEDS[feed]
        self.category = CATEGORIES[feed][category]
        if self.category == None:
            raise ValueError(f'Category "{category}" doesn\'t exist for feed "{feed}"')

        self.active_feed_url = self.feed.format(CATEGORY=self.category)
    
    def swap_category(self, new_category):
        self.category = CATEGORIES[self.feed][new_category]
        if self.category == None:
            raise ValueError(f'Category "{category}" doesn\'t exist for feed "{feed}"')
        
        self.active_feed_url = self.feed.format(CATEGORY=self.category)
    
    def __str__(self):
        return f"""
        Subscription: (
            feed: {self.feed},
            category: {self.category},
            active_feed_url: {self.active_feed_url},
        )
        """


subscription = Subscription()

@app_commands.choices(service=[
    discord.app_commands.Choice(name='Google news', value='google'),
    discord.app_commands.Choice(name='Yahoo', value='yahoo'),
    discord.app_commands.Choice(name='Washington post', value='washington_post'),
])
@app_commands.command()
async def subscribe(interaction: discord.Interaction, service: discord.app_commands.Choice[str]):
    if service.value not in FEEDS.keys():
        await interaction.response.send_message(f'Invalid subscription: "{service}"')
    
    subscription.sub_to(service.value)
    await interaction.response.send_message(f'Subscribed to "{service.name}"!')

@app_commands.command()
async def subscription_info(interaction: discord.Interaction, query: str):
    if query not in ['feed', 'category', 'url']:
        message = 'Invalid query'
    
    if query == 'feed':
        message = f'Feed: {subscription.feed}'
    elif query == 'category':
        message = f'Category: {subscription.category}'
    elif query == 'url':
        message = f'URL: {subscription.active_feed_url}'
    elif query == 'all':
        message = subscription

    await interaction.response.send_message(message)


def get_subscription():
    return subscription


async def setup(app):
    subscription.sub_to('google')
    app.tree.add_command(subscribe)
    app.tree.add_command(subscription_info)