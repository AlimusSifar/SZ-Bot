from discord import app_commands, Interaction, Role
from discord.ext.commands import (
    Bot,
    Cog,
)
from discord.utils import get


class Sorting(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name="sort", description="Sorts the channels or roles.")
    @app_commands.describe(type="The type of sorting to perform.")
    @app_commands.choices(
        type=[
            app_commands.Choice(name="channels", value="channels"),
            app_commands.Choice(name="roles", value="roles"),
        ]
    )
    @app_commands.guilds(767987538941968394)
    @app_commands.checks.has_permissions(manage_channels=True, manage_roles=True)
    async def sort(self, interaction: Interaction, type: str) -> None:
        """
        Sorts the channels or roles. Only works in the server specified.
        Only works for admins.

        Parameters
        ----------
        interaction : Interaction
            The interaction of the command.
        type : str
            The type of sorting to perform.
        """

        await interaction.response.defer(ephemeral=True)
        if type == "channels":
            await sort_channels(interaction)
        elif type == "roles":
            await sort_roles(interaction)
        else:
            await interaction.followup.send("Invalid type")


async def sort_channels(interaction: Interaction) -> None:
    """
    Sorts all the text channels under the subjective category in the server.
    """
    category = get(interaction.guild.categories, id=768411403341529088)
    channels = category.channels
    initial_pos = channels[0].position
    sorted_channels = sorted(channels, key=lambda channels: channels.name)

    if channels != sorted_channels:
        for pos, channel in enumerate(sorted_channels):
            if pos != channel.position:
                await channel.edit(position=initial_pos + pos)
    return await interaction.followup.send(f"✅ Subjective channels are sorted!")


async def sort_roles(interaction: Interaction) -> None:
    """
    Sorts all the BRACU course roles in the server.
    """
    await interaction.response.defer(ephemeral=True)
    roles = interaction.guild.roles
    # reference to SZ-Bot role
    ref_role: Role = get(roles, id=806463759027142667)

    old_roles = [roles[pos] for pos in range(1, ref_role.position)]
    new_roles = sorted(old_roles, reverse=True, key=lambda roles: roles.name)

    if old_roles != new_roles:
        for pos, new_role in enumerate(new_roles):
            if old_roles[pos] != new_role:
                await new_role.edit(position=pos + 1)
    return await interaction.followup.send(f"✅ Course roles are sorted!")


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(Sorting(bot))
