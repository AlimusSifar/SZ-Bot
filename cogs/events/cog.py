from nextcord import Member
from nextcord.ext.commands import Cog, Bot, Context

from utils import logging


class Events(Cog):
    """Bot event handler"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Called when the client is done preparing the data received from Discord"""
        logging.info(f"'{self.bot.user}' is listening.")
        print(f">>> {self.bot.user} is listening <<<", "\n")

    @Cog.listener()
    async def on_member_join(self, member: Member):
        """Triggered when a member joins a guild"""
        logging.info(f"{member} just spawned in this server.")
        print(f">>> {member} just spawned in this server <<<")

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        """Triggered when an error occurs while invoking a command"""
        logging.error(f"User '{ctx.author}' invoked '{ctx.message.content}' command resulting to: [E] {error}.")


def setup(bot: Bot):
    bot.add_cog(Events(bot))
