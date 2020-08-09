# This is the english language file! As an early version,
# if you want to translate, copy this file then rename all
# the imports in the language processor module
# for your language. I will think of a better implementation
# system in future revisions. - Penim

class AdminText(object): # Admin module
    NOT_ADMIN = "I am not admin! I need admin permissions to perform this action!"
    BANNING_USER = "`Banning user...`"
    NO_PERMS = "I do not have sufficient permissions to execute this action!"
    NO_MSG_DEL_PERMS = "I do not have permissions to delete messages, so I cannot delete whatever this user sent."
    BANNED_SUCCESSFULLY = "`{}` was banned!"
    UNBANNING_USER = "`Unbanning user...`"
    UNBANNED_SUCCESSFULLY = "Successfully unbanned!"
    USERID_INVALID = "Invalid UserID!"
    FAILED_FETCH_USER = "Couldn't fetch user."
    KICKING_USER = "`Kicking user...`"
    KICKED_SUCCESSFULLY = "{} has been kicked!"
    ONLY_CHAN_GROUPS = "I can only perform this action in Groups or channels!"
    NOT_USER = "This entity is not a User!"
    PROMT_SELF = "I can't promote myself!"
    ADM_ALRD = "This user is already Admin!"
    PROMTING_USER = "`Promoting user...`"
    NO_ADD_ADM_RIGHT = "I am admin, but I do not have permission to add other admins!"
    PRMT_SUCCESS = "Successfully promoted!"
    TOO_MANY_ADM = "There are too many administrators in this chat!"
    ALREADY_NOT_ADM = "This user is already not an Admin!"
    DMT_MYSELF = "I can't demote myself!"
    DMTING_USER = "`Demoting user...`"
    DMTED_SUCCESSFULLY = "Successfully demoted!"
    NO_DEl_USERS = "No deleted accounts detected!"
    SEARCHING_DEL_USERS = "`Searching for deleted accounts...`"
    FOUND_DEL_ACCS = "Found `{}` deleted accounts! Use .delusers clean to clean them!"
    DELETING_ACCS = "`Removing deleted accounts...`"
    NO_BAN_PERMS = "I have no permissions to ban users!"
    DEL_ALL_SUCCESFULLY = "Successfully removed `{}` deleted accounts!"
    DEL_SOME_SUCCESSFULLY = "Successfully removed `{}` deleted accounts! `{}` admin accounts could not be removed!"
    BANLOG = "#BAN\nUser: [{}]({})\nChat: [{}]({})"
    UNBANLOG = "#UNBAN\nUser: [{}]({})\nChat: [{}]({})"
    KICKLOG = "#KICK\nUser: [{}]({})\nChat: [{}]({})"
    CLEAN_DELACC_LOG = "#DELUSERS\nRemoved `{}` deleted accounts!"
    PROMT_LOG = "#PROMOTE\nUser: [{}]({})\nChat: [{}]({})"
    DMT_LOG = "#DEMOTE\nUser: [{}]({})\nChat: [{}]({})"
    MUTING_USR = "`Muting user...`"
    USER_MUTED = "Successfully muted!"
    UNMUTING_USR = "`Unmuting user...`"
    USER_UNMUTED = "Successfully unmuted!"
    MUTE_LOG = "#MUTE\nUser: [{}]({})\nChat: [{}]({})"
    UNMUTE_LOG = "#UNMUTE\nUser: [{}]({})\nChat: [{}]({})"
    MSG_NOT_FOUND_PIN = "`Reply to a message to pin it!`"
    PINNED_SUCCESSFULLY = "Sucessfully pinned!"

class StatusText(object):
    UBOT = "Userbot Project: "
    SYSTEM_STATUS = "System Status: "
    ONLINE = "Online!"
    VER_TEXT = "Version: "
    USR_TEXT = "User: "
    RTT = "RTT: "
    TELETON_VER = "Telethon version: "
    PYTHON_VER = "Python version: "
    GITAPI_VER = "GitHub API Version: "
    CASAPI_VER = "CAS API Version: "
    COMMIT_NUM = "Revision: "
    ERROR = "ERROR!"
    DAYS = "days"
    BOT_UPTIMETXT = "Bot uptime: "
    MAC_UPTIMETXT = "Server uptime: "

class DeletionsText(object):
    PURGE_COMPLETE = "Purge complete! Deleted `{}` messages!"
    DEL_FAILED = "I cannot delete this message!"
    PURGE_LOG = "#PURGE\nPurged {} messages successfully!"

class GeneralMessages(object):
    ERROR = "ERROR!"
    GET_USER_FROM_EVENT_FAIL = "Invalid user specified!"

