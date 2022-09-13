from discord import (
    Message,
    Member,
    Guild,
    PermissionOverwrite,
    Role,
)
from discord.ext.commands import (
    Context,
)
from discord.utils import get


async def create_text_channel(server: Guild, role: Role):
    # NOTE: FIXED CATEGORY : SUBJECTIVE
    category = get(server.categories, id=768411403341529088)

    # NOTE: Role object of Visitor
    Visitor = get(server.roles, id=785380797380821063)
    # NOTE: Role object of MathBot
    MathBot = get(server.roles, id=768398093376159745)

    overwrites = {
        # overwrites @everyone role
        server.default_role: PermissionOverwrite(view_channel=False),
        MathBot: PermissionOverwrite(view_channel=True),
        Visitor: PermissionOverwrite(view_channel=True),
        role: PermissionOverwrite(view_channel=True),
    }
    return await server.create_text_channel(
        role.name.lower(), category=category, overwrites=overwrites
    )


async def add_role(ctx: Context, role_name: str):
    member: Member = ctx.author
    message: Message = ctx.message
    server: Guild = ctx.guild

    if get(member.roles, name=role_name):
        await message.add_reaction("😤")
        response = (f"You already have `{role_name}` course role.\n"
                    "Don't bother asking again.")
        # LOGGING
        # components.log_to_json(datetime.now(), member, message.content, response)
        return await ctx.reply(response)

    role_found_in_server = get(server.roles, name=role_name)
    if not role_found_in_server:
        role_found_in_server = await server.create_role(
            name=role_name, mentionable=True
        )

    channel_found_in_server = get(server.channels, name=role_name.lower())
    if not channel_found_in_server:
        channel_found_in_server = await create_text_channel(
            server, role_found_in_server
        )

    await message.add_reaction("🆗")
    await member.add_roles(role_found_in_server)
    response = f"`{role_name}` course role has been given to {member.mention}"
    # LOGGING
    # components.log_to_json(datetime.now(), member, message.content, response)
    return await ctx.reply(response)


async def remove_role(ctx: Context, role_name: str):
    member: Member = ctx.author
    message: Message = ctx.message

    role_found_in_member = get(member.roles, name=role_name)

    if not role_found_in_member:
        await message.add_reaction("😤")
        response = (f"You don't have `{role_name}` course role.\n"
                    "Don't bother asking again.")
        return await ctx.reply(response)

    await message.add_reaction("🆗")
    await member.remove_roles(role_found_in_member)
    response = f"`{role_name}` course role has been removed from {member.mention}"
    return await ctx.reply(response)
