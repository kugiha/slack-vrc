from slackbot.bot import respond_to
from vrchat_api import VRChatAPI
from vrchat_api.enum import ReleaseStatus
from auth import a
import re

def get_releaseStatus_emoji(releaseStatus):
    if releaseStatus==ReleaseStatus.PRIVATE:
        # It says private, but it's something like friends+
        return ':family:'
    if releaseStatus==ReleaseStatus.PUBLIC:
        return ':globe_with_meridians:'

@respond_to('^vrconline$')
@respond_to('^online$')
@respond_to('^on$')
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

@respond_to('vrconline g')
@respond_to('online g')
@respond_to('on g')
@respond_to('ong')
def online_grouped(message):
    friends = a.getFriends()
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
        world = a.getWorldById(item[0])
        users = item[1]
        for user in users:
            reply += '*{}*, '.format(user.displayName)
        reply = reply[:-2]
        reply += ' _in {}{}_ (?/{})\n'.format(world.name, get_releaseStatus_emoji(world.releaseStatus), world.capacity)
    reply += 'in-private friends\n'
    for user in private_users:
        reply += '{},'.format(user.displayName)
    reply = reply[:-1]
    message.reply(reply)