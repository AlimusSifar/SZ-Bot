from utils import actions
from utils import components

from nextcord import Message
from nextcord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
)


class RemoveRoles(Cog, name="Remove Roles"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="remove", aliases=["drop"])
    async def remove_roles(self, ctx: Context, *role_names: str.upper):
        """Removes one/more roles from a member"""

        message: Message = ctx.message

        if len(role_names) == 0:
            async with ctx.typing():
                await message.add_reaction("🤔")
                response = "```fix\n❗️ course_name argument missing.```"
                return await ctx.reply(response)

        for role_name in role_names:
            async with ctx.typing():
                if components.role_is_valid(role_name):
                    return await actions.remove_role(ctx, role_name)

                await message.add_reaction("😑")
                response = (f"```fix\n❗️ Invalid course name {role_name}```\n"
                            "> Retry with a valid name. i.e.: CSE###, MAT###, PHY###")
                return await ctx.reply(response)


def setup(bot: Bot):
    bot.add_cog(RemoveRoles(bot))
