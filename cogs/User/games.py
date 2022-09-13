from discord import app_commands, Interaction, Member
from discord.ext.commands import Bot, Cog

from .Games.tic_tac_toe import TicTacToe, TossTicTacToe


class Games(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name="play", description="Select a game to play")
    @app_commands.choices(
        game=[
            app_commands.Choice(name="Tic Tac Toe", value="tic-tac-toe"),
        ]
    )
    @app_commands.describe(with_="2nd player to play with.")
    async def play(self, interaction: Interaction, game: str, with_: Member = None):
        """
        Play a game with another user.

        Parameters
        ----------
        interaction : Interaction
            The interaction of the command.
        game : str
            The game to play.
        with_ : Member, optional
            The second player, by default None.
        """
        await interaction.response.defer()
        player1: Member = interaction.user
        player2: Member = interaction.user
        if with_:
            player2 = with_
        if game == "tic-tac-toe":
            if player1 != player2:
                content = f"**Playing Tic Tac Toe with {player2.mention}.**"
                view = TossTicTacToe(player1, player2)
                await interaction.followup.send(content=content, view=view)
            else:
                view = TicTacToe()
                await interaction.followup.send(view=view)


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(Games(bot))
