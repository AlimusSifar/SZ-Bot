import os
import platform

from aiohttp import ClientSession
from discord import (
    ButtonStyle,
    Colour,
    Embed,
    FFmpegPCMAudio,
    Interaction,
    WebhookMessage,
    app_commands,
)
from discord.ext.commands import Bot, Cog
from discord.ui import Button, View


class Dictionary(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name="define", description="Defines a word")
    @app_commands.describe(word="The word to define")
    @app_commands.choices(confidential=[app_commands.Choice(name="True", value=1)])
    async def define(
        self, interaction: Interaction, word: str, confidential: int = 0
    ) -> None:
        """
        Gets the definition of the word from the API.
        If the word is not found, it will return an error message.

        Parameters
        ----------
        interaction : Interaction
            The interaction of the command.
        word : str
            The word to be searched.
        confidential : int, optional
            Value for ephemeral, by default 0.
        """
        confidential = bool(confidential)
        await interaction.response.defer(ephemeral=confidential)

        # Gets the definition of the word from the API
        response = await self.get_definition_of(word)
        # Processes the data from the API
        data = await self.process_data_from(word, response)
        # Generates an embed from the processed data
        embed, phonetics = await self.generate_embed_from(data)

        # Sends the embed to the user
        if phonetics:
            view = ViewButtons(sorted(phonetics, reverse=True))
            view.message = await interaction.followup.send(
                embed=embed,
                view=view,
                ephemeral=confidential,
            )
        else:
            await interaction.followup.send(embed=embed, ephemeral=confidential)

    async def get_definition_of(self, word: str) -> "list[dict] | dict":
        """
        Gets the definition of the word from the API

        Parameters
        ----------
        word : str
            The word to be searched

        Returns
        -------
        list[dict] | dict
            The data of the word
        """
        endpoint = "http://api.dictionaryapi.dev/api/v2/entries/en/" + word
        async with ClientSession() as session:
            async with session.get(endpoint) as response:
                return await response.json()

    async def process_data_from(
        self, word: str, response: "list[dict] | dict"
    ) -> "tuple[set, set, dict, set] | str":
        """
        Processes the data from the API

        Parameters
        ----------
        word : str

        response : list[dict] | dict
            The data from the API

        Returns
        -------
        tuple[set, set, dict, set] | dict
            The processed data
        """
        if isinstance(response, list):
            word = set()
            phonetics = set()
            meanings: "dict[str, dict[str, list]]" = {}
            license = set()
            for data in response:
                word.add(data["word"])
                [
                    phonetics.add(phonetic.get("audio"))
                    for phonetic in data["phonetics"]
                    if phonetic.get("audio")
                ]
                for meaning in data["meanings"]:
                    meanings[meaning["partOfSpeech"]] = []
                    for definition in meaning["definitions"]:
                        meanings[meaning["partOfSpeech"]].append(
                            (definition.get("definition"), definition.get("example"))
                        )
                license.add(data.get("license").get("name"))
            return word, phonetics, meanings, license
        return word

    async def generate_embed_from(
        self, data: "tuple[set, set, dict, set] | str"
    ) -> "tuple[Embed, set | None]":
        """
        Generates the embed from the processed data

        Parameters
        ----------
        data : tuple[set, set, dict, set] | dict
            The processed data

        Returns
        -------
        tuple[Embed, set | None]
            The embed and the phonetics
        """
        if isinstance(data, str):
            # Handles errors
            embed = Embed(
                title="❌ No Definitions Found",
                description=f"Sorry pal, we couldn't find any definitions for the word **`{data}`**.",
                color=Colour.red(),
            )
            embed.set_author(
                name="Free Dictionary API",
                url="https://dictionaryapi.dev/",
                icon_url="https://cdn-icons-png.flaticon.com/128/3898/3898012.png",
            )
            return embed, None

        word, phonetics, meanings, license_name = data
        pos = meanings.keys()

        embed = Embed(
            title=f"Meaning & Example of '{word.pop()}'",
            color=Colour.random(),
        )
        embed.set_author(
            name="Free Dictionary API",
            url="https://dictionaryapi.dev/",
            icon_url="https://cdn-icons-png.flaticon.com/128/3898/3898012.png",
        )

        for pos in meanings:
            embed.add_field(name=f"✓ {pos}", value="\u200b", inline=False)
            for definition, example in meanings[pos]:
                if definition:
                    embed.add_field(
                        name="🇩efinition", value=f"`{definition}`", inline=False
                    )
                if example:
                    embed.add_field(name="🇪xample", value=f"*{example}*", inline=False)

        embed.set_footer(
            text=f"License: {license_name.pop()}",
            icon_url="https://cdn-icons-png.flaticon.com/512/3522/3522406.png",
        )
        return embed, phonetics


