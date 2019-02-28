import json
from vrchat_api.enum import ReleaseStatus
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }
def get_instanceStatus_emoji(instanceStatus):
    if instanceStatus=='private':
        return ':lock:'
    if instanceStatus=='friends':
        return ':heart:'
    if instanceStatus=='hidden':
        return ':family:'
    if instanceStatus=='public':
        return ':globe_with_meridians:'
