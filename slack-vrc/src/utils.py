import json
from ..utils import get_releaseStatus_emoji
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
def get_releaseStatus_emoji(releaseStatus):
    if releaseStatus==ReleaseStatus.PRIVATE:
        # It says private, but it's something like friends+
        return ':family:'
    if releaseStatus==ReleaseStatus.PUBLIC:
        return ':globe_with_meridians:'
