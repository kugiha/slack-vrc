from slackbot.bot import respond_to
from vrchat_api import VRChatAPI
from vrchat_api.enum import ReleaseStatus
from auth import a
from monitor import UserMonitor, UserMonitorType

@respond_to('^monitor (.*) (.*)$')
@respond_to('^m (.*) (.*)$')
def online(message, mode, displayName):
    message.reply('Setting monitor...')
    monitor_type = UserMonitorType.getUserMonitorTypeByString(mode)
    if monitor_type is None:
        message.reply('No such mode')
        return
    user = get_friend_id_by_display_name(displayName)
    if user is None:
        message.reply('User not found')
        return
    user_monitor = UserMonitor(user, monitor_type, message)

def get_friend_id_by_display_name(displayName):
    friends = a.getFriends(offline=False)
    friends.extend(a.getFriends(offline=True))
    for f in friends:
        print(f.displayName)
        if displayName == f.displayName:
            return f
    return None
