import discord
import components

from datetime import datetime
from discord.ext import commands
from discord.utils import get


#
async def create_text_channel(server: discord.Guild, role: discord.Role) -> discord.TextChannel:
    # NOTE: FIXED CATEGORY : SUBJECTIVE
    category = get(server.categories, id=768411403341529088)

    # NOTE: Role object of Visitor
    Visitor = get(server.roles, id=785380797380821063)
    # NOTE: Role object of MathBot
    MathBot = get(server.roles, id=768398093376159745)

    overwrites = {
        # overwrites @everyone role
        server.default_role:
        discord.PermissionOverwrite(view_channel=False, ),
        MathBot:
        discord.PermissionOverwrite(view_channel=True, ),
        Visitor:
        discord.PermissionOverwrite(view_channel=True, ),
        role:
        discord.PermissionOverwrite(view_channel=True, ),
    }
    return await server.create_text_channel(str(role.name).lower(), category=category, overwrites=overwrites)


#
async def add_role(ctx: commands.Context, role_name: str) -> None:
    member: discord.Member = ctx.author
    message: discord.Message = ctx.message
    server: discord.Guild = ctx.guild

    # IF member has role
    if get(member.roles, name=role_name):
        await message.add_reaction('😤')
        response = f"You already have `{role_name}` course role.\nDon't bother asking again."
        #
        components.log_to_json(datetime.now(), member,
                               message.content, response)
        return await ctx.reply(response)

    # IF member does not have role
    role_found_in_server = get(server.roles, name=role_name)
    # IF role does not exist in server
    if not role_found_in_server:
        role_found_in_server = await server.create_role(name=role_name, mentionable=True)

    # IF role exists in server
    channel_found_in_server = get(server.channels, name=role_name.lower())

    # IF text channel does not exist in server
    if not channel_found_in_server:
        channel_found_in_server = await create_text_channel(server, role_found_in_server)

    # IF text channel exists in server
    await message.add_reaction('🆗')
    await member.add_roles(role_found_in_server)
    response = f'`{role_name}` course role has been given to {member.mention}'
    #
    components.log_to_json(datetime.now(), member,
                           message.content, response)
    return await ctx.reply(response)


#
async def drop_role(ctx: commands.Context, role_name: str) -> None:
    member: discord.Member = ctx.author
    message: discord.Message = ctx.message

    role_found_in_user = get(member.roles, name=role_name)
    # IF member has role
    if role_found_in_user:
        await message.add_reaction('🆗')
        await member.remove_roles(role_found_in_user)
        response = f'`{role_name}` course role has been dropped from {member.mention}'
        #
        components.log_to_json(datetime.now(), member,
                               message.content, response)
        return await ctx.reply(response)

    # IF member does not have role
    await message.add_reaction('😤')
    response = f"You don't have `{role_name}` course role.\nDon't bother asking it again."
    #
    components.log_to_json(datetime.now(), member, message.content, response)
    return await ctx.reply(response)
