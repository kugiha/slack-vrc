from slackbot.bot import respond_to
from vrchat_api import VRChatAPI
from vrchat_api.enum import ReleaseStatus
from auth import a
from monitor import UserMonitor, UserMonitorType

@respond_to('^monitor (.*) (.*)$')
@respond_to('^m (.*) (.*)$')
def monitor_user(message, mode, displayName):
    message.reply('Setting monitor...')
    monitor_type = UserMonitorType.getUserMonitorTypeByString(mode)
    if monitor_type is None:
        message.reply('No such mode')
        return
    user = get_friend_by_display_name(displayName)
    if user is None:
        message.reply('User not found')
        return
    user_monitor = UserMonitor(user, monitor_type, message)

@respond_to('^monitor-all (.*)$')
@respond_to('^ma (.*)$')
def monitor_user_all(message, mode):
    message.reply('Setting monitor...')
    monitor_type = UserMonitorType.getUserMonitorTypeByString(mode)
    if monitor_type is None:
        message.reply('No such mode')
        return
    for f in get_all_friends():
        user_monitor = UserMonitor(f, monitor_type, message)

def get_friend_by_display_name(displayName):
    for f in get_all_friends():
        print(f.displayName)
        if displayName == f.displayName:
            return f
    return None
def get_all_friends():
    friends = a.getFriends(offline=False)
    friends.extend(a.getFriends(offline=True))
    return friends