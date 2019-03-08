from utils import get_instanceStatus_emoji
from fetch_from_db import getOnlineFriends, getWorldInfoById, getInstanceInfoById
from datetime import datetime, timezone, timedelta


def online():
    friends = getOnlineFriends()
    as_of_string = get_as_of_string(friends[0]['updated_at'])
    reply = '\nYour online friends (as of {}):'.format(as_of_string)
    for f in friends:
        reply += '\n* '
        world = getWorldInfoById(f['world_id'])
        instance = getInstanceInfoById(f['world_id'], f['instance_id'])
        if world['type'] == 'private':
            # private
            reply += '*{}* :lock:'.format(f['name'])
        else:
            # public, friends+, etc...
            reply += '*{}* _in {}_{}'.format(
                f['name'], world['name'],
                get_instanceStatus_emoji(instance['type']))
    return reply


def online_grouped():
    friends = getOnlineFriends()
    as_of_string = get_as_of_string(friends[0]['updated_at'])
    users_by_instance = {}
    private_users = []
    for f in friends:
        world = getWorldInfoById(f['world_id'])
        instance = getInstanceInfoById(f['world_id'], f['instance_id'])
        if instance['instance_type'] == 'private':
            # private
            private_users.append(f)
        else:
            # public, friends+, etc...
            if instance[
                    'instance_id_concatenated_with_world_id'] not in users_by_instance.keys(
                    ):
                users_by_instance[
                    instance['instance_id_concatenated_with_world_id']] = []
            users_by_instance[
                instance['instance_id_concatenated_with_world_id']].append(f)
    users_by_instance = sorted(
        users_by_instance.items(),
        key=lambda x: -len(x[1]))  # {'instance_id': [users array]}
    reply = '\nOnline friends (grouped) (as of {})\n'.format(as_of_string)
    for (instance_id_concatenated_with_world_id, users) in users_by_instance:
        world = getWorldInfoById(
            instance_id_concatenated_with_world_id.split('/')[0])
        instance = getInstanceInfoById(
            *instance_id_concatenated_with_world_id.split('/'))
        reply += '* '
        for user in users:
            reply += '*{}*, '.format(user['name'])
        reply = reply[:-2]  # Remove last ', '
        reply += ' _in {}_ ({}/{}) {}\n'.format(
            world['name'], instance['users_count'], world['capacity'],
            get_instanceStatus_emoji(instance['type']))
    reply += 'in-private friends\n'
    for user in private_users:
        reply += '{},'.format(user['name'])
    reply = reply[:-1]
    return reply


def get_as_of_string(updated_at):
    return datetime.fromtimestamp(updated_at, timezone(
        timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
