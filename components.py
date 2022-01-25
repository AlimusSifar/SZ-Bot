import os
import json
import discord

from datetime import datetime
from discord.utils import get
from urllib import request


# WRITING a log file
def log_to_json(now, user, request: str, response: str) -> None:
    """
    Creates a log file of the User requests and Bot responses.
    """

    # CHECKING: if log file exists
    try:
        open("log.json", "r")
    except:
        open("log.json", "x")

    logs = {"log": []}
    
    # READING: log file
    with open("log.json", "r", encoding="utf-8") as jsonfile:
        try:
            log_limit = 1000  # CHANGEABLE
            logs = json.load(jsonfile)

            if len(logs) == log_limit:
                logs["log"] = []

        except:
            with open('log.json', 'w') as jsonfile:
                jsonlog = json.dumps(logs, indent=4)
                jsonfile.write(jsonlog)

    # WRITING: log file
    with open("log.json", "w", encoding="utf-8") as jsonfile:
        newlog = {
            "datetime": str(now),
            "user": str(user),
            "request": str(request),
            "response": str(response)
        }

        logs["log"].append(newlog)
        jsonlog = json.dumps(logs, indent=4)
        jsonfile.write(jsonlog)


# Verify Role Name
def is_valid(role: str) -> bool:
    """
    Verifies the valid BRACU Course Codes
    """
    VALID_COURSE_NAMES: "tuple[str]" = (
        "ANT",
        "BUS",
        "CHE",
        "CSE",
        "ECO",
        "ENG",
        "ENV",
        "MAT",
        "PHY",
        "STA",
    )

    if len(role) == 6:
        if role[:3] in VALID_COURSE_NAMES:
            for ch in role[3:]:
                if int(ch) not in range(10):
                    return False

        return True

    return False


# SORT subjective roles
async def sort_subjective_roles(roles: list) -> None:
    """
        Sorts only the subjective course roles of the guild.
    """
    reference: discord.Role = get(
        roles, id=806463759027142667)  # reference to SZ-Bot role

    subjective = [roles[i] for i in range(1, reference.position)]
    subjective = sorted(subjective, reverse=True, key=lambda roles: roles.name)

    for i in range(len(subjective)):
        await subjective[i].edit(position=i + 1)


# SORT subjective categories
async def sort_subjective_category(server: discord.Guild):
    """
        Sorts only the text channels in subjective category of the guild.
    """
    category = get(server.categories, id=768411403341529088)
    channels = category.channels

    initial_pos: int = channels[0].position
    sorted_channels = sorted(channels, key=lambda channels: channels.name)

    if channels == sorted_channels:
        return

    for i in range(len(sorted_channels)):
        await sorted_channels[i].edit(position=initial_pos + i)


#
async def word_of_the_day(channel: discord.TextChannel):
    URL = "http://api.wordnik.com/v4"

    res = request.urlopen(
        f"{URL}/words.json/wordOfTheDay?api_key={os.getenv('WordnikAPI')}")
    res = json.loads(res.read().decode("utf-8"))

    date = datetime.now().strftime("%A, %d %B %Y")
    word = res["word"]
    definitions: list = res["definitions"]
    examples: list = res["examples"]
    try:
        note = res["note"]
    except Exception as e:
        note = None

    embed = discord.Embed(
        title="Word of the Day",
        type="rich",
        description=f"Date: **{date}**",
        url="https://www.wordnik.com/word-of-the-day",
        color=0xCB4154,
    )

    embed.set_author(
        name="Wordnik",
        url="https://www.wordnik.com",
        icon_url="https://www.wordnik.com/assets/logo-heart.png",
    )

    embed.add_field(
        name=f"Word",
        value=f"*{word}*",
        inline=False,
    )

    embed.add_field(
        name="Definitions:",
        value="__ __",
        inline=False,
    )

    for definition in definitions:
        embed.add_field(
            name=f"[{definition['partOfSpeech']}]",
            value=f"*{definition['text']}*",
            inline=False,
        )

    embed.add_field(
        name="Examples:",
        value="__ __",
        inline=False,
    )

    for example in examples:
        embed.add_field(
            name=f"{example['title']}",
            value=f"*{example['text']}*",
            inline=False,
        )

    if note:
        embed.set_footer(text=f"Note: {note}")

    return await channel.send(embed=embed)
