from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
)

from ..utils import actions, components


class AddRoles(Cog, name="Add Roles"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="add", aliases=[])
    async def add_roles(self, ctx: Context, *role_names: str.upper):
        """
        Adds one/more roles to a member.

        If the role is not found, it will return an error message. If the role is already added,
        it will return an error message. If the role is newly added, it will return a success message.
        """

        if len(role_names) == 0:
            async with ctx.typing():
                await ctx.message.add_reaction("🤔")
                response = "```fix\n❗️ course_name argument missing.```"
                return await ctx.reply(response)

        for role_name in role_names:
            async with ctx.typing():
                if components.role_is_valid(role_name):
                    await actions.add_role(ctx, role_name)
                else:
                    await ctx.message.add_reaction("😑")
                    response = (f"```fix\n❗️ Invalid course name {role_name}```"
                                "\n> Retry with a valid name. i.e.: CSE###, MAT###, PHY###")
                    await ctx.reply(response)


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(AddRoles(bot))
