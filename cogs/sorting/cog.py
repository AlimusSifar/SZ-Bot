from nextcord import Role
from nextcord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
)
from nextcord.utils import get


class Sorting(Cog, name="Sorting"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="sort_channels", aliases=["sortchannels", "sort-channels"])
    async def sort_channels(self, ctx: Context):
        """Sorts all the text channels in subjective category"""

        author_has_permission = ctx.author.guild_permissions.administrator
        if not author_has_permission:
            return await ctx.reply(f"Sorry! You need admin permission")

        await ctx.message.add_reaction("🆗")

        category = get(ctx.guild.categories, id=768411403341529088)
        channels = category.channels

        initial_pos = channels[0].position
        sorted_channels = sorted(channels, key=lambda channels: channels.name)

        async with ctx.typing():
            if channels != sorted_channels:
                for pos in range(len(sorted_channels)):
                    if pos != sorted_channels[pos].position:
                        await sorted_channels[pos].edit(position=initial_pos + pos)

            return await ctx.reply(f"Text channels are sorted!")

    @command(name="sort_roles", aliases=["sortroles", "sort-roles"])
    async def sort_roles(self, ctx: Context):
        """Sorts all the BRACU course roles in the server"""

        author_has_permission = ctx.author.guild_permissions.administrator
        if not author_has_permission:
            return await ctx.reply(f"Sorry! You need admin permission")

        await ctx.message.add_reaction("🆗")

        roles = ctx.guild.roles
        # reference to SZ-Bot role
        ref_role: Role = get(roles, id=806463759027142667)

        old_roles = [roles[pos] for pos in range(1, ref_role.position)]
        new_roles = sorted(
            old_roles, reverse=True, key=lambda roles: roles.name
        )

        async with ctx.typing():
            if old_roles != new_roles:
                for pos in range(len(new_roles)):
                    if old_roles[pos] != new_roles[pos]:
                        await new_roles[pos].edit(position=pos + 1)

            return await ctx.reply(f"Text channels are sorted!")


def setup(bot: Bot):
    bot.add_cog(Sorting(bot))
