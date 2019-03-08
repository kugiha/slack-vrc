import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
friends_table_name = os.environ['friends_table_name']
friends_dynamotable = dynamodb.Table(friends_table_name)
worlds_table_name = os.environ['worlds_table_name']
worlds_dynamotable = dynamodb.Table(worlds_table_name)
instances_table_name = os.environ['instances_table_name']
instances_dynamotable = dynamodb.Table(instances_table_name)


def getOnlineFriends():
    res = friends_dynamotable.scan(FilterExpression=Key('status').eq('online'))
    return res.get('Items')


def getWorldInfoById(worldId):
    res = worlds_dynamotable.get_item(Key={'world_id': worldId})
    return res.get('Item')


def getInstanceInfoById(worldId, instanceId):
    res = instances_table_name(
        Key={
            'instance_id_concatenated_with_world_id':
            get_instance_id_concatenated_with_world_id(worldId, instanceId)
        })
    return res.get('Item')


def get_instance_id_concatenated_with_world_id(worldId, instanceId):
    return worldId + '/' + instanceId
