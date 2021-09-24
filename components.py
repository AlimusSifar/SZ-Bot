import json
import discord

from discord.utils import get


# WRITING a log file
def log_to_json(now, user, request: str, response: str) -> None:
    """
    Creates a log file of the User requests and Bot responses.
    """
    logs = {"log": []}

    # CHECKING: if log file exists
    try:
        open("log.json", "r")

    except:
        open("log.json", "x")

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
