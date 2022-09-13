from os import getenv
from random import choice

from aiohttp import ClientSession
from discord import app_commands, Embed, Interaction, Colour
from discord.ext.commands import Bot, Cog


class Quotes(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.quote_functions = [
            # api_quotable_io,
            go_quotes_api,
            zenquotes_io,
            rapidapi_quotes,
        ]

    @app_commands.command(
        name="quote", description="Returns a quote from a given type."
    )
    @app_commands.describe(type="Type of quote to return.")
    # @app_commands.choices(
    #     type=[
    #         app_commands.Choice(name="random", value="random"),
    #     ]
    # )
    async def quote(self, interaction: Interaction, type: str = "random") -> None:
        """
        Returns a quote from a given type. If no type is given, a random quote is returned.

        Parameters
        ----------
        interaction : Interaction
            The interaction of the command.
        type : str, optional
            The type of quote to be returned, by default "random".
        """
        await interaction.response.defer(thinking=True)
        if type == "random":
            author, quote, site = await choice(self.quote_functions)()
            embed = Embed(
                title=f"{type.title()} Quote",
                colour=Colour.random(),
            )
            embed.add_field(name=f"{author}", value=f"*“{quote}”*", inline=False)
            embed.set_footer(text=f"Source: {site}")
            await interaction.followup.send(embed=embed)


# Functions to call quotes from the APIs
async def api_quotable_io() -> tuple:
    async with ClientSession() as session:
        async with session.get("https://api.quotable.io/random") as response:
            data = await response.json()
            return (
                data.get("author"),
                data.get("content"),
                "api.quotable.io",
            )


async def go_quotes_api() -> tuple:
    async with ClientSession() as session:
        url = "https://goquotes-api.herokuapp.com/api/v1/random?count=1"
        async with session.get(url) as response:
            data = await response.json()
            data = data.get("quotes")[0]
            return (
                data.get("author"),
                data.get("text"),
                "goquotes.docs.apiary.io",
            )


async def zenquotes_io() -> tuple:
    async with ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as response:
            data = await response.json()
            return (
                data[0].get("a"),
                data[0].get("q").strip(),
                "zenquotes.io",
            )


async def rapidapi_quotes() -> tuple:
    async with ClientSession() as session:
        url = "https://quotes15.p.rapidapi.com/quotes/random/"
        headers = {
            "X-RapidAPI-Key": getenv("quotes15.p.rapidapi.com"),
            "X-RapidAPI-Host": "quotes15.p.rapidapi.com",
        }
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return (
                data.get("originator").get("name"),
                data.get("content"),
                "quotes15.p.rapidapi.com",
            )


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(Quotes(bot))
