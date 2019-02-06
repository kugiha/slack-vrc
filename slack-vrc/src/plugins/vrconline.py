from slackbot.bot import respond_to
from vrchat_api import VRChatAPI
from vrchat_api.enum import ReleaseStatus
from auth import a

def get_releaseStatus_emoji(releaseStatus):
    if releaseStatus==ReleaseStatus.PRIVATE:
        # It says private, but it's something like friends+
        return ':family:'
    if releaseStatus==ReleaseStatus.PUBLIC:
        return ':globe_with_meridians:'

@respond_to('vrconline')
@respond_to('online')
@respond_to('on')
def online(message):
    friends = a.getFriends()
    reply = '\nYour online friends:'
    for f in friends:
        reply += '\n* '
        if f.location.private:
            # private
            reply += '*{}* :lock:'.format(f.displayName)
        else:
            # public, friends+, etc...
            world = a.getWorldById(f.location.worldId)
            reply += '*{}* _in {}{}_'.format(f.displayName, world.name, get_releaseStatus_emoji(world.releaseStatus))
    message.reply(reply)
