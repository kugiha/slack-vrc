import os
import time
from vrc_auth import vrc
import boto3
table_name = os.environ['friends_table_name']
dynamodb = boto3.resource('dynamodb')
dynamotable = dynamodb.Table(table_name)
def lambda_handler(_, __):
    friends = vrc.getFriends(offline=False)
    friends.extend(vrc.getFriends(offline=True))
    for f in friends:
        row = {
            'player_id': f.id,
            'player_username': f.username,
            'name': f.displayName, # displayName
            'updated_at': int(time.time())
        }
        if f.location.offline:
            row['status'] = 'offline'
        else:
            row['status'] = 'online'
            if f.location.private:
                row['world_type'] = 'private'
            else:
                # public, friends+, etc...
                row['world_id'] = f.location.worldId
                row['instance_id'] = f.location.instanceId
                world = vrc.getWorldById(f.location.worldId)
                row['world_name'] = world.name
                row['world_thumbnailImageURL'] = getattr(world, 'thumbnailImageURL', None)
                row['world_capacity'] = world.capacity
                if world.friends:
                    row['world_type'] = 'friends'
                elif world.hidden:
                    row['world_type'] = 'hidden'
                else:
                    row['world_type'] = 'unknown'
                instance = vrc.getInstanceById(f.location.worldId, f.location.instanceId)
                row['instance_users_count'] = len(instance.users)
        save_to_db(row)
def save_to_db(payload):
    try:
        res = dynamotable.put_item(
            Item = payload
        )
        print("Succeeded.")
        return
    except Exception as e:
        print("Failed.")
        print(e)
        return