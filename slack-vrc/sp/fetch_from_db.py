import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
table_name = os.environ['friends_table_name']
dynamodb = boto3.resource('dynamodb')
dynamotable = dynamodb.Table(table_name)

def getOnlineFriends():
    res = dynamotable.scan(
        FilterExpression=Key('status').eq('online')
    )
    return res['Items']