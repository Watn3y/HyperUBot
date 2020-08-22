# tguserbot stuff
from tg_userbot import HELP_DICT
from tg_userbot.include.watcher import watcher
from tg_userbot.include.language_processor import MemberInfoText as msgRep, HelpDesignations as helpRep

# Telethon stuff
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipantBanned,
                               ChannelParticipantSelf, ChannelParticipant)
from telethon.errors import ChannelInvalidError, UserIdInvalidError, UserNotParticipantError

# Misc
from datetime import datetime


@watcher(pattern=r"^\.minfo(?: |$)(.*)", outgoing=True)
async def memberinfo(event):
    await event.edit(msgRep.SCAN)

    if event.reply_to_msg_id:
        message = await event.get_reply_message()
        if message.fwd_from is not None and message.fwd_from.channel_id is not None:
            # forwarded message from channel
            await event.edit(msgRep.SCAN_CHANNEL_FAIL)
            return
        elif message.fwd_from is not None and message.fwd_from.from_id is not None:
            # original author from forwarded message
            member = message.fwd_from.from_id
        else:
            # replied message (no forward)
            member = message.from_id
        chat_info = await event.get_chat()
    else:
        try:
            # becomes a list with at least one element and max two elements ([0, 1])
            args = event.pattern_match.group(1).split(" ", 1)
            if len(args) == 2:
                member, chat = args
                try:
                    chat = int(chat)  # chat ID given
                except:
                    pass
                try:
                    chat_info = await event.client.get_entity(chat)
                except:
                    await event.edit(msgRep.FAIL_GET_MEMBER_CHAT)
                    return
            else:
                member = args[0]
                chat_info = await event.get_chat()  # get current chat
        except Exception as e:
            print("Exception:", e)
            await event.edit(msgRep.FAIL_GET_MEMBER_ARGS)
            return

        try:
            member = int(member)  # user ID given
        except:
            pass

        if not member:  # argument empty to check ourself
            member = await event.client.get_me()
            member = member.id

    try:
        member_info = await event.client(GetFullUserRequest(member))  # 'member' = ID
        member_id = member_info.user.id
        member_is_self = member_info.user.is_self
        member_deleted = member_info.user.deleted
        member_name = member_info.user.first_name if not member_deleted else msgRep.DELETED_ACCOUNT
        member_username = member_info.user.username if member_info.user.username else None
        member_name_link = f"<a href=\"tg://user?id={member_id}\">{member_name}</a>"
    except UserIdInvalidError as e:
        print("UserIdInvalidError:", e)
        await event.edit(msgRep.INVALID_USER_ID)
        return
    except Exception as e:
        print("Exception:", e)
        await event.edit(f"`{msgRep.FAIL_GET_MEMBER_DIV}: {e}`")
        return

    try:
        if hasattr(chat_info, "megagroup") and chat_info.megagroup:  # works with supergroups only
            participant_info = await event.client(GetParticipantRequest(chat_info.id, member_id))
        else:
            await event.edit(msgRep.NOT_SUPERGROUP)
            return
        # member_info becomes a participant object now
        member_info = participant_info.participant if participant_info else None
    except ChannelInvalidError as cie:
        print("ChannelInvalidError:", cie)
        await event.edit(msgRep.INVALID_CHAT_ID)
        return
    except UserNotParticipantError as unpe:
        print("UserNotParticipantError:", unpe)
        if member_is_self:
            await event.edit(msgRep.ME_NOT_PART.format(chat_info.title))
        else:
            await event.edit(msgRep.USER_NOT_PART.format(chat_info.title))
        return
    except Exception as e:
        print("Exception:", e)
        await event.edit(msgRep.FAIL_GET_PART)
        return

    # we can't access non-default permissions from other members if we aren't an admin
    # in the specific group
    am_i_admeme = True if hasattr(chat_info, "admin_rights") and \
                       chat_info.admin_rights is not None else False

    x_marks_the_spot = u"\u274C"  # red cross mark emoji
    check_mark = u"\u2705"  # white check mark emoji
    negative_cross = u"\u274E"  # green negative cross mark emoji
    warning = u"\u26A0"  # warning emoji

    default_chat_permissions = chat_info.default_banned_rights

    admin_permissions = {"change_info": x_marks_the_spot,
                         "delete_messages": x_marks_the_spot,
                         "ban_users": x_marks_the_spot,
                         "invite_users": x_marks_the_spot,
                         "pin_messages": x_marks_the_spot,
                         "add_admins": x_marks_the_spot}

    member_permissions = {"send_messages": x_marks_the_spot,
                          "send_media": x_marks_the_spot,
                          "send_stickers": x_marks_the_spot,
                          "send_gifs": x_marks_the_spot,
                          "send_polls": x_marks_the_spot,
                          "embed_links": x_marks_the_spot,
                          "invite_users": x_marks_the_spot,
                          "pin_messages": x_marks_the_spot,
                          "change_info": x_marks_the_spot}

    is_admin, banned, restricted, muted, not_member = (False,)*5
    until_text, by_text = (None,)*2

    if isinstance(member_info, ChannelParticipantCreator):  # Owner
        change_info, delete_messages, ban_users, invite_users, \
        pin_messages, add_admins, root_rights = (check_mark,)*7
        promoted_by = None
        member_status = msgRep.STATUS_OWNER
        is_admin = True
    elif isinstance(member_info, ChannelParticipantAdmin):  # Admin
        admin_rights = member_info.admin_rights
        enabled_rights_count = 0
        root_rights = x_marks_the_spot
        is_admin = True
        for right in vars(admin_rights):
            if getattr(admin_rights, right) is True:
                if str(right) in admin_permissions.keys():
                    admin_permissions[str(right)] = check_mark
                # these attributes are for channels, so we don't need them
                if not str(right) in ["post_messages", "edit_messages"]:
                    enabled_rights_count += 1
        change_info = admin_permissions.get("change_info")
        delete_messages = admin_permissions.get("delete_messages")
        ban_users = admin_permissions.get("ban_users")
        invite_users = admin_permissions.get("invite_users")
        pin_messages = admin_permissions.get("pin_messages")
        add_admins = admin_permissions.get("add_admins")
        if enabled_rights_count == 6:  # max admin rights in groups
            member_status = f"{msgRep.STATUS_ADMIN} " + u"\u2605"  # full rights; star emoji
        elif enabled_rights_count < 5:
            member_status = f"{msgRep.STATUS_ADMIN} " + u"\u32cf"  # limited rights; LTD emoji
        else:
            member_status =  msgRep.STATUS_ADMIN  # default

        promoter = None
        if hasattr(participant_info, "users") and participant_info.users:
            for user in participant_info.users:
                if user.id == member_info.promoted_by:  # promoted_by flag is always set
                    promoter = user
                    break
        if promoter is None:
            promoter = await event.client.get_entity(member_info.promoted_by)
        if promoter.deleted:
            promoted_by = msgRep.DELETED_ACCOUNT
        else:
            promoted_by = "@" + promoter.username if promoter.username is not None else \
                          f"<a href=\"tg://user?id={promoter.id}\">{promoter.first_name}</a>"
    elif isinstance(member_info, ChannelParticipant) or \
         isinstance(member_info, ChannelParticipantSelf):  # Member
        member_status = msgRep.STATUS_MEMBER
        for right in vars(default_chat_permissions):
            if getattr(default_chat_permissions, right) is False:  # False means perm not restricted
                if str(right) in member_permissions.keys():
                    if not am_i_admeme and not member_is_self:
                        member_permissions[str(right)] = warning  # Can't access member's non-default permission
                    else:
                        member_permissions[str(right)] = check_mark
            else:
                if str(right) in member_permissions.keys():
                    member_permissions[str(right)] = negative_cross
        send_messages = member_permissions.get("send_messages")
        send_media = member_permissions.get("send_media")
        if (member_permissions.get("send_stickers") is check_mark and \
            member_permissions.get("send_gifs") is check_mark):
            send_stickers_gifs = check_mark
        elif (member_permissions.get("send_stickers") is warning and \
              member_permissions.get("send_gifs") is warning):
            send_stickers_gifs = warning
        else:
            send_stickers_gifs = negative_cross
        send_polls = member_permissions.get("send_polls")
        embed_links = member_permissions.get("embed_links")
        invite_users = member_permissions.get("invite_users")
        pin_messages = member_permissions.get("pin_messages")
        change_info = member_permissions.get("change_info")
    elif isinstance(member_info, ChannelParticipantBanned):  # Banned/Muted/Restricted member
        if member_info.left:  # member is not a participant but added to exceptions or removed list
            if member_info.banned_rights.view_messages:  # only banned users have this flag set to True
                member_status = msgRep.STATUS_BANNED
                until_text = msgRep.STATUS_BANNED_UNTIL
                by_text = msgRep.STATUS_BANNED_BY
                banned = True
            elif member_info.banned_rights.send_messages:
                member_status = msgRep.STATUS_MUTED_NOT_MEMBER
                until_text = msgRep.STATUS_MUTED_UNTIL
                by_text = msgRep.STATUS_MUTED_BY
                not_member = True
            else:  # for all other cases
                member_status = msgRep.STATUS_RESTRICTED_NOT_MEMBER
                until_text = msgRep.STATUS_RESTRICTED_UNTIL
                by_text = msgRep.STATUS_RESTRICTED_BY
                not_member = True
        elif member_info.banned_rights.send_messages:  # member is participant but silenced
            member_status = msgRep.STATUS_MUTED
            until_text = msgRep.STATUS_MUTED_UNTIL
            by_text = msgRep.STATUS_MUTED_BY
            muted = True
        else:  # member is participant but with limited permissions
            member_status = msgRep.STATUS_RESTRICTED
            until_text = msgRep.STATUS_RESTRICTED_UNTIL
            by_text = msgRep.STATUS_RESTRICTED_BY
            restricted = True
        default_perms_dict = vars(default_chat_permissions)
        member_perms_dict = vars(member_info.banned_rights)
        for key, key2 in zip(default_perms_dict, member_perms_dict):
            if default_perms_dict.get(str(key)) is False and \
               member_perms_dict.get(str(key2)) is False:
                if str(key2) in member_permissions.keys():
                    member_permissions[str(key2)] = check_mark
            elif default_perms_dict.get(str(key)) is True and \
                 member_perms_dict.get(str(key2)) is True:  # default chat restriction
                if str(key2) in member_permissions.keys():
                    member_permissions[str(key2)] = negative_cross

        send_messages = member_permissions.get("send_messages")
        send_media = member_permissions.get("send_media")
        if (member_permissions.get("send_stickers") is check_mark and \
            member_permissions.get("send_gifs") is check_mark):
            send_stickers_gifs = check_mark
        elif (member_permissions.get("send_stickers") is negative_cross and \
              member_permissions.get("send_gifs") is negative_cross):
            send_stickers_gifs = negative_cross  # restricted by default
        else:
            send_stickers_gifs = x_marks_the_spot
        send_polls = member_permissions.get("send_polls")
        embed_links = member_permissions.get("embed_links")
        invite_users = member_permissions.get("invite_users")
        pin_messages = member_permissions.get("pin_messages")
        change_info = member_permissions.get("change_info")

        restricter = None
        if hasattr(participant_info, "users") and participant_info.users:
            for user in participant_info.users:
                if user.id == member_info.kicked_by:
                    restricter = user
                    break
        if restricter is None:
            restricter = await event.client.get_entity(member_info.kicked_by)
        if restricter.deleted:
            restricted_by = msgRep.DELETED_ACCOUNT
        else:
            restricted_by = "@" + restricter.username if restricter.username is not None else \
                            f"<a href=\"tg://user?id={restricter.id}\">{restricter.first_name}</a>"
        year_diff = member_info.banned_rights.until_date.year - datetime.now().year
        # Custom restriction dates in Telegram clients are limited up to a year.
        # Restriction date is set to 'forever' if restriction date is for longer than a year
        if year_diff > 1:
            restricted_date = msgRep.TIME_FOREVER
        else:
            restricted_date = member_info.banned_rights.until_date  # temp stored
            restricted_date = f"<code>{restricted_date.strftime('%b %d, %Y')} - {restricted_date.time()} {restricted_date.tzinfo}</code>"
    else:
        # if user isn't a member then skip
        if member_is_self:
            await event.edit(msgRep.ME_NOT_MEMBER.format(chat_info.title))
        else:
            await event.edit(msgRep.USER_NOT_MEMBER.format(chat_info.title))
        return

    # hasattr() is being often used here as not all ChannelParticipant* objects share the same attributes
    admin_title = member_info.rank if hasattr(member_info, "rank") else None
    join_date = member_info.date if hasattr(member_info, "date") else None
    adder = None
    if hasattr(member_info, "inviter_id") and member_info.inviter_id is not None:
        if hasattr(participant_info, "users") and participant_info.users:
            for user in participant_info.users:
                if user.id == member_info.inviter_id:
                    adder = user
                    break
        if adder is None:
            adder = await event.client.get_entity(member_info.inviter_id)
    if adder is not None:
        if adder.deleted:
            added_by = msgRep.DELETED_ACCOUNT
        else:
            added_by = "@" + adder.username if adder.username is not None else \
                       f"<a href=\"tg://user?id={adder.id}\">{adder.first_name}</a>"
    else:
        added_by = None

    caption = f"<b>{msgRep.MEMBERINFO}:</b>\n"
    caption += f"<b>{msgRep.GENERAL}</b>\n"
    caption += f"{msgRep.MINFO_ID}: <code>{member_id}</code>\n"
    if member_username is not None:
        caption += f"{msgRep.FIRST_NAME}: {member_name}\n"
        caption += f"{msgRep.USERNAME}: @{member_username}\n\n"
    else:
        # link to user profile if member has no username,
        # for deleted accounts it will show plain text instead
        caption += f"{msgRep.FIRST_NAME}: {member_name_link}\n\n"
    caption += f"<b>{msgRep.GROUP}</b>\n"
    caption += f"{msgRep.GROUP_NAME}: {chat_info.title}\n"
    caption += f"{msgRep.STATUS}: {member_status}\n"
    if True in (banned, restricted, muted, not_member):
        if until_text is not None:
            caption += f"{until_text}: {restricted_date}\n"
        if by_text is not None:
            caption += f"{by_text}: {restricted_by}\n"
    if admin_title is not None:
        caption += f"{msgRep.ADMIN_TITLE}: {admin_title}\n\n"
    else:
        caption += "\n"
    caption += f"{msgRep.PERMISSIONS}:\n"
    if is_admin:
        caption += f"- {msgRep.CHANGE_GROUP_INFO} {change_info}\n"
        caption += f"- {msgRep.DELETE_MESSAGES} {delete_messages}\n"
        caption += f"- {msgRep.BAN_USERS} {ban_users}\n"
        caption += f"- {msgRep.INVITE_USERS} {invite_users}\n"
        caption += f"- {msgRep.PIN_MESSAGES} {pin_messages}\n"
        caption += f"- {msgRep.ADD_ADMINS} {add_admins}\n"
        caption += f"- {msgRep.ROOT_RIGHTS} {root_rights}\n\n"
    else:
        caption += f"- {msgRep.SEND_MESSAGES} {send_messages}\n"
        caption += f"- {msgRep.SEND_MEDIA} {send_media}\n"
        caption += f"- {msgRep.SEND_GIFS_STICKERS} {send_stickers_gifs}\n"
        caption += f"- {msgRep.SEND_POLLS} {send_polls}\n"
        caption += f"- {msgRep.EMBED_LINKS} {embed_links}\n"
        caption += f"- {msgRep.INVITE_USERS} {invite_users}\n"
        caption += f"- {msgRep.PIN_MESSAGES} {pin_messages}\n"
        caption += f"- {msgRep.CHANGE_GROUP_INFO} {change_info}\n\n"
        if not am_i_admeme and not member_is_self:
            caption += f"{warning} <i>{msgRep.WARN_ADMIN_PRIV}</i>\n\n"
    if is_admin and promoted_by is not None:
        caption += f"{msgRep.PROMOTED_BY}: {promoted_by}\n"
    if added_by is not None:
        caption += f"{msgRep.ADDED_BY}: {added_by}\n"
    if (not banned and not not_member) and join_date is not None:
        caption += f"{msgRep.JOIN_DATE}: <code>{join_date.strftime('%b %d, %Y')} - {join_date.time()} {join_date.tzinfo}</code>\n"

    await event.edit(caption, parse_mode="html")

    return


HELP_DICT.update({"memberinfo": helpRep.MEMBERINFO_HELP})
