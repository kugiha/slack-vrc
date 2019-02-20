from ..utils import get_releaseStatus_emoji
from ..vrc_auth import vrc

def online():
    friends = vrc.getFriends()
    reply = '\nYour online friends:'
    for f in friends:
        reply += '\n* '
        if f.location.private:
            # private
            reply += '*{}* :lock:'.format(f.displayName)
        else:
            # public, friends+, etc...
            world = vrc.getWorldById(f.location.worldId)
            reply += '*{}* _in {}{}_'.format(f.displayName, world.name, get_releaseStatus_emoji(world.releaseStatus))
    return reply
