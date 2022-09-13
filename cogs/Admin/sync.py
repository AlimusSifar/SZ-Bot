from typing import Literal, Optional

from discord import Object, HTTPException
from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    Greedy,
    command,
    is_owner,
)
from colorama import init, Fore

init(autoreset=True)


class Sync(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="sync")
    @is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Syncs the CommandTree for the Application Commands.

        Only the owner of the bot can use this command.

        Useage:
            `!sync` -> global sync

            `!sync ~` -> sync current guild

            `!sync *` -> copies all global app commands to current guild and syncs

            `!sync ^` -> clears all commands from the current guild target and syncs (removes guild commands)

            `!sync id_1 id_2` -> syncs guilds with id 1 and 2
        """
        async with ctx.typing():
            if not guilds:
                if spec == "~":
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "*":
                    ctx.bot.tree.copy_global_to(guild=ctx.guild)
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "^":
                    ctx.bot.tree.clear_commands(guild=ctx.guild)
                    await ctx.bot.tree.sync(guild=ctx.guild)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()

                await ctx.reply(
                    f"Synced {len(synced)} commands {'globally' if not spec else 'to the current guild.'}"
                )
                print(f"* {Fore.GREEN}Successfully synced tree")
                return

            ret = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except HTTPException:
                    pass
                else:
                    ret += 1

            await ctx.reply(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(Sync(bot))
