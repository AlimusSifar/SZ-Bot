from os import path, listdir, getenv

from nextcord import Intents, Activity, ActivityType
from nextcord.ext.commands import Bot

from utils.keep_alive import keep_alive
from colorama import init, Fore
init(autoreset=True)

print(f"{Fore.GREEN}>>> Successfully imported modules <<<")


def main():
    intents = Intents.default()
    intents.members = True

    command_prefix = ["sz.", "sZ.", "Sz.", "SZ."]
    # `Listening` activity
    activity = Activity(
        type=ActivityType.listening,
        name=f"`{command_prefix[0]}` command",
    )
    bot = Bot(command_prefix, intents=intents, activity=activity)

    for folder in listdir("cogs"):
        if path.exists(path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")

    bot.run(getenv("discord-bot-token"))


if __name__ == "__main__":
    keep_alive()
    main()
