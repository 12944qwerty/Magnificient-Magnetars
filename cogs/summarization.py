import requests
import discord
from discord import app_commands
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer





def get_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        body_text = soup.body.get_text(separator=' ', strip=True)

        return body_text
    else:
        return "Failed to retrieve content"


def get_summary(link, sentences_count, language="english"):
    text = get_text(link)
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    full_summary = ' '.join([str(sentence) for sentence in summary])
    em = discord.Embed(title="Summary: ", description=full_summary)
    em = em.set_footer(text=f'Summary of {link}')

    return em


@app_commands.command()
async def summarize(interaction: discord.Interaction, link: str):
    await interaction.response.defer(ephemeral=False, thinking=False)
    await interaction.followup.send(embed=get_summary(link, 3).set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.avatar
    ))


async def setup(app):
    app.tree.add_command(summarize)