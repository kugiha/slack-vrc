import boto3
from boto3.dynamodb.conditions import Key, Attr
table_name = "slackvrc_friend_status"
dynamodb = boto3.resource('dynamodb')
dynamotable = dynamodb.Table(table_name)

def getOnlineFriends():
    res = dynamotable.query(
        KeyConditionExpression=Key('status').eq('online')
    )
    return res['Items']