class ViewButtons(View):
    """
    Displays all the buttons for the app command.
    """

    children: "list[SpeakButton | DisconnectButton]"
    message: WebhookMessage
    has_disconnect_button: bool = False

    def __init__(self, phonetics: "list[str]"):
        super().__init__(timeout=120)

        for phonetic in phonetics:
            self.add_item(SpeakButton(phonetic))

    async def on_timeout(self):
        # Disables all the buttons
        for button in self.children:
            button.disabled = True
            # button.label = "Times Up!"
        await self.message.edit(view=self)


class SpeakButton(Button[ViewButtons]):
    """
    A button to play the pronunciation of the word.
    """

    def __init__(self, phonetic_url: str):
        super().__init__(
            style=ButtonStyle.success, label=f"🗣️ {phonetic_url[-6:-4].upper()}"
        )
        self.phonetic_url = phonetic_url

    async def callback(self, interaction: Interaction):
        """
        This function gets called when the button is pressed.

        It pronounces the word.

        If the bot is not connected to a voice channel, it connects to the user's voice channel.
        If the bot is already connected to a voice channel, it disconnects from it and
        connects to the user's voice channel.

        Parameters
        ----------
        interaction : Interaction
            The interaction object.
        """
        # Connects the bot for voice support
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            if interaction.user.voice:
                await interaction.user.voice.channel.connect()
            else:
                # Sends a new ephemeral message
                content = "You are not connected to a voice channel."
                await interaction.response.send_message(content=content, ephemeral=True)
                return
        elif voice_client.is_playing():
            voice_client.stop()

        # Path to ffmpeg
        if platform.system() == "Linux":
            FFMPEG_PATH = os.getenv("ffmpeg-path-linux")
        elif platform.system() == "Windows":
            FFMPEG_PATH = os.getenv("ffmpeg-path-windows")
        source = FFmpegPCMAudio(self.phonetic_url, executable=FFMPEG_PATH)

        # Plays the audio
        voice_client = interaction.guild.voice_client
        # await asyncio.sleep(1)
        voice_client.play(source)

        # Adds a disconnect button
        if not self.view.has_disconnect_button:
            self.view.add_item(DisconnectButton())
            self.view.has_disconnect_button = True

        # Edits the original message
        await interaction.response.edit_message(view=self.view)


class DisconnectButton(Button[ViewButtons]):
    """
    A button to disconnect the client from the voice channel
    """

    def __init__(self):
        super().__init__(style=ButtonStyle.danger, label="Disconnect!")

    async def callback(self, interaction: Interaction):
        """
        This function gets called when the button is pressed.

        It disconnects the client from the voice channel and
        removes the button from the view.

        Parameters
        ----------
        interaction : Interaction
            The interaction that triggered the callback.
        """
        await interaction.guild.voice_client.disconnect()
        self.view.remove_item(self)
        self.view.has_disconnect_button = False
        await interaction.response.edit_message(view=self.view)


async def setup(bot: Bot) -> None:
    """
    Loads the cog

    Parameters
    ----------
    bot : Bot
        The bot instance
    """
    await bot.add_cog(Dictionary(bot))
