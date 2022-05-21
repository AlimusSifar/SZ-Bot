from utils import actions
from utils import components

from nextcord import Message
from nextcord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
)


class AddRoles(Cog, name="Add Roles"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="add", aliases=[])
    async def add_roles(self, ctx: Context, *role_names: str.upper):
        """Adds one/more roles to a member"""

        message: Message = ctx.message

        if len(role_names) == 0:
            async with ctx.typing():
                await message.add_reaction("🤔")
                response = "```fix\n❗️ course_name argument missing.```"
                return await ctx.reply(response)

        for role_name in role_names:
            async with ctx.typing():
                if components.role_is_valid(role_name):
                    return await actions.add_role(ctx, role_name)

                await message.add_reaction("😑")
                response = "```fix\n❗️ Invalid course name {role}``` \
                    \n> Retry with a valid name. i.e.: CSE###, MAT###, PHY###"
                return await ctx.reply(response)


def setup(bot: Bot):
    bot.add_cog(AddRoles(bot))
