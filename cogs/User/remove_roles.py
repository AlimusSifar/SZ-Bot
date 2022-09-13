from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
)

from ..utils import actions, components


class RemoveRoles(Cog, name="Remove Roles"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="remove", aliases=["drop"])
    async def remove_roles(self, ctx: Context, *role_names: str.upper):
        """
        Removes one/more roles from a member.

        If the role is not found, it will return an error message. If the role is already removed,
        it will return an error message. If the role is newly removed, it will return a success message.
        """

        if len(role_names) == 0:
            async with ctx.typing():
                await ctx.message.add_reaction("🤔")
                response = "```fix\n❗️ course_name argument missing.```"
                return await ctx.reply(response)

        for role_name in role_names:
            async with ctx.typing():
                if components.role_is_valid(role_name):
                    await actions.remove_role(ctx, role_name)
                else:
                    await ctx.message.add_reaction("😑")
                    response = (f"```fix\n❗️ Invalid course name {role_name}```\n"
                                "> Retry with a valid name. i.e.: CSE###, MAT###, PHY###")
                    await ctx.reply(response)


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(RemoveRoles(bot))
