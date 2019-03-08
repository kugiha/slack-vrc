import os
import time
from vrc_auth import vrc
import boto3
dynamodb = boto3.resource('dynamodb')
friends_table_name = os.environ['friends_table_name']
friends_dynamotable = dynamodb.Table(friends_table_name)
worlds_table_name = os.environ['worlds_table_name']
worlds_dynamotable = dynamodb.Table(worlds_table_name)
instances_table_name = os.environ['instances_table_name']
instances_dynamotable = dynamodb.Table(instances_table_name)


def lambda_handler(_, __):
    friends = vrc.getFriends(offline=False)
    friends.extend(vrc.getFriends(offline=True))
    for f in friends:
        row = {
            'player_id': f.id,
            'player_username': f.username,
            'name': f.displayName,  # displayName
            'updated_at': int(time.time())
        }
        if f.location.offline:
            row['status'] = 'offline'
        else:
            row['status'] = 'online'
            if f.location.private:
                row['instance_type'] = 'private'
            else:
                # public, friends+, etc...
                row['world_id'] = f.location.worldId
                row['instance_id'] = f.location.instanceId
                fetch_world_if_needed(f.location.worldId)

        save_to_db(row, friends_table_name)


def fetch_world_if_needed(worldId):
    res = worlds_dynamotable.get_item(Key={'world_id': worldId})
    if res['Item'] and res['Item']['update_interval_count'] > 0:
        worlds_dynamotable.update_item(
            Key={'world_id': worldId},
            UpdateExpression=
            'set update_interval_count = update_interval_count - 1')
        return
    world = vrc.getWorldById(worldId)
    row = {}
    row['name'] = world.name
    row['thumbnailImageURL'] = getattr(world, 'thumbnailImageURL', None)
    row['capacity'] = world.capacity
    save_to_db(row, worlds_dynamotable)


def fetch_instance_if_needed(worldId, instanceId):
    res = instances_dynamotable.get_item(Key={'instance_id': instanceId})
    if res['Item'] and res['Item']['update_interval_count'] > 0:
        instances_dynamotable.update_item(
            Key={'instance_id': instanceId},
            UpdateExpression=
            'set update_interval_count = update_interval_count - 1')
        return
    instance = vrc.getInstanceById(worldId, instanceId)
    row = {}
    row['instance_users_count'] = len(instance.users)
    if instance.friends:
        row['instance_type'] = 'friends'
    elif instance.hidden:
        row['instance_type'] = 'hidden'
    else:
        row['instance_type'] = 'public'
    save_to_db(row, instances_dynamotable)


def save_to_db(payload, table):
    try:
        res = table.put_item(Item=payload)
        print("Succeeded.")
        return
    except Exception as e:
        print("Failed.")
        print(e)
        return