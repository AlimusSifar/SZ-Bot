import os
import discord
import actions
import components
import keep_alive

from datetime import datetime
from discord.ext import commands, tasks

print(f'Status#001 - Packages OK', '\n')

intents = discord.Intents.default()
intents.members = True

# NOTE: Bot object
PREFIX = "sz."
bot = commands.Bot(command_prefix=PREFIX, help_command=None, intents=intents)


#
@bot.event
async def on_ready():
    # `Listening` activity
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=PREFIX,
    ))
    print(f'Status#002 - {bot.user.name} is listening.', '\n')


# HELP COMMAND
@bot.command(name="help")
async def help(ctx: commands.Context):
    async with ctx.typing():
        embed = discord.Embed(title="Commands",
                              description="Basic command patterns",
                              color=0x45b865)
        # embed.set_author(name="SZ Bot", icon_url="https://cdn.discordapp.com/avatars/799989827834478602/018456925efab272d09f8149c9ec8649.webp?size=1024")
        embed.add_field(name="Add",
                        value="`sz.add [role] [role]*`",
                        inline=True)
        embed.add_field(name="Remove",
                        value="`sz.remove [role] [role]*`",
                        inline=True)
        embed.add_field(name="Sort",
                        value="`sz.sort [roles]/[channels]`",
                        inline=True)
        embed.set_footer(text="`*` : Zero or multiple roles can be given")
        return await ctx.reply(embed=embed)


# ADD COMMAND
@bot.command(name="add")
async def add_roles(ctx: commands.Context, *roles: str.upper):
    message: discord.Message = ctx.message

    if len(roles) == 0:
        async with ctx.typing():
            await message.add_reaction('🤔')
            response = '```fix\n❗️ course_name argument missing.```'
            components.log_to_json(datetime.now(), ctx.author, message.content,
                                   response)
            return await ctx.reply(response)

    for role in roles:
        async with ctx.typing():
            if components.is_valid(role):
                await actions.add_role(ctx, role)

            else:
                await message.add_reaction('😑')
                response = '```fix\n❗️ Invalid course name {role}```\n> Retry with a valid name. i.e.: CSE###, MAT###, PHY###'
                #
                components.log_to_json(datetime.now(), ctx.author,
                                       message.content, response)
                return await ctx.reply(response)


# REMOVE COMMAND
@bot.command(name="remove")
async def remove_roles(ctx: commands.Context, *roles: str.upper):
    message: discord.Message = ctx.message

    if len(roles) == 0:
        async with ctx.typing():
            await message.add_reaction('🤔')
            response = '```fix\n❗️ course_name argument missing.```'
            components.log_to_json(datetime.now(), ctx.author, message.content,
                                   response)
            return await ctx.reply(response)

    for role in roles:
        async with ctx.typing():
            if components.is_valid(role):
                await actions.remove_role(ctx, role)

            else:
                await message.add_reaction('😑')
                response = '```fix\n❗️ Invalid course name {role}```\n> Retry with a valid name. i.e.: CSE###, MAT###, PHY###'
                #
                components.log_to_json(datetime.now(), ctx.author,
                                       message.content, response)
                await ctx.reply(response)


#
@bot.command(name="sort")
async def sort(ctx: commands.Context, cmd: str.lower):
    if ctx.author == ctx.guild.owner:
        async with ctx.typing():
            if cmd == "roles":
                await components.sort_subjective_roles(ctx.guild.roles)

            elif cmd == "channels":
                await components.sort_subjective_category(ctx.guild)

        await ctx.message.add_reaction('🆗')
        return await ctx.reply(f"{cmd.title()} are sorted!")

    return await ctx.reply(f"Admin permission is required!")


# Word of the Day
@bot.command(name="word-of-the-day")
async def wotd(ctx: commands.Context):
    await auto_wotd.start(ctx)


# LOOP: 1 DAY
@tasks.loop(hours=24)
async def auto_wotd(ctx: commands.Context):
    await components.word_of_the_day(ctx)


if __name__ == '__main__':
    keep_alive.keep_alive()
    bot.run(os.getenv("SZ_BOT"))
