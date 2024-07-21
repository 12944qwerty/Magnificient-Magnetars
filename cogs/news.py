from typing import Any

import discord
from discord import app_commands, Interaction
import feedparser

current_search = ''
previous_search = ''
news_view_page = 1


def getNews(query, page):
    global previous_search
    global current_search
    previous_search = current_search
    em1 = discord.Embed(title=f'News articles on \"{query}\"')
    em2 = discord.Embed(title=f'News articles on \"{query}\"')
    em3 = discord.Embed(title=f'News articles on \"{query}\"')
    em4 = discord.Embed(title=f'News articles on \"{query}\"')
    current_search = query
    # get the url of the search
    rss_url = f'https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en'

    feed = feedparser.parse(rss_url)

    x = 0

    if feed.entries:
        for entry in feed.entries:
            # for every news article add a field for it
            x = x + 1
            title = entry.title
            link = entry.link
            pubdate = entry.published
            if x <= 5:
                em1 = em1.add_field(name=title, value=f'{link} \n Published on {pubdate}', inline=False)

            elif x > 5 and x <= 10:
                em2 = em2.add_field(name=title, value=f'{link} \n Published on {pubdate}', inline=False)

            elif x > 10 and x <= 15:
                em3 = em3.add_field(name=title, value=f'{link} \n Published on {pubdate}', inline=False)

            elif x > 15 and x <= 20:
                em4 = em4.add_field(name=title, value=f'{link} \n Published on {pubdate}', inline=False)
    else:
        em1.add_field(name="No articles found", value=":(")
        em2.add_field(name="No articles found", value=":(")
        em3.add_field(name="No articles found", value=":(")
        em4.add_field(name="No articles found", value=":(")

    em1.set_footer(text=f'Page {page}/4')
    em2.set_footer(text=f'Page {page}/4')
    em3.set_footer(text=f'Page {page}/4')
    em4.set_footer(text=f'Page {page}/4')

    if page == 1:
        return em1

    elif page == 2:
        return em2

    elif page == 3:
        return em3

    elif page == 4:
        return em4

    else:
        raise ValueError('Invalid page')





class NewsDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='World', description='Get world news'),
            discord.SelectOption(label='Sports', description='Get world news'),
            discord.SelectOption(label='Technology', description='Get world news'),
            discord.SelectOption(label='Health', description='Get world news'),
            discord.SelectOption(label='Politics', description='Get world news'),
            discord.SelectOption(label='Science', description='Get world news'),
            discord.SelectOption(label='Business', description='Get world news')
        ]
        self.page = 1
        self.total_pages = 4

        super().__init__(placeholder='Choose a topic', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: Interaction):
        if self.values[0] == 'World':
            await interaction.response.send_message(embed=getNews('World', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())

        if self.values[0] == 'Sports':
            await interaction.response.send_message(embed=getNews('Sports', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())

        if self.values[0] == 'Technology':
            await interaction.response.send_message(embed=getNews('Technology', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())

        if self.values[0] == 'Health':
            await interaction.response.send_message(embed=getNews('Health', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())

        if self.values[0] == 'Politics':
            await interaction.response.send_message(embed=getNews('Politics', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())

        if self.values[0] == 'Science':
            await interaction.response.send_message(embed=getNews('Science', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())

        if self.values[0] == 'Business':
            await interaction.response.send_message(embed=getNews('Business', 1).set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar
            ), view=NewsView())


class NewsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(NewsDropdown())
        self.total_pages = 4

    @discord.ui.button(label="<", style=discord.ButtonStyle.green, custom_id="prev")  # , emoji="" if wanted
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global news_view_page
        global current_search
        global previous_search
        if current_search != previous_search:
            news_view_page = 1

        if news_view_page > 1:
            news_view_page = news_view_page - 1
        else:
            news_view_page = self.total_pages
        await interaction.response.edit_message(embed=getNews(current_search, news_view_page).set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.avatar
        ), view=NewsView())

    @discord.ui.button(label=">", style=discord.ButtonStyle.green, custom_id="next")  # , emoji="" if wanted
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global news_view_page
        global current_search
        global previous_search
        if current_search != previous_search:
            news_view_page = 1

        if news_view_page < self.total_pages:
            news_view_page = news_view_page + 1
        else:
            news_view_page = 1

        await interaction.response.edit_message(embed=getNews(current_search, news_view_page).set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.avatar
        ), view=NewsView())


@app_commands.command(name='news', description='get some news')
async def news(interaction: discord.Interaction, query: str):
    view = NewsView()

    await interaction.response.send_message(
        embed=getNews(query, 1).set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar),
        view=view
    )


async def setup(app):
    app.tree.add_command(news)
