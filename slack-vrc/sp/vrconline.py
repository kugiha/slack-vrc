from utils import get_instanceStatus_emoji
from fetch_from_db import getOnlineFriends
from datetime import datetime, timezone, timedelta

def online():
    friends = getOnlineFriends()
    as_of_string = get_as_of_string(friends[0]['updated_at'])
    reply = '\nYour online friends (as of {}):'.format(as_of_string)
    for f in friends:
        reply += '\n* '
        if f.get('instance_type')=='private':
            # private
            reply += '*{}* :lock:'.format(f['name'])
        else:
            # public, friends+, etc...
            reply += '*{}* _in {}_{}'.format(f['name'], f['world_name'], get_instanceStatus_emoji(f['instance_type']))
    return reply

def online_grouped():
    friends = getOnlineFriends()
    as_of_string = get_as_of_string(friends[0]['updated_at'])
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
    reply = '\nOnline friends (grouped) (as of {})\n'.format(as_of_string)
    for item in users_by_world:
        reply += '* '
        users = item[1]
        for user in users:
            reply += '*{}*, '.format(user['name'])
        reply = reply[:-2]
        reply += ' _in {}_ ({}/{}) {}\n'.format(users[0]['world_name'], users[0]['instance_users_count'], users[0]['world_capacity'], get_instanceStatus_emoji(users[0]['instance_type']))
    reply += 'in-private friends\n'
    for user in private_users:
        reply += '{},'.format(user['name'])
    reply = reply[:-1]
    return reply

def get_as_of_string(updated_at):
    return datetime.fromtimestamp(updated_at, timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')