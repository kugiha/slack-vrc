from utils import get_releaseStatus_emoji
from vrc_auth import vrc
from fetch_from_db import getOnlineFriends

def online():
    friends = getOnlineFriends()
    reply = '\nYour online friends:'
    for f in friends:
        reply += '\n* '
        if f.get('instance_type')=='private':
            # private
            reply += '*{}* :lock:'.format(f['name'])
        else:
            # public, friends+, etc...
            reply += '*{}* _in {}_'.format(f['name'], f['world_name'])
    return reply

def online_grouped():
    friends = getOnlineFriends()
    users_by_world = {}
    private_users = []
    for f in friends:
        if f.get('instance_type')=='private':
            # private
            private_users.append(f)
        else:
            # public, friends+, etc...
            if f['instance_id'] not in users_by_world.keys():
                users_by_world[f['instance_id']] = []
            users_by_world[f['instance_id']].append(f)
    users_by_world = sorted(users_by_world.items(), key=lambda x: -len(x[1])) # {'instance_id': [users array]}
    reply = '\nOnline friends (grouped)\n'
    for item in users_by_world:
        reply += '* '
        users = item[1]
        for user in users:
            reply += '*{}*, '.format(user['name'])
        reply = reply[:-2]
        reply += ' _in {}_ ({}/{})\n'.format(users[0]['world_name'], users[0]['instance_users_count'], users[0]['world_capacity'])
    reply += 'in-private friends\n'
    for user in private_users:
        reply += '{},'.format(user['name'])
    reply = reply[:-1]
    return reply