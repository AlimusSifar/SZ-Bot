from ast import literal_eval
import asyncio
from os import getenv

from colorama import init, Fore
from discord import (
    Activity,
    ActivityType,
    Intents,
)
from discord.ext.commands import Bot
import dotenv

from cogs.utils.keep_alive import keep_alive

dotenv.load_dotenv()
init(autoreset=True)

if getenv("PREFIXES") is None:
    raise ValueError("No prefixes provided")
else:
    PREFIXES = literal_eval(str(getenv("PREFIXES")))


class Bot_(Bot):
    extensions: list[str] = [
        "cogs.Admin.sync",
        "cogs.Admin.sort",
        "cogs.Events.cog",
        "cogs.User.add_roles",
        "cogs.User.dictionary",
        "cogs.User.games",
        # "cogs.User.morsecode",
        # "cogs.User.ping",
        "cogs.User.quotes",
        "cogs.User.remove_roles",
    ]

    def __init__(self):
        super().__init__(
            command_prefix=PREFIXES,
            intents=Intents.all(),
            activity=Activity(
                name=f"prefix `{PREFIXES[0]}`",
                type=ActivityType.listening,
            ),
        )

    async def setup_hook(self) -> None:
        for ext in self.extensions:
            await self.load_extension(ext)
            print(f"* {Fore.GREEN}Loaded `{ext}` extension.")


async def main():
    bot = Bot_()
    async with bot:
        if getenv("sz-bot-token") is None:
            raise ValueError("No token provided")
        else:
            await bot.start(str(getenv("sz-bot-token")))


if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
