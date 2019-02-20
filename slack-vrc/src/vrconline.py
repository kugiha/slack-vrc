from utils import get_releaseStatus_emoji
from vrc_auth import vrc

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

def online_grouped():
    friends = vrc.getFriends()
    users_by_world = {}
    private_users = []
    for f in friends:
        if f.location.private:
            # private
            private_users.append(f)
        else:
            # public, friends+, etc...
            if f.location.worldId not in users_by_world.keys():
                users_by_world[f.location.worldId] = []
            users_by_world[f.location.worldId].append(f)
    users_by_world = sorted(users_by_world.items(), key=lambda x: -len(x[1]))
    reply = '\nOnline friends (grouped)\n'
    for item in users_by_world:
        reply += '* '
        world = vrc.getWorldById(item[0])
        users = item[1]
        for user in users:
            reply += '*{}*, '.format(user.displayName)
        reply = reply[:-2]
        reply += ' _in {}{}_ (?/{})\n'.format(world.name, get_releaseStatus_emoji(world.releaseStatus), world.capacity)
    reply += 'in-private friends\n'
    for user in private_users:
        reply += '{},'.format(user.displayName)
    reply = reply[:-1]
    return reply